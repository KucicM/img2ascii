from collections import namedtuple
import string


from PIL import Image, ImageFont, ImageDraw

PixelMapping = namedtuple("PixleMapping", ["chars", "weights"])

def computeMapping() -> PixelMapping:
    m = []
    for char in string.printable:
        if char in list("\t\n\r\x0b\x0c"): continue
        m.append((mean_char_pixel(char), char))
    m.sort()
    return PixelMapping(chars=[c for _, c in m], weights=[(w - m[0][0]) / (m[-1][0] - m[0][0]) for w, _ in m])

def mean_char_pixel(char: str, font_size: int = 20, font_name: str = "arial.ttf") -> float:
    font = ImageFont.truetype(font_name, font_size)
    _, _, x1, y1 = font.getbbox(char)
    img = Image.new('L', (x1, y1), color=255)
    draw = ImageDraw.Draw(img)
    draw.text((0, 0), char, font=font, fill=0)
    pixles = img.getdata()
    return -sum(pixles) // len(pixles)

mapping = computeMapping()

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
        for val, char in zip(mapping.weights, mapping.chars):
            if (diff := abs(val - pixel)) < min_distance:
                min_distance, min_char = diff, char
        print(min_char, end="")
    print()
