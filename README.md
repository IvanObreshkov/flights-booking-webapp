## How to set up the project
### Git hooks

Install pre-commit hook:

```shell 
make install-hooks  # POSIX compliant shells only
```
Do not install the hooks if you are going to be using `Powershell`

The hook auto-updates the `requirements.txt` file

### Backend
The Python version used for this project is 3.10.11
#### How to install Python 3.10.11
To make your life easier it is recommended to use `pyenv`. Here is an excellent [guide](https://brain2life.hashnode.dev/how-to-install-pyenv-python-version-manager-on-ubuntu-2004) on how to install it.
Run:
```bash
pyenv install 3.10.11
```

#### Creating a Python 3.10.11 Virtual environment
We recommend using `pyenv virtualenv` for creating the virtual environment, but you can use whatever tool you like.
To create your virtual environment run:

```shell 
cd api && pyenv virtualenv 3.10.11 fllights-env
```
```shell
pyenv local flights-env
```
