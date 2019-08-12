import os
import time
import cv2


def is_path_existed_if_no_mk_it(path):
    """
    Check the path existing or not, if not create it.
    :param path: Must be a path not a file.
    :return: No return.
    """
    if not os.path.exists(path):
        os.mkdir(path)
        pass
    pass


def resize_img(src, dst):
    file_list = os.listdir(src)
    for i in file_list:
        temp_img = cv2.imread(src + i)
        resize_image = cv2.resize(temp_img, (540, 360))
        cv2.imwrite(dst + i, resize_image)
        print("{:s} has been resized.".format(i))
        pass
    pass


def extract_frame(src, dst):
    video = cv2.VideoCapture(src)
    time_interval = 1   # set a extract time window
    count = 0
    save_count = 0
    while True:
        success, frames = video.read()
        count += 1
        if not success:
            print("Video has been all read")
            break
            pass
        if count % time_interval == 0:
            save_count += 1
            save_name = "{:04d}.png".format(save_count)
            resize_image = cv2.resize(frames, (540, 360))
            cv2.imwrite(dst + save_name, resize_image)
            print("{:s} has been saved".format(save_name))
            pass
        pass

    pass


def switch_network(var):
    switcher = {
        0: "FlowNet2",
        1: "FlowNet2-c",
        2: "FlowNet2-C",
        3: "FlowNet2-cs",
        4: "FlowNet2-CS",
        5: "FlowNet2-css",
        6: "FlowNet2-CSS",
        7: "FlowNet2-css-ft-sd",
        8: "FlowNet2-CSS-ft-sd",
        9: "FlowNet2-s",
        10: "FlowNet2-S",
        11: "FlowNet2-SD",
        12: "FlowNet2-ss",
        13: "FlowNet2-SS",
        14: "FlowNet2-sss",
        15: "FlowNet2-KITTI",
        16: "FlowNet2-Sintel"
    }
    return switcher.get(var, 'netError')
    pass


def move_big_file(src, dst):
    src_list = os.listdir(src)
    for i in src_list:
        os.rename(src + i, dst + i)
        print("{:s} has been renamed.".format(i))
        pass
    pass


if __name__ == "__main__":
    print("Start processing...")
    start_time = time.time()
    print("#" * 120)
    # src_path = "/home/zqs/shenzj/data/publish_data/DataSet1/KINECT/RGB_KINECT_CAPTURE/"
    # dst_path = "/home/zqs/shenzj/data/publish_data/DataSet2/KINECT/RGB_KINECT_CAPTURE/"
    # move_big_file(src_path, dst_path)

    # img_src = "/ssd_data/zqs/workspace/flownet2/flownet2-docker/data/test/"
    # img_dst = "/ssd_data/zqs/workspace/flownet2/flownet2-docker/data/test_resize/"
    # is_path_existed_if_no_mk_it(img_dst)
    # resize_img(img_src, img_dst)
    # src_mp4 = "/home/zqs/shenzj/data/publish_data/DataSet1/RGB_HIKVISION/O001P009C001T001S002.mp4"
    # dst_png = "/ssd_data/zqs/workspace/flownet2/flownet2-docker/data/test_long/"
    # is_path_existed_if_no_mk_it(dst_png)
    # extract_frame(src_mp4, dst_png)
    # raise RuntimeError

    # sh_path = "/ssd_data/zqs/workspace/flownet2/flownet2-docker/run-network.sh"
    # net_work = switch_network(9)
    # gpu_id = 0
    # first_frame_list = "data/1.txt"
    # second_frame_list = "data/2.txt"
    # flo_out_list = "data/3.txt"
    # os.chdir("/ssd_data/zqs/workspace/flownet2/flownet2-docker/")
    # flownet_cmd = "sudo {:s} -n {:s} -g {:01d} {:s} {:s} {:s}".format(sh_path, net_work, gpu_id, first_frame_list, second_frame_list, flo_out_list)
    # os.system(flownet_cmd)

    end_time = time.time()
    print("#" * 120)
    print("Finished! Time elapse: {:.2f} seconds.".format(end_time - start_time))
    pass
