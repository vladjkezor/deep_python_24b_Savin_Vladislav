from setuptools import setup
from Cython.Build import cythonize


def main():
    setup(
        ext_modules=cythonize(["custom_json.pyx"]),
    )


if __name__ == "__main__":
    main()