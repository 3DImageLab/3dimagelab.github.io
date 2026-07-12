#!/usr/bin/env python3
"""批量压缩网站图片：缩放到合理尺寸 + 转换为WebP格式"""

from PIL import Image
import os

BASE = os.path.dirname(os.path.abspath(__file__))
IMAGES = os.path.join(BASE, 'images')

# 需要处理的图片配置：(相对路径, 最大宽度, 最大高度, WebP质量)
CONFIGS = [
    # Gallery - 原始5712x4284，缩到1920宽度用于全屏轮播
    ('gallery/河北-野三坡.jpg', 1920, 1080, 80),
    ('gallery/河北-野三坡2.jpg', 1920, 1080, 80),
    ('gallery/古北水镇-scaled.jpeg', 1920, 1080, 80),
    # Research - 卡片图，640宽够用
    ('research/affective.jpg', 640, 400, 75),
    ('research/detection.jpg', 640, 400, 75),
    ('research/simulation.jpg', 640, 400, 75),
    ('research/llm_decision.jpg', 640, 400, 75),
    # Faculty - 头像，200px足够
    ('team/faculty/zhuojunbao.png', 200, 200, 75),
    ('team/faculty/liuqiankun.png', 200, 200, 75),
    ('team/faculty/wangwei.jpg', 200, 200, 75),
    ('team/faculty/hutianyu.jpg', 200, 200, 75),
    ('team/faculty/zoubochao.jpg', 200, 200, 75),
    ('team/faculty/chenjiansheng.jpg', 200, 200, 75),
    ('team/faculty/mahuimin.jpg', 200, 200, 75),
    ('team/faculty/wangrongquan.jpg', 200, 200, 75),
    ('team/faculty/tansongchao.png', 200, 200, 75),
]

def process_image(rel_path, max_w, max_h, quality):
    src = os.path.join(IMAGES, rel_path)
    if not os.path.exists(src):
        print(f"  SKIP (not found): {rel_path}")
        return None

    # 生成WebP路径
    base, _ = os.path.splitext(rel_path)
    webp_rel = base + '.webp'
    webp_path = os.path.join(IMAGES, webp_rel)

    orig_size = os.path.getsize(src)
    print(f"  {rel_path} ({orig_size//1024}KB) → {webp_rel}")

    img = Image.open(src)
    # 如果有alpha通道，转为RGB（WebP需要）
    if img.mode in ('RGBA', 'P'):
        bg = Image.new('RGB', img.size, (255, 255, 255))
        if img.mode == 'P':
            img = img.convert('RGBA')
        bg.paste(img, mask=img.split()[3] if 'A' in img.mode else None)
        img = bg
    elif img.mode != 'RGB':
        img = img.convert('RGB')

    # 等比缩放
    w, h = img.size
    ratio = min(max_w / w, max_h / h, 1.0)
    if ratio < 1.0:
        new_w, new_h = int(w * ratio), int(h * ratio)
        img = img.resize((new_w, new_h), Image.LANCZOS)
        print(f"    resize: {w}x{h} → {new_w}x{new_h}")
    else:
        print(f"    keep: {w}x{h}")

    # 保存WebP
    img.save(webp_path, 'WEBP', quality=quality, method=4)
    new_size = os.path.getsize(webp_path)
    saving = (1 - new_size / orig_size) * 100
    print(f"    {orig_size//1024}KB → {new_size//1024}KB (节省 {saving:.0f}%)")

    return webp_rel

if __name__ == '__main__':
    print("=== 图片优化开始 ===\n")
    results = []
    for rel_path, max_w, max_h, quality in CONFIGS:
        result = process_image(rel_path, max_w, max_h, quality)
        if result:
            results.append((rel_path, result))

    print("\n=== 完成！替换对照表 ===")
    for old, new in results:
        print(f"  {old} → {new}")