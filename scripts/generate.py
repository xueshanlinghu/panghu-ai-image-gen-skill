#!/usr/bin/env python3
"""
胖狐AI图片生成脚本
支持文生图和图生图功能，支持 gpt-image-2.5-flare、gpt-image-2.5-sunburst 和 gpt-image-2。

@author: 雪山凌狐
@license: MIT
"""
import argparse
import json
import os
import re
import time
from pathlib import Path

import requests
from dotenv import load_dotenv

SKILL_DIR = Path(__file__).parent.parent
load_dotenv(SKILL_DIR / ".env")

API_URL_GENERATE = "https://api.ace.324567.xyz/openai/images/generations"
API_URL_EDIT = "https://api.ace.324567.xyz/openai/images/edits"
API_KEY = os.getenv("PANGHU_API_KEY")
OUTPUT_DIR = SKILL_DIR / "生成结果"
MODEL_CONFIG_PATH = SKILL_DIR / ".panghu-image-models.json"

SUPPORTED_MODELS = (
    "gpt-image-2.5-flare",
    "gpt-image-2.5-sunburst",
    "gpt-image-2",
)
RECOMMENDED_TEXT_MODEL = "gpt-image-2.5-flare"
RECOMMENDED_EDIT_MODEL = "gpt-image-2.5-sunburst"
FIXED_MODERATION = "low"


def sanitize_filename(text, max_len=20):
    """从提示词生成安全的文件名，过滤非法字符。"""
    text = re.sub(r'[\\/*?:"<>|]', "", text)
    text = text.strip().replace(" ", "_")[:max_len]
    return text if text else "generated_image"


def load_model_config():
    """读取本地模型偏好；缺失或损坏时回退到推荐默认。"""
    defaults = {
        "onboarding_completed": False,
        "text_to_image_model": RECOMMENDED_TEXT_MODEL,
        "image_to_image_model": RECOMMENDED_EDIT_MODEL,
    }
    if not MODEL_CONFIG_PATH.exists():
        return defaults

    try:
        with MODEL_CONFIG_PATH.open("r", encoding="utf-8") as f:
            config = json.load(f)
    except (OSError, json.JSONDecodeError):
        return defaults

    result = defaults.copy()
    result["onboarding_completed"] = bool(config.get("onboarding_completed", False))
    for key in ("text_to_image_model", "image_to_image_model"):
        value = config.get(key)
        if value in SUPPORTED_MODELS:
            result[key] = value
    return result


def save_model_config(text_model=None, edit_model=None):
    """保存长期模型偏好。"""
    config = load_model_config()
    if text_model is not None:
        config["text_to_image_model"] = text_model
    if edit_model is not None:
        config["image_to_image_model"] = edit_model
    config["onboarding_completed"] = True
    with MODEL_CONFIG_PATH.open("w", encoding="utf-8") as f:
        json.dump(config, f, ensure_ascii=False, indent=2)
        f.write("\n")
    return config


def resolve_model(args):
    """按 单次覆盖 > 本地偏好 > 内置推荐 的优先级选择模型。"""
    if args.model:
        return args.model, "单次指定"

    config = load_model_config()
    if args.image:
        return config["image_to_image_model"], "图生图默认"
    return config["text_to_image_model"], "文生图默认"


def main():
    parser = argparse.ArgumentParser(description="使用胖狐AI生成图片")
    parser.add_argument("--prompt", help="图片描述提示词（最长支持32000字符）")
    parser.add_argument("--image", help="图生图模式下的输入图片路径")
    parser.add_argument("--model", choices=SUPPORTED_MODELS, help="仅本次生成覆盖默认模型")
    parser.add_argument("--set-text-model", choices=SUPPORTED_MODELS, help="长期设置文生图默认模型")
    parser.add_argument("--set-edit-model", choices=SUPPORTED_MODELS, help="长期设置图生图默认模型")
    parser.add_argument("--show-model-config", action="store_true", help="显示当前模型偏好")
    parser.add_argument("--size", default="3840x2160", help="图片尺寸：宽x高（默认3840x2160 4K横屏）")
    parser.add_argument("--quality", default="high", choices=["auto", "high", "medium", "low"], help="图片质量，默认high最高清")
    parser.add_argument("--background", default="auto", choices=["auto", "transparent", "opaque"], help="背景模式：透明/不透明/自动")
    parser.add_argument("--output_format", default="png", choices=["png", "jpeg", "webp"], help="输出图片格式，默认png")
    parser.add_argument("--save", help="自定义本地保存路径，默认自动保存到生成结果目录")
    parser.add_argument("--no-save", action="store_true", help="不自动保存到本地，仅返回URL")

    args = parser.parse_args()

    if args.set_text_model or args.set_edit_model:
        config = save_model_config(args.set_text_model, args.set_edit_model)
        print("✅ 默认模型偏好已保存")
        print(f"文生图：{config['text_to_image_model']}")
        print(f"图生图：{config['image_to_image_model']}")
        if not args.prompt:
            return 0

    if args.show_model_config:
        config = load_model_config()
        print(json.dumps(config, ensure_ascii=False, indent=2))
        if not args.prompt:
            return 0

    if not args.prompt:
        parser.error("生成图片时必须提供 --prompt")

    if not API_KEY:
        print("❌ 错误：.env文件中未配置PANGHU_API_KEY")
        return 1

    headers = {
        "accept": "application/json",
        "authorization": f"Bearer {API_KEY}",
    }

    if args.background == "transparent" and args.output_format == "jpeg":
        args.output_format = "png"
        print("ℹ️  透明背景自动切换为png格式以支持透明通道")

    selected_model, model_source = resolve_model(args)
    data = {
        "model": selected_model,
        "prompt": args.prompt,
        "n": "1",
        "size": args.size,
        "quality": args.quality,
        "response_format": "url",
        "output_format": args.output_format,
        "background": args.background,
        "moderation": FIXED_MODERATION,
    }

    files = None
    if args.image:
        image_path = Path(args.image)
        if not image_path.exists():
            print(f"❌ 错误：输入图片不存在：{args.image}")
            return 1
        suffix = image_path.suffix.lower()
        mime_map = {
            ".jpg": "image/jpeg",
            ".jpeg": "image/jpeg",
            ".png": "image/png",
            ".webp": "image/webp",
        }
        mime_type = mime_map.get(suffix, "image/jpeg")
        files = {"image": (image_path.name, open(image_path, "rb"), mime_type)}
        print("🖼️  图生图模式：已加载输入图片")

    print("🎨 正在生成图片...")
    print(f"🤖 模型：{selected_model}（{model_source}）")
    print(f"📝 提示词：{args.prompt[:100]}{'...' if len(args.prompt) > 100 else ''}")
    print(f"📐 尺寸：{args.size} | 质量：{args.quality} | 格式：{args.output_format}")
    print("⏳ 请稍候，高清/4K图片生成可能需要1-5分钟，请耐心等待不要中断...")

    try:
        if files:
            response = requests.post(API_URL_EDIT, headers=headers, data=data, files=files, timeout=1800)
        else:
            headers["content-type"] = "application/json"
            response = requests.post(API_URL_GENERATE, headers=headers, json=data, timeout=1800)

        response.raise_for_status()
        result = response.json()

        if not result.get("success", False):
            error = result.get("error", {})
            print(f"❌ 生成失败：{error.get('message', '未知错误')}")
            print(f"错误码：{error.get('code', 'unknown')}")
            return 1

        image_url = result["data"][0]["url"]
        elapsed = result.get("elapsed", 0)
        cost = result.get("cost", {}).get("amount", 0)
        total_tokens = result.get("usage", {}).get("total_tokens", 0)
        task_id = result.get("task_id")

        print("\n✅ 图片生成成功！")
        print(f"🔗 图片地址：{image_url}")
        print(f"⏱️  生成耗时：{elapsed:.1f} 秒")
        print(f"💰 消耗积分：{cost} 点")
        print(f"🔢 总Token用量：{total_tokens}")
        print(f"🆔 任务ID：{task_id}")

        if not args.no_save:
            if args.save:
                save_path = Path(args.save)
            else:
                OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
                ts = time.strftime("%Y%m%d_%H%M%S")
                filename = f"{sanitize_filename(args.prompt)}_{ts}.{args.output_format}"
                save_path = OUTPUT_DIR / filename

            save_path.parent.mkdir(parents=True, exist_ok=True)
            print(f"\n💾 正在保存图片到 {save_path}...")
            img_response = requests.get(image_url, timeout=300)
            img_response.raise_for_status()
            with open(save_path, "wb") as f:
                f.write(img_response.content)
            print("✅ 图片保存成功！")

        return 0

    except requests.exceptions.RequestException as e:
        print(f"❌ 请求失败：{str(e)}")
        if hasattr(e, "response") and e.response is not None:
            print(f"返回内容：{e.response.text[:500]}")
        return 1
    finally:
        if files and "image" in files:
            files["image"][1].close()


if __name__ == "__main__":
    raise SystemExit(main())
