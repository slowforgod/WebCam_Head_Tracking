import cv2
import numpy as np
import mediapipe as mp
import asyncio
import websockets
import json

model_points = np.array([
    (0.0, 0.0, 0.0),
    (0.0, -330.0, -65.0),
    (-225.0, 170.0, -135.0),
    (225.0, 170.0, -135.0),
    (-150.0, -150.0, -125.0),
    (150.0, -150.0, -125.0)
])

LANDMARK_INDEXES = [1, 152, 33, 263, 61, 291]

mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh()
cap = cv2.VideoCapture(0)

async def main():
    uri = "ws://localhost:8765"
    async with websockets.connect(uri) as websocket:
        while True:
            ret, frame = await asyncio.to_thread(cap.read)  # 비동기 스레드에서 읽기
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

                    focal_length = w
                    center = (w / 2, h / 2)
                    camera_matrix = np.array([
                        [focal_length, 0, center[0]],
                        [0, focal_length, center[1]],
                        [0, 0, 1]
                    ], dtype='double')

                    dist_coeffs = np.zeros((4, 1))

                    success, rotation_vector, translation_vector = cv2.solvePnP(
                        model_points, image_points, camera_matrix, dist_coeffs
                    )

                    rmat, _ = cv2.Rodrigues(rotation_vector)
                    pose_mat = cv2.hconcat((rmat, translation_vector))
                    _, _, _, _, _, _, euler_angles = cv2.decomposeProjectionMatrix(pose_mat)

                    pitch, yaw, roll = [float(angle) for angle in euler_angles]
                    x, y, z = translation_vector.flatten()

                    data = {
                        "rotation": {"yaw": yaw, "pitch": pitch, "roll": roll},
                        "position": {"x": x, "y": y, "z": z}
                    }

                    await websocket.send(json.dumps(data))
                    print(f"[Sent] {data}")

            cv2.imshow("Head Tracking", frame)
            if cv2.waitKey(1) & 0xFF == 27:
                break

    cap.release()
    cv2.destroyAllWindows()

asyncio.run(main())