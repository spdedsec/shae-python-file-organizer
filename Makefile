# SHAE File Organizer — Makefile
# No compile step (Python standard library). Targets: test, install, clean.

PYTHON ?= python3
SRC := src/main.py
TEST_DIR := /tmp/shae-organize-test

.PHONY: all test install clean setup-test

all:
	@echo "shae-file-organizer: interpreted Python, no build step required."

test: setup-test
	@echo "== list =="
	$(PYTHON) $(SRC) list $(TEST_DIR)
	@echo "== organize =="
	$(PYTHON) $(SRC) organize $(TEST_DIR)
	@echo "== list after organize =="
	$(PYTHON) $(SRC) list $(TEST_DIR)
	@echo "== undo =="
	$(PYTHON) $(SRC) undo $(TEST_DIR)
	@echo "== list after undo =="
	$(PYTHON) $(SRC) list $(TEST_DIR)

setup-test:
	@rm -rf $(TEST_DIR)
	@mkdir -p $(TEST_DIR)
	@touch $(TEST_DIR)/alpha.jpg $(TEST_DIR)/beta.png $(TEST_DIR)/gamma.svg
	@touch $(TEST_DIR)/report.pdf $(TEST_DIR)/notes.txt $(TEST_DIR)/data.csv $(TEST_DIR)/readme.md
	@touch $(TEST_DIR)/song.mp3 $(TEST_DIR)/track.wav
	@touch $(TEST_DIR)/clip.mp4 $(TEST_DIR)/movie.mkv
	@touch $(TEST_DIR)/backup.zip $(TEST_DIR)/archive.tar.gz
	@touch $(TEST_DIR)/mystery.xyz

install:
	bash scripts/install.sh

clean:
	@rm -rf $(TEST_DIR)
