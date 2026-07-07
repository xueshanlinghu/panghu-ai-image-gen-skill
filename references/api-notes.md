# 胖狐AI图片接口 使用注意事项
## 端点信息
- 接口地址：POST `https://api.acedata.cloud/openai/images/generations`
- 请求头规则：
  - 文生图：使用 `Content-Type: application/json`，参数以JSON格式提交
  - 图生图：**必须使用** `Content-Type: multipart/form-data`，图片以表单字段`image`上传，其余参数以普通表单字段提交（使用JSON格式提交图生图请求会报错）
- 统一认证头：`authorization: Bearer <PANGHU_API_KEY>`

## 参数规则
### 固定参数
- `model`: 固定使用 `gpt-image-2`
- `n`: 固定值为 `1`（当前接口仅支持单张图片生成）
- `response_format`: 固定为 `url`（返回CDN直链，效率最高）

### 可选参数
| 参数名 | 可选值 | 说明 |
|--------|--------|------|
| `prompt` | 字符串，最长32000字符 | 图片描述提示词 |
| `size` | `auto`/预设尺寸/自定义`宽x高` | 自定义尺寸必须满足：<br>1. 宽高均为16的倍数<br>2. 最长边≤3840px<br>3. 总像素≤8,294,400（约830万） |
| `quality` | `auto`(默认)/`high`/`medium`/`low` | 生成质量，质量越高耗时越长、细节越好 |
| `background` | `auto`(默认)/`transparent`/`opaque` | 背景模式：`transparent`为透明背景，**必须配合png/webp格式使用**，jpeg不支持透明通道 |
| `output_format` | `png`(默认)/`jpeg`/`webp` | 输出图片格式 |
| `image` | 本地文件路径 | 仅图生图使用，上传的参考/编辑图片，支持png/jpg/webp，建议大小≤10MB |

## 响应格式
### 成功响应
```json
{
  "success": true,
  "task_id": "任务唯一ID（用于问题排查）",
  "data": [{"url": "图片CDN直链地址"}],
  "elapsed": 93.5, // 生成耗时（秒）
  "cost": {"amount": 0.11}, // 消耗积分数量
  "usage": {"total_tokens": 13513} // 总Token消耗
}
```
### 错误响应
```json
{
  "success": false,
  "error": {"code": "错误码", "message": "错误说明"},
  "trace_id": "请求跟踪ID，反馈问题时提供"
}
```

## 实操注意事项
1. **超时设置**：1024x1024中等质量图片生成约需50-70秒，4K高清图片最长可能需要120秒，请求超时时间必须设置≥180秒，避免生成中途断开。
2. **积分消耗**：基础1024x1024/medium质量图片每张消耗0.11积分，更高分辨率/质量会按比例增加消耗。
3. **链接有效性**：返回的CDN图片链接长期有效，可直接访问、下载或对外引用。
4. **常见错误**：
   - 尺寸不合法：检查是否满足16倍数、分辨率限制
   - 透明背景无效：确认输出格式为png/webp
   - 图生图上传失败：确认使用multipart/form-data格式而非JSON
