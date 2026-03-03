install:
	pip install -r requirements.txt

gate:
	python main.py gate

test:
	pytest tests/ -v --cov=src

lint:
	flake8 src/ --max-line-length=120
