from setuptools import setup, find_packages

setup(
    name='ksd',
    version='0.1.0',
    description='Utility for decoding python secretes',
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
