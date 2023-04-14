# Keyword-Explorer

## Dependencies

- Local version of `academicworld` database on MySQL, MongoDB, and Neo4j
- Password is set to `test_root` for both MySQL and Neo4j
- Graph Data Science library is installed on Neo4j ([Installation Guide](https://neo4j.com/docs/graph-data-science/current/installation/neo4j-desktop/))


## Setup

Create virtual environment with required python dependencies
```{zsh}
make env
```

Activate virtual environment
```{zsh}
source venv/bin/activate
```

## Run

Start the web application
```{zsh}
python3 main.py
```