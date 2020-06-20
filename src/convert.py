import sys
import json
from dmp2ro import RO_Crate_constructor

if len(sys.argv) == 2:
    in_PATH = sys.argv[1]
    out_PATH = "ro-crate-metadata.jsonld"
elif len(sys.argv) == 3:
    in_PATH = sys.argv[1]
    out_PATH = sys.argv[2]
else:
    print("Please provide input and output file")
    exit(0)

RCC = RO_Crate_constructor(in_PATH)
rocrate = RCC.construct()
RCC.write(out_PATH)

print("DONE")