import re
import math
import argparse
import time
import shutil
import numpy as np
import dippy as dp


def selectKey(npz):
    print("<Select Key>")
    for f in npz.files:
        print(" ", f, ":", npz[f].dtype, npz[f].shape)
    key = input(f"  {npz.files} >> ")
    print("")
    return key


def selectNum(npy, numStr):
    if numStr is None:
        print("<Select Num>")
        print(" ", npy.dtype, npy.shape)
        numStr = input(f"  [0-{npy.shape[0]-1}] >> ")
        print("")
    try:
        nums = [int(numStr), ]
    except ValueError:
        nums = re.findall(r"[0-9]+", numStr)
        nums = range(int(nums[0]), int(nums[1]) + 1)
    return nums


def displayImg(ndimg, doKmeans, doDithering, doBinarize, doInverseNP, asAA):
    if len(ndimg.shape) == 3:
        ndimg = dp.convertColor(ndimg)
    if doKmeans:
        ndimg = dp.kmeans(ndimg, N=doKmeans)
    if doDithering:
        ndimg = dp.dithering(ndimg, method="atkinson")
    if doBinarize:
        ndimg = dp.binarize(ndimg, threshold=doBinarize)
    if doInverseNP:
        ndimg = dp.binarize(ndimg, threshold=1)
        ndimg = dp.inverseNP(ndimg)
    terminal_size = shutil.get_terminal_size()
    if asAA:
        if terminal_size.columns < ndimg.shape[0]:
            rate = ((terminal_size.columns) / (ndimg.shape[0]))
        else:
            rate = 1
        dp.printImgAA(ndimg, rate)
    else:
        if terminal_size.columns < ndimg.shape[0]//2:
            rate = ((terminal_size.columns) / (ndimg.shape[0]//2))
        else:
            rate = 1
        dp.printImg(ndimg, rate)


def main(args):
    path = args.file
    if path[-3:] in ["bmp", "png"]:
        ndimg, parmas = dp.readImg(path)
    elif path[-3:] == "npy":
        tmp = np.load(path)
        tmp = np.squeeze(tmp)
        nums = selectNum(tmp, args.num)
    elif path[-3:] == "npz":
        tmp = np.load(path)
        if args.key is None:
            key = selectKey(tmp)
        else:
            key = args.key
        nums = selectNum(tmp[key], args.num)
    else:
        print("File Type Error")
        raise Exception
    try:
        while True:
            for num in nums:
                if path[-3:] == "npy":
                    ndimg = tmp[num]
                elif path[-3:] == "npz":
                    ndimg = tmp[key][num]
                print(f"[{num:>3}]")
                displayImg(
                    ndimg,
                    doKmeans=args.kmeans,
                    doDithering=args.dithering,
                    doBinarize=args.binarize,
                    doInverseNP=args.inverseNP,
                    asAA=args.AA
                )
                if args.gif:
                    if args.AA:
                        print(f"\033[{math.ceil(ndimg.shape[0]/2)+2}F")
                    else:
                        print(f"\033[{math.ceil(ndimg.shape[0]/4)+2}F")
                    time.sleep(0.5)
                if args.save:
                    dp.writeImg(args.save+f"{num}.png", ndimg)
            if args.gif is False:
                break
    except UnboundLocalError:
        displayImg(
            ndimg,
            doKmeans=args.kmeans,
            doDithering=args.dithering,
            doBinarize=args.binarize,
            doInverseNP=args.inverseNP,
            asAA=args.AA
        )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="")
    parser.add_argument("file", help="load file path")
    parser.add_argument("-k", "--key", help="select npz key")
    parser.add_argument("-n", "--num", help="select image num")
    parser.add_argument("-s", "--save", help="save folder path")
    parser.add_argument("-K", "--kmeans", type=int, help="able kmeans & N(1~255)")
    parser.add_argument("-D", "--dithering", action="store_true", help="able dithering")
    parser.add_argument("-B", "--binarize", type=int, help="able binarize & Threshold(0~255)")
    parser.add_argument("-I", "--inverseNP", action="store_true", help="able inverseNP")
    parser.add_argument("--AA", action="store_true", help="print as AA [default is braile]")
    parser.add_argument("--gif", action="store_true", help="print like Gif")
    args = parser.parse_args()
    main(args)
