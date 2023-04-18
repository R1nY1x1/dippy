import argparse
import sys
import termios
from concurrent import futures
import numpy as np
import dippy as dp


def interactiveLoop(command):
    while(True):
        # =magmax/python-readchar.git/../_posix_read.py=
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        term = termios.tcgetattr(fd)
        try:
            term[3] &= ~(termios.ICANON | termios.ECHO | termios.IGNBRK | termios.BRKINT)
            termios.tcsetattr(fd, termios.TCSAFLUSH, term)
            char = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        # ====================So far====================
        command["cmd"] = char
        if command["cmd"] in ["q"]:
            break
        elif command["cmd"] in ["c"]:
            command["ch"] = (command["ch"] + 1) if command["ch"] < 1 else 0
        if command["ch"] == 0:
            if command["cmd"] in ["j"]:
                command["curY"] = command["curY"] + 1 if command["curY"] < (command["scale"]//2-1) else command["curY"]
            elif command["cmd"] in ["k"]:
                command["curY"] = command["curY"] - 1 if command["curY"] > 0 else command["curY"]
            elif command["cmd"] in ["h"]:
                command["curX"] = command["curX"] - 1 if command["curX"] > 0 else command["curX"]
            elif command["cmd"] in ["l"]:
                command["curX"] = command["curX"] + 1 if command["curX"] < (command["scale"]//2-1) else command["curX"]


def printLoop(command, ndimg):
    rate = 1 / command["scale"]
    w = int(4/rate)
    while True:
        dp.printImgXY(ndimg, int(w/2)+2, 1, rate=rate)
        dp.printImgXY(np.ones((4, 4)), int(w/2)+command["curX"]*2+2, command["curY"]+2, fc=1)
        dp.printImgXY(ndimg[w*command["curY"]:w*(command["curY"]+1), w*command["curX"]:w*(command["curX"]+1)], 1, 1)
        if command["cmd"] in ["q"]:
            break


def flameOfScale16(args):
    print("\033[2J")
    print("\033[1m\033[35m")
    print("\033[1;0H+--------------------------------+----------------+----------------+")
    print("\033[2;0H|                                |                |                |")
    print("\033[3;0H|                                |                |                |")
    print("\033[4;0H|                                |                |                |")
    print("\033[5;0H|                                |                |                |")
    print("\033[6;0H|                                |                |                |")
    print("\033[7;0H|                                |                |                |")
    print("\033[8;0H|                                |                |                |")
    print("\033[9;0H|                                |                |                |")
    print("\033[10;0H|                                +----------------+----------------+")
    print("\033[11;0H|                                |                |                |")
    print("\033[12;0H|                                |                |                |")
    print("\033[13;0H|                                |                |                |")
    print("\033[14;0H|                                |                |                |")
    print("\033[15;0H|                                |                |                |")
    print("\033[16;0H|                                |                |                |")
    print("\033[17;0H|                                |                |                |")
    print("\033[18;0H+--------------------------------+----------------+----------------+")
    print("\033[0m")
    print(f"\033[11;35H\033[{'1m [+]' if args.kmeans else '0m [-]'} Kmeans\033[0m")
    print(f"\033[12;35H\033[{'1m [+]' if args.dithering else '0m [-]'} Dithering\033[0m")
    print(f"\033[13;35H\033[{'1m [+]' if args.binarize else '0m [-]'} Binarize\033[0m")
    print(f"\033[14;35H\033[{'1m [+]' if args.inverseNP else '0m [-]'} InverseNP\033[0m")


def flameOfScale32(args):
    print("\033[2J")
    print("\033[1m\033[35m")
    print("\033[1;0H+----------------------------------------------------------------+--------------------------------+--------------------------------+")
    print("\033[2;0H|                                                                |                                |                                |")
    print("\033[3;0H|                                                                |                                |                                |")
    print("\033[4;0H|                                                                |                                |                                |")
    print("\033[5;0H|                                                                |                                |                                |")
    print("\033[6;0H|                                                                |                                |                                |")
    print("\033[7;0H|                                                                |                                |                                |")
    print("\033[8;0H|                                                                |                                |                                |")
    print("\033[9;0H|                                                                |                                |                                |")
    print("\033[10;0H|                                                                |                                |                                |")
    print("\033[11;0H|                                                                |                                |                                |")
    print("\033[12;0H|                                                                |                                |                                |")
    print("\033[13;0H|                                                                |                                |                                |")
    print("\033[14;0H|                                                                |                                |                                |")
    print("\033[15;0H|                                                                |                                |                                |")
    print("\033[16;0H|                                                                |                                |                                |")
    print("\033[17;0H|                                                                |                                |                                |")
    print("\033[18;0H|                                                                +--------------------------------+--------------------------------+")
    print("\033[19;0H|                                                                |                                |                                |")
    print("\033[20;0H|                                                                |                                |                                |")
    print("\033[21;0H|                                                                |                                |                                |")
    print("\033[22;0H|                                                                |                                |                                |")
    print("\033[23;0H|                                                                |                                |                                |")
    print("\033[24;0H|                                                                |                                |                                |")
    print("\033[25;0H|                                                                |                                |                                |")
    print("\033[26;0H|                                                                |                                |                                |")
    print("\033[27;0H|                                                                |                                |                                |")
    print("\033[28;0H|                                                                |                                |                                |")
    print("\033[29;0H|                                                                |                                |                                |")
    print("\033[30;0H|                                                                |                                |                                |")
    print("\033[31;0H|                                                                |                                |                                |")
    print("\033[32;0H|                                                                |                                |                                |")
    print("\033[33;0H|                                                                |                                |                                |")
    print("\033[34;0H+----------------------------------------------------------------+--------------------------------+--------------------------------+")
    print("\033[0m")
    print(f"\033[19;67H\033[{'1m [+]' if args.kmeans else '0m [-]'} Kmeans\033[0m")
    print(f"\033[20;67H\033[{'1m [+]' if args.dithering else '0m [-]'} Dithering\033[0m")
    print(f"\033[21;67H\033[{'1m [+]' if args.binarize else '0m [-]'} Binarize\033[0m")
    print(f"\033[22;67H\033[{'1m [+]' if args.inverseNP else '0m [-]'} InverseNP\033[0m")


def main(args):
    path = args.file
    print(f"ImagePath >> {path}")
    if path[-3:] in ["bmp", "png"]:
        ndimg, parmas = dp.readImg(path)
    elif path[-3:] in ["npy", "npz"]:
        tmp = np.load(path)
        if path[-3:] == "npz":
            print("<Select Key>")
            for f in tmp.files:
                print(" ", f, ":", tmp[f].dtype, tmp[f].shape)
            key = input(f"  {tmp.files} >> ")
            print("")
            tmp = tmp[key]
        print("<Select Num>")
        print(" ", tmp.dtype, tmp.shape)
        numStr = input(f"  [0-{tmp.shape[0]-1}] >> ")
        print("")
        num = int(numStr)
        ndimg = tmp[num]
    else:
        print("File Type Error")
        raise Exception

    command = {"cmd": "", "curX": 0, "curY": 0, "ch": 0, "scale": args.scale}
    if command["scale"] == 16:
        flameOfScale16(args)
    elif command["scale"] == 32:
        flameOfScale32(args)

    if len(ndimg.shape) == 3:
        ndimg = dp.convertColor(ndimg)
    mag = dp.fft(dp.resize(ndimg, (command["scale"]*2, command["scale"]*2)))[0]
    mag = dp.binarize(mag, method="otsu")
    # mag = dp.resize(mag, (command["scale"]*2, command["scale"]*2))
    dp.printImgXY(mag, (51 if command["scale"] == 16 else 99), 1)
    hist = np.histogram(ndimg, bins=(command["scale"]*2), range=(0, 256))[0]
    hist = hist / max(hist) * ((7 if command["scale"] == 16 else 15)*4)
    histimg = np.zeros(((7 if command["scale"] == 16 else 15)*4, command["scale"]*2))
    for i in range(len(hist)):
        histimg[:int(hist[i]), i] = 1
    dp.printImgXY(histimg[::-1, :], (51 if command["scale"] == 16 else 99), (11 if command["scale"] == 16 else 19))

    if args.fitting:
        ndimg = dp.resize(ndimg, (int(512*((command["scale"]/16)**2)), int(512*((command["scale"]/16)**2))))
    if len(ndimg.shape) == 3:
        ndimg = dp.convertColor(ndimg)
    if args.kmeans:
        ndimg = dp.kmeans(ndimg, N=args.kmeans)
    if args.dithering:
        ndimg = dp.dithering(ndimg, method="atkinson")
    if args.binarize:
        if args.binarize == "otsu":
            ndimg = dp.binarize(ndimg, method="otsu")
        else:
            ndimg = dp.binarize(ndimg, threshold=int(args.binarize))
    if args.inverseNP:
        ndimg = dp.binarize(ndimg, threshold=1)
        ndimg = dp.inverseNP(ndimg)

    future_list = []
    with futures.ThreadPoolExecutor(max_workers=3) as executor:
        future_list.append(executor.submit(printLoop, command=command, ndimg=ndimg))
        future_list.append(executor.submit(interactiveLoop, command=command))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="")
    parser.add_argument("file", help="load file path")
    parser.add_argument("-S", "--scale", type=int, default=16, choices=[16, 32], help="Image Scale")
    parser.add_argument("-F", "--fitting", action="store_true", help="able resize")
    parser.add_argument("-K", "--kmeans", type=int, help="able kmeans & N(1~255)")
    parser.add_argument("-D", "--dithering", action="store_false", help="DISable dithering")
    parser.add_argument("-B", "--binarize", help="able binarize & Threshold(0~255 or \"otsu\")")
    parser.add_argument("-I", "--inverseNP", action="store_true", help="able inverseNP")
    args = parser.parse_args()
    main(args)
