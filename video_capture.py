import os
import shutil
import subprocess
import sys
import time
import logging
import cv2


class VideoCapture:
    def __init__(self):
        self.frame_rate = 25.0
        self.postfix_file = 2
        if self.postfix_file == 1:
            self.postfix = ".avi"
            pass
        else:
            self.postfix = ".mp4"
            pass
        self.phase_number = None
        if self.postfix_file == 2:
            self.path_in = "/home/zqs/shenzj/data/publish_data/RGB_HIKVISION"
            self.path_out = "/home/zqs/shenzj/data/publish_data/RGB_HIKVISION_CAPTURE"
            self.log_path = "/home/zqs/shenzj/data/publish_data/log/RGB_split_log"
            pass
        else:
            self.path_in = "/home/zqs/shenzj/data/publish_data/RGB_KINECT"
            self.path_out = "/home/zqs/shenzj/data/publish_data/RGB_KINECT_CAPTURE"
            self.log_path = "/home/zqs/shenzj/data/publish_data/log/Kinect_split_log"
            self.coefficient_path = "/home/zqs/shenzj/data/publish_data/log/split_coefficient.txt"
            self.coefficient_dict = self.get_coefficient(self.coefficient_path)
            pass
        self.frame_path_in = "/home/zqs/shenzj/data/publish_data/label/"
        self.name = None
        self.phase1_people_number = [274, 21, 160, 50, 81, 36, 45, 173, 97, 158, 88, 111, 49, 110, 240, 199, 56, 54, 95,
                                     252, 106, 77, 12, 58, 128, 261, 176, 53, 135, 78, 96, 272, 63, 264, 105, 258, 170, 74,
                                     217, 245, 113, 82, 259, 132, 9, 43, 191, 91, 75, 99, 265, 218, 153, 41, 187, 260, 202,
                                     238, 168, 59, 145, 133, 182, 73, 257, 76, 90, 11, 157, 148, 155, 46, 163, 62, 60, 42,
                                     172, 177, 194, 198, 8, 164, 30, 38, 37, 2, 262, 143, 70, 40, 247]
        self.phase2_people_number = [131, 147, 66, 269, 84, 226, 151, 139, 159, 256, 214, 222, 235, 141, 117, 263, 28, 26, 130,
                                     16, 205, 150, 244, 5, 271, 47, 273, 4, 203, 181, 197, 94, 39, 137, 103, 190, 3, 85, 165, 200,
                                     223, 237, 175, 233, 68, 179, 100, 242, 22, 136, 228, 67, 275, 24, 23, 215, 104, 6, 134, 98,
                                     225, 149, 178, 171, 7, 161, 72, 183, 107, 93, 188, 80, 102, 32, 234, 195, 250, 156, 236, 52,
                                     241, 123, 125, 127, 166, 276, 19, 25, 192, 124, 230, 169, 206, 35, 33, 184, 64, 268, 44, 162,
                                     61, 186, 219, 101, 17, 87, 69, 115, 34, 196, 229, 120, 231, 10, 121, 243, 220, 138, 174, 154,
                                     267, 221, 1, 31, 232, 116, 108, 126, 71, 251, 180, 270, 239, 216, 55, 118, 14, 109, 146, 189,
                                     112, 29, 20, 210, 248, 129, 213, 114, 57, 122, 201, 83, 79, 86, 193, 142, 119, 211, 51, 254,
                                     246, 167, 140, 13, 18, 204, 266, 253, 255, 227, 185, 224, 249, 144, 209, 65, 92, 27, 89, 15,
                                     208, 207, 48, 212, 152]
        pass

    @staticmethod
    def change_frame_2_time(frame_rate, frame):
        seconds = float('%.3f' % (frame / frame_rate))
        milliseconds = int(seconds * 1000) % 1000
        seconds = int(seconds)
        minutes, seconds = divmod(seconds, 60)
        hours, minutes = divmod(minutes, 60)
        return_time = "{:02d}:{:02d}:{:02d}.{:03d}".format(hours, minutes, seconds, milliseconds)
        return return_time

    def get_file_path(self):
        file_path_list = []
        for file in os.listdir(self.path_in):
            filepath = os.path.join(self.path_in, file)
            file_path_list.append(filepath)
            pass
        return file_path_list

    @staticmethod
    def get_action_number(action_number):
        a = "A0"
        if len(action_number) == 1:
            a = '{}{}'.format("A00", action_number)
        elif len(action_number) == 2:
            a = '{}{}'.format("A0", action_number)
        else:
            print("There are something wrong about the action number!")
        return a

    @staticmethod
    def get_coefficient(path):
        return_dict = {}
        with open(path, "r") as f:
            lines = f.readlines()
            for line in lines:
                content = line.split(",")
                return_dict[content[0]] = {"C016": content[1], "C017": content[2], "C018": content[3], "C019": content[4].strip()}
        f.close()
        return return_dict

    def capture(self, file_path_list):
        for file_path in file_path_list:
            file_name_with_postfix = os.path.basename(file_path)
            original_video = cv2.VideoCapture(file_path)
            if original_video.isOpened():
                file_name = file_name_with_postfix[:-4]
                file_name1 = '{}{}{}'.format(file_name[4:8], file_name[-8:], ".txt")  # label file name
                file_name2 = '{}{}'.format(file_name[4:8], file_name[-8:])  # label name
                frame_path = '{}/{}'.format(self.frame_path_in, file_name1)  # label path
                kinect_number = file_name[8:12]  # camera number

                if os.path.exists(frame_path):
                    f1 = open(frame_path, "r")
                    lines = f1.readlines()
                    for i in lines:
                        arr_temp = i.split(',')
                        action_number = arr_temp[0]
                        a = self.get_action_number(action_number)
                        file_out_name = '{}{}'.format(file_name, a)
                        file_path_out = '{}/{}{}'.format(self.path_out, file_out_name, self.postfix)
                        if os.path.exists(file_path_out):
                            print("{:s} split video already exists~~~".format(file_path_out))
                            logger.info("{:s} split video already exists~~~".format(file_path_out))
                            continue
                            pass
                        if len(arr_temp) != 5:
                            self.name = "Label format has wrong!"
                            print(self.name)
                            logger.info("{},{}".format(file_out_name, self.name))
                            continue
                            pass
                        if arr_temp[3] != "2" or arr_temp[4] != "2":
                            coefficient = 1.0
                            if self.postfix_file == 1:
                                if int(file_name[5:8]) in self.phase1_people_number:
                                    self.phase_number = 1
                                    pass
                                else:
                                    self.phase_number = 2
                                    pass
                                try:
                                    coefficient = float(self.coefficient_dict[file_name2][kinect_number])
                                    pass
                                except:
                                    self.name = "There are something wrong about coefficient!"
                                    logger.info("{},{}".format(file_name_with_postfix, self.name))
                                    continue
                                    pass
                                pass
                            frame_rate1 = self.frame_rate * coefficient
                            frame_rate1 = float('%.1f' % frame_rate1)
                            start = self.change_frame_2_time(25.0, float(arr_temp[1]))
                            end = self.change_frame_2_time(25.0, float(arr_temp[2]))
                            end_frame = float(arr_temp[2]) * coefficient
                            if self.postfix_file == 1 and self.phase_number == 2:
                                start = self.change_frame_2_time(30.0, float(arr_temp[1]) * coefficient)
                                end = self.change_frame_2_time(30.0, float(arr_temp[2]) * coefficient)
                                frame_rate1 = 30.0
                                pass
                            ffmpeg_cmd = "ffmpeg -i {:s} -vcodec copy -acodec copy -ss {:s} -to {:s} {:s}".format(file_path, start, end, file_path_out)
                            # print(coefficient, ffmpeg_cmd)
                            # raise RuntimeError
                            if (end_frame - original_video.get(7)) > 16:
                                self.name = "End frame greater than source total frame 15!"
                                logger.info("{},{}".format(file_out_name, self.name))
                                continue
                                pass
                            else:
                                if os.system(ffmpeg_cmd) is 0:
                                    if os.path.exists(file_path_out):
                                        video = cv2.VideoCapture(file_path_out)
                                        if not video.isOpened():
                                            # Delete the video in question, and replace it with the way of image re-composition.
                                            self.name = "The first method of cutting has problems"
                                            logger.info("{},{}".format(file_out_name, self.name))
                                            # Remove the wrong video.
                                            os.remove(file_path_out)
                                            picture_path = '{}/{}/{}'.format(self.log_path, "picture", file_out_name)
                                            if not os.path.exists(picture_path):
                                                os.makedirs(picture_path)
                                            picture_path_out = '{}{}'.format(picture_path, "/%3d.jpeg")
                                            ffmpeg_cmd = "ffmpeg -i {:s} -r {:s} -ss {:s} -to {:s} {:s}".format(file_path, str(frame_rate1).split('.')[0], start, end, picture_path_out)
                                            if os.system(ffmpeg_cmd) is 0:
                                                ffmpeg_cmd = "ffmpeg -y -r {} -i {}/%3d.jpeg {}".format(str(frame_rate1), picture_path, file_path_out)
                                                if os.system(ffmpeg_cmd) is 0:
                                                    self.name = "Composite video by image!"
                                                    logger.info("{},{}".format(file_out_name, self.name))
                                                    pass
                                                shutil.rmtree(picture_path)
                                            else:
                                                self.name = "The second method also does not work"
                                                logger.info("{},{}".format(file_name_with_postfix, self.name))
                                                pass
                                            pass
                                        else:
                                            print(file_path_out, "done~")
                                            pass
                                        pass
                                    else:
                                        self.name = "Maybe the action label is wrong!"
                                        logger.info("{},{}".format(file_out_name, self.name))
                                        pass
                                    pass
                                pass
                            pass
                        else:
                            self.name = "Action judge or time windows has wrong!"
                            print(self.name)
                            logger.info("{},{}".format(file_out_name, self.name))
                            pass
                        pass
                    f1.close()
                    pass
                else:
                    self.name = "Can not find the label file!"
                    logger.info("{},{}".format(file_name1, self.name))
                    continue
                    pass
            else:
                self.name = "Source video can not open!"
                logger.info("{},{}".format(file_name_with_postfix, self.name))
            pass
        pass
    pass


if __name__ == "__main__":
    pro = VideoCapture()
    file_path_lst = pro.get_file_path()
    file_path_lst.sort()
    print("Total: ", file_path_lst.__len__())
    print('start ...')
    t1 = time.time() * 1000
    logging.basicConfig(level=logging.DEBUG,
                        filename='{}/{}_split_mp4.log'.format(pro.log_path, time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime())),
                        datefmt='%Y/%m/%d %H:%M:%S',
                        format='%(message)s')
    logger = logging.getLogger(__name__)
    pro.capture(file_path_lst)
    t2 = time.time() * 1000
    print('take time:' + str((t2 - t1) / 1000) + 's')
    print('end.')
