.PHONY: all install run

all: install

install:
	poetry install

run: install
	poetry run python app.py
