const { ValidationError } = require('../utils/errors');
const logger = require('../utils/logger');

class ContentService {
  // ...existing code...
  
  async generateContent(params) {
    this.validateParams(params);
    
    try {
      // ...existing code...
    } catch (error) {
      throw new ValidationError('内容生成失败');
    }
  }

  validateParams(params) {
    const requiredFields = ['topic', 'format', 'length'];
    const missingFields = requiredFields.filter(field => !params[field]);
    
    if (missingFields.length > 0) {
      throw new ValidationError(
        `缺少必要参数: ${missingFields.join(', ')}`
      );
    }

    if (params.length && (params.length < 100 || params.length > 10000)) {
      throw new ValidationError('内容长度必须在100-10000之间');
    }

    const validFormats = ['article', 'video', 'image'];
    if (!validFormats.includes(params.format)) {
      throw new ValidationError(
        `不支持的格式: ${params.format}. 支持的格式: ${validFormats.join(', ')}`
      );
    }
  }
}
