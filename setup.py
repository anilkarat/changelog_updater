from setuptools import setup

setup(
    name='changelog-updater',
    packages=['changelog_updater'],
    scripts=['changelog_updater/changelog_script.py'],
    version='0.1.30',
    install_requires=[],
    author='Ankit Richariya',
    author_email='ankit.richariya@voiro.com',
    classifiers=[ 'Environment :: Web Environment', 'Framework :: Django', 'Operating System :: OS Independent', 'Programming Language :: Python',]
)    
