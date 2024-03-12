from setuptools import find_packages
from setuptools import setup

with open("requirements.txt") as f:
    content = f.readlines()
requirements = [x.strip() for x in content if "git+" not in x]

setup(name='moji',
      version="0.0.5",
      description="Moji Model",
      author="Caro, Feli, Sarita",
      url="https://github.com/cparran/moji",
      install_requires=requirements,
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False)
