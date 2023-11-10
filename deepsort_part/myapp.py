# vim: expandtab:ts=4:sw=4
from __future__ import division, print_function, absolute_import

import argparse
import os

import cv2
import numpy as np

from deep_sort import nn_matching
from deep_sort.detection import Detection
from deep_sort.tracker import Tracker

import models
import myutils
import datetime

import yolov2_pynq

import subprocess

track_res = []
track_res_pre = []
track_hav = []

def create_detections(tracker_info):
    detection_list = []
    for info in tracker_info:
        detection_list.append(Detection(info[1], info[3], info[2], info[0]))
    return detection_list


def run(min_confidence, max_cosine_distance, nn_budget):
    metric = nn_matching.NearestNeighborDistanceMetric(
        "cosine", max_cosine_distance, nn_budget)
    tracker = Tracker(metric)
    results = []
    

    models.delete_all_object()
    date_start = datetime.datetime.now()

    frame_idx = 0
    for jjj in range(1, 1000):

        print("Processing frame %05d" % frame_idx)

        # Load image and generate detections.

        cam_img_path = "/home/xilinx/webcam.jpg"
        cmd="fswebcam  --no-banner --save {} -d /dev/video0 2> /dev/null".format(cam_img_path)
        p=subprocess.Popen(cmd,shell=True)
        return_code=p.wait()  #等待子进程结束，并返回状态码；
        print("return_code", return_code)
        
        detections = create_detections(yolov2_pynq.kick_off(cam_img_path))
        detections = [d for d in detections if d.confidence >= min_confidence]

        print(detections)


        # Update tracker.
        tracker.predict()
        tracker.update(detections)

        global track_res
        global track_res_pre
        global track_hav

        track_res = []

        # Store results.
        for track in tracker.tracks:
            if not track.is_confirmed() or track.time_since_update > 1:
                continue
            bbox = track.to_tlwh()
            results.append([
                frame_idx, track.track_id, bbox[0], bbox[1], bbox[2], bbox[3]])
            
            track_res.append(track.track_id)
            if not track.track_id in track_hav:
                img_path = "data/{}-{}.jpg".format(track.detection.name, track.track_id)
                myutils.crop_and_save_image(cv2.imread(cam_img_path, cv2.IMREAD_COLOR),
                                            track.to_tlwh().astype(np.int_), img_path)
                models.create_object(track.track_id, "{}".format(track.detection.name),
                                     img_path, datetime.datetime.now(), track.detection.confidence)
                track_hav.append(track.track_id)
                print("track {},{} add to database!!!".format(track.detection.name, datetime.datetime.now()))
            else:
                models.update_object_exit_time(track.track_id,
                                           datetime.datetime.now())
                print("track {},{} update to database!!!".format(track.detection.name, datetime.datetime.now()))

            
        # diff = set(track_res).difference(set(track_res_pre))
        # for track_id in diff:
        #     print("diff", track_id)
        #     models.update_object_exit_time(track_id,
        #                                    datetime.datetime.now())

        print(track_res)

        track_res_pre = track_res[:]

        frame_idx += 1


if __name__ == "__main__":
    run(0.5, 0.025
        , 100)
