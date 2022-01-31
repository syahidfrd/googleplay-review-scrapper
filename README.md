# Google Play review scrapper
Google Play review scrapper integrated with [Qiscus](https://qiscus.com) custom channel

### Requirements

- Python3
- PostgreSQL
- Service account file `publisher.json`. (Put it in the root of the project directory)


### Setting up Project

Create virtual environment
```bash
python3 -m venv venv
```

Activate virtual environment
```bash
source venv/bin/activate
```

Install all project dependencies
```bash
pip install -r requirements.txt
```

Create environment variables
```bash
cp .env.example .env
```

Run server
```bash
# debug mode: off
flask run

# debug mode: on
python3 wsgi.py
```