<p align="center">
  <h1 align="center">🦊 胖狐AI图片生成技能</h1>
  <p align="center">Hermes Agent 技能 | 支持 GPT Image 2.5 的文生图/图生图工具</p>
</p>

---

## 项目简介
这是一个为 Hermes Agent 开发的图片生成技能，对接胖狐AI图片接口，支持文生图、图生图/图片编辑和最高4K分辨率。

当前支持模型：
- `gpt-image-2.5-flare`：文生图推荐默认，速度更快。
- `gpt-image-2.5-sunburst`：图生图/编辑推荐默认，精准控制更强。
- `gpt-image-2`：继续兼容，可按需指定。

首次使用时，Agent 会向用户简要说明 Flare / Sunburst 的区别并完成一次默认模型选择；偏好写入本地 `.panghu-image-models.json`，以后可以单次临时切换，也可以长期修改默认值。

## 核心特性
- 文生图默认 `gpt-image-2.5-flare`
- 图生图默认 `gpt-image-2.5-sunburst`
- 支持首次 onboarding 与长期模型偏好
- 兼容 `gpt-image-2`
- 支持 4K、多比例、透明背景、自动保存和提示词模板

## 安装
```bash
cd ~/.hermes/skills/media/
git clone https://github.com/xueshanlinghu/panghu-ai-image-gen-skill.git
cd panghu-ai-image-gen-skill
cp .env.example .env
pip install requests python-dotenv
```

在 `.env` 填写：
```env
PANGHU_API_KEY=你的API密钥
```

## 使用
直接对 Hermes 说：
- “帮我生成一张赛博朋克城市夜景的4K电脑壁纸”
- “给我做一个透明背景的狐狸logo”
- “帮我修改这张图，给小猫加个圣诞帽”
- “这一次用 Sunburst 生成”
- “以后文生图都用 Sunburst”

首次生成前会完成一次模型偏好设置；之后自动沿用。

## 高级手动调用
```bash
# 文生图：默认自动选择 Flare
python scripts/generate.py --prompt "星空雪山"

# 图生图：默认自动选择 Sunburst
python scripts/generate.py --prompt "把猫变成白色" --image ./input.jpg

# 单次临时改模型
python scripts/generate.py --prompt "产品海报" --model gpt-image-2.5-sunburst

# 长期修改默认模型
python scripts/generate.py --set-text-model gpt-image-2.5-flare --set-edit-model gpt-image-2.5-sunburst

# 查看当前偏好
python scripts/generate.py --show-model-config
```

## 本地配置
`.panghu-image-models.json` 会在首次 onboarding 后生成，用于保存模型偏好。该文件已加入 `.gitignore`。

## 目录结构
```text
panghu-ai-image-gen-skill/
├── SKILL.md
├── README.md
├── .env.example
├── .gitignore
├── scripts/generate.py
├── references/api-notes.md
├── references/prompt-templates.md
└── 生成结果/
```

## 开源协议
MIT License © 2026 雪山凌狐
