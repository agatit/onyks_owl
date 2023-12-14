import cv2


def draw_image_with_rectangles(image, boxes):
    for box in boxes:
        text = box[0]
        coordinates = box[1:]
        y1, y2, x1, x2 = coordinates
        cv2.rectangle(image, (x1, y1), (x2, y2), (0, 0, 255), 2)

        padding = 10
        cv2.putText(image, text, (x1, y1 - padding), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 255), 2)
    return image


def show_image_with_rectangles(image_path, boxes, text=""):
    image = cv2.imread(image_path)
    # image = cv2.resize(image, (640, 640))

    image = draw_image_with_rectangles(image, boxes)
    image = cv2.resize(image, (860, 640))
    cv2.imshow(image_path, image)

    cv2.waitKey(0)
    cv2.destroyAllWindows()
