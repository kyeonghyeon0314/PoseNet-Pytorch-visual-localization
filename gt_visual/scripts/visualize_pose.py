#!/usr/bin/env python3.8

import rospy
import tf
import tf.transformations as tft
from geometry_msgs.msg import PoseStamped , PoseArray, Pose
import time
import numpy as np

def parse_gt_file(file_path):
    poses = []
    with open(file_path, 'r') as file:
        lines = file.readlines()
        for line in lines:
            parts = line.strip().split()
            image_path = parts[0]
            timestamp = float(image_path.split('_')[-1].split('.')[0] + '.' + image_path.split('_')[-1].split('.')[1])
            px, py, pz = float(parts[1]), float(parts[2]), float(parts[3])
            qx, qy, qz, qw = float(parts[4]), float(parts[5]), float(parts[6]), float(parts[7])
            poses.append((timestamp, (px, py, pz, qx, qy, qz, qw)))
    return poses

def transform_pose(pose):
    px, py, pz = pose[0], pose[1], pose[2]
    qx, qy, qz, qw = pose[3], pose[4], pose[5], pose[6]
    
    transformed_px = -pz
    transformed_py = -px
    transformed_pz = py
    
    quat = [qx, qy, qz, qw]
    #x 축 90도 회전
    rot_quat_x = tft.quaternion_from_euler(np.pi / 2, 0, 0)
    #z 축 -90도 회전
    rot_quat_z = tft.quaternion_from_euler(0, 0, -np.pi / 2)

    # 기존 퀀터니언과 회전 퀀터니언을 곱하여 새로운 퀀터니언 생성
    quat_after_x = tft.quaternion_multiply(rot_quat_x, quat)
    transformed_quat = tft.quaternion_multiply(rot_quat_z, quat_after_x)
    
    return transformed_px, transformed_py, transformed_pz, transformed_quat[0], transformed_quat[1], transformed_quat[2], transformed_quat[3]

def publish_pose(publisher, pose):
    transformed_pose = transform_pose(pose)
    pose_msg = Pose()
    pose_msg.pose.position.x = pose[0]
    pose_msg.pose.position.y = pose[1]
    pose_msg.pose.position.z = pose[2]
    pose_msg.pose.orientation.x = pose[3]
    pose_msg.pose.orientation.y = pose[4]
    pose_msg.pose.orientation.z = pose[5]
    pose_msg.pose.orientation.w = pose[6]
    return pose_msg

def main():
    rospy.init_node('gt_pose_visualizer', anonymous=True)
    pose_publisher = rospy.Publisher('/gt_poses', PoseStamped, queue_size=10)

    gt_file_path = '/home/kimkh/PoseNet-Pytorch/PoseNet/AirLAB/pose_data_test.txt'  # 실제 파일 경로
    poses = parse_gt_file(gt_file_path)

    rate = rospy.Rate(60)  # 60 Hz
    pose_array_msg = PoseArray()
    pose_array_msg.header.frame_id = 'map'

    for timestamp, pose in poses:
        if rospay.is_shutdown():
            break
        pose_msg = publish_pose(pose_publisher, pose)
        pose_array_msg.poses.append(pose_msg)
        pose_publisher.publish(pose_array_msg)
        rate.sleep()

if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException:
        pass


