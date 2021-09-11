from setuptools import find_packages, setup

PKG_VERSION = "0.0.1.dev1"


def setup_package() -> None:
    setup(
        name="Python Architecture Patterns Example",
        author="Kybeidos GmbH",
        setup_requires=["setuptools"],
        packages=find_packages(exclude=["tests"]),
        version=PKG_VERSION,
    )


if __name__ == "__main__":
    setup_package()
