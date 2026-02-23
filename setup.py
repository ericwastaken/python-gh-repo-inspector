from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="gh-repo-inspector",
    version="1.0.0",
    author="Eric Soto",
    author_email="eric@issfl.com",
    description="A command line tool to retrieve GitHub repo metadata, including commit information.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ericwastaken/gh-repo-inspector",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "click==8.1.8",
        "requests==2.32.3",
        "python-dotenv==1.0.1",
        "pyyaml==6.0.2",
        "pendulum==3.0.0",
        "babel==2.17.0",
    ],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Operating System :: POSIX",
        "Operating System :: MacOS",
        "Operating System :: Microsoft :: Windows",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.11",
    entry_points={
        "console_scripts": [
            "gh-repo-inspector=gh_repo_inspector.cli.main:main",
        ],
    },
    license="MIT",
    license_files=("LICENSE",),
)
