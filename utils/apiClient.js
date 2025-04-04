const axios = require('axios');
const { ApiError } = require('./errors');
const logger = require('./logger');

class ApiClient {
  constructor(baseUrl, apiKey, options = {}) {
    this.maxRetries = options.maxRetries || 3;
    this.timeout = options.timeout || 30000;
    this.retryDelay = options.retryDelay || 1000;

    this.client = axios.create({
      baseUrl,
      timeout: this.timeout,
      headers: {
        'Authorization': `Bearer ${apiKey}`,
        'Content-Type': 'application/json',
        ...options.headers
      }
    });

    this._setupInterceptors();
    this._setupCircuitBreaker();
  }

  _setupInterceptors() {
    this.client.interceptors.response.use(
      response => response.data,
      async error => {
        const config = error.config;

        if (!config || !config.retry) {
          config.retry = 0;
        }

        if (config.retry >= this.maxRetries) {
          throw new ApiError(
            `请求失败: ${error.message}`,
            error.response?.status
          );
        }

        config.retry += 1;
        logger.warn(`重试请求 (${config.retry}/${this.maxRetries})`);

        return new Promise(resolve => {
          setTimeout(() => resolve(this.client(config)),
            this.retryDelay * Math.pow(2, config.retry));
        });
      }
    );
  }

  _setupCircuitBreaker() {
    this.failureCount = 0;
    this.lastFailureTime = null;
    this.circuitOpen = false;
    this.resetTimeout = 60000; // 1分钟后重置
  }

  async _checkCircuitBreaker() {
    if (!this.circuitOpen) return true;

    const now = Date.now();
    if (this.lastFailureTime && (now - this.lastFailureTime) > this.resetTimeout) {
      this.circuitOpen = false;
      this.failureCount = 0;
      return true;
    }
    throw new ApiError('服务暂时不可用，请稍后重试');
  }

  async post(endpoint, data) {
    return await this.request('post', endpoint, data);
  }

  async get(endpoint) {
    return await this.request('get', endpoint);
  }

  async request(method, url, data = null) {
    await this._checkCircuitBreaker();
    
    try {
      const response = await this.client({ method, url, data });
      this.failureCount = 0;
      return response;
    } catch (error) {
      this.failureCount++;
      this.lastFailureTime = Date.now();
      
      if (this.failureCount >= 5) {
        this.circuitOpen = true;
      }
      
      throw error;
    }
  }
}

module.exports = ApiClient;
