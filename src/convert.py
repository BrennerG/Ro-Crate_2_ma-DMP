import sys
import json
from dmp2ro import RO_Crate_constructor
from ro2dmp import DMP_Constructor

clean = False

# get arguments
if len(sys.argv) == 3:
    in_PATH = sys.argv[1]
    out_PATH = sys.argv[2]
    clean = False
elif len(sys.argv) == 4 and sys.argv[1] == '-c':
    in_PATH = sys.argv[2]
    out_PATH = sys.argv[3]
    clean = True
else:
    print("Incorrect Usage please use:")
    print('python3 convert.py <source_path> <target_path>')
    print("or")
    print("python3 convert.py -c <source_path> <target_path>")
    exit(0)

if in_PATH.endswith("json"):
    RCC = RO_Crate_constructor(in_PATH)
    RCC.construct(clean)
    RCC.write(out_PATH)
elif in_PATH.endswith("jsonld"):
    DC = DMP_Constructor(in_PATH)
    DC.construct(clean)
    DC.write(out_PATH)

print("DONE")