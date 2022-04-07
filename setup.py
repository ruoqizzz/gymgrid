import setuptools
from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(name='gymgrid2',
      version='1.2.5',
      author="Ruoqi Zhang",
      author_email="ruoqi.zhang.666@gmail.com",
      maintainer="Cedric Hermans",
      maintainer_email="cedric_hermans@hotmail.com",
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/CedricHermansBIT/gymgrid",
      packages=setuptools.find_packages(),
      python_requires='>=3.5',
      classifiers=[
              "Programming Language :: Python :: 3",
              "License :: OSI Approved :: MIT License",
              "Operating System :: OS Independent",
      ],
      install_requires=['gym', 'numpy']
      )
