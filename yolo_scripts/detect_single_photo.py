import cv2

from yolo.yolo_detector import YoloDetector
from src.opencv_tools.image_transformations import show_image_with_rectangles

if __name__ == '__main__':
    # print(torch.cuda.get_arch_list())
    # print(torch.version.cuda)
    # print(torch.cuda.is_available())

    model_path = "models/l_owl_4.pt"
    image_path = "test_images/chojny/owl_dataset (1008).jpg"
    print(model_path, image_path)

    detector = YoloDetector(model_path)

    image = cv2.imread(image_path)
    found_bounding_boxes = detector.detect_image(image)
    print(found_bounding_boxes)

    show_image_with_rectangles(image_path, found_bounding_boxes)

    # model, classes, device = detection.initialize_model(model_path)
    # print(detection.find_object_in_photo(img, model, classes, device, interesting_labels_table))
