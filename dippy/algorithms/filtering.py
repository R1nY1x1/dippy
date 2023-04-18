import numpy as np


def filtering(src: np.ndarray, kernel: np.ndarray) -> np.ndarray:
    """
    shape = (src.shape[0] - kernel.shape[0] + 1, src.shape[1] - kernel.shape[1] + 1) + kernel.shape
    strides = src.strides * 2
    tmp = np.lib.stride_tricks.as_strided(src, shape, strides)
    dst = np.zeros(src.shape)
    dst[1:-1, 1:-1] = np.einsum('kl,ijkl->ij', kernel, tmp).astype(np.uint8)
    """
    tmp = np.zeros((src.shape[0]+2, src.shape[1]+2))
    tmp[1:-1, 1:-1] = src
    shape = (tmp.shape[0] - kernel.shape[0] + 1, tmp.shape[1] - kernel.shape[1] + 1) + kernel.shape
    strides = tmp.strides * 2
    stride = np.lib.stride_tricks.as_strided(tmp, shape, strides)
    dst = np.einsum('kl,ijkl->ij', kernel, stride).astype(np.uint8)
    return dst
