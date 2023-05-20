# https://stackoverflow.com/questions/24736146/how-to-use-virtualenv-in-makefile
# https://www.gnu.org/software/make/manual/html_node/Rule-Introduction.html

watch: venv/touchfile

venv/touchfile: requirements.txt
	@test -d venv
	@. venv/bin/activate; pip install --upgrade pip; pip install -Ur requirements.txt
	@touch venv/touchfile

freeze:
	@pip freeze > requirements.txt

lines:
	@pygount --format=summary --suffix=py,css ./src

env:
	@python3 -m venv venv
	@. venv/bin/activate; pip install --upgrade pip; pip install -Ur requirements.txt

install: env
	@. venv/bin/activate; python3 src/install.py

url:
	@. venv/bin/activate; python3 src/crossref.py

app:
	@. venv/bin/activate; python3 src/app.py

format:
	@. venv/bin/activate; isort .
	@. venv/bin/activate; black .

# Inspecting CrossRef API Results
latest:
	@$(eval latest=`ls -1t src/expansion/pub_crossref_urls | head -n 1`)
	@jq . src/expansion/pub_crossref_urls/$(latest)
	
tail:
	@grep -i "high_match" src/expansion/pub_crossref_urls.jsonl | tail -n 5 | jq

count:
	@wc -l src/expansion/pub_crossref_urls.jsonl
	@grep -i "high_match" src/expansion/pub_crossref_urls.jsonl | wc -l
	@grep -i "low_match" src/expansion/pub_crossref_urls.jsonl | wc -l
	@grep -i "api_error" src/expansion/pub_crossref_urls.jsonl | wc -l

dupes:
	@sort src/expansion/pub_crossref_urls.jsonl | uniq -c | sort -rn | awk 'int($1)>1'

long:
	@awk '{print length, $0}' src/expansion/pub_crossref_urls.jsonl | sort -nr | head -1

# CrossRef API Testing
crossref:
	@curl -H "Accept: application/json" "https://api.crossref.org/works?query.title=room+at+the+bottom&query.author=richard+feynman&mailto=derekz3@illinois.edu"
	@curl -H "Accept: application/json" "https://api.crossref.org/works?query.bibliographic=room+at+the+bottom&query.author=richard+feynman&rows=1&mailto=derekz3@illinois.edu"
	@curl -H "Accept: application/json" "https://api.crossref.org/works?select=URL&query.bibliographic=room+at+the+bottom&query.author=richard+feynman&rows=1&mailto=derekz3@illinois.edu"
	@curl -H "Accept: application/json" "https://api.crossref.org/works?select=URL&rows=1&query.bibliographic=ON+THE+USE+OF+HIERARCHIES+AND+FEEDBACK+FOR+INTELLIGENT+VIDEO+QUERY+SYSTEMS&query.author=Agouris+Peggy&mailto=derekz3@illinois.edu"
	@curl -H "Accept: application/json" "https://api.crossref.org/works?select=URL,score&rows=1&query.bibliographic=ON+THE+USE+OF+HIERARCHIES+AND+FEEDBACK+FOR+INTELLIGENT+VIDEO+QUERY+SYSTEMS&query.author=Agouris+Peggy&mailto=derekz3@illinois.edu"