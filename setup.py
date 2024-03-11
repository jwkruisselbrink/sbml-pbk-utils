import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name='sbmlpbkutils',
    version='0.0.1',
    author='Johannes Kruisselbrink',
    author_email='jwkruisselbrink@gmail.com',
    description='Utils for FAIR PBK model development with SBML.',
    long_description=long_description,
    long_description_content_type ="text/markdown",
    url='https://github.com/jwkruisselbrink/sbml-pbk-utils',
    license='MIT',
    packages=['sbmlpbkutils'],
    install_requires=[
        'antimony>=2.15.0',
        'numpy>=1.26.4',
        'python-libsbml>=5.20.2',
        'sbmlutils>=0.9.0',
        'tellurium>=2.2.10'
    ],
    keywords=['pbk','sbml','fair']
)
