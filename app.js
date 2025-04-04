const errorHandler = require('./middleware/errorHandler');

// 添加全局错误处理中间件
app.use(errorHandler);
