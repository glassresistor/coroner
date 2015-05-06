# Installation
```
sudo apt-get install libmysqlclient-dev
pip install -r requirements/app.txt
```

# Usage

To pull a single component, like articles:

```
python __init__.py article
```

To pull just a few components:

```
python __init__.py article -n 40
```

View all options using `-h`.

## Running tests

Currently this is pegged at Python 2.7, so the tests must be run thusly:
```
python -m py.test tests
```
