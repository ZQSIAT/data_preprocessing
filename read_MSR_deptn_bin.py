# this code is for reading MSR_dataset depth codes.

import numpy as np
import cv2

class ReadMSRdepth(object):

    def __init__(self):
        self.dst_path = ""
        pass
    def read_msr_depth_maps(self, depth_file, seqs_idx, norm_val=False, vector_convert=None, header_only=False,
                            is_segment=False, is_mask=False):
        r""" Read the MSR binary file of depth maps, and then return depth maps and
        mask maps.

        Param:
            depth_file (string): the path for a depth file (*.bin).
            is_segment (bool): set it 'True' to get human segmented maps.
            is_mask: set it 'True' to get mask maps
        Return:
            depth_map (np.uint32): in format of '[frames, height, width]'
            mask_map (np.uint8): in format of '[frames, height, width]'
            Note: mask_map is returned only the input parameter 'is_mask' is 'True'
        """

        file_ = open(depth_file, 'rb')

        # get header info
        # print(np.fromstring(file_.read(4), dtype=np.int32))
        # raise RuntimeError
        frames = np.fromstring(file_.read(4), dtype=np.int32)[0]
        cols = np.fromstring(file_.read(4), dtype=np.int32)[0]
        rows = np.fromstring(file_.read(4), dtype=np.int32)[0]

        if header_only:
            return [frames, rows, cols]

        # read the remaining data
        sdata = file_.read()

        # depth maps and mask images are stored together per row
        dt = np.dtype([('depth', np.int32, cols), ('mask', np.uint8, cols)])
        frame_data = np.fromstring(sdata, dtype=dt)

        # extract the depth maps and mask data
        depth_map = frame_data['depth'].reshape([frames, rows, cols])
        mask_map = frame_data['mask'].reshape([frames, rows, cols])

        if is_segment:
            mask_map_inv = mask_map == 0
            depth_map[mask_map_inv] = 0

        if seqs_idx is not None:
            depth_map = depth_map[seqs_idx, :]
            mask_map = mask_map[seqs_idx, :]

        depth_map = depth_map.astype(np.float)

        if norm_val:
            # depth_map = (depth_map - 800.0) / 3200.0  # valid 800-4000mm
            depth_map = depth_map / 4000.0  # valid 800-4000mm
            depth_map = np.clip(depth_map, 0.0, 1.0)
            depth_map = depth_map * 255.0

        if vector_convert is not None:
            depth_map = vector_convert(depth_map)

        else:
            depth_map = depth_map[:, np.newaxis]

        if is_mask:
            return depth_map, mask_map
        else:
            return depth_map
    pass


if __name__ == "__main__":
    my_task = ReadMSRdepth()
    temp_path = "D:/pycharm_project/temp/a01_s01_e02_depth.bin"
    depth_arr = my_task.read_msr_depth_maps(temp_path, 15)
    print(depth_arr.shape)
    cv2.imshow("test", depth_arr.reshape(240, 320))
    cv2.waitKey(0)
    pass
