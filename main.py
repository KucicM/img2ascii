from typing import List, Tuple
from PIL import Image, ImageFont, ImageDraw

class Img2Text:
    __CHARS = """0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~ """
    __FONT = ImageFont.truetype("arial.ttf", 20)
    def __init__(self):
        m = sorted([(self._mean_char_pixel(c), c) for c in self.__CHARS])
        self.chars = [c for _, c in m]
        self.ws = [(w - m[0][0]) / (m[-1][0] - m[0][0]) for w, _ in m]

    def _mean_char_pixel(self, char: str) -> float:
        img = Image.new('L', self.__FONT.getbbox(char)[2:], color=255)
        draw = ImageDraw.Draw(img)
        draw.text((0, 0), char, font=self.__FONT, fill=0)
        pixles = img.getdata()
        return -sum(pixles) // len(pixles)

    def render(self, img, new_size: Tuple[int, int]) -> str:
        rimg = img.resize(new_size, Image.HAMMING)
        pixels = self._norm_img(rimg.getdata())
        chars = [self._find(p) for p in pixels]
        batches = [chars[i:i+rimg.size[0]] for i in range(0, len(chars), rimg.size[0])]
        return "\n".join(("".join(b) for b in batches))
    
    def _norm_img(self, pixels: List[int]) -> List[float]:
        min_val, max_val = min(pixels), max(pixels)
        return [(p - min_val) / (max_val - min_val) for p in pixels]

    def _find(self, pixel: float) -> str:
        l, h = 0, len(self.ws) -1
        while l <= h:
            mid = (h + l) // 2
            if pixel < self.ws[mid]: h = mid - 1
            elif pixel > self.ws[mid]: l = mid + 1
            else: return self.chars[mid]
        return self.chars[l] if (self.ws[l] - pixel) < (pixel - self.ws[h]) else self.chars[h]


if __name__ == "__main__":
    img = Image.open("badger.jpg").convert("L")
    img2Text = Img2Text()
    print(img2Text.render(img, (128, 64)))

