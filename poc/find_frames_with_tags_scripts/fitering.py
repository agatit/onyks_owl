from typing import Callable

import numpy as np
import torch
from torchvision import transforms

SIMILARITY_DIFF_RATIO = 21.3
SIMILARITY_CONV_THRESHOLD = 1700


def filter_batch(batch: list[np.ndarray], similarity_fun: Callable[[np.ndarray, np.ndarray], bool]) -> list[np.ndarray]:
    if len(batch) < 1:
        return batch

    new_batch = []
    src_frame = None
    for current_frame in batch:
        if not similarity_fun(src_frame, current_frame):
            new_batch.append(current_frame)
            src_frame = current_frame

    return new_batch


def similarity_diff(img_1: np.ndarray, img_2: np.ndarray) -> bool:
    if img_1 is None:
        return False

    difference_array = img_1 - img_2
    square_difference_array = np.square(difference_array)
    similarity = square_difference_array.sum()

    height, width, _ = img_1.shape
    similarity /= width * height

    similarity_threshold = width / SIMILARITY_DIFF_RATIO

    return similarity > similarity_threshold


def similarity_conv(image1: np.ndarray, image2: np.ndarray, model, device) -> float:
    if image1 is None:
        return False

    # Convert the images to tensors
    image1_tensor = transforms.ToTensor()(image1).to(device)
    image2_tensor = transforms.ToTensor()(image2).to(device)

    # Add a fourth dimension for the batch and extract the features
    features1 = model.extract_features(image1_tensor.unsqueeze(0))["features"]
    features2 = model.extract_features(image2_tensor.unsqueeze(0))["features"]

    # Calculate the Euclidean distance of the features
    value = round(np.linalg.norm(
        np.array(features1.detach().to(torch.device("cpu"))) - np.array(features2.detach().to(torch.device("cpu")))), 4)

    # if value > then threshold then are different
    return value > SIMILARITY_CONV_THRESHOLD

