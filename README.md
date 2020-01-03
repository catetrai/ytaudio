#### Development

### Build & deploy
1. Clone repository
2. Create python virtual environment
```bash
$ sudo apt-get update && sudo apt-get install python3-venv
$ cd /path/to/repo
$ python3 -m venv venv
```
3. Install dependencies in virtual environment
```bash
$ cd /path/to/repo
$ source venv/bin/activate
(venv)$ pip install -r requirements.txt
```
4. Create the SQLite database
```bash
(venv)$ flask db upgrade
```

### Run
```bash
(venv)$ flask run --host=0.0.0.0
```
