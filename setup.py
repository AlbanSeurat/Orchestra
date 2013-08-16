from setuptools import setup, find_packages

packages = find_packages()

setup(
    name = "Orchestra",
    version = "0.1",
    packages = find_packages(),
    scripts = ['manage_movie.py'],
	
    author= "Alkpone",
    author_email = "alkpone@alkpone.com",
    url = "https://github.com/Alkpone/Orchestra"
)


