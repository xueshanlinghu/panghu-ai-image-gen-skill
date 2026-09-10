# 胖狐AI图片接口使用注意事项

## 端点
- 文生图：POST `https://api.ace.324567.xyz/openai/images/generations`
- 图生图/编辑：POST `https://api.ace.324567.xyz/openai/images/edits`
- 文生图使用 `Content-Type: application/json`
- 图生图使用 `multipart/form-data`
- 认证头：`authorization: Bearer <PANGHU_API_KEY>`

## 模型
支持：
- `gpt-image-2.5-flare`：推荐文生图默认，速度更快，适合日常生成与快速迭代。
- `gpt-image-2.5-sunburst`：推荐图生图/编辑默认，能力和编辑控制更强。
- `gpt-image-2`：兼容旧模型，继续支持，但不再作为内置默认模型。

脚本选择优先级：单次 `--model` > `.panghu-image-models.json` 长期偏好 > 内置推荐默认。

内置推荐默认：
- 文生图：`gpt-image-2.5-flare`
- 图生图：`gpt-image-2.5-sunburst`

## 固定参数
每次请求必须包含：
- `n`: `"1"`
- `response_format`: `"url"`

## 主要参数
| 参数 | 可选值/格式 | 说明 |
|---|---|---|
| `model` | 三个支持模型之一 | 由脚本解析默认或单次覆盖 |
| `prompt` | 字符串，最长 32000 字符 | 图片描述 |
| `size` | `auto` / 预设 / 自定义 `宽x高` | 自定义宽高需为16倍数；最长边≤3840；总像素≤8,294,400 |
| `quality` | `auto` / `high` / `medium` / `low` | 默认 high |
| `background` | `auto` / `transparent` / `opaque` | transparent 需 png/webp |
| `output_format` | `png` / `jpeg` / `webp` | 默认 png |
| `image` | 本地图片路径 | 仅图生图，支持 png/jpg/jpeg/webp |

## 本地模型偏好文件
技能根目录的 `.panghu-image-models.json` 保存长期偏好，例如：

```json
{
  "onboarding_completed": true,
  "text_to_image_model": "gpt-image-2.5-flare",
  "image_to_image_model": "gpt-image-2.5-sunburst"
}
```

该文件属于每个安装实例的本地偏好，不应提交 Git。

## 请求格式
文生图使用 JSON；图生图将同一组普通字段放入 multipart/form-data，同时以 `image` 字段上传图片。

## 实操注意事项
1. 生成请求脚本超时 1800 秒；高清任务等待较久时不要提前重复提交。
2. 输入图片 MIME 必须根据原文件后缀决定，不能按输出格式决定。
3. 透明背景若指定 jpeg，脚本自动切换为 png。
4. 返回 CDN 图片链接后，下载超时为 300 秒。
