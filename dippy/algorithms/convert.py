import numpy as np
np.seterr(divide='ignore', invalid='ignore')


def inverseNP(src: np.ndarray) -> np.ndarray:
    dst = 255 - src
    return dst


def convertColor(src: np.ndarray, method: str = "rgb2gray") -> np.ndarray:
    """
    https://docs.opencv.org/4.x/de/d25/imgproc_color_conversions.html
    """
    if len(src.shape) == 3:
        if method == "rgb2gray":
            # dst = np.apply_along_axis(
            #     lambda x: 0.299*x[0] + 0.587*x[1] + 0.114*x[2],
            #     # lambda x: 0.333*x[0] + 0.333*x[1] + 0.333*x[2],
            #     2,
            #     src)
            dst = 0.299*src[:, :, 0] + 0.587*src[:, :, 1] + 0.114*src[:, :, 2]
        elif method == "rgb2bgr":
            dst = src[:, :, [2, 1, 0]]
        elif method == "rgb2hsv":
            """
            V = max(R, G, B)
            S = (V - min(R, G, B)) / V
            H = if V == R then       60*(G-B) / (V-min(R, G, B)
                if V == G then 120 + 60*(B-R) / (V-min(R, G, B)
                if V == B then 240 + 60*(R-G) / (V-min(R, G, B)
            ---
            Expression H with index,
                (120 * i) + 60*(((i+1)%3)-(i-1)%3) / (V-min(R, G, B))
                where i == 0 is R, i == 1 is G, i == 2 is B
            ---
            """
            src = src.astype(np.int16)
            dst = src.copy()
            mins = np.min(src, axis=2)
            idxs = np.argmax(src, axis=2)
            tmp = np.rot90(np.rot90(src, axes=(1, 2)))
            addends = 60 * idxs
            minuends = np.choose((idxs + 1) % 3, tmp)
            subtrahends = np.choose((idxs - 1) % 3, tmp)
            v = np.choose(idxs, tmp)
            s = np.divide(
                    v - mins,
                    v,
                    out=np.zeros_like(v, dtype=np.float64),
                    where=(v != 0))
            h = addends + (60 * (minuends - subtrahends) / (v - mins))
            dst[:, :, 0] = h / 2
            dst[:, :, 1] = s * 255
            dst[:, :, 2] = v * 255
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


def tonecurve(src: np.ndarray, lut: np.ndarray = np.arange(256)) -> np.ndarray:
    dst = lut[src]
    return dst.astype(np.uint8)


def polygonalTC(src: np.ndarray, threshold: int = 128) -> np.ndarray:
    lut = np.full((256), 255)
    for i in range(threshold):
        lut[i] = i * (255 / threshold)
    dst = lut[src]
    return dst.astype(np.uint8)


def gammaTC(src: np.ndarray, gamma: float = 2) -> np.ndarray:
    lut = np.array([255 * (x / 255) ** (1 / gamma) for x in range(256)])
    dst = lut[src]
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
