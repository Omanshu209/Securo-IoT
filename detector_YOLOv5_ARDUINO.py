import pathlib
pathlib.PosixPath = pathlib.WindowsPath

MODEL = 0 # {0, 1}
ARDUINO = False
MODELS = ["yolov5s.pt", "yolov5s_package_detection.pt"]

if MODEL != 0 and ARDUINO:
	import serial
	PORT = "COM6"
	BAUDRATE = 9600
	arduino = serial.Serial(port = PORT, baudrate = BAUDRATE, timeout = 1)

import cv2
import torch.hub as hub
import numpy as np

import time

yolo = hub.load(
	"ultralytics/yolov5", 
	"custom", 
	path = f"YOLOv5/{MODELS[MODEL]}"
)

if MODEL == 1:
	yolo.conf = 0.8

def send_data(number):
	if MODEL != 0 and ARDUINO:
		arduino.write(bytes(str(number), "utf-8"))

cap = cv2.VideoCapture(1)

while True:
	ret, frame = cap.read()
	img = np.array(frame)
	results = yolo(img)
	cv2.imshow(f"YOLOv5 - {MODELS[MODEL]}", np.squeeze(results.render()))

	if MODEL != 0 and len(results.xyxy[0]) > 0:
		send_data(8)
		time.sleep(5)
	
	if cv2.waitKey(1) & 0xFF == ord("q"):
		break

cap.release()
cv2.destroyAllWindows()
