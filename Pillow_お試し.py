from PIL import Image, ImageDraw, ImageFont

img = Image.new("RGB", (200, 300), (255, 255, 255))
draw = ImageDraw.Draw(img)
draw.rectangle([(0, 0), (199, 299)], outline=(0, 0, 0), width=5)
font = ImageFont.truetype("seguisym.ttf", 128) #
draw.text((10, 100), "\u2666", fill=(255, 0, 0), font=font)  # ♦
draw.text((110, 100), "1", fill=(0, 0, 0), font=font)        # 1
img.show()  # VS Codeなら画像ビューアで開く
