<p align="center">
  <h1 align="center">🦊 胖狐AI图片生成技能</h1>
  <p align="center">Hermes Agent 技能 | 小白友好的AI文生图/图生图工具，支持4K高清生成</p>
</p>

---

## 📖 项目简介
这是一个为 [Hermes Agent](https://hermes-agent.nousresearch.com/) 开发的图片生成技能，对接胖狐AI（基于gpt-image-2模型），支持文生图、图生图（图片编辑）功能，最高支持4K高清分辨率，面向小白用户设计，全程大白话交互，不需要懂任何技术就能用。

## ✨ 核心特性
- 🎨 **文生图**：输入文字描述生成高质量图片，提示词最长支持32000字符
- 🖼️ **图生图/改图**：上传已有图片，根据要求修改风格、添加元素、调整内容
- 🔝 **4K超清**：支持最高4K（3840x2160）分辨率生成，不管什么尺寸统一按张计费
- 📱 **多比例预设**：内置常用比例：
  - 16:9 4K横屏（电脑壁纸/视频封面）
  - 9:16 4K竖屏（手机壁纸/短视频封面）
  - 3:4 4K竖图（小红书笔记/竖版海报，小红书最佳比例）
  - 1:1 4K方形（头像/朋友圈/社交媒体配图）
  - 支持任意自定义尺寸（宽高为16倍数，最长边≤3840px）
- 🪟 **透明背景**：支持生成透明背景PNG图标、logo、贴纸
- 💬 **小白友好**：AI自动引导交互，推荐最优参数，不会返回任何技术命令/代码，全程自然语言对话
- 💾 **自动保存**：生成的图片自动保存到本地，返回可直接访问的CDN直链

## 🚀 安装方法
1. 进入你的Hermes技能目录：
   ```bash
   cd ~/.hermes/skills/media/
   ```
2. 克隆本仓库：
   ```bash
   git clone https://github.com/xueshanlinghu/panghu-ai-image-gen-skill.git
   ```
3. 配置API密钥：
   - 复制 `.env.example` 为 `.env`
   - 在 `.env` 中填写你的胖狐AI API密钥：
     ```env
     PANGHU_API_KEY=你的API密钥
     ```
4. 安装依赖：
   ```bash
   cd panghu-ai-image-gen-skill
   pip install requests python-dotenv
   # 或使用uv
   uv pip install requests python-dotenv
   ```
5. 重启Hermes Agent，技能会自动加载。

## 📝 使用方法
安装完成后，你只需要用自然语言和Hermes说你要生成图片就可以了，比如：
- "帮我生成一张赛博朋克城市夜景的4K电脑壁纸"
- "给我做一个透明背景的狐狸logo"
- "帮我修改这张图，给小猫加个圣诞帽"
- "生成一张小红书春季穿搭封面，3:4比例"

AI会自动和你确认需求、推荐合适的参数，生成完成后直接给你图片链接和本地保存路径，不需要你敲任何命令。

## ⚙️ 高级手动调用（给技术用户）
如果你想手动调用脚本，可以直接运行：
```bash
# 基础文生图（4K高清）
python scripts/generate.py --prompt "你的图片描述" --size "3840x2160" --quality high

# 生成手机壁纸
python scripts/generate.py --prompt "星空雪山" --size "2160x3840" --quality high

# 生成小红书3:4竖图
python scripts/generate.py --prompt "春季穿搭封面" --size "2448x3264" --quality high

# 透明背景logo
python scripts/generate.py --prompt "科技感狐狸logo" --size "2048x2048" --background transparent

# 图生图编辑
python scripts/generate.py --prompt "把猫变成白色" --image ./input.jpg --quality high

# 保存到指定路径
python scripts/generate.py --prompt "可爱橘猫" --save ./cat.png
```

## 📁 目录结构
```
panghu-ai-image-gen-skill/
├── SKILL.md              # Hermes技能规范（给AI看的交互规则）
├── README.md             # 本说明文件
├── LICENSE               # MIT开源协议
├── .gitignore            # Git过滤规则
├── .env.example          # 配置模板
├── .env                  # 本地配置（含API密钥，不上传）
├── scripts/
│   └── generate.py       # 核心生成脚本
├── references/
│   └── api-notes.md      # 接口技术参考文档
└── 生成结果/              # 生成图片默认保存目录（不上传）
```

## 📄 开源协议
MIT License © 2026 雪山凌狐

## 💡 注意事项
1. 使用前需要先在胖狐AI平台注册账号并充值积分，生成一张图片约消耗0.11积分（4K高清）
2. 4K高清图片生成约需60-120秒，请耐心等待，不要中断请求
3. 透明背景仅支持PNG/WebP格式，JPG不支持透明通道
4. 自定义尺寸宽高必须是16的倍数，总像素不超过830万，最长边不超过3840px
