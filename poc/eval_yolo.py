import itertools
from pathlib import Path

import click
from ultralytics import YOLO


@click.command(context_settings=dict(
    ignore_unknown_options=True,
    allow_extra_args=True,
))
@click.option("-m", "--model", "model_path",
              required=True, type=click.Path(), help="https://docs.ultralytics.com/usage/cfg/")
@click.pass_context
def main(context, model_path):
    model_path = Path(model_path)
    kwargs = pair_list_to_dict(context.args)

    model = YOLO(model_path)
    det_metrics = model.val(**kwargs)

    pass


def pair_list_to_dict(_list: list):
    pairs = itertools.zip_longest(*[iter(_list)] * 2, fillvalue=None)
    dct = {key.replace("-", ""): value for key, value in pairs}
    return dct


if __name__ == '__main__':
    main()
