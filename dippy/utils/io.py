import zlib
import binascii
from typing import Tuple
import numpy as np


def b2ndarray(bimg: bytes, width: int, height: int, isColor: bool) -> np.ndarray:
    ndimg = (np.frombuffer(bimg, dtype=np.uint8))
    if isColor:
        ndimg = ndimg.reshape([height, width, 3], order='C').copy()
        # ndimg = ndimg.transpose(0, 2, 1).copy()
    else:
        ndimg = ndimg.reshape([height, width], order='C').copy()
        # ndimg = ndimg.T.copy()
    return ndimg


def ndarray2b(ndimg: np.ndarray) -> Tuple[bytes, int]:
    if len(ndimg.shape) == 3:
        # ndimg = ndimg.transpose(0, 2, 1).copy()
        bimg = ndimg.reshape(-1, order='C').copy().tobytes()
        bc = 0x08 * 3
    else:
        # ndimg = ndimg.T.copy()
        bimg = ndimg.reshape(-1, order='C').copy().tobytes()
        bc = 0x08
    return bimg, bc


def readImg(path: str):
    if path[-3:] == "bmp":
        w, h, bc, ct, bimg = readBmp(path)
        params = {"ft": "bmp", "w": w, "h": h, "bc": bc, "ct": ct}
        isColor = ((bc >> 3) == 3)
        ndimg = b2ndarray(bimg, w, h, isColor)
        if len(ndimg.shape) == 3:
            ndimg = ndimg[::-1, :, [2, 1, 0]]
        else:
            ndimg = ndimg[::-1, :]
        return ndimg, params
    elif path[-3:] == "png":
        w, h, d, cType, interlace, bimg = readPng(path)
        params = {"ft": "png", "w": w, "h": h, "d": d, "cType": cType, "interlace": interlace}
        isColor = (cType == 2)
        ndimg = b2ndarray(bimg, w, h, isColor)
        return ndimg, params
    else:
        print("Unknown FileType Error")


def writeImg(path: str, ndimg: np.ndarray, params=None):
    if path[-3:] == "bmp":
        if params:
            w = params["w"]
            h = params["h"]
            ct = params["ct"]
        else:
            if len(ndimg.shape) == 3:
                w = ndimg.shape[1]
                h = ndimg.shape[0]
            else:
                w = ndimg.shape[1]
                h = ndimg.shape[0]
            ct = []
        if len(ndimg.shape) == 3:
            ndimg = ndimg[::-1, :, [2, 1, 0]]
        else:
            ndimg = ndimg[::-1, :]
        bimg, bc = ndarray2b(ndimg)
        writeBmp(path, w, h, bc, ct, bimg)
    elif path[-3:] == "png":
        if params:
            w = params["w"]
            h = params["h"]
            d = params["d"]
            cType = params["cType"]
            interlace = params["interlace"]
        else:
            if len(ndimg.shape) == 3:
                w = ndimg.shape[1]
                h = ndimg.shape[0]
                d = 8
                cType = 2
            else:
                w = ndimg.shape[1]
                h = ndimg.shape[0]
                d = 8
                cType = 0
            interlace = 0
        bimg, _ = ndarray2b(ndimg)
        writePng(path, w, h, d, cType, interlace, bimg)
    else:
        print("Unknown FileType Error")


def readBmp(path: str):
    with open(path, "rb") as f:
        # BMP file header
        f.read(2)  # bfType
        f.read(4)  # bfSize         = int.from_bytes(f.read(4), byteorder='little')
        f.read(2)  # bfReserved1    = int.from_bytes(f.read(2), byteorder='little')
        f.read(2)  # bfReserved2    = int.from_bytes(f.read(2), byteorder='little')
        bfOffBits = int.from_bytes(f.read(4), byteorder='little')

        # BMP information header
        f.read(4)  # bcSize         = int.from_bytes(f.read(4), byteorder='little')
        bcWidth = int.from_bytes(f.read(4), byteorder='little')
        bcHeight = int.from_bytes(f.read(4), byteorder='little')
        f.read(2)  # bcPlanes       = int.from_bytes(f.read(2), byteorder='little')
        bcBitCount = int.from_bytes(f.read(2), byteorder='little')
        f.read(4)  # biCompression  = int.from_bytes(f.read(4), byteorder='little')
        f.read(4)  # biSizeImage    = int.from_bytes(f.read(4), byteorder='little')
        f.read(4)  # biXPixPerMeter = int.from_bytes(f.read(4), byteorder='little')
        f.read(4)  # biYPixPerMeter = int.from_bytes(f.read(4), byteorder='little')
        biClrUsed = int.from_bytes(f.read(4), byteorder='little')
        f.read(4)  # biCirImportant = int.from_bytes(f.read(4), byteorder='little')

        colorTable = f.read(biClrUsed << 2)
        _ = f.read(bfOffBits - (0x0e + 0x28 + (biClrUsed << 2)))
        pixels = f.read()

        return bcWidth, bcHeight, bcBitCount, colorTable, pixels


def readPng(path: str):
    with open(path, "rb") as f:
        # PNG header
        f.read(8)  # pngSignature = int.from_bytes(f.read(8), byteorder='big')

        # IHDR chunk
        f.read(4)  # chLength     = int.from_bytes(f.read(4), byteorder='big')
        f.read(4)  # chType       = int.from_bytes(f.read(4), byteorder='big')
        width = int.from_bytes(f.read(4), byteorder='big')
        height = int.from_bytes(f.read(4), byteorder='big')
        depth = int.from_bytes(f.read(1), byteorder='big')
        colorType = int.from_bytes(f.read(1), byteorder='big')
        f.read(1)  # compression  = int.from_bytes(f.read(1), byteorder='big')
        f.read(1)  # filter       = int.from_bytes(f.read(1), byteorder='big')
        interlace = int.from_bytes(f.read(1), byteorder='big')
        f.read(4)  # CRC          = int.from_bytes(f.read(4), byteorder='big')

        # Other chunks
        offset = 0
        cmp_data = []
        while True:
            length = int.from_bytes(f.read(4), byteorder='big')
            chunkType = f.read(4).decode()
            if chunkType == "IDAT":
                cmp_data[offset:] = f.read(length)
                f.read(4)  # CRC
                offset += length
            elif chunkType == "IEND":
                break
            else:
                f.read(length)
                f.read(4)  # CRC

        # Decompress data
        decmp_data = zlib.decompress(bytearray(cmp_data))

        # Apply filter
        if colorType == 0:
            bitsPerPixel = depth
        elif colorType == 2:
            bitsPerPixel = depth * 3
        elif colorType == 3:
            bitsPerPixel = depth
        elif colorType == 4:
            bitsPerPixel = depth * 2
        elif colorType == 6:
            bitsPerPixel = depth
        rowLength = int(1 + (bitsPerPixel * width + 7) / 8)
        filtered_data = []
        rowData = []
        prevRowData = [0 for _ in range(rowLength)]
        bytesPerPixel = int((bitsPerPixel + 7) / 8)
        for h in range(height):
            offset = h * rowLength
            rowData[0:] = decmp_data[offset:offset+rowLength]
            filterType = int(rowData[0])

            currentScanData = rowData[1:].copy()
            prevScanData = prevRowData[1:].copy()

            if filterType == 0:
                pass
            elif filterType == 1:
                for i in range(0, len(currentScanData)):
                    if (i - bytesPerPixel) < 0:
                        currentScanData[i] += 0
                    else:
                        currentScanData[i] += currentScanData[i-bytesPerPixel]
                    currentScanData[i] %= 256
            elif filterType == 2:
                for i in range(0, len(currentScanData)):
                    currentScanData[i] += prevScanData[i]
                    currentScanData[i] %= 256
            elif filterType == 3:
                for i in range(0, bytesPerPixel):
                    currentScanData[i] += int(prevScanData[i] / 2)
                    currentScanData[i] %= 256
                for i in range(bytesPerPixel, len(currentScanData)):
                    if (i - bytesPerPixel) < 0:
                        tmp = int(prevScanData[i] / 2)
                    else:
                        tmp = int(
                            (currentScanData[i-bytesPerPixel]+prevScanData[i]) / 2)
                    currentScanData[i] += tmp
                    currentScanData[i] %= 256
            elif filterType == 4:
                for i in range(0, bytesPerPixel):
                    a = 0
                    c = 0
                    for j in range(i, len(currentScanData), bytesPerPixel):
                        b = prevScanData[j]
                        pa = b - c
                        pb = a - c
                        pc = abs(pa + pb)
                        pa = abs(pa)
                        pb = abs(pb)
                        if (pa <= pb) and (pa <= pc):
                            pass
                        elif pb <= pc:
                            a = b
                        else:
                            a = c
                        a += currentScanData[j]
                        a &= 0xff
                        currentScanData[j] = a % 256
                        c = b
            else:
                # Bad Filter Type Error
                pass
            filtered_data[h*len(currentScanData):] = currentScanData.copy()
            prevRowData[0:] = rowData[0:1]
            prevRowData[1:] = currentScanData.copy()

        return width, height, depth, colorType, interlace, bytearray(filtered_data)


def readJpg(path: str):
    pass


def readGif(path: str):
    with open(path, "rb") as f:
        # BMP file header
        f.read(6)  # gifSignature
        f.read(6)  # Version

        f.read(4)  # width = int.from_bytes(f.read(4), byteorder='big')
        f.read(4)  # height = int.from_bytes(f.read(4), byteorder='big')
        f.read(2)  # field = int.from_bytes(f.read(2), byteorder='big')
        # Global Color Table Flag
        # | Color Resolution
        # | |   Sort Flag
        # | |   | Size of Global Color Table
        # 1 010 0 001
        bgColor = int.from_bytes(f.read(2), byteorder='big')
        aspectRatio = int.from_bytes(f.read(2), byteorder='big')

        f.read(6)  # colorTable = int.from_bytes(f.read(6), byteorder='big')
        f.read(6)  # colorTable = int.from_bytes(f.read(6), byteorder='big')
        f.read(6)  # colorTable = int.from_bytes(f.read(6), byteorder='big')
        f.read(6)  # colorTable = int.from_bytes(f.read(6), byteorder='big')

        separator = int.from_bytes(f.read(2), byteorder='big')
        f.read(4)  # lPosition = int.from_bytes(f.read(4), byteorder='big')
        f.read(4)  # tPosition = int.from_bytes(f.read(4), byteorder='big')
        width = int.from_bytes(f.read(4), byteorder='big')
        height = int.from_bytes(f.read(4), byteorder='big')
        f.read(2)  # field = int.from_bytes(f.read(2), byteorder='big')
        # Local Color Table Flag
        # | Interlace Flag
        # | | Sort Flag
        # | | | Reserved
        # | | | |  Size of Local Color Table
        # 0 0 0 00 000

        f.read(2)  # codeSizeLZW = int.from_bytes(f.read(2), byteorder='big')
        size = int.from_bytes(f.read(2), byteorder='big')
        pixels = f.read(size)

        f.read(2)  # terminator = int.from_bytes(f.read(2), byteorder='big')
        f.read(2)  # trailer = int.from_bytes(f.read(2), byteorder='big')

        return pixels


def writeBmp(path: str, width: int, height: int, bitCount: int, colorTables, pixels):
    with open(path, 'wb') as f:
        lenOfColors = len(colorTables)
        numOfColors = lenOfColors >> 2
        if (bitCount >> 3) == 1:
            color = [(i // 4 if (i % 4) != 0 else 0) for i in range(1, 1025)]
        else:
            color = None
        try:
            lenOfColor = len(color)
        except TypeError:
            lenOfColor = 0
        bfOffBits = 0x0e + 0x28 + lenOfColors + lenOfColor
        lenOfPixels = len(pixels)
        fileSize = bfOffBits + lenOfPixels

        # BMP file header
        b = bytearray([0x42, 0x4d])
        b.extend(fileSize.to_bytes(4, 'little'))
        b.extend((0).to_bytes(2, 'little'))
        b.extend((0).to_bytes(2, 'little'))
        b.extend(bfOffBits.to_bytes(4, 'little'))

        # BMP information header
        b.extend((0x28).to_bytes(4, 'little'))
        b.extend(width.to_bytes(4, 'little'))
        b.extend(height.to_bytes(4, 'little'))
        b.extend((1).to_bytes(2, 'little'))
        b.extend((bitCount).to_bytes(2, 'little'))
        b.extend((0).to_bytes(4, 'little'))
        b.extend(lenOfPixels.to_bytes(4, 'little'))
        b.extend((0).to_bytes(4, 'little'))
        b.extend((0).to_bytes(4, 'little'))
        b.extend(numOfColors.to_bytes(4, 'little'))
        b.extend((0).to_bytes(4, 'little'))

        b.extend(colorTables)
        try:
            b.extend(bytearray(color))
        except TypeError:
            pass
        b.extend(pixels)

        f.write(b)


def writePng(
        path: str,
        width: int,
        height: int,
        depth: int,
        colorType: int,
        interlace: int,
        pixels):
    with open(path, 'wb') as f:
        # PNG signature
        b = bytearray([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a])

        # IHDR
        b.extend((13).to_bytes(4, 'big'))
        b.extend(bytearray([ord(x) for x in "IHDR"]))
        # b.extend(bytearray([0x49, 0x48, 0x44, 0x52]))
        b.extend(width.to_bytes(4, 'big'))
        b.extend(height.to_bytes(4, 'big'))
        b.extend(depth.to_bytes(1, 'big'))
        b.extend(colorType.to_bytes(1, 'big'))
        b.extend((0).to_bytes(1, 'big'))
        b.extend((0).to_bytes(1, 'big'))
        b.extend(interlace.to_bytes(1, 'big'))
        tmp = (
            bytearray([ord(x) for x in "IHDR"])
            + width.to_bytes(4, 'big')
            + height.to_bytes(4, 'big')
            + depth.to_bytes(1, 'big')
            + colorType.to_bytes(1, 'big')
            + (0).to_bytes(1, 'big')
            + (0).to_bytes(1, 'big')
            + interlace.to_bytes(1, 'big'))
        crcIHDR = binascii.crc32(tmp, 0)
        b.extend(crcIHDR.to_bytes(4, 'big'))

        # sRGB
        b.extend((1).to_bytes(4, 'big'))
        b.extend(bytearray([ord(x) for x in "sRGB"]))
        # b.extend(bytearray([0x73, 0x52, 0x47, 0x42]))
        b.extend(bytearray([0x00]))
        b.extend(bytearray([0xae, 0xce, 0x1c, 0xe9]))

        # IDAT
        if colorType == 0:
            bitsPerPixel = depth
        elif colorType == 2:
            bitsPerPixel = depth * 3
        elif colorType == 3:
            bitsPerPixel = depth
        elif colorType == 4:
            bitsPerPixel = depth * 2
        elif colorType == 6:
            bitsPerPixel = depth
        rowLength = int((bitsPerPixel * width + 7) / 8)
        data = []
        for h in range(height):
            offset = h * (rowLength)
            # data[offset:] = [0]
            data.append(0)
            data[offset+h+1:] = pixels[offset:offset+rowLength]
        cmp_data = zlib.compress(bytearray(data))

        b.extend(len(cmp_data).to_bytes(4, 'big'))
        b.extend(bytearray([ord(x) for x in "IDAT"]))
        b.extend(cmp_data)
        crcIDAT = binascii.crc32(bytearray([ord(x) for x in "IDAT"])+cmp_data, 0)
        b.extend(crcIDAT.to_bytes(4, 'big'))

        # IEND
        b.extend((0).to_bytes(4, 'big'))
        b.extend(bytearray([ord(x) for x in "IEND"]))
        b.extend(bytearray([0xae, 0x42, 0x60, 0x82]))

        f.write(b)
