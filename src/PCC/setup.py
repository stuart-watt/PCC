from setuptools import find_packages, setup

with open("requirements.txt", "r", encoding="utf-8") as f:
    requires = f.read().split("\n")

DESCRIPTION = "PCC Segmentation Package"

# Setting up
setup(
    name="PCC",
    description=DESCRIPTION,
    packages=find_packages(),
    python_requires=">=3",
    install_requires=requires,
    include_package_data=True,
)
