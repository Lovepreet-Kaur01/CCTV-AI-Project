import cv2
from ultralytics import YOLO
import os
from datetime import datetime

# Load YOLOv8 model
model = YOLO("yolov8n.pt")


# VIDEO FILE DETECTION
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

        cv2.imshow("Video Detection", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()

    cv2.destroyAllWindows()

    return results_list


# LIVE CAMERA DETECTION
def live_detection():

    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

    if not cap.isOpened():

        print("Camera not opening")

        return []

    results_list = []

    os.makedirs("detections", exist_ok=True)

    while True:

        ret, frame = cap.read()

        if not ret:

            print("Failed to capture frame")

            break

        current_time = datetime.now().strftime(
            "%d-%m-%Y %I:%M:%S %p"
        )

        results = model(frame)

        person_count = 0

        for r in results:

            for box in r.boxes:

                cls = int(box.cls[0])

                label = model.names[cls]

                if label == "person":

                    person_count += 1

                    x1, y1, x2, y2 = map(
                        int,
                        box.xyxy[0]
                    )

                    cv2.rectangle(
                        frame,
                        (x1, y1),
                        (x2, y2),
                        (0, 255, 0),
                        2
                    )

                    cv2.putText(
                        frame,
                        "Person",
                        (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.7,
                        (0, 255, 0),
                        2
                    )

                    results_list.append(label)

        cv2.putText(
            frame,
            f"Persons: {person_count}",
            (20, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (255, 0, 0),
            2
        )

        if person_count > 2:

            cv2.putText(
                frame,
                "ALERT: Too many people!",
                (20, 80),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 0, 255),
                3
            )

        cv2.putText(
            frame,
            current_time,
            (20, 120),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (255, 255, 255),
            2
        )

        if person_count > 0:

            timestamp = datetime.now().strftime(
                "%Y%m%d_%H%M%S"
            )

            filename = (
                f"detections/person_{timestamp}.jpg"
            )

            cv2.imwrite(filename, frame)

        cv2.imshow(
            "AI CCTV Surveillance",
            frame
        )

        if cv2.waitKey(1) & 0xFF == ord('q'):

            break

    cap.release()

    cv2.destroyAllWindows()

    return results_list