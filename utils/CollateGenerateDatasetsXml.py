#!/usr/bin/env python

from datetime import datetime
from glob import glob
from pathlib import Path
from shutil import copyfile
import xml.etree.ElementTree as ET

from tqdm import tqdm


def main():
    main_xml = "./erddap/content/datasets_template.xml"
    xml_snips = glob("./logs/loop/*.xml")

    main_tree = ET.parse(main_xml)
    main_root = main_tree.getroot()

    for xml in tqdm(xml_snips):
        try:
            snip_tree = ET.parse(xml)
            snip_root = snip_tree.getroot()
            main_root.append(snip_root)
        except ET.ParseError:  # for empty files
            pass

    datasets_file = "./erddap/content/datasets.xml"

    backup = lambda file: copyfile(file, Path("./erddap/content/history/").joinpath(datetime.now().strftime("%Y-%m-%d-%T") + "." + str(Path(file.name))))
    
    # Back up the old file
    backup(datasets_file)

    # Write the new file
    main_tree.write(datasets_file, encoding="utf-8")

    xml_string = '<?xml version="1.0" encoding="ISO-8859-1" ?>'

    with open(datasets_file, "r+") as f:
        r = f.read()
        f.seek(0, 0)
        f.write(xml_string + "\n")
        f.write(r)

    # Back up the new file
    backup(datasets_file)

if __name__ == "__main__":
    main()
