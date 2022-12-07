from imageai.Detection import ObjectDetection
import tensorflow as tf

detector = ObjectDetection()

model_path = "./models/yolo-tiny.h5"
input_path = "./input/maptest.png"
output_path = "./output/newimage.jpg"

detector.setModelTypeAsTinyYOLOv3()

detector.setModelPath(model_path)
detector.loadModel()

detection = detector.detectObjectsFromImage(input_image = input_path, output_image_path = output_path)

for item in detection:
    print(item["name"] , " : ", item["percentage_probability"])


