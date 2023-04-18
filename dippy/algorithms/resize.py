import numpy as np
from typing import Tuple


def resize(src: np.ndarray, size: Tuple[int, int]) -> np.ndarray:
    if len(src.shape) == 3:
        size = (size[0], size[1], 3)
    dst = np.empty(size)
    for y_dst in range(0, size[0]):
        y_src = y_dst / (size[0] / float(src.shape[0]))
        oy_src = int(y_src)
        if oy_src > (src.shape[0] - 2):
            oy_src = src.shape[0] - 2
        w_y = y_src - oy_src
        for x_dst in range(0, size[1]):
            x_src = x_dst / (size[1] / float(src.shape[1]))
            ox_src = int(x_src)
            if ox_src > (src.shape[1] - 2):
                ox_src = src.shape[1] - 2
            w_x = x_src - ox_src
            dst[y_dst][x_dst] = (
                (1 - w_x) * (1 - w_y) * src[oy_src][ox_src]
                + w_x * (1 - w_y) * src[oy_src][ox_src+1]
                + (1 - w_x) * w_y * src[oy_src+1][ox_src]
                + w_x * w_y * src[oy_src+1][ox_src+1]
            )
    return dst.astype(np.uint8)
