from setuptools import setup, find_packages

with open('README.md') as file:
    long_description = file.read()

setup(
    name='chamd',
    python_requires='>=3.5, <4',
    version='0.5.12',
    description='Conversion and cleaning of CHILDES CHA files into PaQu Plaintext Metadata Format',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Digital Humanities Lab, Utrecht University',
    author_email='digitalhumanities@uu.nl',
    url='https://github.com/UUDigitalHumanitieslab/chamd',
    license='MIT',
    packages=['chamd'],
    zip_safe=True,
    entry_points={
        'console_scripts': [
            'chamd = chamd.__main__:main'
        ]
    })
