
all: launch

launch:
	python3 -m main -l Paris

learn:
	python3 -m tadashi.train_network

overwatch:
	python3 -m tadashi.Monitoring.View.monitoringGui

install:
	pip3 install -r requirements.txt

lint:
	pep8 .

require:
	pipreqs . --force

clean:
	find . -type f -name '*.json' -delete
	find . -type f -name '*.pyc' -delete
	find . -type f -name '*.svg' -delete
	find . -type f -name '*.png' -delete
	find . -type f -name '*.dat' -delete
	find . -type d -name '__pycache__' -delete

test:
	pytest
	find . -type f -name '*.json' -delete
	find . -type f -name '*.pyc' -delete
	find . -type f -name '*.svg' -delete
	find . -type f -name '*.png' -delete
	find . -type f -name '*.dat' -delete
	find . -type d -name '__pycache__' -delete