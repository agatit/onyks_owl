import cv2 as cv
import torch


class YoloDetector:
    interesting_labels_table = ["vertical_text", "horizontal_tex", "container_corners", "container", "railcar_boogie",
                                "railcar_text", "railcar_gap"]

    def __init__(self, model_path):
        self.model_path = model_path

        model, classes, device = self.initialize_model(self.model_path)
        self.model = model
        self.classes = classes
        self.device = device


    @staticmethod
    def initialize_model(model_path):
        model = torch.hub.load('ultralytics/yolov5', 'custom', path=model_path)
        classes = model.names
        device = 'cuda' if torch.cuda.is_available() else 'cpu'

        model.to(device)

        return model, classes, device

    def detect_image(self, image):
        model = self.model
        detection_result = model(image)

        # output format
        cols = ["name", "ymin", "ymax", "xmin", "xmax"]
        results_df = detection_result.pandas().xyxy[0]
        results_df = results_df[cols]

        # filter interesting labels
        results_df = results_df[results_df["name"].isin(self.interesting_labels_table)]

        # float to int
        numeric_cols_labels = cols[1:]
        for label in numeric_cols_labels:
            results_df[label] = results_df[label].astype(int)

        return results_df.values.tolist()
