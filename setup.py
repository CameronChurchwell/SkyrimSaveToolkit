from distutils.core import setup

setup(
    name='SkyrimSaveToolkit',
    version='0.2',
    description='Toolkit for working with Skyrim save files',
    author='Cameron Churchwell',
    author_email='cameronchurchwell2024@u.northwestern.edu',
    install_requires=[
        'mothpriest',
        'lz4'
    ],
    packages=['skyrimsavetoolkit'],
)