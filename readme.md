# Installation
```
sudo apt-get install libmysqlclient-dev
pip install -r requirements.txt
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
