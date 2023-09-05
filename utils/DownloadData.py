#!/usr/bin/env python

"""
Downloads data from the Bio-ORACLE server using pyo-oracle.
"""

import argparse
import pyo_oracle as pyo


def main(args):
    layers = pyo.list_layers(time_period="present", depth="surf", dataframe=False)
    print(f"Layers to be downloaded:\n{'\n'.join(layers)}.")
    pyo.download_layers(
        layers,
        args.outdir,
        skip_confirmation=True,
        timestamp=False,
        log=False,
        timeout=600,
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Download data from the Bio-ORACLE server using pyo-oracle."
    )
    parser.add_argument("-o", "--outdir", type=str, help="Output directory.")
    args = parser.parse_args()
    main(args)
