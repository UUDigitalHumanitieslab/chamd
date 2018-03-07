from setuptools import setup, find_packages

setup(
    name='chamd',
    python_requires='>=3.4, <4',
    version='0.3.2',
    description='TEI Reader',
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
