"""
API Docs - AI API文档工具
支持OpenAPI生成、文档生成、SDK生成
"""

import json
import os
from typing import Dict, List, Any
from datetime import datetime

try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False


class APIDocsTools:
    """
    AI API文档工具
    支持：OpenAPI、文档、SDK
    """

    def __init__(self, model: str = "mimo-v2.5-pro", api_key: str = None, base_url: str = None):
        self.model = model
        if OPENAI_AVAILABLE:
            self.client = OpenAI(
                api_key=api_key or os.environ.get('OPENAI_API_KEY', ''),
                base_url=base_url or os.environ.get('OPENAI_BASE_URL', 'https://api.xiaomimimo.com/v1')
            )
        else:
            self.client = None

    def generate_openapi(self, description: str, endpoints: List[Dict]) -> str:
        """生成OpenAPI规范"""
        if not self.client:
            return "LLM客户端未配置"

        endpoints_text = json.dumps(endpoints, ensure_ascii=False)

        prompt = f"""请根据以下描述生成OpenAPI 3.0规范：

描述：{description}
端点：{endpoints_text}

请返回完整的YAML格式OpenAPI规范："""

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=3000
        )

        return response.choices[0].message.content

    def generate_api_docs(self, openapi_spec: str) -> str:
        """生成API文档"""
        if not self.client:
            return "LLM客户端未配置"

        prompt = f"""请根据以下OpenAPI规范生成用户友好的API文档：

{openapi_spec[:2000]}

要求：
1. 清晰的端点说明
2. 请求/响应示例
3. 错误码说明
4. 认证说明"""

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=3000
        )

        return response.choices[0].message.content

    def generate_sdk(self, openapi_spec: str, language: str = "Python") -> str:
        """生成SDK代码"""
        if not self.client:
            return "LLM客户端未配置"

        prompt = f"""请根据以下OpenAPI规范生成{language} SDK：

{openapi_spec[:2000]}

要求：
1. 完整的客户端类
2. 类型提示
3. 错误处理
4. 使用示例"""

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=4000
        )

        return response.choices[0].message.content

    def generate_postman_collection(self, openapi_spec: str) -> str:
        """生成Postman集合"""
        if not self.client:
            return "LLM客户端未配置"

        prompt = f"""请根据以下OpenAPI规范生成Postman集合：

{openapi_spec[:2000]}

请返回完整的Postman集合JSON："""

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=3000
        )

        return response.choices[0].message.content

    def generate_changelog(self, old_spec: str, new_spec: str) -> str:
        """生成API变更日志"""
        if not self.client:
            return "LLM客户端未配置"

        prompt = f"""请比较以下两个OpenAPI规范，生成变更日志：

旧版本：
{old_spec[:1000]}

新版本：
{new_spec[:1000]}

请生成Markdown格式的变更日志："""

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=1000
        )

        return response.choices[0].message.content

    def validate_spec(self, openapi_spec: str) -> Dict:
        """验证OpenAPI规范"""
        if not self.client:
            return {"error": "LLM客户端未配置"}

        prompt = f"""请验证以下OpenAPI规范：

{openapi_spec[:2000]}

请返回JSON格式：
{{
    "valid": true/false,
    "errors": ["错误1", "错误2"],
    "warnings": ["警告1", "警告2"],
    "suggestions": ["建议1", "建议2"]
}}"""

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=500
        )

        try:
            content = response.choices[0].message.content
            import re
            json_match = re.search(r'\{.*\}', content, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
        except:
            pass

        return {"validation": content}


def create_tools(**kwargs) -> APIDocsTools:
    """创建API文档工具"""
    return APIDocsTools(**kwargs)


if __name__ == "__main__":
    tools = create_tools()

    print("API Docs Tools")
    print()

    # 测试
    spec = tools.generate_openapi("用户管理系统", [
        {"method": "GET", "path": "/users", "description": "获取用户列表"},
        {"method": "POST", "path": "/users", "description": "创建用户"}
    ])
    print(spec[:300] + "...")
