lint:
	flake8 suntime tests

test:
	 venv/bin/python3 -m unittest discover -s test/ -p "test_*.py" -v

coverage:
	coverage run -m unittest discover -s test/ -p "test_*.py"
	coverage html --omit="venv/*" -d coverage_html
	firefox coverage_html/index.html