import click
import cv2

from image_event_handler import ImageEventHandler


@click.command()
@click.argument("file_path")
def main(file_path):
    image = cv2.imread(file_path)
    window_name = "image"
    image_event_handler = ImageEventHandler(image, window_name)

    cv2.imshow(window_name, image)
    cv2.setMouseCallback('image', image_event_handler.mouse_callback())

    while True:
        key = cv2.waitKey(0)

        if key == 32:
            image_event_handler.reload_image()

        if key == 27:
            break

    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
