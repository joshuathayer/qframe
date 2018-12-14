import setuptools

with open("README.md", 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name="qframe",
    version="0.0.1",
    author="Joshua Thayer",
    author_email="joshuathayer@riseup.net",
    description="Declarative Qt layout rendering and data binding",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/joshuathayer/qframe",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
