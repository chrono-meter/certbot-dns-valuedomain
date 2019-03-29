from setuptools import setup, find_packages 


with open('README.md') as fp:
    long_description = fp.read()


setup(
    name='certbot-dns-valuedomain',
    version='1.0.0',
    author='chrono-meter@gmx.net',
    author_email='chrono-meter@gmx.net',
    description='Certbot plugin for authentication using value-domain',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/chrono-meter/certbot-dns-valuedomain',
    packages=find_packages(),
    python_requires=' >=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*',
    install_requires=[
        'certbot',
        'requests',
        'beautifulsoup4',
        # 'dnspython',
    ],
    entry_points={
        'certbot.plugins': [
            'dns = certbot_dns_valuedomain:Authenticator',
        ],
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Plugins',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: MIT License',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Security',
        'Topic :: System :: Installation/Setup',
        'Topic :: System :: Networking',
        'Topic :: System :: Systems Administration',
        'Topic :: Utilities',
    ],
)
