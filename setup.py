from setuptools import setup, find_packages
from os import path

here = path.abspath(path.dirname(__file__))


# long description
def get_readme():
    with open(path.join(here, 'README.md'), 'r') as fh:
        return fh.read()


# single sourcing the version truth
def get_version(rel_path: str):
    codes = ''
    with open(path.join(here, rel_path), 'r') as fh:
        codes = fh.read()

    for line in codes.splitlines():
        if line.startswith('__version__'):
            delim = '"' if '"' in line else "'"
            return line.split(delim)[1]
    else:
        raise RuntimeError('Unable to find version string')


setup(
    author='JaylanLiu',
    author_email='liujilong@outlook.com',
    name='jupyter_web_report',
    version=get_version('jupyter_web_report/__init__.py'),
    description='jupyter web report',
    long_description=get_readme(),
    long_description_content_type='text/markdown',
    url='https://github.com/JaylanLiu/jupyter-web-report',
    packages=find_packages(),

    #py_modules=['jupyter-web-report'],
    install_requires=['nbconvert==5.4.1', 'argparse'],
    data_files=[('example',
                 ['example/model.ipynb', 'example/data_mutation.txt']),
                ('imgs', [
                    'imgs/template_notebook_configuration.gif',
                    'imgs/template_notebook_configuration2.gif',
                    'imgs/template_notebook_configuration3.gif'
                ])],
    python_requires='>=3.6',

    # '-' is illegal in the module name
    # the two sub-level of package
    entry_points={
        'console_scripts': ['jwr=jupyter_web_report.jupyter_web_report:main']
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Scientific/Engineering :: Bio-Informatics',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ])
