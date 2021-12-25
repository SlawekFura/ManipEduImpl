import os
import sys
print("os dirname", os.path.dirname("test.py"))
sys.path.append(os.path.dirname(os.path.abspath("test.py")))
print("syspath", sys.path)
print("abspath", os.path.abspath("test.py"))
