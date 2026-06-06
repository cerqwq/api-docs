# 📚 API Docs

AI API文档工具，支持OpenAPI生成、文档生成、SDK生成。

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-blue?logo=python" />
  <img src="https://img.shields.io/badge/OpenAI-API-green?logo=openai" />
  <img src="https://img.shields.io/badge/License-MIT-yellow" />
</p>

## ✨ 特性

- 📋 OpenAPI规范生成
- 📖 API文档生成
- 🔧 SDK代码生成
- 📮 Postman集合生成
- 📊 变更日志生成
- ✅ 规范验证

## 🚀 快速开始

```bash
pip install openai

python tools.py
```

## 📖 使用

```python
from api_docs import create_tools

tools = create_tools()

# 生成OpenAPI
spec = tools.generate_openapi("用户管理系统", endpoints)

# 生成文档
docs = tools.generate_api_docs(spec)

# 生成SDK
sdk = tools.generate_sdk(spec, "Python")

# 生成Postman集合
postman = tools.generate_postman_collection(spec)

# 生成变更日志
changelog = tools.generate_changelog(old_spec, new_spec)

# 验证规范
validation = tools.validate_spec(spec)
```

## 📁 项目结构

```
api-docs/
├── tools.py       # API文档工具核心
└── README.md
```

## 📄 许可证

MIT License
