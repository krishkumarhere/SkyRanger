import cv2
from ultralytics import YOLO

# Load the YOLOv8n model (pretrained on COCO dataset)
model = YOLO("yolov8n.pt")

# Open webcam (0 = default laptop cam)
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Run YOLOv8 detection
    results = model(frame)

    # Plot results on frame
    annotated_frame = results[0].plot()

    # Show in window
    cv2.imshow("YOLOv8 Live Detection", annotated_frame)

    # Break if 'q' key pressed
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
import cv2
from ultralytics import YOLO

# Load the YOLOv8n model (pretrained on COCO dataset)
model = YOLO("yolov8n.pt")

# Open webcam (0 = default laptop cam)
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Run YOLOv8 detection
    results = model(frame)

    # Plot results on frame
    annotated_frame = results[0].plot()

    # Show in window
    cv2.imshow("YOLOv8 Live Detection", annotated_frame)

    # Break if 'q' key pressed
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
