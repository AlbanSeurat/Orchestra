from setuptools import setup, find_packages
import pprint

packages = find_packages()
pprint.pprint(packages)

setup(
    name = "Orchestra",
    version = "0.1",
    packages = [ 'orchestra' ],
    data_files=[ ('', ['__main__.py', ]) ],
    
    author= "Alkpone",
    author_email = "alkpone@alkpone.com",
    url = "https://github.com/Alkpone/Orchestra"
)


