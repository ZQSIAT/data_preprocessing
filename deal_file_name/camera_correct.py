import cv2
import os
assert cv2.__version__[0] == '3'
import numpy as np
import glob
import time


#要提取视频的文件名，隐藏后缀
sourceFileName='F:/camera/c1'
#转换为视频文件，图片路径
input_pic_path =sourceFileName+ '/vedio/'    # 帧图存放位置
#存放黑白格子路径
checkboard_path= 'F:/camera/correct'
#黑白格子行列
M = 6
N = 9
#畸变校正后图片存放路径
corrected_path = 'F:/camera/corrected/'
#校正图片数
count = 0
# 生成视频的帧率
FPS = 25
# 图片的宽度、高度
width_and_height = (1280, 720)
#输出视频名字
output_video_name = "F:/camera/c1/1.avi"

def vidoe_to_img(sourceFileName):
    #在这里把后缀接上
    video_path = os.path.join("", "", sourceFileName+'.mp4')
    times=0
    #提取视频的频率，每25帧提取一个
    frameFrequency=1
    #输出图片到当前目录vedio文件夹下
    outPutDirName=sourceFileName+'/vedio/'
    if not os.path.exists(outPutDirName):
        #如果文件目录不存在则创建目录
        os.makedirs(outPutDirName)
    camera = cv2.VideoCapture(video_path)
    while True:
        times+=1
        res, image = camera.read()
        if not res:
            print('not res , not image')
            break
        if times%frameFrequency==0:
            cv2.imwrite(outPutDirName + str(times)+'.jpg', image)
            print(outPutDirName + str(times)+'.jpg')
    print('图片提取结束')
    camera.release()

time_start = time.time()
vidoe_to_img(sourceFileName)



def get_K_and_D(checkerboard, imgsPath):
    CHECKERBOARD = checkerboard
    subpix_criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.1)
    calibration_flags = cv2.fisheye.CALIB_RECOMPUTE_EXTRINSIC + cv2.fisheye.CALIB_CHECK_COND + cv2.fisheye.CALIB_FIX_SKEW
    objp = np.zeros((1, CHECKERBOARD[0] * CHECKERBOARD[1], 3), np.float32)
    objp[0, :, :2] = np.mgrid[0:CHECKERBOARD[0], 0:CHECKERBOARD[1]].T.reshape(-1, 2)
    _img_shape = None
    objpoints = []
    imgpoints = []
    images = glob.glob(imgsPath + '/*.jpg')
    for fname in images:
        img = cv2.imread(fname)
        if _img_shape == None:
            _img_shape = img.shape[:2]
        else:
            assert _img_shape == img.shape[:2], "All images must share the same size."

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        ret, corners = cv2.findChessboardCorners(gray, CHECKERBOARD,
                                                 cv2.CALIB_CB_ADAPTIVE_THRESH + cv2.CALIB_CB_FAST_CHECK + cv2.CALIB_CB_NORMALIZE_IMAGE)
        if ret == True:
            objpoints.append(objp)
            cv2.cornerSubPix(gray, corners, (3, 3), (-1, -1), subpix_criteria)
            imgpoints.append(corners)
        N_OK = len(objpoints)
        K = np.zeros((3, 3))
        D = np.zeros((4, 1))
        rvecs = [np.zeros((1, 1, 3), dtype=np.float64) for i in range(N_OK)]
        tvecs = [np.zeros((1, 1, 3), dtype=np.float64) for i in range(N_OK)]
        rms, _, _, _, _ = \
            cv2.fisheye.calibrate(
                objpoints,
                imgpoints,
                gray.shape[::-1],
                K,
                D,
                rvecs,
                tvecs,
                calibration_flags,
                (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 1e-6)
            )
        DIM = _img_shape[::-1]
        print("Found " + str(N_OK) + " valid images for calibration")
        print("DIM=" + str(_img_shape[::-1]))
        print("K=np.array(" + str(K.tolist()) + ")")
        print("D=np.array(" + str(D.tolist()) + ")")

    return DIM, K, D


# 计算内参和矫正系数
'''
# checkerboard： 棋盘格的格点数目
# imgsPath: 存放鱼眼图片的路径
'''
DIM, K, D = get_K_and_D((M, N), checkboard_path)

def undistort(img_path,count):
    img = cv2.imread(img_path)
    img = cv2.resize(img, DIM)
    map1, map2 = cv2.fisheye.initUndistortRectifyMap(K, D, np.eye(3), K, DIM,cv2.CV_16SC2)
    undistorted_img = cv2.remap(img, map1, map2, interpolation=cv2.INTER_LINEAR,borderMode=cv2.BORDER_CONSTANT)
    if not os.path.exists(corrected_path):
        os.mkdir(corrected_path)
    cv2.imwrite(corrected_path+str(count)+'.jpg', undistorted_img)
image = os.listdir(input_pic_path)
image.sort(key=lambda x:int(x[:-4]))
for image_name in image:
    # print(image_name)
    count += 1
    image_path = input_pic_path+image_name
    undistort(image_path,count)


# time_start = time.time()
fourcc = cv2.VideoWriter_fourcc(*'MJPG')
videoWriter = cv2.VideoWriter(output_video_name, fourcc, FPS, width_and_height)

pic_name_all = os.listdir(corrected_path)
pic_name_all.sort(key=lambda x:int(x[:-4]))
for pic_name in pic_name_all:
    img_name = corrected_path + pic_name
    frame = cv2.imread(img_name)
    videoWriter.write(frame)
    print("%s/%s" % (pic_name_all.index(pic_name) + 1, len(pic_name_all)), img_name)
videoWriter.release()

print("cost_time=", time.time() - time_start)
