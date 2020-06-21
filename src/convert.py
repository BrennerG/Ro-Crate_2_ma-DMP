import sys
import json
from dmp2ro import RO_Crate_constructor
from ro2dmp import DMP_Constructor

if len(sys.argv) == 2:
    in_PATH = sys.argv[1]
    out_PATH = "ro-crate-metadata.jsonld"
elif len(sys.argv) == 3:
    in_PATH = sys.argv[1]
    out_PATH = sys.argv[2]
else:
    print("Please provide input and output file")
    exit(0)

if in_PATH.endswith("json"):
    RCC = RO_Crate_constructor(in_PATH)
    RCC.construct()
    RCC.write(out_PATH)
elif in_PATH.endswith("jsonld"):
    DC = DMP_Constructor(in_PATH)
    DC.construct()
    DC.write(out_PATH)

print("DONE")