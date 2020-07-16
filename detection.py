# source https://www.learnopencv.com/faster-r-cnn-object-detection-with-pytorch/

import torchvision
import torchvision.transforms as T
import torch
import cv2
import matplotlib.pyplot as plt
from PIL import Image
import glob
import os
import threading
from multiprocessing import Pool
from torchvision import transforms
model = torchvision.models.mobilenet_v2(pretrained=True)

model.eval()

# define the objects that we can detect
classes  = [
    '__background__', 'person', 'bicycle', 'car', 'motorcycle', 'airplane', 'bus',
    'train', 'truck', 'boat', 'traffic light', 'fire hydrant', 'N/A', 'stop sign',
    'parking meter', 'bench', 'bird', 'cat', 'dog', 'horse', 'sheep', 'cow',
    'elephant', 'bear', 'zebra', 'giraffe', 'N/A', 'backpack', 'umbrella', 'N/A', 'N/A',
    'handbag', 'tie', 'suitcase', 'frisbee', 'skis', 'snowboard', 'sports ball',
    'kite', 'baseball bat', 'baseball glove', 'skateboard', 'surfboard', 'tennis racket',
    'bottle', 'N/A', 'wine glass', 'cup', 'fork', 'knife', 'spoon', 'bowl',
    'banana', 'apple', 'sandwich', 'orange', 'broccoli', 'carrot', 'hot dog', 'pizza',
    'donut', 'cake', 'chair', 'couch', 'potted plant', 'bed', 'N/A', 'dining table',
    'N/A', 'N/A', 'toilet', 'N/A', 'tv', 'laptop', 'mouse', 'remote', 'keyboard', 'cell phone',
    'microwave', 'oven', 'toaster', 'sink', 'refrigerator', 'N/A', 'book',
    'clock', 'vase', 'scissors', 'teddy bear', 'hair drier', 'toothbrush'
]

# Defing PyTorch Transform
preprocess = transforms.Compose([
	transforms.Resize(256),
	transforms.CenterCrop(224),
	transforms.ToTensor(),
	transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
])
	

def get_prediction(frame, threshold):
	img = Image.fromarray(frame)
	img = preprocess(img) # Apply the transform to the images
	img = img.unsqueeze(0)
	pred = model(img) # Pass the image to the model
	_, indices = torch.sort(pred, descending=True)
	print(indices[0][:1])
	#print(str(idx) + ' ' for idx in indices[0][:5])
	#preds = [(classes[idx], percentage[idx].item()) for idx in indices[0][:5]]
	#pred_boxes = pred_boxes[:pred_t+1]
	#pred_class = pred_class[:pred_t+1]
	return None, None



def detect_frame(frame, threshold=0.5, rect_th=1, text_size=1, text_th=1):
	boxes, pred_cls = get_prediction(frame, threshold) # Get predictions
	img = frame # Read image with cv2
	#img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB) # Convert to RGB
	if boxes != None:
		for i in range(len(boxes)):
			cv2.rectangle(img, boxes[i][0], boxes[i][1],color=(0, 255, 0), thickness=rect_th) # Draw Rectangle with the coordinates
		cv2.putText(img,pred_cls[i], boxes[i][0],  cv2.FONT_HERSHEY_SIMPLEX, text_size, (0,255,0),thickness=text_th) # Write the prediction class
	return img	


def object_detection(frame, filename, threshold=0.5, rect_th=1, text_size=1, text_th=1):
	boxes, pred_cls = get_prediction(frame, threshold) # Get predictions
	img = frame # Read image with cv2
	#img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB) # Convert to RGB
	for i in range(len(boxes)):
		cv2.rectangle(img, boxes[i][0], boxes[i][1],color=(0, 255, 0), thickness=rect_th) # Draw Rectangle with the coordinates
		cv2.putText(img,pred_cls[i], boxes[i][0],  cv2.FONT_HERSHEY_SIMPLEX, text_size, (0,255,0),thickness=text_th) # Write the prediction class
	plt.figure(figsize=(20,30)) # display the output image
	plt.imshow(img)
	plt.xticks([])
	plt.yticks([])
	plt.show()
	write_detection(plt, filename)

def write_detection(plt, filename):
	plt.savefig(filename)


def object_detection_by_frame(filename, threshold=0.7, rect_th=2, text_size=2, text_th=2):
	img = cv2.imread(filename)
	boxes, pred_cls = get_prediction(filename, threshold)

	img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
	if boxes != -1 or pred_cls != -1:
		for i in range(len(boxes)):
			cv2.rectangle(img, boxes[i][0], boxes[i][1], color = (0, 255, 0), thickness = rect_th)
			cv2.putText(img, pred_cls[i], boxes[i][0], cv2.FONT_HERSHEY_SIMPLEX, text_size, (0, 255, 0), thickness = text_th)

	plt.figure(figsize=(16,9))
	plt.imshow(img)
	return plt


def detect_all_frames(input, output):
	i = 0
	for filename in sorted(glob.glob(input + '/*.jpg'), key = os.path.getmtime):
		print(filename)
		plt = object_detection_by_frame(filename)
		write_detection(plt, output + '/frame' + str(i) + '.jpg')
		i += 1
		plt.close()


# detectes and writes to 'detected_output' directory
def detect_and_write(filename):
	print('detecting: ' , filename)
	plt = object_detection_by_frame(filename)
	write_detection(plt, filename)
	plt.close()
	print('detection complete: ' , filename)

def threaded_detection(inputDir, outputDir):
	i = 0
	pool = Pool(processes = 1)
	files = sorted(glob.glob(inputDir + '/*.jpg'), key = os.path.getmtime)
	pool.map(detect_and_write, files)
