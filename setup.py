from setuptools import setup, find_packages

tests_require = ['mock']

setup(
    name='flask-emailactivation',
    version='0.1',
    author='Tomas Drencak',
    packages=find_packages(exclude=["*.tests", "*.tests.*", "tests.*", "tests"]),
    install_requires=['itsdangerous', 'simplejson', 'Flask-Mail'],
    tests_require=tests_require,
    extras_require={'test': tests_require}
)
