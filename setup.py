import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name='sbml-pbk-toolbox',
    version='0.0.1',
    author='Johannes Kruisselbrink',
    author_email='jwkruisselbrink@gmail.com',
    description='Toolbox for FAIR PBK model development with SBML.',
    long_description=long_description,
    long_description_content_type ="text/markdown",
    url='https://github.com/jwkruisselbrink/sbml-pbk-toolbox',
    license='MIT',
    packages=['sbmlPbkToolbox'],
    package_dir={"": "src"},
    install_requires=[
        'antimony>=2.13.2',
        'numpy>=1.21.1',
        'python-libsbml>=5.20.2',
        'sbmlutils>=0.8.7',
        'tellurium>=2.2.8'
    ]
)