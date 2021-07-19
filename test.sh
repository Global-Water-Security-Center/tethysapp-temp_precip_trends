#!/usr/bin/env bash
if [ ! -f "$1" ]; then
    echo "Usage: . test.sh [/path/to/manage.py]";
    return 1;
fi
rm -f .coverage
echo "Running Tests..."
coverage run -a --rcfile coverage.ini -m unittest tethysapp.temp_precip_trends.tests.unit_tests
coverage run -a --rcfile coverage.ini $1 test tethysapp.temp_precip_trends.tests.integrated_tests
echo "Combined Coverage Report..."
coverage report --rcfile=coverage.ini
echo "Linting..."
flake8
echo "Testing Complete"
