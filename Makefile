NAME = Memegen

.PHONY: all install run build clean clean-all

all: install

install: .venv/flag
.venv/flag: poetry.lock
	@ poetry config virtualenvs.in-project true
	poetry install
	@ touch $@

poetry.lock: pyproject.toml
	poetry lock
	@ touch $@

run: install
	poetry run python app.py

build: install dist/$(NAME).zip

dist/$(NAME).zip: dist/$(NAME).app
	cd dist && zip -r $(NAME).zip $(NAME).app

dist/$(NAME).app: app.py Makefile poetry.lock
	poetry run pyinstaller app.py --name=$(NAME) --noconsole --noconfirm --onefile --icon=../memegen/docs/logo.png
	open dist/$(NAME).app

clean:
	rm -rf .venv build dist
