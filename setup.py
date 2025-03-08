from setuptools import setup, find_packages


def read_requirements(filename):
    """Read a requirements.txt file and return a list of dependencies."""
    with open(filename, "r") as f:
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
)
