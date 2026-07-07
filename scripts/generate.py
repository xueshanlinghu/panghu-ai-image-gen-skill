#!/usr/bin/env python3
"""
胖狐AI图片生成脚本
支持文生图和图生图功能，基于gpt-image-2模型

@author: 雪山凌狐
@license: MIT
"""
import os
import argparse
import requests
from dotenv import load_dotenv
from pathlib import Path

# 从技能目录下的.env文件加载环境变量
SKILL_DIR = Path(__file__).parent.parent
load_dotenv(SKILL_DIR / ".env")

API_URL = "https://api.acedata.cloud/openai/images/generations"
API_KEY = os.getenv("PANGHU_API_KEY")

def main():
    parser = argparse.ArgumentParser(description="使用胖狐AI生成图片")
    parser.add_argument("--prompt", required=True, help="图片描述提示词（最长支持32000字符）")
    parser.add_argument("--image", help="图生图模式下的输入图片路径")
    parser.add_argument("--size", default="1024x1024", help="图片尺寸：宽x高（例如1024x1024、3840x2160，也可填auto自动选择）")
    parser.add_argument("--quality", default="auto", choices=["auto", "high", "medium", "low"], help="图片质量")
    parser.add_argument("--background", default="auto", choices=["auto", "transparent", "opaque"], help="背景模式：透明/不透明/自动")
    parser.add_argument("--output_format", default="png", choices=["png", "jpeg", "webp"], help="输出图片格式")
    parser.add_argument("--save", help="本地保存路径（例如./output.png），不填则仅返回URL")
    
    args = parser.parse_args()
    
    if not API_KEY:
        print("❌ 错误：.env文件中未配置PANGHU_API_KEY")
        return 1
    
    headers = {
        "accept": "application/json",
        "authorization": f"Bearer {API_KEY}",
    }
    
    # 基础参数
    data = {
        "model": "gpt-image-2",
        "prompt": args.prompt,
        "n": "1",
        "size": args.size,
        "quality": args.quality,
        "response_format": "url",
        "output_format": args.output_format,
        "background": args.background
    }
    
    files = None
    # 如果传入了输入图片则开启图生图模式，使用multipart/form-data上传
    if args.image:
        image_path = Path(args.image)
        if not image_path.exists():
            print(f"❌ 错误：输入图片不存在：{args.image}")
            return 1
        # 构造multipart文件上传
        files = {
            "image": (image_path.name, open(image_path, "rb"), f"image/{args.output_format if args.output_format != 'jpg' else 'jpeg'}")
        }
        # 图生图模式不设置Content-Type，让requests自动生成multipart/form-data边界
        print("🖼️  图生图模式：已加载输入图片")
    
    print(f"🎨 正在生成图片...")
    print(f"📝 提示词：{args.prompt[:100]}{'...' if len(args.prompt) > 100 else ''}")
    print(f"📐 尺寸：{args.size} | 质量：{args.quality} | 格式：{args.output_format}")
    print("⏳ 请稍候，高清/4K图片生成可能需要30-120秒...")
    
    try:
        if files:
            # 图生图用multipart/form-data
            response = requests.post(API_URL, headers=headers, data=data, files=files, timeout=180)
        else:
            # 文生图用application/json
            headers["content-type"] = "application/json"
            response = requests.post(API_URL, headers=headers, json=data, timeout=180)
        
        response.raise_for_status()
        result = response.json()
        
        if not result.get("success", False):
            error = result.get("error", {})
            print(f"❌ 生成失败：{error.get('message', '未知错误')}")
            print(f"错误码：{error.get('code', 'unknown')}")
            return 1
        
        # 解析成功返回结果
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
        
        # 如果指定了保存路径则下载到本地
        if args.save:
            save_path = Path(args.save)
            save_path.parent.mkdir(parents=True, exist_ok=True)
            print(f"\n💾 正在保存图片到 {save_path}...")
            img_response = requests.get(image_url, timeout=60)
            img_response.raise_for_status()
            with open(save_path, "wb") as f:
                f.write(img_response.content)
            print(f"✅ 图片保存成功！")
        
        return 0
        
    except requests.exceptions.RequestException as e:
        print(f"❌ 请求失败：{str(e)}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"返回内容：{e.response.text[:500]}")
        return 1
    finally:
        if files and "image" in files:
            files["image"][1].close()

if __name__ == "__main__":
    exit(main())
