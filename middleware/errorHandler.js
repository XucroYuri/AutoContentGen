const logger = require('../utils/logger');

const errorHandler = (err, req, res, next) => {
  logger.error('Error occurred:', {
    error: err.message,
    stack: err.stack,
    path: req.path,
    method: req.method,
    body: req.body
  });

  const status = err.status || 500;
  const message = err.message || '服务器内部错误';
  
  // 开发环境返回详细错误信息
  const response = {
    status: 'error',
    message,
    ...(process.env.NODE_ENV === 'development' && {
      stack: err.stack,
      details: err.details
    })
  };

  res.status(status).json(response);
};

module.exports = errorHandler;