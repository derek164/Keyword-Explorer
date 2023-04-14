# Keyword-Explorer

## Dependencies

- Local version of `academicworld` database on MySQL, MongoDB, and Neo4j
- Password is set to `test_root` for both MySQL and Neo4j


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