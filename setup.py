from setuptools import setup, find_packages

setup(
    name='gisdA',
    version='1.0.0',
    url='https://github.com/yooha1003/gisdA',
    author='Uksu, Choi',
    author_email='qtwing@naver.com',
    description='Advanced Google image searching and downloading script',
    packages=find_packages(),
    install_requires=['selenium', 'argparse', 'tqdm', 'requests', 'urllib3', 'pillow'],
)
