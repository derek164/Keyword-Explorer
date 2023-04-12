# https://stackoverflow.com/questions/24736146/how-to-use-virtualenv-in-makefile
# https://www.gnu.org/software/make/manual/html_node/Rule-Introduction.html

watch: venv/touchfile

venv/touchfile: requirements.txt
	@test -d venv
	@. venv/bin/activate; pip install --upgrade pip; pip install -Ur requirements.txt
	@touch venv/touchfile

env:
	@python3 -m venv venv
	@. venv/bin/activate; pip install --upgrade pip; pip install -Ur requirements.txt

run:
	@. venv/bin/activate; python3 main.py