# This code is designed for find bad ntu rgb+d skeleton files, and record somethings about it.

import shutil as st
import os
import time
import scipy.io as scio
from multiprocessing import Pool
import numpy as np

def mat_load(path):
    data = scio.loadmat(path)
    return data
    pass

def clear_ntu_rgbd_zero_rows_samples(a):

    data = mat_load(a)
    skeleton_data_kb = data["kb"]

    if np.sum(np.all(skeleton_data_kb, axis=1) == 0) >= 3:
        print(a.split('/')[-1])
        # broken_skeleton_file.write(str(a.split('/')[-1]) + "\n")
        pass
    elif "kb2" in data.keys():
        skeleton_data_kb2 = data["kb2"]
        if np.sum(np.all(skeleton_data_kb2, axis=1) == 0) >= 3:
            # broken_skeleton_file.write(str(a.split('/')[-1]) + "\n")
            print(a.split('/')[-1])
            pass
        pass
    else:
        # print("{:s} good!".format(a.split('/')[-1]))
        pass
    pass

def find_ntu_skeleton_bad_data_and_delete_it():
    skeleton_dir = 'F:/ntu_rgbd_skeleton_process/ntu_rgbd_skeletons'
    txt_file = 'F:/ntu_rgbd_skeleton_process/bad_data_list.txt'
    with open(txt_file) as lf:
        for line in lf.readlines():
            label_line = line.strip('\n')
            delete_path = skeleton_dir + label_line + '.skeleton'
            if (os.path.exists(delete_path)):
                os.remove(delete_path)
                print("{:s} has deleted!!!".format(label_line))
                pass
            else:
                print("A enenenneenen~~~ {:s} does not existed!!!!!!!!!".format(label_line))
                pass
            pass
        lf.close()
        pass
    pass
# get file list
def get_file_list(a = ""):
    return_list = []
    file_list = os.listdir(a)
    file_list.sort()
    for i,ICount in enumerate(file_list):
        return_list.append(a + ICount)
        pass
    return return_list
    pass

if __name__ == "__main__":

    find_ntu_skeleton_bad_data_and_delete_it()

    # source = "F:/ntu_rgbd_skeleton_process/mat_ntu_skeleton/"
    # one_samples = "S013C003P028R001A051.mat"
    # data = mat_load(source + one_samples)
    # skeleton_data_kb = data["kb"]
    # if np.sum(np.all(skeleton_data_kb,axis=1) == 0) >= 3:
    #     print("broken")
    #     pass
    # else:
    #     print("good!")
    #     pass
    # if "kb2" in data.keys():
    #     skeleton_data_kb2 = data["kb2"]
    #     if np.sum(np.all(skeleton_data_kb2, axis=1) == 0) >= 3:
    #         print("broken")
    #         pass
    #     else:
    #         print("good!")
    #         pass
    #     pass
    # raise RuntimeError
    # print(data["kb"])
    # print(type(data["kb"]))
    # print(data["kb"].shape)
    # files_list = get_file_list(source)
    # print("Start processing...")
    # start_time = time.time()
    # print("#" * 120)

    # global broken_skeleton_file
    # broken_skeleton_file = open('{:s}_broken_skeleton_list.txt'.format(time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime())), 'w')

    # processing by pool map
    # p = Pool(8)
    # res1 = p.map(clear_ntu_rgbd_zero_rows_samples, files_list)

    # broken_skeleton_file.close()
    # end_time = time.time()
    # print("#" * 120)
    # print("Finished! Time elapse: {:.2f} minutes.".format((end_time - start_time) / 60.0))
    # retE = [i for i in s1 if i in s2]
    # print(retE)
    # print(len(retE))
    pass