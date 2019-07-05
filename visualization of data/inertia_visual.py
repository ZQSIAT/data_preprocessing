# =================
# Author: qs.zhao
# Date: 2019-7-2
# Function: this code is for visualization of IMU data including acceleration, gyro, quaternion, velocity, position.
# =================

import random
import time
from PIL import Image, ImageOps
import numpy as np
import numbers
import math
import os
import matplotlib.pyplot as plt
import logging

logging.basicConfig(level=logging.DEBUG,
                    filename='./log/{:s}_inertial_visual.log'.format(time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime())),
                    datefmt='%Y/%m/%d %H:%M:%S',
                    format='%(asctime)s - %(name)s - %(levelname)s - %(lineno)d - %(module)s - %(message)s')
logger = logging.getLogger(__name__)


class InertiaVisual(object):
    def __init__(self):

        pass

    @staticmethod
    def read_txt(path):
        file_content = []
        with open(path) as lf:
            for i, line in enumerate(lf.readlines()):
                txt_line = line.strip("\n ").split(" ")
                # raise RuntimeError
                if len(txt_line) == 338:#
                    file_content.append(txt_line)
                    pass
                else:
                    print("Frame {:d} of this file [{:s}] failed!!!".format(i + 1, path))
                    continue
                    pass
                pass
            pass
        return file_content
        pass

    @staticmethod
    def generate_inertial_date(self, data_type):
        """
        This is the script to generate the acceleration, gyro, quaternion, velocity and position data in the form of F x (17*N)
        :param data_type:string, select a type of data which you need to generate.
        Incleding: "acceleration","gyro","quaternion","velocity", "position".
        :return:target_data:ndarray. return a ndarray data in the form of F x (17*N), N named 3 or 4, Frame means frames of this file.
        """
        target_data = []
        # --todo--
        return target_data
        pass

    pass


if __name__ == "__main__":
    print("Start processing...")
    start_time = time.time()
    print("#" * 120)
    my_task = InertiaVisual()
    temp_path = "D:/pycharm_project/temp/inertial.txt"

    content = my_task.read_txt(temp_path)

    img_array = np.concatenate([np.expand_dims(x, 0) for x in content], axis=0)

    # content = np.array(content)
    # print(content.reshape(432, 338))
    # print(content.size)
    print(img_array)
    print(img_array.shape)
    # print(np.array(label_content)[:, 3], '\n', len(label_content))
    # np.savetxt('test.txt', np.array(label_content), delimiter=',', fmt='%s')
    # label_list = my_task.generate_list()
    # print(label_list[1])

    # processing by pool map
    # p = Pool(8)

    end_time = time.time()
    print("#" * 120)
    print("Finished! Time elapse: {:.2f} minutes.".format((end_time - start_time) / 60.0))
    pass
