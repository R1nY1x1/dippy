# dippy

Dippy is DIP(Digital Image Processing) in Python3.

This library depends on Numpy only.


## Installation

```
$ pip install dip-python
```

## Features

### Algorithm

- [ ] Convert
    - [ ] Color
        - [x] rgb2gray
        - [x] rgb2bgr
        - [ ] rgb2hsv
    - [x] binarize
        - [x] threshold
        - [x] otsu
    - [ ] Histgram Equalization
    - [ ] Tonecurve
        - [ ] Polygonal
        - [ ] Gamma
        - [ ] Sin
        - [x] Posterization
            - [x] Nearest Neighhbor
            - [x] Equality
        - [ ] Solarization
    - [ ] Dithering(support 2way)
        - [x] Nearest Neighbor
        - [x] Floyd-Steinberg
        - [x] Sierra Lite
        - [x] Atkinson
        - [ ] Poison Disk Sampling
        - [ ] Mosaic
    - [ ] Declease Color
        - [x] kMeans
- [ ] Filtering
    - [ ] Spatial
        - [ ] Average
        - [ ] Weighted Average
        - [ ] Gaussian
        - [ ] Prewitt
        - [ ] Sobel
        - [ ] Laplacian
        - [ ] Sharping
        - [ ] k-Nearest Neighbor
        - [ ] Bilateral
        - [ ] Non-Local Mean
        - [ ] Median
    - [ ] Freaquency
        - [ ] Low Pass
        - [ ] High Pass
        - [ ] Band Pass
        - [ ] High Emphasis
        - [ ] Gaussian Low Pass
        - [ ] Gaussian High Pass
        - [ ] Gaussian Band Pass
        - [ ] Gaussian High Emphasis
- [ ] Resize
    - [x] Bi-Linear
- [ ] Image Operation
    - [ ] Alpha Blending
    - [ ] Emboss
    - [ ] Mask

### Utils

- [ ] I/O
    - [x] BMP
    - [x] PNG
    - [ ] JPEG
    - [ ] GIF

### Extra

- [x] Print
    - [x] Braile
    - [x] AA
    - [x] Animation
- [ ] TUI
    - [x] Print
        - [x] Image
        - [x] Histgram
        - [x] Spectrum
    - [ ] Processing
