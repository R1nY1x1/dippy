import re
import argparse
import shutil
import numpy as np
import dippy as dp


def selectKey(npz):
    print("<Select Key>")
    for f in npz.files:
        print(f, ":", npz[f].dtype, npz[f].shape)
    key = input(f"{npz.files} >> ")
    print("")
    return key


def selectNum(npy, numStr):
    if numStr is None:
        print("<Select Num>")
        print(npy.dtype, npy.shape)
        numStr = input(f"0-{npy.shape[0]-1} >> ")
        print("")
    try:
        nums = [int(numStr), ]
    except ValueError:
        nums = re.findall(r"[0-9]+", numStr)
        nums = range(int(nums[0]), int(nums[1]) + 1)
    return nums


def displayImg(ndimg, doKmeans, doDithering, doInverseNP):
    if len(ndimg.shape) == 3:
        ndimg = dp.convertColor(ndimg)
    if doKmeans:
        ndimg = dp.kmeans(ndimg, N=16)
    if doDithering:
        ndimg = dp.dithering(ndimg, method="atkinson")
    if doInverseNP:
        ndimg = dp.binarize(ndimg, threshold=1)
        ndimg = dp.inverseNP(ndimg)
    terminal_size = shutil.get_terminal_size()
    if terminal_size.columns < ndimg.shape[0]//2:
        rate = ((terminal_size.columns) / (ndimg.shape[0]//2))
    else:
        rate = 1
    dp.printImg(ndimg, rate)


def main(args):
    path = args.file
    if path[-3:] in ["bmp", "png"]:
        ndimg, parmas = dp.readImg(path)
        displayImg(ndimg, args.kmeans, args.dithering, args.inverseNP)
    elif path[-3:] == "npy":
        tmp = np.load(path)
        nums = selectNum(tmp, args.num)
        for num in nums:
            ndimg = tmp[num]
            print(f"[{num}]")
            displayImg(ndimg, args.kmeans, args.dithering)
    elif path[-3:] == "npz":
        tmp = np.load(path)
        if args.key is None:
            key = selectKey(tmp)
        else:
            key = args.key
        nums = selectNum(tmp[key], args.num)
        for num in nums:
            ndimg = tmp[key][num]
            print(f"[{num}]")
            displayImg(ndimg, args.kmeans, args.dithering, args.inverseNP)
    else:
        print("File Type Error")
    if args.save:
        dp.writeImg(args.save, ndimg)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="")
    parser.add_argument("file", help="load file path")
    parser.add_argument("-k", "--key", help="select npz key")
    parser.add_argument("-n", "--num", type=int, help="select image num")
    parser.add_argument("-s", "--save", help="save file path")
    parser.add_argument("-K", "--kmeans", action="store_true", help="able kmeans")
    parser.add_argument("-D", "--dithering", action="store_true", help="able dithering")
    parser.add_argument("-I", "--inverseNP", action="store_true", help="able inverseNP")
    args = parser.parse_args()
    main(args)
