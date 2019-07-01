import os
import numpy as np
import time
from multiprocessing import Pool
import logging
import shutil as st
import cv2

logging.basicConfig(level=logging.DEBUG,
                    filename='{:s}_add_total_frames_to_label_file_title.log'.format(time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime())),
                    datefmt='%Y/%m/%d %H:%M:%S',
                    format='%(asctime)s - %(name)s - %(levelname)s - %(lineno)d - %(module)s - %(message)s')
logger = logging.getLogger(__name__)

class AddTotalFrame(object):
    def __init__(self):
        self.label_path = "/ssd_data/zqs/workspace/new_label/92_276/"
        self.files_path_1 = "/home/zqs/shenzj/data/Preprocessing_Test/DataSet2/RGB_HIKVISION/"
        self.dst_path = "/ssd_data/zqs/workspace/new_label/92_276_frames/"
        pass
    def filter_sequence(self, end_or_start = True, key_words = None, src_list = None):
        if end_or_start:
            temp = list(filter(lambda x: x.startswith(key_words), src_list))
            pass
        else:
            temp = list(filter(lambda x: x.endswith(key_words), src_list))
            pass
        temp.sort()
        return temp
        pass

    def add_total_frame(self):
        label_list = self.generate_list(self.label_path)
        # file_list = self.generate_list(self.files_path_1 + self.menus_path[1])
        # filter_list = self.filter_sequence(False, 'S008.txt', file_list[1])
        for i, ICount in enumerate(label_list[1]):
            for j in range(1, 16):
                file_name = ICount.replace('P', 'O002P').replace('T', 'C{:03d}T'.format(j)).replace('txt', 'mp4')
                # print(file_name)
                # raise RuntimeError
                src_path = self.files_path_1 + file_name
                total_frames = int(cv2.VideoCapture(src_path).get(7))
                src_name = self.label_path + ICount
                dst_name = self.dst_path + ICount.replace('.txt', 'F{:06d}.txt'.format(total_frames))
                if os.path.exists(src_path) and cv2.VideoCapture(src_path).isOpened() and not os.path.exists(dst_name):
                    os.rename(src_name, dst_name)
                    print("\"{:s}\" has rename!".format(ICount))
                    logger.info("\"{:s}\" has rename!".format(ICount))
                    break
                    pass
                else:
                    continue
                    pass
                pass
            print("\"{:s}\" has done!".format(ICount))
            # raise RuntimeError
            pass
        # print(file_list[1])
        # raise RuntimeError
        pass

    def generate_list(self, path):
        original_path = path
        path_list = []
        file_list = os.listdir(original_path)
        for i, ICount in enumerate(file_list):
            path_list.append(original_path + ICount)
            pass
        path_list.sort()
        file_list.sort()
        return path_list, file_list
        pass
    pass


if __name__ == "__main__":
    print("Start processing...")
    start_time = time.time()
    print("#" * 120)
    workspace_path = "/ssd_data/zqs/workspace/my-dataset-processing/"
    good_video_path = "/ssd_data/zqs/good/g1.mp4"
    broken_video_path = "/ssd_data/zqs/broken/b1.mp4"

    my_task = AddTotalFrame()
    my_task.add_total_frame()
    # file_list = my_task.generate_list("/ssd_data/zqs/workspace/new_label/92_276/")
    # print(file_list[1])
    # image = cv2.VideoCapture(good_video_path)
    # if cv2.VideoCapture(good_video_path).isOpened():
    #     print("good")
    #     print(cv2.VideoCapture(good_video_path).get(7))
    #     pass

    # print(image.get(7))
    # my_pool = Pool(4)
    # my_task = my_pool.map(my_split_emotion.split_emotion_data, file_list[0])

    end_time = time.time()
    print("#" * 120)
    print("Finished! Time elapse: {:.2f} minutes.".format((end_time - start_time) / 60.0))

    pass

