from setuptools import setup, find_packages


def readme():
    with open("README.md", 'r') as f:
        return f.read()


setup(
    name="slackbotframework",
    description="A framework for building internal integration slack bots",
    version="0.0.1",
    long_description=readme(),
    author="Brian Balsamo",
    author_email="Brian@BrianBalsamo.com",
    packages=find_packages(
        exclude=[
        ]
    ),
    include_package_data=True,
    url='https://github.com/bnbalsamo/slackbotframework',
    install_requires=[
    ],
    tests_require=[
        'pytest'
    ],
    test_suite='tests'
)
