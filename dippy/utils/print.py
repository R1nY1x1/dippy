import math
import numpy as np


def printImg(img: np.ndarray, rate: float = 1):
    brailles = img2braille(img, rate)
    for b in brailles:
        print(b)


def printImgXY(img: np.ndarray, x: int, y: int, fc: int = 7, rate: float = 1):
    """
    fc = ColorCode:
        0: Black
        1: Red
        2: Green
        3: Yellow
        4: Blue
        5: Magenta
        6: Cyan
        7: White
    """
    brailles = img2braille(img, rate)
    print(f"\033[{y-1};1H")
    for b in brailles:
        print(f"\033[{x+1}G\033[{fc+30}m"+b)
    print("\033[0m")


def img2braille(img: np.ndarray, rate: float = 1) -> list:
    brailles = []
    for y in range(0, img.shape[1], math.ceil(4/rate)):
        tmp = ""
        for x in range(0, img.shape[0], math.ceil(2/rate)):
            flags = 0
            try:
                flags += (0b00000001 if img[y][x] else 0)
                flags += (0b00000010 if img[y+1][x] else 0)
                flags += (0b00000100 if img[y+2][x] else 0)
                flags += (0b00001000 if img[y+3][x] else 0)
                flags += (0b00010000 if img[y][x+1] else 0)
                flags += (0b00100000 if img[y+1][x+1] else 0)
                flags += (0b01000000 if img[y+2][x+1] else 0)
                flags += (0b10000000 if img[y+3][x+1] else 0)
            except IndexError:
                continue
            braille = 0x2800
            braille += (flags & 0b00001000) << 3
            braille += (flags & 0b01110000) >> 1
            braille += (flags & 0b10000111)
            tmp += chr(braille)
        brailles.append(tmp)
    return brailles
