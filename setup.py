import re

from setuptools import setup

with open('gitlabcli/__init__.py', 'r') as fh:
    version = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]', fh.read(), re.MULTILINE).group(1)


setup(
    name='gitlabcli',
    version=version,
    description='CLI tool for gitlab API',
    author='Alexandre Cunha',
    author_email='alexandre.cunha@gmail.com',
    license='MIT',
    packages=['gitlabcli'],
    install_requires=[
        'requests>=2.0',
    ],
    entry_points={'console_scripts': ['gitlabcli = gitlabcli:run']},
    classifiers=[
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
    ],
    url='http://github.com/alercunha/gitlab-cli',
)
