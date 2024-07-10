# PosNet-Pytorch-visual-localization
reference
* [LeGO-LOAM](https://github.com/RobustFieldAutonomyLab/LeGO-LOAM)
* [PoseNet-Pytorch](https://github.com/youngguncho/PoseNet-Pytorch)

## 진행환경
* ROS1 noetic
* ubuntu 20.04 lts
* opencv 4.2.0
* pcl 1.10
* python 3.8.10
* pytorch
* numpy
* torchvision
* tensorboard
* tensorboardx
* pandas


# 진행 과정
* PosNet-Pytorch 학습
* LeGO-LOAM 설치
* GT 제작(Lidar, SLAM(LeGO-LOAM))
* 수집한 데이터 PoseNet에 학습
* Visual Localization Node 제작
* 실시간으로 GT의 pose정보와 Predict한 pose정보를 Rviz상에서 시각화하기



# PosNet-Pytorch 학습 실습
논문에는 GoogleNet을 활용하는데 ResNet이 기본 선택 되어 있습니다.(논문 발표 당시 GoogleNet이 대중적이라고 합니다.)

tensorboard 사용전 환경변수 설정

1. tensorboard 설치 경로를 확인합니다.
```
pip show tensorboard
```
2. TensorBoard가 설치된 경로를 시스템 PATH에 추가합니다.
```
code ~/.bashrc
```

![tensorboard환경변수설정](https://github.com/kyeonghyeon0314/PoseNet-Pytorch-visual-localization/assets/132433953/a4357321-dba8-4ae3-a91e-1a6e551e6ed2)



### -[KingsCollege Dataset](http://mi.eng.cam.ac.uk/projects/relocalisation/)
- 기본 셋팅 [ Epoch : 400, lr : 0.0001, dropout rate : 0.5, model 저장 : 50, batch_size : 16, num_epoch_decay : 50(감소율 0.1) ]
![초기학습 진행 그래프](https://github.com/kyeonghyeon0314/PoseNet-Pytorch-visual-localization/assets/132433953/6ef86f09-bf52-42a7-b35b-bd8cc4c7db69)


[--lr 0.001 --dropout_rate 0.3 --num_epochs 200 --num_epochs_decay 20 --model_save_step 10]  의 설정으로 실행 해보았지만 얻은 수확은 없었습니다.
  
- 기존에 학습 해 두었던 것이 컴퓨터를 바꾸면서 날아가 다시 학습하기에 너무 오래 걸려 향후 학습을 진행하고 우선 초기 학습모델로 진행 하도록 하겠습니다.(24.07.06.sat) , 기존 학습 정보
![model174](https://github.com/kyeonghyeon0314/PoseNet-Pytorch-visual-localization/assets/132433953/b26a65d9-7701-4e37-998f-7cc3097796f4)
![model274](https://github.com/kyeonghyeon0314/PoseNet-Pytorch-visual-localization/assets/132433953/762bd5f9-ece6-4ac8-b696-a34037c735c0)
![model 299](https://github.com/kyeonghyeon0314/PoseNet-Pytorch-visual-localization/assets/132433953/7c50400b-0ee1-493f-a104-e7c8815beae3)


# LeGO-LOAM 설치 및 환경과 맞추기
전에 컴파일 과정에서 utillity.h , Cmake.txt 변경 과 같은 여러번의 시도하였지만 해결하지 못하였습니다.

[결국 같이 진행한 분의 도움을 받아 해결하였습니다.](https://github.com/Cascio99/Posenet-Pytorch-Visual-Localization/blob/main/README.md?plain=1)

최종적으로 utillity.h , Cmake.txt , voxel_grid.h 변경

# GT제작(Lidar, SLAM(LeGO-LOAM))

GT를 제작할때 첫시도에 bag 파일에서 나오는 토픽을 구독하여 이미지와 pose 정보를 저장하는 방식으로 노드를 제작하였습니다. 그러나 이 것은 실시간성이 부족하여 로봇을 운행하는데 적합하지 않습니다. 그러나 LeGO-LOAM을 활용하면 실시 포즈 추정 데이터를 활용 할 수 있습니다. 두 방법 모두 기재해 놓도록 하겠습니다.

## bag 파일에서 나오는 토픽 활용(실시간성이 좋지 않음)
1. 패키지 제작
```
catkin_create_pkg synchronizing rospy cv_bridge tf message_filters sensor_msgs
```

* cv_bridge : 이미지 압축을 해제하고 처리하기 위해
* tf : transform 토픽을 subscribe 하고 pose 정보 추출
* message_filters : 시간 동기화를 위한 ApproximateTimeSynchronizer를 제공(일부 오차를 허용)
* sensor_msgs : 이미지 메시지(CompressedImage)를 사용
```
touch image_pose_synchronizer.py  # 파이썬 파일 생성
```
[image_pose_synchronizer.py 생성은 해당 코드 참조](https://github.com/Taemin0707/Regala/blob/main/regala_ros/src/video_stitcher_timeshync.py)



2. 노드 실행 및 gt 제작
* roscore
* 구현한 ROS 노드 실행 : 위에서 제작 노드 실행 (저장하고 싶은 디렉토리에서)
```
rosrun synchronizing image_pose_synchronizer.py
```
* ROS bag 파일 재생 :
```
rosbag play dataset_train.bag --clock(시간 동기화)
rosbag play dataset_test.bag --clock
```
test 데이터셋의 파일 손상이 되어 reindex 진행
```
rosbag reindex dataset_test.bag 
```
* 결과 확인(이미지 와 pose 정보가 동기화되어 저장되었는지 확인)

[LeGO-LOAM 실행 및 GT 제작 영상 첨부 (github_upload - Clipchamp로 제작 (1))](https://github.com/kyeonghyeon0314/PoseNet-Pytorch-visual-localization.git)

![Screenshot from 2024-07-07 16-58-38](https://github.com/kyeonghyeon0314/PoseNet-Pytorch-visual-localization/assets/132433953/51360090-9b0a-4edd-af69-a9473508292a){: width="60" height="60%"}

PoseNet 학습시 dataloader.py 만들기 용이하게 pose 데이터를 하나의 txt로 만들어 질 수 있도록 image_pose_synchronizer.py를 수정 하였습니다.
```
#기존 코드
    pose_data = f"{position.x},{position.y},{position.z},{orientation.x},{orientation.y},{orientation.z},{orientation.w}\n"
    pose_filename = f"pose_{timestamp.secs}_{timestamp.nsecs}.txt"
    pose_path = os.path.join("poses", pose_filename)  # pose 저장 경로 설정
    with open(pose_path, "w") as f:
        f.write(pose_data)
```
```
#수정 코드
    pose_data = f"images_{test, train 상황에 맞게 수정}/{image_filename} {position.x} {position.y} {position.z} {orientation.x} {orientation.y} {orientation.z} {orientation.w}\n"
    
    
    pose_filename = "poses.txt"
    pose_path = os.path.join("poses", pose_filename)  # pose 저장 경로 설정
    with open(pose_path, "a") as f:  #append 모드로 파일 열기
        f.write(pose_data)
```
![Screenshot from 2024-07-07 23-35-45](https://github.com/kyeonghyeon0314/AirLAB_toy_project/assets/132433953/8eeb2e60-4a4e-4f66-a3ef-bbaad9ae9538)

사진을 보시면 이미지 파일개수와 pose 정보의 개수가 동일 한것을 확인 할 수 있고 PoseNet-Pytorc의 소스코드를 그대로 활용하기 편리해졌습니다. 

+ 학습에는 지장이 없었는데 test 과정에서 문제가 생겨 GT를 좀더 상황에 맞게 설정후 다시 학습을 시켰습니다.(7/09/02:11)

아래 영상은 bag 파일에서 나오는 토픽을 가지고 학습된 PoseNet모델로 pose를 추정하는 영상입니다. 35초 부터 영상을 보시면 bag파일 play는 멈췄지만 실시간성이 좋지 않아 계속해서 추정을 하고 있는 모습을 볼 수 있습니다. 

https://github.com/kyeonghyeon0314/AirLAB_toy_project/assets/132433953/93003094-f34e-4798-8cde-25a0dd92db13










## LeGO-LOAM 활용(실시간성 용이)
패키지 생성 및 빌드
```
cd ~/catkin_ws/src
catkin_create_pkg image_pose_sync rospy std_msgs sensor_msgs nav_msgs
cd ~/catkin_ws
chmod +x /catkin_ws/src/image_pose_sync/scripts/image_pose_sync.py
catkin_make
```

실행 파일 제작
```
mkdir script
touch image_pose_sync.py
```
CMakelist와 package xml 도 수정 하였습니다.
* 실행 과정
```
roscore
roslaunch lego_loam run.launch
rosrun image_pose_sync image_pose_sync.py --mode train
rosbag play data_train.bag --clock
```
* 결과
![GT 제작](https://github.com/kyeonghyeon0314/AirLAB_toy_project/assets/132433953/488860d6-3366-49f2-bc20-47401d22895e)
이미지 데이터와 pose 정보의 개수가 일치하여 시간 동기화가 제대로 되어진 것을 확인 하였습니다. 그리고 실시간성이 더 좋아져 데이터 셋의 크기도 증가한것으로 확인 됩니다.


# 취득한 GT AirLab Dataset으로 학습 및 테스트
기존 dataset_train.txt 를 보면 3번쨰 라인까지 데이터의 정보에 대한 정보를 담고 있습니다. 해당 부분만 수정하여 학습을 진행하였습니다.
```
class CustomDataset(Dataset):
    def __init__(self, image_path, metadata_path, mode, transform, num_val=100):
        self.image_path = image_path
        self.metadata_path = metadata_path
        self.mode = mode
        self.transform = transform
        raw_lines = open(self.metadata_path, 'r').readlines()
        self.lines = raw_lines[0:]  # 기존은 4번째 부터 
```

## 학습실행 
```
python3 train.py --image_path ./PoseNet/AirLAB --metadata_path ./PoseNet/AirLAB/poses_data_train.txt
```



### 최적의 파라미터 조합하기 ( 진행중 )
```
python3 train.py --image_path ./PoseNet/AirLAB --metadata_path ./PoseNet/AirLAB/poses_train.txt --batch_size 32 --num_epochs 150 --lr 0.001 --num_epochs_decay 25 --model_save_step 25
```
```
python3 train.py --image_path ./PoseNet/AirLAB --metadata_path ./PoseNet/AirLAB/poses_train.txt --batch_size 32 --num_epochs 300 --model_save_step 10 --sample_step 100 --lr 0.001 --num_epochs_decay 20 --num_workers 6
```

# Test dataset으로 실시간으로 GT의 pose정보와 Predict한 pose정보를 Rviz상에서 시각화하기
## Predict한 Pose RViz상에 시각화 하기
패키지 생성
```
catkin_create_pkg <패키지 이름> cv_bridge geometry_msgs message_filters rospy visualization_msgs

```
실행 코드 파일 생성
```
touch PoseNet_predictor.py  #생성 후 코드 작성
```
실행 권한 부여하기
```
chmod +x /catkin_ws/src/synchronizing/scripts/PoseNet_predictor.py
```

* ROS 실행 순서
```
roscore
rosrun {패키지명} pose_visualizer.py
rviz
rosbag play dataset_test.bag
```










