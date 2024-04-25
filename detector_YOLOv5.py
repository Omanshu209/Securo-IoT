MODEL = 0 # {0, 1}
MODELS = ["yolov5s.pt", "yolov5s_package_detection.pt"]

import cv2
import torch.hub as hub
import numpy as np

yolo = hub.load(
	"ultralytics/yolov5", 
	"custom", 
	path = f"YOLOv5/{MODELS[MODEL]}"
)

cap = cv2.VideoCapture(0)

while True:
	ret, frame = cap.read()
	img = np.array(frame)
	results = yolo(img)
	cv2.imshow(f"YOLOv5 - {MODELS[MODEL]}", np.squeeze(results.render()))
	
	if cv2.waitKey(1) & 0xFF == ord("q"):
		break

cap.release()
cv2.destroyAllWindows()
