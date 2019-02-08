import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="noms",
    version="0.0.3",
    author="Noah Trenaman",
    author_email="hello@noahtrenaman.com",
    description="Nutrient Object Management System (noms) using the USDA's Standard Reference Database",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/noahtren/noms",
    packages=setuptools.find_packages(),
    include_package_data=True,
    install_requires=[
          'copy',
          'operator',
          'requests',
          'json'
      ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)