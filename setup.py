from setuptools import setup, find_packages

setup(
    name='retort',
    version='0.1',
    description='Simple migration scripting for SQL using SQLAlchemy.',
    author='C. Nicholas Long (https://nicklong.io/craft)',
    author_email='adoc@code.webmob.net',
    url='https://github.com/adoc/pyretort',
    install_requires=[],
    setup_requires=[],
    tests_requires=['nose']
    packages=find_packages(),
    scripts=['scripts/migrate'],
    include_package_data=True,
    test_suite='nose.collector',
    zip_safe=False
)
