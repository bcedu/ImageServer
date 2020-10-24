from setuptools import setup, find_packages

with open("dev_requirements.txt", "r") as dev_deps:
    test_deps = [dep.strip() for dep in dev_deps.readlines() if dep.strip()]

setup(
    name="ImageServer",
    version="1.0",
    packages=find_packages(),
    install_requires=[
        "Flask",
        "Flask-SQLAlchemy",
    ],
)
