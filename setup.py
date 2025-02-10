from setuptools import setup, find_packages

setup(
    name="gconda",
    version="0.1.1",
    author="Hoang-Phat Vu",
    author_email="phatvucoder@gmail.com",
    description="A library to manage environment on Google Colab and Kaggle.",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/phatvucoder/G-conda",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[
        "condacolab",
    ],
)
