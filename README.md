## Getting Started

To get started with this environment, follow these steps to set up your development environment.

### Requirements

- Python 3.10

### Setup Instructions

1. **Add the deadsnakes PPA and install Python 3.10:**

```
$ sudo add-apt-repository ppa:deadsnakes/ppa
$ sudo apt update
$ sudo apt install python3.10 python3.10-venv python3.10-dev
```

2. **Create and activate a virtual environment:**

```
$ python3.10 -m venv venv
$ source venv/bin/activate
```

3. **Install the required Python packages:**

```
$ pip install --upgrade pip
$ pip3 install -r requirements.txt
```

### To switch between `.ipynb` and `.py`
```
$ jupytext --to py example.ipynb
$ jupytext --to ipynb example.py
```

### To save matplotlib objects instead of dealing with setting up X-windowing

Change `plt.show` to `plt.savefig('filename.png')` then open it with `open filename.png` and close
it with `<C-q>`.
