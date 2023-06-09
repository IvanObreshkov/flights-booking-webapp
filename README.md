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
After pyenv is installed run:
```bash
pyenv install 3.10.11
```

#### Creating a Python 3.10.11 Virtual environment for our project
```bash
pyenv virtualenv 3.10.11 env-flights-webapp 
```
### To activate the virtaulenv

Change to the `/api` directory
```bash
cd api/
```
And run:
```bash
pyenv local env-flights-webapp
```

Now you are ready to start coding. For further information please read the README.md file in the `/api` directory of the project.
