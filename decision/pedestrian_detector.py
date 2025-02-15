import cv2
import numpy as np

# Update these paths as needed (ensure they point to the correct files)
YOLO_CONFIG_PATH = "decision/yolo/yolov3.cfg"
YOLO_WEIGHTS_PATH = "decision/yolo/yolov3.weights"
YOLO_CLASSES_PATH = "decision/yolo/coco.names"

# Load the COCO class labels
with open(YOLO_CLASSES_PATH, "r") as f:
    classes = [line.strip() for line in f.readlines()]

# In the COCO dataset, the "person" class is usually the first one (index 0)
PERSON_CLASS_ID = classes.index("person") if "person" in classes else 0

# Load the YOLO network
net = cv2.dnn.readNetFromDarknet(YOLO_CONFIG_PATH, YOLO_WEIGHTS_PATH)
net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
net.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)

def detect_pedestrians(image, conf_threshold=0.5, nms_threshold=0.4):
    (H, W) = image.shape[:2]
    # Get the output layer names
    layer_names = net.getLayerNames()
    unconnected_out_layers = net.getUnconnectedOutLayers()
    
    # Check if the output is a list of integers or a list of lists/arrays.
    if isinstance(unconnected_out_layers[0], (np.int32, int)):
        ln = [layer_names[i - 1] for i in unconnected_out_layers]
    else:
        ln = [layer_names[i[0] - 1] for i in unconnected_out_layers]

    # Create a blob from the input image and perform a forward pass
    blob = cv2.dnn.blobFromImage(image, 1/255.0, (416, 416), swapRB=True, crop=False)
    net.setInput(blob)
    layer_outputs = net.forward(ln)

    boxes = []
    confidences = []

    for output in layer_outputs:
        for detection in output:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if class_id == PERSON_CLASS_ID and confidence > conf_threshold:
                # Scale the bounding box coordinates back to the image size
                box = detection[0:4] * np.array([W, H, W, H])
                (centerX, centerY, width, height) = box.astype("int")
                x = int(centerX - (width / 2))
                y = int(centerY - (height / 2))
                boxes.append([x, y, int(width), int(height)])
                confidences.append(float(confidence))

    # Apply non-maxima suppression to filter overlapping boxes
    idxs = cv2.dnn.NMSBoxes(boxes, confidences, conf_threshold, nms_threshold)
    detections = []
    if len(idxs) > 0:
        for i in idxs.flatten():
            detections.append({
                "bbox": boxes[i],
                "confidence": confidences[i]
            })
    return detections


def pedestrian_in_path(detections, image_width, central_fraction=1.0):
    """
    Determines if any detected pedestrian is in the center of the image.
    The central_fraction defines what fraction of the image width is considered "in-path."
    """
    print("I am called")
    if not detections:
        return False

    center_x_min = int((1 - central_fraction) / 2 * image_width)
    center_x_max = int((1 + central_fraction) / 2 * image_width)

    for detection in detections:
        x, y, w, h = detection["bbox"]
        bbox_center_x = x + w // 2
        if center_x_min <= bbox_center_x <= center_x_max:
            print(f"Pedestrian detected in path with center x: {bbox_center_x}")
            return True
    return False
