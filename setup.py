from setuptools import setup, find_packages

setup(
    name='codius-cli',
    version='0.1.0',
    package_dir={'': 'src'},
    packages=find_packages(where='src'),
    include_package_data=True,
    install_requires=[
        'rich',
        'importlib_metadata; python_version<"3.8"',
    ],
    entry_points={
        'console_scripts': [
            'codius=main:main',
        ],
    },
    author='David Runemalm',
    author_email='david.runemalm@gmail.com',
    description='A coding assistant for domain-driven design projects in ASP.NET Core.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/runemalm/codius-cli',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
    ],
    python_requires='>=3.7',
)
