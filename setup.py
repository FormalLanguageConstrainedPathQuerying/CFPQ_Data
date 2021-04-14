from pathlib import Path

import setuptools

with open(Path(__file__).parent / "docs" / "README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

with open("requirements.txt") as f:
    required = f.read().splitlines()

with open("cfpq_data/__init__.py") as f:
    for line in f:
        if line.startswith("__version__"):
            version = line.strip().split()[-1][1:-1]
            break

authors = {
    "vdshk": ("Vadim Abzalov", "vadim.i.abzalov@gmail.com"),
    "Yakonick": ("Nikita Kovalev", "Nikitoskova123@gmail.com"),
}

setuptools.setup(
    name="cfpq_data",
    version=version,
    description="Graphs and grammars for experimental analysis of context-free path querying algorithms",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    url="https://github.com/JetBrains-Research/CFPQ_Data",
    license="Apache License 2.0",
    author=authors["vdshk"][0],
    author_email=authors["vdshk"][1],
    package_data={"": ["*.json"], "cfpq_data": ["data/*/Grammars/*.txt"]},
    include_package_data=True,
    python_requires=">=3.7",
    install_requires=required,
)
