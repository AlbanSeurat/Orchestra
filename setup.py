from setuptools import setup, find_packages
import pprint

packages = find_packages()
pprint.pprint(packages)

setup(
    name = "Orchestra",
    version = "0.1",
    packages = find_packages("src"),
    package_dir={"": "src"},
    data_files=[ ('', ['src/__main__.py', 'src/manage_movie.py' ]) ],
    install_requires=['setuptools', 'putio.py', "requests", "iso8601" ],
    namespace_packages=['orchestra',],
    py_modules=['orchestra'],

    author= "Alkpone",
    author_email = "alkpone@alkpone.com",
    url = "https://github.com/Alkpone/Orchestra"
)


