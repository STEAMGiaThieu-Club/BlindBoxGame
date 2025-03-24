TARGET = Program.exe
SRC = main.py
ICON = img/closed.png
FLAGS = --onefile --noconsole --icon=$(ICON)

all:
	py $(SRC)

run:
	dist/$(TARGET)

build:
	cp -r img dist/img
	cp -r fonts dist/fonts
	cp gift.csv dist/gift.csv
	cp fig.csv dist/fig.csv
	pyinstaller $(FLAGS) $(SRC) --name=$(TARGET)

