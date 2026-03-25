import cv2
from ultralytics import YOLO

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


# 🔹 LIVE CAMERA DETECTION
def live_detection():
    cap = cv2.VideoCapture(0)

    results_list = []

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        results = model(frame)

        for r in results:
            for box in r.boxes:
                cls = int(box.cls[0])
                label = model.names[cls]

                results_list.append(label)

                x1, y1, x2, y2 = map(int, box.xyxy[0])
                cv2.rectangle(frame, (x1,y1), (x2,y2), (0,255,0), 2)
                cv2.putText(frame, label, (x1,y1-10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,255,0), 2)

        cv2.imshow("Live CCTV", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

    return results_list