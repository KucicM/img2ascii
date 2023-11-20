from typing import List, Tuple
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


def render(img: List[float], size: Tuple[int, int], map: PixelMapping) -> str:
    _, w = size
    ret, line = [], []
    for pixel in img:
        line.append(closes(map, pixel))
        if len(line) == w:
            ret.append("".join(line))
            line = []
    return "\n".join(ret)

def closes(map: PixelMapping, pixel: float) -> str:
    min_c, min_v = "", float("inf")
    for c, v in zip(map.chars, map.weights):
        if (diff := abs(v - pixel)) < min_v:
            min_c, min_v = c, diff
    return min_c

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

print(render(img_pixels, resize_img.size, mapping))

