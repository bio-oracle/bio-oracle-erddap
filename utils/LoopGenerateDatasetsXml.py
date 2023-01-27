#!/usr/bin/env python

from glob import glob
from shutil import copyfile
import subprocess

from tqdm import tqdm
from CollateGenerateDatasetsXml import main as collate


def main():
    layers = glob("/data/layers/*/")

    print(f"Found {len(layers)} layers.")
    print(f"Processing layers. Files will be created in the 'logs/datasets' directory.")
    for layer in tqdm(layers):
        layer_basename = layer.split("/")[-2].rstrip("/")
        p = subprocess.Popen(process_layer(layer).split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = p.communicate()
        with open(f"logs/datasets/logs/{layer_basename}_stdout.log", "w") as f:
            f.write("stdout:\n")
            f.write(stdout.decode())
            f.write("stderr:\n")
            f.write(stderr.decode())
        outfile_xml = "logs/datasets/" + layer_basename + ".xml"
        copyfile("logs/GenerateDatasetsXml.out", outfile_xml)


def process_layer(layer):
    layer = layer.replace("/data/layers", "/datasets")
    cmd = f"./GenerateDatasetsXml.sh EDDGridFromNcFiles {layer} climatologydecadedepthsurf.nc {layer}climatologydecadedepthsurf.nc nothing nothing nothing nothing"
    return cmd


if __name__ == "__main__":
    main()
    print("Finished generating XMLs. Collating.")
    collate()
    print("All done.")
