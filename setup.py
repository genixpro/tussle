import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))

with open("requirements.txt", 'rt') as f:
    requirements = [r.strip() for r in f.readlines() if r.strip()]

setup(
    name='tussle',
    version='0.0.1',
    description="Tussle - Debate with strangers',
    long_description=open("README.md", "rt").read(),
    classifiers=[
        'Programming Language :: Python',
        'Framework :: Flask',
    ],
    author='Bradley Arsenault',
    author_email='genixpro@gmail.com',
    url='tussle.com',
    keywords='artificial intelligence llm',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    extras_require={
    },
    package_data={
        'tussle': [
            '**/*.csv',
            '**/*.json',
            '**/*.tsv',
            '**/*.txt',
            '**/*.yaml',
        ]
    },
    python_requires='>=3.6',
    install_requires=requirements,
    entry_points={
        'console_scripts': [
            'tussle_dev_server = tussle.general.bin.dev_api_server:main',
            'tussle_server = tussle.general.bin.gunicorn_api_server:main',
            'tussle_copy_production_data = tussle.general.bin.copy_production_data:main',
            'tussle_run_all_tests = tussle.general.bin.run_all_tests:main',
            'tussle_run_all_tests_parallel = tussle.general.bin.run_all_tests_parallel:main',
            'tussle_run_fast_tests = tussle.general.bin.run_fast_tests:main',
            'tussle_run_slow_tests = tussle.general.bin.run_slow_tests:main',
            'tussle_run_slow_tests_parallel = tussle.general.bin.run_slow_tests_parallel:main',
            'tussle_run_rapid_internal_test_suite = tussle.general.bin.run_rapid_internal_test_suite:main',
            'tussle_run_internal_only_tests = tussle.general.bin.run_internal_only_test_suite:main',
            'tussle_run_external_tests = tussle.general.bin.run_external_test_suite:main',
            'tussle_profile_startup_time = tussle.general.bin.profile_startup_time:main',
        ]
    }
)

