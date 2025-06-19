# bigworld_exporter/version.py

# 语义化版本号：MAJOR.MINOR.PATCH
VERSION = (0, 1, 0)

def version_str():
    return ".".join(str(v) for v in VERSION)
