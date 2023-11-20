from PIL import Image, ImageFont, ImageDraw
import string

def calculate_avg_pixel(char: str, font_size: int, font_name: str = "arial.ttf") -> float:
    font = ImageFont.truetype(font_name, font_size)
    _, _, x1, y1 = font.getbbox(char)
    img = Image.new('L', (x1, y1), color=255)
    draw = ImageDraw.Draw(img)
    draw.text((0, 0), char, font=font, fill=0)
    pixles = img.getdata()
    return -(sum(pixles) // len(pixles)) / 255

chars = string.printable
mapping = []
for char in string.printable:
    if char in list("\t\n\r\x0b\x0c"): continue
    avg = calculate_avg_pixel(char, 20)
    mapping.append((avg, char))
mapping.sort()

min_val, max_val = mapping[0][0], mapping[-1][0]
mapping = [((v - min_val) / (max_val - min_val), c) for v, c in mapping]


GRID_SIZE = (70, 70)

path = "badger.jpg"
img = Image.open(path).convert("L")
print(f"original size {img.size}")

resize_img = img.resize(GRID_SIZE, Image.HAMMING)
print(f"original size {resize_img.size}")

img_pixels = resize_img.getdata()
min_val, max_val = min(img_pixels), max(img_pixels)
img_pixels = [(p - min_val) / (max_val - min_val) for p in img_pixels]

i = 0
for _ in range(GRID_SIZE[1]):
    for _ in range(GRID_SIZE[0]):
        min_distance, min_char = float("inf"), ""
        pixel, i = img_pixels[i], i + 1
        for val, char in mapping:
            if (diff := abs(val - pixel)) < min_distance:
                min_distance, min_char = diff, char
        print(min_char, end="")
    print()
