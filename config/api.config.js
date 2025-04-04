module.exports = {
  topaz: {
    baseUrl: 'https://api.topazlabs.com/v1',
    endpoints: {
      upscale: '/upscale'
    },
    timeout: 30000,
    maxRetries: 3
  },
  runwayml: {
    baseUrl: 'https://api.runwayml.com/v1',
    endpoints: {
      video: '/video'
    },
    timeout: 60000,
    maxRetries: 3
  },
  openai: {
    baseUrl: 'https://api.openai.com/v1',
    endpoints: {
      completions: '/completions'
    },
    timeout: 15000,
    maxRetries: 2
  },
  defaultConfig: {
    timeout: 30000,
    maxRetries: 3,
    headers: {
      'Accept': 'application/json',
      'User-Agent': 'AutoContentGen/1.0'
    }
  }
};
