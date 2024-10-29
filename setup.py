from setuptools import setup, find_packages
from setuptools.command.install import install
from pathlib import Path


# Read version from version.py
version = {}
with open("version.py") as fp:
    exec(fp.read(), version)

this_directory = Path(__file__).parent
long_description = (this_directory / "package.md").read_text()


class PostInstallCommand(install):
    """Custom post-installation for installation mode."""

    def run(self):
        install.run(self)


# Read the requirements from the requirements.txt file
with open("tools/make/requirements.txt") as requirements_file:
    requirements = requirements_file.read().splitlines()

setup(
    name="hdp-cairo-dev",
    long_description=long_description,
    long_description_content_type="text/markdown",
    version=version["__version__"],
    packages=(
        find_packages(where="src") +
        find_packages(where="tools")
    ),
    install_requires=requirements,
    package_dir={
        "tools": "tools",
        "contract_bootloader": "src/contract_bootloader",
    },
    zip_safe=False,
    package_data={
        "tools": ["**/*.py"],
        "contract_bootloader": ["*.cairo", "*/*.cairo", "*/*.py", "**/*.py", "memorizer/**/*.py"],
    },
    cmdclass={"install": PostInstallCommand},
)
