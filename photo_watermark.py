import os
import sys
import argparse
from PIL import Image, ImageDraw, ImageFont
import piexif
from datetime import datetime

# 支持的图片格式
SUPPORTED_FORMATS = ['.jpg', '.jpeg', '.png']

# 水印位置映射
POSITION_MAP = {
    'top-left': (0, 0),
    'top-right': (1, 0),
    'bottom-left': (0, 1),
    'bottom-right': (1, 1),
    'center': (0.5, 0.5)
}

def get_exif_date(img_path):
    try:
        exif_dict = piexif.load(img_path)
        date_str = exif_dict['Exif'].get(piexif.ExifIFD.DateTimeOriginal)
        if date_str:
            date = date_str.decode().split(' ')[0].replace(':', '-')
            return date
    except Exception:
        pass
    return None

def add_watermark(img_path, out_path, text, font_size, color, position):
    image = Image.open(img_path).convert('RGBA')
    txt_layer = Image.new('RGBA', image.size, (255,255,255,0))
    draw = ImageDraw.Draw(txt_layer)
    try:
        font = ImageFont.truetype("arial.ttf", font_size)
    except:
        font = ImageFont.load_default()
    # 兼容 Pillow 新旧版本
    try:
        bbox = draw.textbbox((0, 0), text, font=font)
        text_size = (bbox[2] - bbox[0], bbox[3] - bbox[1])
    except AttributeError:
        text_size = draw.textsize(text, font=font)
    pos = calc_position(image.size, text_size, position)
    draw.text(pos, text, font=font, fill=color+(128,))
    watermarked = Image.alpha_composite(image, txt_layer).convert('RGB')
    watermarked.save(out_path)

def calc_position(img_size, text_size, position):
    x_ratio, y_ratio = POSITION_MAP.get(position, (1,1))
    x = int((img_size[0] - text_size[0]) * x_ratio)
    y = int((img_size[1] - text_size[1]) * y_ratio)
    return (x, y)

def process_images(src_path, font_size, color, position):
    if os.path.isfile(src_path):
        files = [src_path]
        base_dir = os.path.dirname(src_path)
    else:
        files = [os.path.join(dp, f) for dp, dn, filenames in os.walk(src_path) for f in filenames]
        base_dir = src_path
    out_dir = os.path.join(base_dir, '_watermark')
    os.makedirs(out_dir, exist_ok=True)
    for file in files:
        ext = os.path.splitext(file)[1].lower()
        if ext not in SUPPORTED_FORMATS:
            continue
        date = get_exif_date(file)
        if not date:
            print(f"跳过无EXIF时间的图片: {file}")
            continue
        out_path = os.path.join(out_dir, os.path.basename(file))
        add_watermark(file, out_path, date, font_size, color, position)
        print(f"已处理: {file} -> {out_path}")

def parse_color(color_str):
    if color_str.startswith('#') and len(color_str) == 7:
        return tuple(int(color_str[i:i+2], 16) for i in (1, 3, 5))
    # 支持常见英文色名
    COLORS = {'red':(255,0,0), 'green':(0,255,0), 'blue':(0,0,255), 'white':(255,255,255), 'black':(0,0,0)}
    return COLORS.get(color_str.lower(), (255,255,255))

def main():
    print('批量图片EXIF水印工具')
    path = input('请输入图片文件或目录路径: ').strip()
    while not os.path.exists(path):
        print('路径不存在，请重新输入。')
        path = input('请输入图片文件或目录路径: ').strip()

    while True:
        try:
            font_size = int(input('请输入字体大小（如30）: ').strip())
            if font_size > 0:
                break
        except Exception:
            pass

    color_str = input('请输入字体颜色（如#FF0000或red）: ').strip()
    color = parse_color(color_str)

    print('可选位置: ' + ', '.join(POSITION_MAP.keys()))
    while True:
        position = input('请输入水印位置: ').strip()
        if position in POSITION_MAP:
            break

    process_images(path, font_size, color, position)

if __name__ == '__main__':
    main()
