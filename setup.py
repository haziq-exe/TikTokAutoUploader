# setup.py

from setuptools import setup

setup(
    name='tiktokautouploader',
    version='2.6',
    packages=['tiktokautouploader'],
    description='Upload or schedule videos to tiktok with viral tiktok sounds and hashtags that work and bypass captchas',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    keywords=['tiktok', 'autoupload', 'tiktokautoupload', 'tiktoks'],
    author='HAZIQ KHALID',
    author_email='haziqmk123@gmail.com',
    url='https://github.com/haziq-exe/TikTokAutoUploader',
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    install_requires=[
        'playwright>=1.0.0',
        'requests>=2.0.0',
        'Pillow>=8.0.0',
        'transformers>=4.0.0',
        'torch>=1.0.0',
        'scikit-learn>=0.24.0',
        'inference>=0.17.1',
    ],
)
