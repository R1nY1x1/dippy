import numpy as np
np.seterr(divide='ignore', invalid='ignore')


def inverseNP(src: np.ndarray) -> np.ndarray:
    dst = 255 - src
    return dst


def convertColor(src: np.ndarray, method: str = "rgb2gray") -> np.ndarray:
    if len(src.shape) == 3:
        if method == "rgb2gray":
            """
            dst = np.apply_along_axis(
                lambda x: 0.299*x[0] + 0.587*x[1] + 0.114*x[2],
                # lambda x: 0.333*x[0] + 0.333*x[1] + 0.333*x[2],
                2,
                src)
            """
            dst = 0.299*src[:, :, 0] + 0.587*src[:, :, 1] + 0.114*src[:, :, 2]
        elif method == "rgb2bgr":
            dst = src[:, :, [2, 1, 0]]
    return dst.astype(np.uint8)


def binarize(src: np.ndarray, method: str = "threshold", threshold: int = 128) -> np.ndarray:
    if method == "threshold":
        lut = np.zeros((256))
        lut[threshold:] = 255
        dst = lut[src]
    elif method == "otsu":
        hist, _ = np.histogram(src, bins=256, range=[0, 256])
        hist_norm = hist.ravel()/hist.sum()
        Q = hist_norm.cumsum()
        bins = np.arange(256)
        fn_min = np.inf
        threshold = -1
        for i in range(1, 256):
            p1, p2 = np.hsplit(hist_norm, [i, ])
            q1, q2 = Q[i], Q[255]-Q[i]
            if q1 < 1.e-6 or q2 < 1.e-6:
                continue
            b1, b2 = np.hsplit(bins, [i, ])
            m1, m2 = np.sum(p1*b1)/q1, np.sum(p2*b2)/q2
            v1, v2 = np.sum(((b1-m1)**2)*p1)/q1, np.sum(((b2-m2)**2)*p2)/q2
            fn = (v1*q1) + (v2*q2)
            if fn < fn_min:
                fn_min = fn
                threshold = i
        dst = np.where(src <= threshold, 0, 255)
    return dst.astype(np.uint8)


def posterization(src: np.ndarray, method: str = "nearest_neighbor", tone=8) -> np.ndarray:
    lut = np.zeros((256))
    if method == "nearest_neighbor":
        tmp = 255 / ((tone - 1) * 2)
        for t in range(1, tone):
            lut[int(tmp*(2*t-1)):] = int((255/(tone-1)) * t)
    elif method == "equality":
        for t in range(1, tone):
            lut[int((255/tone)*t):] = int((255/(tone-1)) * t)
    dst = lut[src]
    return dst.astype(np.uint8)
