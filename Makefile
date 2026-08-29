.PHONY: setup dev build test clean docker-up docker-down

setup:
	pip install -r backend/requirements.txt
	cd frontend && npm install

dev:
	python main.py

build:
	cd frontend && npm run build

test:
	PYTHONPATH=backend python -m pytest -v backend/tests

docker-up:
	docker-compose up --build -d

docker-down:
	docker-compose down

clean:
	rm -rf backend/__pycache__ frontend/dist
