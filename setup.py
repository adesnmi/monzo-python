from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="monzo",
    version="0.9.0",
    description="A python SDK for interacting with the Monzo API.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/muyiwaolu/monzo-python",
    author="Muyiwa Olu",
    author_email="muyiolu94@gmail.com",
    license="MIT",
    packages=["monzo"],
    install_requires=[
        "requests==2.20.0",
        "requests-oauthlib==1.0.0",
        "python-dotenv==0.5.1",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
)
