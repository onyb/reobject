from setuptools import setup, find_packages

setup(
    name='reobject',
    version='0.9a7',
    description='Python without ifs and buts',
    url='https://github.com/onyb/reobject',
    author='Anirudha Bose',
    author_email='ani07nov@gmail.com',
    license='Apache-2.0',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    keywords=['orm', 'python', 'object-oriented-programming', 'django'],
    install_requires=[
       'attrs>=17.2.0',
    ],
    packages=find_packages(exclude=['tests', 'tests.*']),
)
