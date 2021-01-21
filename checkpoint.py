#!/usr/bin/env python
"""
Continuously increment an integer value in "foo" and "scores.yaml". Initial value will be read
from "start" parameter. After each iteration, a DVC checkpoint will be created.
"""

import os

from ruamel.yaml import YAML

from dvc.api import make_checkpoint


EPOCHS=2


def main():
    output_file = "foo"
    metrics_file = "scores.yaml"
    yaml = YAML()

    with open("params.yaml") as fobj:
        params = yaml.load(fobj)
    start = params.get("start", 0)
    alpha = params["alpha"]

    for e in range(EPOCHS):
        if os.path.exists(output_file):
            with open(output_file, "r") as fobj:
                try:
                    data = fobj.read()
                    iter_ = int(data) + 1
                except ValueError:
                    iter_ = start
        else:
            iter_ = start

        with open(output_file, "w") as fobj:
            fobj.write(f"{iter_}")
        with open(metrics_file, "w") as fobj:
            yaml.dump({"epoch": iter_}, fobj)

        make_checkpoint()


if __name__ == "__main__":
    main()
