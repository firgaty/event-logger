"""Setup"""

import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="event-logger",
    version="0.1.0",
    author="Félix Desmaretz",
    author_email="felix.desmaretz@protonmail.com",
    description="An event logger",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/sampleproject",
    project_urls={
        # "Bug Tracker": "https://github.com/pypa/sampleproject/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.9",
    install_requires=["pandas", "argparse", "argcomplete", "dash", "sortedcontainers"],
    entry_points={
        "console_scripts": [
            "pylogger = pyeventlogger.__main__:main",
        ],
    },
)
