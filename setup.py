from setuptools import setup, find_packages
import pprint

#pprint.pprint(find_packages("eggs/setuptools-1.0-py2.7.egg"))

setup(
    name = "Orchestra",
    version = "0.1",
    #packages = find_packages("src", "eggs"),
    packages=['orchestra' ] + find_packages("eggs/requests-1.2.3-py2.7.egg") + find_packages("eggs/iso8601-0.1.4-py2.7.egg"),
    package_dir={"": "src", "requests" : "eggs/requests-1.2.3-py2.7.egg/requests", "iso8601" : "eggs/iso8601-0.1.4-py2.7.egg/iso8601" },
    data_files=[ ('', ['src/__main__.py', 'src/manage_movie.py', "eggs/putio.py-2.1.0-py2.7.egg/putio.py" ]), ("requests", [ "eggs/requests-1.2.3-py2.7.egg/requests/cacert.pem" ] )],
    install_requires=['setuptools', 'putio.py', "requests", "iso8601" ],
    namespace_packages=['orchestra'],
    py_modules=['orchestra'],

    author= "Alkpone",
    author_email = "alkpone@alkpone.com",
    url = "https://github.com/Alkpone/Orchestra"
)


