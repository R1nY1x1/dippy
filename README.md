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
    - [x] Inverse NegPog
    - [x] Color
        - [x] rgb2gray
        - [x] rgb2bgr
        - [x] rgb2hsv
    - [x] binarize
        - [x] threshold
        - [x] otsu
    - [ ] Histgram Equalization
    - [x] Tonecurve
        - [x] Polygonal
        - [x] Gamma
        - [x] Posterization
            - [x] Nearest Neighhbor
            - [x] Equality
    - [ ] Dithering(support 2way)
        - [x] Nearest Neighbor
        - [x] Floyd-Steinberg
        - [x] Sierra Lite
        - [x] Atkinson
        - [ ] Poison Disk Sampling
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
    - [ ] Nearest Neighbor
    - [x] Bi-Linear
    - [ ] Bi-Cubic
    - [ ] Lanczos
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
