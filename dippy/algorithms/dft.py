import numpy as np
np.seterr(divide="ignore")


def fft(src: np.ndarray) -> np.ndarray:
    f = np.fft.fft2(src)
    shift_f = np.fft.fftshift(f)
    spc = 20 * np.log(np.abs(shift_f))
    spc[np.isinf(spc)] = np.max(spc)
    spc = (spc / np.max(spc)) * 256
    unshift_f = np.fft.ifftshift(shift_f)
    i_f_xy = np.fft.ifft2(unshift_f).real
    return spc.astype(np.uint8), i_f_xy.astype(np.uint8)
