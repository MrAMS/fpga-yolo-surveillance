import os
import cv2

def crop_and_save_image(image, bbox, save_path):
    """
    Crops the image according to the given bbox and saves it to the given folder.

    Parameters:
    - image: input image.
    - bbox: tuple of (x, y, width, height) of the bounding box.
    - save_folder: directory to save the cropped image.

    Returns:
    - save_path: the file path where the cropped image is saved.
    """
    
    # 如果图像不能加载，则返回None
    if image is None:
        return
    
    # 解析bbox坐标
    x, y, width, height = bbox
    print(x, y, width, height)
    
    # 根据bbox裁剪图像
    cropped_image = image[y:y+height, x:x+width]

    if cropped_image.size ==0:
        return
    
    # 保存裁剪后的图像
    cv2.imwrite(save_path, cropped_image)
