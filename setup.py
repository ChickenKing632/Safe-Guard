from setuptools import setup, find_packages

setup(
    name='SafeGuardAntivirus',
    version='1.0',
    description='SafeGuardAntivirus is an open-source antivirus solution with an integrated firewall for comprehensive protection against malware threats. The script provides easy customization, proactive threat detection, and quarantine capabilities.',
    author='ChickenWithACrown',
    author_discord_user='chickenwithacrown',
    url='https://github.com/ChickenWithACrown/SafeGuardAntivirus',
    packages=find_packages(),
    install_requires=[
        # List dependencies here
    ],
    entry_points={
        'console_scripts': [
            'safeguard = SafeGuardAntivirusWithFirewall:main',
        ],
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: Unlicense',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)
