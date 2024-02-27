from setuptools import setup, find_packages


from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name='ksd',
    version='0.1.0',
    description='Utility for decoding python secretes',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Joe Jasinski',
    author_email='joe.jasinski@gmail.com',
    url='https://xebia.com/blog/setup-py',
    packages=find_packages(include=['ksd',]),
    install_requires=[
        'PyYAML>=5.0',
    ],
    extras_require = {
        'tests': [
            'pytest>=8',
        ],
    },
    entry_points={
        'console_scripts': [
            'ksd = ksd.ksd:main',
        ]
    },
)
