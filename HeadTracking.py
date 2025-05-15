import cv2
import numpy as np
import mediapipe as mp
import math

# 3D 모델 포인트 (간단화된 얼굴 모델: 코끝, 눈, 입 등)
model_points = np.array([
    (0.0, 0.0, 0.0),             # Nose tip
    (0.0, -330.0, -65.0),        # Chin
    (-225.0, 170.0, -135.0),     # Left eye left corner
    (225.0, 170.0, -135.0),      # Right eye right corner
    (-150.0, -150.0, -125.0),    # Left mouth corner
    (150.0, -150.0, -125.0)      # Right mouth corner
])

# 선택한 얼굴 랜드마크 인덱스
LANDMARK_INDEXES = [1, 152, 33, 263, 61, 291]

mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh()

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break
    h, w = frame.shape[:2]
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = face_mesh.process(frame_rgb)

    if results.multi_face_landmarks:
        for landmarks in results.multi_face_landmarks:
            image_points = []
            for idx in LANDMARK_INDEXES:
                lm = landmarks.landmark[idx]
                x, y = int(lm.x * w), int(lm.y * h)
                image_points.append((x, y))
                cv2.circle(frame, (x, y), 3, (0, 255, 0), -1)

            image_points = np.array(image_points, dtype='double')

            min_x, min_y = w, h
            max_x, max_y = 0, 0
            for lm in landmarks.landmark:
                px, py = int(lm.x * w), int(lm.y * h)
                min_x, min_y = min(min_x, px), min(min_y, py)
                max_x, max_y = max(max_x, px), max(max_y, py)
            cv2.rectangle(frame, (min_x, min_y), (max_x, max_y), (0, 0, 255), 2)
            print(f"[Face BBOX] Top-Left: ({min_x}, {min_y}) | Bottom-Right: ({max_x}, {max_y})")
    
            # 카메라 매트릭스
            focal_length = w
            center = (w / 2, h / 2)
            camera_matrix = np.array([
                [focal_length, 0, center[0]],
                [0, focal_length, center[1]],
                [0, 0, 1]
            ], dtype='double')

            dist_coeffs = np.zeros((4, 1))  # 왜곡 없음 가정

            success, rotation_vector, translation_vector = cv2.solvePnP(
                model_points, image_points, camera_matrix, dist_coeffs
            )

            # 회전 벡터 → 오일러 각도 (yaw, pitch, roll)
            rmat, _ = cv2.Rodrigues(rotation_vector)
            pose_mat = cv2.hconcat((rmat, translation_vector))
            _, _, _, _, _, _, euler_angles = cv2.decomposeProjectionMatrix(pose_mat)

            pitch, yaw, roll = [float(angle) for angle in euler_angles]

            # 이동 방향
            x, y, z = translation_vector.flatten()

            print(f"[6DOF] Rotation => Yaw: {yaw:.2f}, Pitch: {pitch:.2f}, Roll: {roll:.2f}")
            print(f"[6DOF] Position => X: {x:.2f}, Y: {y:.2f}, Z: {z:.2f}")
            print("-" * 60)

    cv2.imshow("Head Tracking 6DOF", frame)
    if cv2.waitKey(1) & 0xFF == 27:  # ESC 키
        break

cap.release()
cv2.destroyAllWindows()
