"""setup commit"""

from setuptools import setup

setup(
    name="final",
    version="0.0.1",
    description="final utilities",
    maintainer="Yi Ying Li",
    maintainer_email="yiyingl4@andrew.cmu.edu",
    license="MIT",
    packages=["final"],
    scripts=[],
    entry_points={"console_scripts": ["oa = final.main:main"]},
    long_description="""A set of bibtex utilities""",
)
