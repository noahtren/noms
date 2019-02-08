import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="noms",
    version="0.1.0",
    author="Noah Trenaman",
    author_email="hello@noahtrenaman.com",
    description="Nutrient Object Management System (noms) using the USDA's Standard Reference Database",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/noahtren/noms",
    packages=setuptools.find_packages(),
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)