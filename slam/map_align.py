import numpy as np
import json

mapA = '/home/ming/repos/RVSS_wshop/COMPETITION_DATA/map1.txt'
mapB = '/home/ming/repos/RVSS_wshop/COMPETITION_DATA/map2.txt'

with open(mapA) as f:
    print(json.loads(f.read()))