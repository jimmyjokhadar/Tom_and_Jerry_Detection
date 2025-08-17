import cv2
import base64
import numpy as np
from ultralytics import YOLO

class TomJerryDetector:
    def __init__(self):
        print("Loading Tom & Jerry YOLO model...")
        self.model = YOLO("model/tomjerry_yolo11.pt")  # path to your trained YOLO weights
        print("Model loaded successfully.")

    def draw_boxes(self, img, detections):
        """
        Draw bounding boxes + labels on the image.
        detections = list of dicts like:
        [{"box": [x1,y1,x2,y2], "label": "Tom", "score": 0.95}, ...]
        """
        for det in detections:
            x1, y1, x2, y2 = det["box"]
            label, score = det["label"], det["score"]

            cv2.rectangle(img, (x1, y1), (x2, y2), (0,255,0), 2)
            cv2.putText(img, f"{label} {score:.2f}", (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,255,0), 2)
        return img

    def detect_objects(self, image_bytes, max_size=800):
        # Decode uploaded image
        img = cv2.imdecode(np.frombuffer(image_bytes, np.uint8), cv2.IMREAD_COLOR)

        results = self.model(img)
        detections = []

        for r in results[0].boxes:
            x1, y1, x2, y2 = map(int, r.xyxy[0])
            cls = int(r.cls[0])
            score = float(r.conf[0])
            label = self.model.names[cls]
            if score > 0.7:

                detections.append({
                    "box": [x1, y1, x2, y2],
                    "label": label,
                    "score": score
                })

        # Draw boxes
        img_with_boxes = self.draw_boxes(img.copy(), detections)

        # 🔹 Resize image BEFORE encoding (keep aspect ratio)
        h, w = img_with_boxes.shape[:2]
        if max(h, w) > max_size:
            scale = max_size / max(h, w)
            new_w, new_h = int(w * scale), int(h * scale)
            img_with_boxes = cv2.resize(img_with_boxes, (new_w, new_h), interpolation=cv2.INTER_AREA)

        # Encode to base64 for frontend
        _, buffer = cv2.imencode(".jpg", img_with_boxes)
        img_base64 = base64.b64encode(buffer).decode("utf-8")

        return {
            "detections": detections,
            "labels": [d["label"] for d in detections],
            "scores": [d["score"] for d in detections],
            "image": img_base64
        }
