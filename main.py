import json
from PIL import Image
import os

# 读取 JSON 文件
with open('SpriteInfo.json', 'r') as file:
    data = json.load(file)

# 图片文件名和路径
image_files = {
    "Knight": "Knight.png",
    "Knight Slug Cln": "Knight Slug Cln.png",
    "Knight Dream Gate Cln": "Knight Dream Gate Cln.png",
    "Spell Effects 2": "Spell Effects 2.png"
}

# 创建输出文件夹
output_dir = 'output'
os.makedirs(output_dir, exist_ok=True)

# 处理每个 sprite
for idx, (sid, sx, sy, swidth, sheight, sfilpped, scollectionname,spath) in enumerate(zip(
    data['sid'],
    data['sx'],
    data['sy'],
    data['swidth'],
    data['sheight'],
    data['sfilpped'],
    data['scollectionname'],
    data['spath']
)):
    image_file = image_files.get(scollectionname)
    output_path = os.path.join('output', spath)
    if image_file and not os.path.exists(output_path):
        # 加载图片
        try:
            img = Image.open(image_file)
        except FileNotFoundError as e:
            print(f"Error: {e}. File {image_file} not found.")
            continue  
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
        # 计算裁剪区域,裁剪图片
        if not sfilpped:
            left = sx
            top = img.height - sy - sheight
            right = left + swidth
            bottom = top + sheight
        else:
            left = sx
            top = img.height - sy - swidth # 翻转y轴
            right = left + sheight
            bottom = top + swidth 
        sprite = img.crop((left, top, right, bottom))      
        if sfilpped:      
            # 水平镜像
            sprite = sprite.transpose(Image.FLIP_LEFT_RIGHT)
            # 顺时针旋转 90 度
            sprite = sprite.rotate(-90, expand=True)
        # 保存裁剪后的图片
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        sprite.save(os.path.join(output_dir, spath))
        print(f"{output_path} OK")
    else:
        print(f"file already exist{output_path}")
print("done")
