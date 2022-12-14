# 2022_full-stack-dev

## Backend

### Getting started

The backend app is written in and expects Python 3.8.3

- `cd backend`
- `python3 -m pip install --upgrade pip`
- `python3 -m pip install -r requirements.txt`
- `python3 -m uvicorn src.main:app --reload --host 0.0.0.0 --port 5000`

Then go to <http://0.0.0.0:5000/docs> in your browser to see the swagger (API docs) page for your app.

### Developing

To install the dev requirements (linters, etc) in the backend app:

- `python3 -m pip install -r dev-requirements.txt`

Run the linters as follows (backend):

- `python3 -m isort -w 79 --profile=black .`
- `python3 -m black --line-length 79 -S .`

### Known bugs

If you are using PyEnv, you may encounter an issue with _sqlite3:

```
ModuleNotFoundError: No module named '_sqlite3'
```

If this happens, you will need to install `libsqlite3-dev`:

`sudo apt install libsqlite3-dev`

## Frontend

### Getting started

The frontend application is written in JavaScript (React) and expects Node 16 to be installed on your system

- `cd frontend`
- `npm install`
- `npm start`

## The Task

For this assessment, we would like you to look for bugs (Please consult data/source.json for what should be in the API response) and write what you would consider to be a good bug report. Then write appropriate test(s) to capture the problem(s).
