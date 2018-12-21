#!/usr/bin/env python
import os
import sys
from PIL import Image
import json

def frames_from_data(filename, ext):
    data_filename = filename + ext
    if ext == '.json':
        json_data = open(data_filename)
        data = json.load(json_data)
        frames = {}
        for f in data['frames']:
            x = int(float(data['frames'][f]["x"]))
            y = int(float(data['frames'][f]["y"]))
            w = int(float(data['frames'][f]["w"]))
            h = int(float(data['frames'][f]["h"]))
            real_w = int(float(data['frames'][f]["sourceW"]))
            real_h = int(float(data['frames'][f]["sourceH"]))
            d = {
                'box': (
                    x,
                    y,
                    x + w,
                    y + h
                ),
                'real_sizelist': [
                    real_w,
                    real_h
                ],
                'result_box': (
                    int((real_w - w) / 2),
                    int((real_h - h) / 2),
                    int((real_w + w) / 2),
                    int((real_h + h) / 2)
                ),
                'rotated': False
            }
            frames[f] = d
        json_data.close()
        return frames.items()
    else:
        print("Wrong data format on parsing: '" + ext + "'!")
        exit(1)


def gen_png_from_data(filename, ext):
    big_image = Image.open(filename + ".png")
    frames = frames_from_data(filename, ext)
    for k, v in frames:
        frame = v
        box = frame['box']
        rect_on_big = big_image.crop(box)
        real_sizelist = frame['real_sizelist']
        result_image = Image.new('RGBA', real_sizelist, (0, 0, 0, 0))
        result_box = frame['result_box']
        result_image.paste(rect_on_big, result_box, mask=0)
        if frame['rotated']:
            result_image = result_image.transpose(Image.ROTATE_90)
        if not os.path.isdir(filename):
            os.mkdir(filename)
        outfile = (filename + '/' + k)
        if not outfile.endswith('.png'):
            outfile += '.png'
        print(outfile, "generated")
        result_image.save(outfile)


def get_sources_file(filename):
    data_filename = filename + ext
    png_filename = filename + '.png'
    if os.path.exists(data_filename) and os.path.exists(png_filename):
        gen_png_from_data(filename, ext)
    else:
        print("Make sure you have both " + data_filename + " and " + png_filename + " files in the same directory")


# Use like this: python unpacker.py [Image Path or Image Name(but no suffix)] [Type:plist or json]
if __name__ == '__main__':
    if len(sys.argv) <= 1:
        print("You must pass filename as the first parameter!")
        exit(1)
    # filename = sys.argv[1]
    path_or_name = sys.argv[1]
    ext = '.json'
    get_sources_file(path_or_name)
