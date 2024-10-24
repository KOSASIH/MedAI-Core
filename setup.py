# setup.py

from setuptools import setup, find_packages

setup(
    name='MedAI-Core',
    version='0.1.0',
    author='KOSASIH',
    author_email='kosasihg88@gmail.com',
    description='A high-tech health monitoring and virtual assistant system.',
    packages=find_packages(),
    install_requires=[
        'Flask==2.1.2',
        'pandas==1.4.2',
        'matplotlib==3.5.1',
        'scikit-learn==1.0.2',
        'numpy==1.22.3',
    ],
    entry_points={
        'console_scripts': [
            'medai-core=api.routes:app.run',  # Adjust this entry point as needed
        ],
    },
)
