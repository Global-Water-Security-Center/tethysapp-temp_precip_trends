#!/usr/bin/env bash
if [ ! -f "$1" ]; then
    echo "Usage: . test.sh [/path/to/manage.py]";
    return 1;
fi
rm -f .coverage
echo "Running Tests..."
coverage run -a --rcfile coverage.ini -m unittest discover -s tests/unit_tests -p "*_tests.py"
coverage run -a --rcfile coverage.ini $1 test tests/integrated_tests/ -p="*_tests.py"
echo "Combined Coverage Report..."
coverage report --rcfile=coverage.ini
echo "Linting..."
flake8
echo "Testing Complete"
