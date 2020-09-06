# import os
# import sys
# sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.demo import count_files

def test_count_files():
    path = "/home1/hli/xiongweiyu/data/LIDC/LIDC-IDRI/LIDC-IDRI-0106/"
    assert count_files(path) == 159
