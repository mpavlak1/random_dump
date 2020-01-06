#Built-ins
import sys

#Self
PACKAGES_PATHS = ['C:/Users/Public/PythonPackages']

for PATH in PACKAGES_PATHS: sys.path.append(PATH)
sys.path = list(set(sys.path))


