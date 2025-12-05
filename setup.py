"""Setup configuration for Munim."""
from setuptools import setup, find_packages

setup(
    name="munim",
    version="0.1.0",
    description="Bank statement parser and expense categorizer for Indian banks",
    packages=find_packages(exclude=["tests", "assets", "munim_venv"]),
    python_requires=">=3.8",
    install_requires=[
        "click==8.3.1",
        "PyYAML==6.0.3",
    ],
    entry_points={
        "console_scripts": [
            "munim=cli:cli",
        ],
    },
)
