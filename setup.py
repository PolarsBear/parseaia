ver = "0.2.2"
import setuptools, os

print(os.listdir("./"))

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="Parse-AIA-PolarsBear",
    version=ver,
    author="Lars Von Wangenheim",
    author_email="larzitovw@gmail.com",
    description="A package for reading .aia files from App Inventor",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/PolarsBear/parseaia",
    project_urls={
        "Bug Tracker": "https://github.com/PolarsBear/parseaia/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=["xmltodict","Pillow","zipfile","json"],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
)