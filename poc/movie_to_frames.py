import os
import shutil
from pathlib import Path
import click
import cv2

from opencv_tools.camera import frame_capture_gen


@click.command()
@click.option("--movie_path")
@click.option("--output_directory", default="output")
@click.option("--image_extension", default="jpg")
def main(movie_path, output_directory, image_extension):
    movie_path = Path(movie_path)
    movie_name = movie_path.stem
    output_directory = Path(output_directory).joinpath(movie_name)

    if output_directory.exists():
        shutil.rmtree(output_directory)
    os.mkdir(output_directory)

    print(movie_path, output_directory)

    count = 0
    for frame in frame_capture_gen(str(movie_path)):
        file_name = f"frame_{count}.{image_extension}"
        file_path = Path(output_directory).joinpath(file_name)

        cv2.imwrite(str(file_path), frame)
        count = count + 1

        if count % 50 == 0:
            print(f"processed: {count}")


if __name__ == '__main__':
    main()
