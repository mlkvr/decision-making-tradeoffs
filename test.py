import cv2
from decision.pedestrian_detector import detect_pedestrians, pedestrian_in_path

image = cv2.imread("camera_outputs/simulation_20250202_232711/frame_000164.png")
detections = detect_pedestrians(image, conf_threshold=0.3)  # Lower threshold for testing
print(detections)
print("Pedestrian in path?", pedestrian_in_path(detections, image.shape[1], central_fraction=1.0))
cv2.imshow("Test", image)
cv2.waitKey(0)
cv2.destroyAllWindows()
