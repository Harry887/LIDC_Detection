from setuptools import find_packages, setup


version_file = 'src/version.py'


def readme():
    with open('README.md', encoding='utf-8') as f:
        content = f.read()
    return content


def get_version():
    with open(version_file, 'r') as f:
        exec(compile(f.read(), version_file, 'exec'))
    return locals()['__version__']


if __name__ == '__main__':
    setup(
        name='lidcdet',
        version=get_version(),
        description='LIDC-IDRI Detection Toolbox',
        long_description=readme(),
        long_description_content_type='text/markdown',
        author='Xiong Weiyu',
        author_email='xiongweiyu@bupt.edu.cn',
        # url='https://www.konghy.com',
        packages=find_packages(exclude=('data')),
        classifiers=[
            'Development Status :: 3 - Alpha',
            'License :: OSI Approved :: Apache Software License',
            'Operating System :: OS Independent',
            'Programming Language :: Python :: 3',
            'Programming Language :: Python :: 3.6',
            'Programming Language :: Python :: 3.7',
            'Programming Language :: Python :: 3.8',
        ],
        license='Apache License 2.0',
    )
