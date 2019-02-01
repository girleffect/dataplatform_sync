import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.rst')) as f:
    README = f.read()

with open(os.path.join(here, 'requirements.txt')) as f:
    requires = f.read().split("\n")

with open(os.path.join(here, 'VERSION')) as f:
    version = f.read().split("\n")[0]


setup(
    name='dataplatform_sync',
    version=version,
    description='praekelt',
    long_description=README,
    classifiers=[
        "Programming Language :: Python",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
    ],
    author='Praekelt.org',
    author_email='dev@praekelt.org',
    url='https://github.com/praekeltfoundation/',
    license='BSD',
    keywords='praekelt, web, django',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=requires,
    tests_require=requires,
    entry_points={}
)
