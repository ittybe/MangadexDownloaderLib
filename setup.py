import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="MangadexDownloaderLib",
    packages=setuptools.find_namespace_packages(),
    author="ittybe",
    author_email="ittybemain@gmail.com",
    description="fast downloading manga from mangadex in pdf format",
    long_description=long_description,
    version="1.0.0",
    python_requires='>=3.8',
    install_requires=[
        "Pillow==7.2.0",
        "PyPDF2==1.26.0",
        "requests==2.24.0"
    ],
    url="https://github.com/ittybe/MangadexDownloaderLib"
)