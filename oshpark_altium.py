#!/usr/bin/python3
import argparse
import datetime
import os
import zipfile


# Layer, outline, solder mask
EXPECTED_BOTTOM = (".gbl", ".gbo", ".gbs")
EXPECTED_TOP = (".gtl", ".gto", ".gts")
EXPECTED = EXPECTED_TOP + EXPECTED_BOTTOM

OUTLINE = (".gm17")

def is_xln_file(path: str) -> bool:
    assert os.path.exists(path), "Path does not exist:" + path
    contents = open(path).read()
    return contents.startswith("M48")

now = datetime.datetime.now()
default_name = now.strftime("export-%Y%m%d_%h%m%s.zip")

parser = argparse.ArgumentParser(
    description="A utility to take the default exports from altium to the oshpark expected format")
parser.add_argument("--folder", help="The folder to inspect", required=True)
parser.add_argument("--output", help="The name of the output file", default=default_name)
args = parser.parse_args()

assert os.path.isdir(args.folder), "Input folder does not exist:" + args.folder
z = zipfile.ZipFile(args.output, "w", zipfile.ZIP_DEFLATED)


def write_and_note(path: str, dest: str):
    print("\t{} --> Zip({})".format(path, dest))
    z.write(path, dest)

for fname in sorted(os.listdir(args.folder)):
    fpath = os.path.join(args.folder, fname)
    if not os.path.isfile(fpath):
        continue

    prefix, extension = os.path.splitext(fname)
    
    if extension.lower() in EXPECTED:
        write_and_note(fpath, fname)
    
    if extension.lower() in OUTLINE:
        write_and_note(fpath, prefix + ".GKO")

    if extension.lower() == ".txt" and is_xln_file(fpath):
        write_and_note(fpath, prefix + ".XLN")

z.close()
