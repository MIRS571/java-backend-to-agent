# 环境变量与密钥

## 本地文件

仓库只提交 `.env.example`：

```ini
LLM_MODEL=
LLM_API_KEY=
LLM_BASE_URL=
```

本地复制为 `.env` 后填写真实值。`.env` 已被 Git 忽略。

应用读取后应尽早校验必填变量：

```python
import os


def required_env(name: str) -> str:
    value = os.getenv(name)
    if value is None or not value.strip():
        raise RuntimeError(f"缺少必填环境变量：{name}")
    return value.strip()
```

`os.getenv(name)` 返回环境变量对应的字符串；变量不存在时返回 `None`。它不会自动验证空字符串、URL、模型能力或密钥有效性。

## 安全边界

- 不在聊天、截图、日志或异常信息中展示密钥。
- 不把真实厂商 URL 和模型名写入公开示例。
- CI 不依赖个人密钥，普通测试使用 Fake 或 Mock。
- integration 测试缺少环境变量时应明确跳过，而不是伪装成通过。
- 若密钥曾进入 Git 历史，仅删除当前文件不够，必须立即在厂商侧吊销并重新生成。

## 配置分层

| 配置 | 示例 | 是否进入仓库 |
| --- | --- | --- |
| 稳定非敏感默认值 | 超时上限、功能开关默认值 | 可以 |
| 环境相关非敏感值 | 服务地址、环境名 | 只放空变量或安全占位说明 |
| 密钥与凭证 | API Key、数据库密码、内部令牌 | 不可以 |
| 测试固定数据 | Fake Model 输出、内存 Document | 可以，但不得包含真实业务数据 |
