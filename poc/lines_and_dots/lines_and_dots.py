import click
import cv2

image = None
WINDOW_NAME = "image"


def mouse_click(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        put_text_kwargs = {
            "img": image,
            "text": f"left:{(x, y)}",
            "org": (x, y),
            "fontFace": cv2.FONT_HERSHEY_SIMPLEX,
            "fontScale": 2,
            "color": (255, 0, 0)
        }

        cv2.putText(**put_text_kwargs)
        cv2.imshow(WINDOW_NAME, image)

    # if event == cv2.EVENT_RBUTTONDOWN:
    #     cv2.imshow(WINDOW_NAME, image)


@click.command()
@click.argument("file_path")
def main(file_path):
    global image
    image = cv2.imread(file_path)

    cv2.imshow(WINDOW_NAME, image)
    cv2.setMouseCallback('image', mouse_click)

    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()