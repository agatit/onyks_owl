import glob
from itertools import product
from pathlib import Path

import click
import yaml
from mmocr.apis import MMOCRInferencer
from tqdm import tqdm

from io_utils.utils import make_clean_dir


@click.command()
@click.option("-in", "--input", "input_dir",
              required=True, type=click.Path(exists=True, dir_okay=True),
              help="select directory with movies_paths")
@click.option("-out", "--output", "output_dir",
              required=True, type=click.Path(),
              help="select output directory for measurements")
@click.option("-c", "--config", "config_path", type=click.Path(exists=True, file_okay=True),
              required=True, default="resources/find_frames_with_tags.yaml", help="yaml config path")
def main(input_dir, output_dir, config_path):
    input_dir = Path(input_dir)
    output_dir = Path(output_dir)

    make_clean_dir(output_dir)

    with open(config_path) as f:
        config = yaml.load(f, Loader=yaml.FullLoader)

    glob_mask = f"*{config['extension']}"
    images = glob.glob(str(input_dir / glob_mask))
    images = [Path(i) for i in images]

    for det, rec in tqdm(product(config["detection"], config["recognition"])):
        try:
            inferencer = MMOCRInferencer(det=det, rec=rec)

            current_output_path = output_dir / f"{det}_{rec}"
            results = {}
            for image in images:
                results[image.stem] = inferencer(str(image),
                                                 out_dir=str(current_output_path),
                                                 save_pred=True,
                                                 save_vis=True)
                # results[image.stem] = inferencer(str(image), show=True)

            with open(output_dir / f"{det}_{rec}.json", "w") as file:
                yaml.dump(results, file)
        except Exception as e:
            print(e)
            continue


if __name__ == '__main__':
    main()
