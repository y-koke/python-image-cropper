"""
Press the left mouse button on the top left pixel of the range you want to crop.
While holding the button, Move the pointer to the lower right pixel of the range you want to cropped.
Release the mouse button.
Then press the keyboard to select the process.
[F] key : Go to the next image without saving.
[S] key : Go to the next image with saving.
[B] key : Back to one previous image.
[Q] key : Exit.

"""

import os
import sys
import glob
import argparse
import pathlib

import cv2
import numpy as np


class Points():

    def __init__(self):
        self.min_x = 0
        self.min_y = 0
        self.max_x = 0
        self.max_y = 0

    def set_min(self, x, y):
        self.min_x = x
        self.min_y = y

    def set_max(self, x, y):
        self.max_x = x
        self.max_y = y

    def get_min(self):
        return self.min_x, self.min_y

    def get_max(self):
        return self.max_x, self.max_y


def mouse_event(event, x, y, flags, params):

    name, img, points = params

    if event == cv2.EVENT_LBUTTONDOWN:
        points.set_min(x,y)
        h, w = img.shape[0], img.shape[1]
        cv2.line(img, (x, 0), (x, h - 1), (0, 255, 0), 2)
        cv2.line(img, (0, y), (w - 1, y), (0, 255, 0), 2)
        cv2.imshow(name, img)

    if event == cv2.EVENT_LBUTTONUP:
        points.set_max(x,y)
        h, w = img.shape[0], img.shape[1]
        cv2.line(img, (x, 0), (x, h - 1), (0, 255, 0), 2)
        cv2.line(img, (0, y), (w - 1, y), (0, 255, 0), 2)
        cv2.imshow(name, img)

    if event == cv2.EVENT_MOUSEMOVE:
        img_cp2 = np.copy(img)
        h, w = img_cp2.shape[0], img_cp2.shape[1]
        cv2.line(img_cp2, (x, 0), (x, h - 1), (255, 0, 0), 2)
        cv2.line(img_cp2, (0, y), (w - 1, y), (255, 0, 0), 2)
        cv2.imshow(name, img_cp2)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('data_dir', help = 'The directory which the images to be croped contained.', type = str)
    parser.add_argument('save_dir', help = 'The directory which the croped images will be saved.', type = str)
    parser.add_argument('--skip', help = 'Number of skipped images.', type = int, default = 0)
    parser.add_argument('--start', help = 'The filename of image which starts processing.', type = str)
    parser.add_argument('--window_w', help = 'Width of window', default = 1000, type = int)
    parser.add_argument('--window_h', help = 'Height of window', default = 1000, type = int)
    args = parser.parse_args()

    filenames = glob.glob( os.path.join(args.data_dir, '*') )

    points = Points()

    i = 0
    num_files = len(filenames)
    if args.skip > 0 & args.skip < num_files:
        i = args.skip

    if args.start:
        j = 0
        for filename in filenames:
            name = os.path.basename(filename)
            if name == args.start:
                i = j
                break
            j += 1

    while (True):
        if i<0:
            i = 0
        for filename in filenames[i:]:
            name = os.path.basename(filename)
            img = cv2.imread(filename)
            img_cp = np.copy(img)

            min_x, min_y = points.get_min()
            max_x, max_y = points.get_max()
            h, w = img.shape[0], img.shape[1]

            cv2.namedWindow(name, cv2.WINDOW_KEEPRATIO | cv2.WINDOW_NORMAL)
            cv2.setMouseCallback(name, mouse_event, [name, img_cp, points])
            back_flag = False

            cv2.imshow(name, img)
            cv2.moveWindow(name, 0, 0)
            cv2.resizeWindow(name, args.window_w, args.window_h)

            while (True):
                key = cv2.waitKey(1)&0xFF
                if key == ord('f'):
                    if i >= len(filenames) - 1:
                        i -= 1
                    break

                if key == ord('b'):
                    back_flag = True
                    i -= 1
                    break

                if key == ord('s'):
                    min_x, min_y = points.get_min()
                    max_x, max_y = points.get_max()
                    cv2.imwrite( os.path.join(args.save_dir, name) , img[min_y:max_y, min_x:max_x] )
                    if i >= len(filenames) - 1:
                        i -= 1
                    break

                if key == ord('q'):
                    print('Escape while opening this image : ' + str(name))
                    print('Order of this image : ' + str(i))
                    cv2.destroyAllWindows()
                    sys.exit()

            cv2.destroyAllWindows()
            if back_flag == True:
                break
            i += 1


if __name__ == '__main__':
    main()
