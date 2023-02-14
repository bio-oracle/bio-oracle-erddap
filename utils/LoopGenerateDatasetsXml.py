#!/usr/bin/env python

"""
This script loops over the datasets in the /data/layers/ directory and runs the GenerateDatasetsXml.sh
script.
"""

import argparse
from glob import glob
from shutil import copyfile
import subprocess

from tqdm import tqdm
from CollateGenerateDatasetsXml import main as collate


def main(args):
    layers = glob(args.glob_string)

    if include := args.include:
        include = include.split(",")
        layers = [layer for layer in layers if any([string in layer for string in include])]

    if exclude := args.exclude:
        exclude = exclude.split(",")
        layers = [layer for layer in layers if not any([string in layer for string in include])]

    print(f"Found {len(layers)} layers.")
    print(f"Processing layers with GenerateDatasetsXml.sh. Files will be created in the 'logs/datasets' directory.")
    for layer in tqdm(layers):
        layer_basename = layer.split("/")[-2].rstrip("/")
        layer_dir = "/".join(layer.split("/")[:-1])
        filename = layer.split("/")[-1][:-3]
        cmd = process_layer(layer_dir, filename).split()
        if not args.dry_run:
            p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            stdout, stderr = p.communicate()
            with open(f"logs/datasets/logs/{layer_basename}_{filename}_stdout.log", "w") as f:
                f.write("stdout:\n")
                f.write(stdout.decode())
                f.write("stderr:\n")
                f.write(stderr.decode())
            outfile_xml = "logs/datasets/" + layer_basename + "_" + filename + ".xml"
            copyfile("logs/GenerateDatasetsXml.out", outfile_xml)
        else:
            print(cmd)
    if (not args.skip_collate) and (not args.dry_run):
        print("Finished generating XMLs. Collating.")
        collate()
        print("All done.")


def process_layer(layer_dir, filename):
    layer_dir = layer_dir.replace("/data/layers", "/datasets")
    cmd = f"./GenerateDatasetsXml.sh EDDGridFromNcFiles {layer_dir} {filename}.nc {layer_dir}/{filename}.nc nothing nothing nothing nothing"
    return cmd


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Loop over datasets in the /data/layers directory and run the GenerateDatasetsXml.sh script.")
    parser.add_argument("-i", "--include", help="INCLUDE strings, comma-separated. Only include datasets that contain these strings in their ID.", default=None, required=False)
    parser.add_argument("-e", "--exclude", help="EXCLUDE strings, comma-separated. Exclude datasets that contain these strings in their ID.", default=None, required=False)
    parser.add_argument("-g", "--glob-string", help="Glob string to be used to look for files.", default="/data/layers/*/*.nc", required=False)
    parser.add_argument("--skip-collate", help="Only generate the XML snippets, don't collate them with the CollateGenerateDatasetsXml.py script.", action="store_true", required=False)
    parser.add_argument("--dry-run", help="Only print the GenerateDatasetsXml.sh command and don't run anything.", action="store_true", required=False)
    args = parser.parse_args()
    main(args)
