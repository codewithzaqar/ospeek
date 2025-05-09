from setuptools import setup, find_packages

setup(
    name="ospeek",
    version="0.0.4",
    packages=find_packages(),
    install_requires=[],
    entry_points={
        "console_scripts": [
            "ospeek=src.main:main",
        ],
    },
    author="codewithzaqar",
    description="A CLI tool to display system information",
    python_requires=">=3.6",
)