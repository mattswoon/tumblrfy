from setuptools import find_packages, setup


setup(
    name='tumblrfy',
    description='tumblrfy your text',
    author='mattswoon',
    install_requires=[
        'numpy',
        'word2number',
        'num2words'
    ],
    entry_points={
        'console_scripts': [
            'tumblrfy = tumblrfy.main:main'
        ]
    }
)
