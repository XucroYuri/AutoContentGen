
const express = require('express');
const router = express.Router();
const { asyncHandler } = require('../utils/asyncHandler');
const contentService = require('../services/contentService');

// 使用 asyncHandler 统一处理异步错误
router.post('/generate', asyncHandler(async (req, res) => {
  const result = await contentService.generateContent(req.body);
  res.json(result);
}));

module.exports = router;