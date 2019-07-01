"""
time: 2019-04-26
author: zqs
introduction: for hikvision mp4 clean, first, find broken files, second, delete them.
"""
import logging
import subprocess
import os
import shutil as st
import time
from multiprocessing import Pool
import random

logging.basicConfig(level=logging.DEBUG,
                    filename='{:s}_some_error_file.log'.format(time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime())),
                    datefmt='%Y/%m/%d %H:%M:%S',
                    format='%(asctime)s - %(name)s - %(levelname)s - %(lineno)d - %(module)s - %(message)s')
logger = logging.getLogger(__name__)
class HikvisionClean():
    def find_ffmpeg_hikvision_mp4_broken(a):

        broken_mp4_subject = open('test {:s}_broken_mp4_subject.txt'.format(time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime())), 'w')

        for i, ICount in enumerate(a):
            camera_list = os.listdir(ICount)
            # print(camera_list)
            for j, JCount in enumerate(camera_list):
                video_path = ICount + JCount
                # print(video_path)
                cmd_ffmpeg_check_file = "ffmpeg -v error -i {:s} -f null -".format(video_path)
                # os.system(cmd_ffmpeg_check_file)
                if os.system(cmd_ffmpeg_check_file) == 0:
                    print("{:s} is good!".format(video_path))
                    pass
                else:
                    print("~~~ {:s} was broken ~~~".format(video_path))
                    broken_mp4_subject.write(str(video_path) + " was broken ~~~~~!!!\n")
                    pass
                # raise RuntimeError
                pass
            pass
        broken_mp4_subject.close()
        pass

    pass

if __name__ == "__main__":
    print("Start processing...")
    start_time = time.time()
    print("#" * 120)
    temp_path = "F:/pycharm_preject/temp/"

    my_hikvision = HikvisionClean()
    # my_rename_hikvision.save_names()
    file_list = my_rename_hikvision.generate_list()
    # processing by pool map
    my_pool = Pool(4)
    my_task = my_pool.map(my_rename_hikvision.rename_hikvision, file_list[0])

    end_time = time.time()
    print("#" * 120)
    print("Finished! Time elapse: {:.2f} minutes.".format((end_time - start_time) / 60.0))
    pass
