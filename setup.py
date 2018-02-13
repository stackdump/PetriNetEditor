from setuptools import setup, find_packages

DESC = "A brython console for bitwrap-io."

setup(
    name="bitwrap-brython",
    version="0.1.0",
    author="Matthew York",
    author_email="myork@stackdump.com",
    description=DESC,
    license='MIT',
    keywords='brython',
    packages=find_packages() + ['twisted.plugins'],
    include_package_data=True,
    install_requires=[ 'honcho==1.0.1', 'txbitwrap==0.3.0'],
    long_description=DESC,
    url="www.blahchain.com/bitwrap-brython",
    classifiers=[],
)
