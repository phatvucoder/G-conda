# G-Conda

## Introduction

**G-Conda** is a Python library that simplifies Conda environment management on **Google Colab** and **Kaggle**. This library supports checking, installing Conda, creating new Python environments, and running commands within Conda environments automatically.

## Installation

You can install **G-Conda** using `pip`:

```sh
pip install gconda
```

## Usage

```python
from gconda import gconda
```

### 1. Check Conda and Python availability

```python
from gconda.gconda import check_conda, check_python

print("Conda available:", check_conda())
print("Python available:", check_python())
```

```python
print("Conda available:", gconda.check_conda())
print("Python available:", gconda.check_python())
```

### 2. Install Conda (if not already installed)

```python
from gconda.gconda import install_conda
install_conda()
```

```python
gconda.install_conda()
```

### 3. Create a new environment with a specific Python version

```python
from gconda.gconda import setup_env
setup_env(python_version="3.10", env_name="gconda")
```

```python
gconda.setup_env(python_version="3.10", env_name="gconda")
```

### 4. Run a pip-installed library command within the Conda environment

```python
from gconda.gconda import run_library_command
run_library_command("gdown", "--version")
```

```python
gconda.run_library_command("gdown", "--version")
```

## License

G-Conda is released under the **GNU GPL v3.0** license.

## References

G-Conda is built upon and integrates features from several established projects. We acknowledge and appreciate the contributions of the following projects:

- **[miniconda](https://docs.conda.io/en/latest/miniconda.html)**: A lightweight Conda distribution used for efficient package and environment management.
- **[condacolab](https://github.com/conda-incubator/condacolab)**: A library that enables Conda usage on Google Colab.

These projects have played a crucial role in shaping the functionality of G-Conda.

## Author

- **Hoang-Phat Vu**
- Email: [phatvucoder@gmail.com](mailto\:phatvucoder@gmail.com)
- GitHub: [phatvucoder](https://github.com/phatvucoder)

## Contributions

Contributions, bug reports, and improvements are welcome. Please create an **issue** or submit a **pull request** on [GitHub](https://github.com/phatvucoder/G-conda).

