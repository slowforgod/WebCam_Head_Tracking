## WebCam_Head_Tracking

### 📋 개요
HeadTracker는 MediaPipe Face Mesh를 사용하여 웹캠을 통해 실시간으로 머리의 회전, 기울기, 위치를 추적하는 Python 애플리케이션입니다. 게임 제어, VR/AR 애플리케이션, 접근성 도구 등 다양한 용도로 활용할 수 있습니다.

### ✨ 주요 기능

실시간 머리 자세 추적 (Yaw, Pitch, Roll)
머리 위치 좌표 감지
눈 깜빡임 감지
입 열기/닫기 감지
다양한 출력 포맷 지원 (JSON, OSC, 키보드 입력)
캘리브레이션 기능
멀티 카메라 지원

### 🚀 빠른 시작
필요 조건

Python 3.8 이상
웹캠 또는 USB 카메라
Windows 10/11, macOS, Linux

설치

저장소 클론

bashgit clone https://github.com/yourusername/headtracker.git
cd headtracker

가상환경 생성 (권장)

bashpython -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

의존성 설치

bashpip install -r requirements.txt
기본 사용법
bashpython headtracker.py
또는 설정 파일과 함께:
bashpython headtracker.py --config config.json

### 📖 사용법
기본 추적
pythonfrom headtracker import HeadTracker

tracker = HeadTracker()
tracker.start()

while True:
    pose_data = tracker.get_pose()
    print(f"Yaw: {pose_data['yaw']:.2f}, Pitch: {pose_data['pitch']:.2f}, Roll: {pose_data['roll']:.2f}")
고급 설정
pythonconfig = {
    "camera_id": 0,
    "detection_confidence": 0.5,
    "tracking_confidence": 0.5,
    "smoothing": True,
    "output_format": "json"
}

tracker = HeadTracker(config)
### ⚙️ 설정 옵션
매개변수기본값설명camera_id0카메라 디바이스 IDdetection_confidence0.5얼굴 감지 신뢰도 임계값tracking_confidence0.5추적 신뢰도 임계값smoothingTrue데이터 스무딩 활성화max_faces1추적할 최대 얼굴 수

### 📊 출력 데이터 형식
json{
  "timestamp": 1234567890.123,
  "pose": {
    "yaw": -15.2,
    "pitch": 8.7,
    "roll": -2.1
  },
  "position": {
    "x": 0.15,
    "y": -0.08,
    "z": -0.95
  },
  "landmarks": {
    "nose_tip": [320, 240],
    "left_eye": [285, 220],
    "right_eye": [355, 220]
  },
  "gestures": {
    "blink_left": false,
    "blink_right": true,
    "mouth_open": false
  }
}

### 🔧 캘리브레이션

애플리케이션 실행
카메라 앞에서 정면을 바라보기
'C' 키를 눌러 캘리브레이션 시작
머리를 천천히 좌우, 상하로 움직이기
'S' 키를 눌러 캘리브레이션 저장

### 🐛 문제 해결
일반적인 문제들
카메라가 인식되지 않을 때:
bash# 사용 가능한 카메라 목록 확인
python -c "import cv2; print([i for i in range(10) if cv2.VideoCapture(i).read()[0]])"
성능이 느릴 때:

detection_confidence와 tracking_confidence 값 증가
카메라 해상도 낮추기
GPU 가속 활성화 (pip install mediapipe-gpu)

추적이 불안정할 때:

조명 개선
카메라와의 거리 조정 (50-100cm 권장)
배경 단순화

