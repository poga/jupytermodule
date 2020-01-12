from distutils.core import setup
setup(
    name='jupytermodule',  # How you named your package folder (MyLib)
    packages=['jupytermodule'],  # Chose the same as "name"
    version=
    '0.1',  # Start with a small number and increase it with every change you make
    license=
    'MIT',  # Chose a license from here: https://help.github.com/articles/licensing-a-repository
    description=
    'import jupyter notebooks as python modules',  # Give a short description about your library
    author='Poga Po',  # Type in your name
    author_email='poga.po@gmail.com',  # Type in your E-Mail
    url=
    'https://github.com/poga/jupytermodule',  # Provide either the link to your github or to your website
    keywords=['jupyter', 'notebook'],  # Keywords that define your package best
    install_requires=[  # I get to this in a second
        'nbconvert',
        'nbformat',
        'IPython',
        'astor',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
)