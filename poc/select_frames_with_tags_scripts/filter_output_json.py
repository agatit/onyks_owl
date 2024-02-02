def filter_output_json(output_json, filter_config):
    for dataset_name, frames in output_json.items():
        last_label_occurrence = {label: 0 for label in filter_config["labels"]}
        step = filter_config["step"]
        confidence_threshold = filter_config["confidence_threshold"]

        def filter_output_json_wrapper(frame: dict):
            return filter_output_json_frames(frame, last_label_occurrence, step, confidence_threshold)

        output_json[dataset_name] = list(filter(filter_output_json_wrapper, frames))


def filter_output_json_frames(frame: dict, last_label_occurrence: dict, step: int, confidence_threshold: float):
    class_name = frame["detection_result"]["class_name"]
    confidence = frame["detection_result"]["confidence"]
    frame_number = frame["frame_number"]

    if class_name not in last_label_occurrence.keys():
        return False

    if confidence < confidence_threshold:
        return False

    last_occurrence = last_label_occurrence[class_name]
    current_occurrence = frame_number

    passed_frames_number = abs(last_occurrence - current_occurrence)
    if 0 < passed_frames_number < step:
        return False
    else:
        last_label_occurrence[class_name] = current_occurrence
        return True
