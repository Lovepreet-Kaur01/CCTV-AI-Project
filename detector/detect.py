import cv2
from ultralytics import YOLO
import os
from datetime import datetime

model = YOLO("yolov8n.pt")

# 🔹 VIDEO FILE DETECTION
def detect_objects(video_path):
    cap = cv2.VideoCapture(video_path)

    results_list = []

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        results = model(frame)

        for r in results:
            for box in r.boxes:
                cls = int(box.cls[0])
                label = model.names[cls]
                results_list.append(label)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    return results_list


# 🔹 LIVE CAMERA DETECTION (FINAL VERSION 🔥)
def live_detection():
    cap = cv2.VideoCapture(0)

    results_list = []

    # Create folder for saving images
    os.makedirs("detections", exist_ok=True)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        results = model(frame)

        person_count = 0  # 🔢 count persons

        for r in results:
            for box in r.boxes:
                cls = int(box.cls[0])
                label = model.names[cls]

                # 🎯 Person-only detection
                if label == "person":
                    person_count += 1

                    x1, y1, x2, y2 = map(int, box.xyxy[0])

                    # Draw box
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                    cv2.putText(frame, label, (x1, y1 - 10),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

                    results_list.append(label)

        # 🔢 Show count
        cv2.putText(frame, f"Persons: {person_count}",
                    (20, 40),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (255, 0, 0),
                    2)

        # 🚨 Alert system
        if person_count > 2:
            cv2.putText(frame,
                        "ALERT: Too many people!",
                        (20, 80),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        1,
                        (0, 0, 255),
                        3)

        # 🕒 Real-time Date & Time (NEW 🔥)
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cv2.putText(frame,
                    current_time,
                    (20, frame.shape[0] - 20),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.7,
                    (0, 255, 255),
                    2)

        # 📸 Save image when person detected
        if person_count > 0:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"detections/detect_{timestamp}.jpg"
            cv2.imwrite(filename, frame)

        cv2.imshow("Live CCTV", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

    return results_list