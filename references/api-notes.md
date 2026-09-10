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
| `image` | 本地主图路径 | 仅图生图，支持 png/jpg/jpeg/webp |
| `image-extra` | 本地额外参考图路径，可重复传入 | 仅图生图；每张参考图对应一个 `image[]` multipart 字段 |

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
文生图使用 JSON。

图生图使用 multipart/form-data：
- 主图固定使用字段 `image`。
- 每张额外参考图重复使用字段 `image[]`。
- `requests` 侧应使用 list of tuples 构造 `files`，以保留多个同名 `image[]` 字段；不要把多张图片塞进同一个 `image` 键。
- `--image-extra` 只能配合 `--image` 使用，不能单独触发图生图。

## 实操注意事项
1. 生成请求脚本超时 1800 秒；高清任务等待较久时不要提前重复提交。
2. 输入图片 MIME 必须根据原文件后缀决定，不能按输出格式决定。
3. 透明背景若指定 jpeg，脚本自动切换为 png。
4. 多图参考更容易让模型重绘整图；局部修改且要求其他内容尽量保持不变时优先单图编辑。
5. JPG/JPEG 参考图若遇到无具体原因的 `400 bad_request`，可先转换为 PNG 再重试一次。
6. 返回 CDN 图片链接后，下载超时为 300 秒。
