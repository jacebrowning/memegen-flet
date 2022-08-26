NAME = Memegen

.PHONY: all install run build clean clean-all

all: install

install:
	poetry env use /usr/local/bin/python3
	poetry install

run: install
	poetry run python app.py

build: install dist/$(NAME).app
dist/$(NAME).app:
	poetry run pyinstaller app.py --name $(NAME) --noconsole --noconfirm --onefile
	open dist/$(NAME).app

clean:
	rm -rf build dist

clean-all: clean
	rm -rf .venv
