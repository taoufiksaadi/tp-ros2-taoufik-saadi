import os
from glob import glob

from setuptools import setup

package_name = "tp_moveit_py"

setup(
    name=package_name,
    version="1.0.0",
    packages=[package_name],
    data_files=[
        ("share/ament_index/resource_index/packages", ["resource/" + package_name]),
        ("share/" + package_name, ["package.xml"]),
        (os.path.join("share", package_name, "launch"), glob("launch/*.launch.py")),
        (os.path.join("share", package_name, "config"), glob("config/*")),
    ],
    install_requires=["setuptools"],
    zip_safe=True,
    maintainer="Nicolas SEGUY",
    maintainer_email="nicolas.seguy@univ-evry.fr",
    description="Lancement de MoveIt 2 pour piloter le Panda avec MoveItPy",
    license="BSD-3-Clause",
    entry_points={
        "console_scripts": [
            "verif = tp_moveit_py.verif:main",
            "sequence = tp_moveit_py.sequence:main",
        ],
    },
)
