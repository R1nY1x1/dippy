import re
import argparse
import numpy as np
import dippy as dp

def selectKey(npz):
    print("<Select Key>")
    for f in npz.files:
        print(f, ":", npz[f].dtype, npz[f].shape)
    key = input(f"{npz.files} >> ")
    return key


def selectNum(npy, numStr):
    if numStr == None:
        print("<Select Num>")
        print(npy.dtype, npy.shape)
        numStr = input(f"0-{npy.shape[0]-1} >> ")
    try:
        nums = [int(numStr),]
    except ValueError:
        nums = re.findall(r"[0-9]+", numStr)
        nums = range(int(nums[0]), int(nums[1])+1)
    return nums


def displayImg(ndimg, doKmeans, doDithering):
    if doKmeans:
        ndimg = dp.kmeans(ndimg, 255)
    if doDithering:
        ndimg = dp.dithering(ndimg, method="atkinson")
    dp.printImg(ndimg, 1)


def main(args):
    path = args.file
    if path[-3:] == "png":
        w, h, d, cType, interlace, bimg = dp.readImg(path)
        isColor = False
        ndimg = dp.b2ndarray(bimg, w, h, isColor)
        ndimg = ndimg[::-1, :]
        ndimg = ndimg.T.copy()
        displayImg(ndimg, args.kmeans, args.dithering)
    elif path[-3:] == "npy":
        tmp = np.load(path)
        nums = selectNum(tmp, args.num)
        for num in nums:
            ndimg = tmp[num]
            print(f"[{num}]")
            displayImg(ndimg, args.kmeans, args.dithering)
    elif path[-3:] == "npz":
        tmp = np.load(path)
        if args.key == None:
            key = selectKey(tmp)
        else:
            key = args.key
        nums = selectNum(tmp[key], args.num)
        for num in nums:
            ndimg = tmp[key][num]
            print(f"[{num}]")
            displayImg(ndimg, args.kmeans, args.dithering)
    else:
        print("File Type Error")
        raise FileNotFoundError


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="")
    parser.add_argument("file", help="load file")
    parser.add_argument("-k", "--key", help="select npz key")
    parser.add_argument("-n", "--num", type=int, help="select image num")
    parser.add_argument("-K", "--kmeans", action="store_false", help="DISable kmeans")
    parser.add_argument("-D", "--dithering", action="store_true", help="able dithering")
    args = parser.parse_args()
    main(args)
