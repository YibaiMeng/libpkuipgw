import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="libpkuipgw",
    version="0.1.3",
    author="Meng Yibai",
    author_email="mengyibai@pku.edu.cn",
    license="MIT",
    description="Python library for accessing the Internet in Peking University.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/YibaiMeng/libpkuipgw",
    packages=["libpkuipgw"],
    install_requires=["requests"],
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
)
