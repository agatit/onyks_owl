import click

import itertools

import yaml
from ultralytics import YOLO


@click.command(context_settings=dict(
    ignore_unknown_options=True,
    allow_extra_args=True,
))
@click.option("-tc", "--train_config", "train_config",
              required=True, type=click.Path(exists=True),
              help="path to train yolo config")
@click.option("-w", "--weights", "weights",
              required=True, type=str,
              help=".pt file with weights")
@click.pass_context
def main(context, train_config, weights):
    with open(train_config) as f:
        train_config = yaml.load(f, Loader=yaml.FullLoader)

    training_args = train_config["training"]
    augmentation = train_config["augmentation"]
    kwargs = pair_list_to_dict(context.args)

    model = YOLO(weights)

    model.train(**augmentation, **training_args, **kwargs)


def pair_list_to_dict(_list: list):
    pairs = itertools.zip_longest(*[iter(_list)] * 2, fillvalue=None)
    dct = {key.replace("-", ""): value for key, value in pairs}
    return dct


if __name__ == '__main__':
    main()
