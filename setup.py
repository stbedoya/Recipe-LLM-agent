from setuptools import setup, find_packages
import os


def read_requirements(filename):
    """Read a requirements.txt file and return a list of dependencies."""
    with open(filename, "r", encoding="utf-8") as f:
        return [
            line.strip()
            for line in f.readlines()
            if line.strip() and not line.startswith("#")
        ]


setup(
    name="recipe_agent",
    version="0.1",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=read_requirements("requirements.txt"),
    python_requires=">=3.8",
    author="Stefany Bedoya",
    description="Generative recipe generator",
    long_description=(
        open("README.md", "r", encoding="utf-8").read()
        if os.path.exists("README.md")
        else ""
    ),
    long_description_content_type="text/markdown",
)
