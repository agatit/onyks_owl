import click
import cv2


@click.command()
@click.option("-in", "--input", "input_movie",
              required=True, type=click.Path(exists=True, file_okay=True),
              help="path to movie")
@click.option("-s", "--stop", "stop_frame",
              type=int, default=-1,
              help="number of stop frame")
def main(input_movie, stop_frame):
    cap = cv2.VideoCapture(input_movie)

    fps = int(cap.get(cv2.CAP_PROP_FPS))
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    # fourcc = int(cap.get(cv2.CAP_PROP_FOURCC))
    fourcc = cv2.VideoWriter_fourcc(*"MJPG")

    frames = 0
    calc_timestamp = 0

    while cap.isOpened():
        frame_exists, curr_frame = cap.read()
        if frame_exists:
            timestamp = cap.get(cv2.CAP_PROP_POS_MSEC) / 1000
            calc_timestamp += 1 / fps

            print(f"{frames:05d}: {timestamp - calc_timestamp:.2f}")
            frames += 1
        else:
            break

        if frames > stop_frame:
            break

        resized_frame = cv2.resize(curr_frame, (width // 2, height // 2))
        cv2.imshow("f", resized_frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()


if __name__ == '__main__':
    main()
