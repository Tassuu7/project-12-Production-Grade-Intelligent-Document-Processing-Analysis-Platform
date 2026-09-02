.PHONY: install run test lint measure build docker-build docker-run clean

install:
	pip install -r requirements.txt

run:
	python main.py

test:
	python -m pytest tests/ -v

measure:
	python measure.py

build:
	@echo "Build completed successfully."

docker-build:
	docker build -t nexus-docintel:latest .

docker-run:
	docker run -p 8000:8000 nexus-docintel:latest
