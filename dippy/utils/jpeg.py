import numpy as np


SJpegProperty = {
    "CanDecode": None,
    "HSize": None,
    "VSize": None,
    "Dimension": None,
    "SamplePrecision": None,
    "CommentP": None,
    "Format": None,
    "MajorRevisions": None,
    "MinorRevisions": None,
    "Units": None,
    "HDensity": None,
    "VDensity": None,
    "HThumbnail": None,
    "VThumbnail": None,
    "ExtensionCode": None
}

kYDcDhtT = [
    0xff, 0xc4,
    0x00, 0x1f,
    0x00,
    0x00, 0x01, 0x05, 0x01, 0x01, 0x01, 0x01, 0x01,
    0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07,
    0x08, 0x09, 0x0a, 0x0b
]

kCDcDhtT = []
kYAcDhtT = []
kCAcDhtT = []

SHuffmanCodeTable = {
    "numOfElement": None,
    "SizeTP": None,
    "CodeTP": None
}

kYDcSizeT = [
    0x0002, 0x0003, 0x0003, 0x0003,
    0x0003, 0x0003, 0x0004, 0x0005,
    0x0006, 0x0007, 0x0008, 0x0009
]

kYDcCodeT = [
    0x0000, 0x0002, 0x0003, 0x0004,
    0x0005, 0x0006, 0x000e, 0x001e,
    0x003e, 0x007e, 0x00fe, 0x01fe
]

SHuffmanDecodeTable = {
    "numOfElement": None,
    "SizeTP": None,
    "CodeTP": None,
    "ValueTP": None
}

kYQuantumT = [
    16, 11, 10, 16, 24, 40, 51, 61,
    12, 12, 14, 19, 26, 58, 60, 55,
    14, 13, 16, 24, 40, 57, 69, 56,
    14, 17, 22, 29, 51, 87, 80, 62,
    18, 22, 37, 56, 68, 109, 103, 77,
    24, 35, 55, 64, 81, 104, 113, 92,
    49, 64, 78, 87, 103, 121, 120, 101,
    72, 92, 95, 98, 112, 100, 103, 99
]

mQTA = [[0 for _ in range(64)] for _ in range(4)]

# eMarker
emSOF0 = 0xc0
emDHT = 0xc4
emSOI = 0xd8
emEOI = 0xd9
