from pathlib import Path

import setuptools

with open(Path(__file__).parent / 'docs' / 'README.md', "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open('requirements.txt') as f:
    required = f.read().splitlines()

setuptools.setup(
    name='cfpq_data',
    version='0.0.0',
    description='Graphs and grammars for experimental analysis of context-free path querying algorithms',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=setuptools.find_packages(),
    url='https://github.com/JetBrains-Research/CFPQ_Data',
    license='Apache License 2.0',
    author='Abzalov Vadim, Kovalev Nikita',
    author_email='vadim.i.abzalov@gmail.com, Nikitoskova123@gmail.com',
    package_data={'': ['*.json'], 'cfpq_data': ['data/*/Grammars/*.txt']},
    include_package_data=True,
    python_requires='>=3.8',
    install_requires=required
)
