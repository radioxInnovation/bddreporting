from setuptools import setup, find_packages

setup(
    name="bddreporting",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[ "pypandoc-binary", "pyyaml", "mako", "jinja2", "jsonschema", "behave"],
    description="A library providing BDD hooks with decorators",
    author="Frank Rettig",
    author_email="mail@radiox-innovation.de",
    url="https://github.com/radioxInnovation//bddreporting",
    python_requires='>=3.6',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: Other/Proprietary License",
        "Operating System :: OS Independent",
    ],
)
