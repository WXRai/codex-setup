# Codex CLI 第三方 API 配置工具

为 OpenAI Codex CLI 快速配置第三方兼容 API（如 azapi.com.cn、自建代理等），只需填入 URL 和 Key 即可一键完成。

---

## 文件说明

| 文件 | 作用 |
|------|------|
| `codex_config.py` | 核心配置脚本 |
| `setup.bat` | 检查python是否安装 |

---

## 环境要求

- Python 3.8 或更高版本
- Windows / macOS / Linux 均可

### 安装 Python

从官网下载安装：https://www.python.org/downloads/

> Windows 安装时**务必勾选** "Add Python to PATH"

---

## 使用方法

### 方式一：双击运行（推荐 Windows 用户）

1. 将 `setup.bat` 和 `codex_config.py` 放在**同一文件夹**
2. 先双击运行`setup.bat`
3. 再双击运行`codex_config.py`
4. 按提示输入 API Base URL 和 API Key
5. 按 Enter 退出

### 方式二：命令行运行

```bash
# 交互模式
python codex_config.py

# 参数模式（直接填入，不提示）
python codex_config.py -u azapi.com.cn -k sk-your-key-here

# 查看当前配置
python codex_config.py --show

# 清除配置
python codex_config.py --clear
```

---

## 配置示例

以 `azapi.com.cn` 为例：

```
Enter API Base URL (例: azapi.com.cn): azapi.com.cn
Enter API Key: sk-your-api-key
```

脚本会自动：
- 补全 `https://` 协议头
- 追加 `/v1` API 路径
- 写入 `~/.codex/config.toml` 和 `~/.codex/auth.json`

---

## 配置文件位置

| 系统 | 路径 |
|------|------|
| Windows | `C:\Users\<用户名>\.codex\` |
| macOS | `~/.codex/` |
| Linux | `~/.codex/` |

生成的文件：
- `config.toml` — Provider 配置
- `auth.json` — API Key 存储

---

## 常见问题

**Q: 双击后窗口一闪而过**

A: 请通过 `setup.bat` 运行，或先确认 Python 已安装并加入 PATH。

**Q: Codex 报错 "failed to read configuration layers"**

A: 运行 `codex_config.py --clear` 清除旧配置后重新配置。

**Q: 使用什么 Key？**

A: 填入你第三方 API 提供商的 Key（不是 OpenAI 官方 Key）。

---

## 技术细节

生成的 `config.toml` 格式：

```toml
model = "gpt-4o"
model_provider = "custom"

[model_providers.custom]
name = "Custom Provider"
base_url = "https://azapi.com.cn/v1"
wire_api = "responses"
requires_openai_auth = true
```

`requires_openai_auth = true` 让 Codex 从 `auth.json` 中读取 `OPENAI_API_KEY`。

---

## 捐赠

如果觉得项目对你有帮助，可以请我喝杯咖啡：

![捐赠二维码](https://www.helloimg.com/i/2026/06/15/6a300cfa868ff.jpg)

---

## 联系方式

![微信二维码](https://www.helloimg.com/i/2025/01/23/67925bdf3f70f.jpg)
