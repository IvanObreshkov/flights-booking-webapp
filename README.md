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
We recommend using `virtualenv` for creating the virtual environment if you are using PyCharm and WSL, but you can use whatever tool you like.
To install `virtualenv` use:

```shell 
pip3 install virtualenv
```
To view the path to your python 3.10.11 run:
```shell 
which python3
```
⚠️This command assumes that you have set Python 3.10.11 globally with 
`pyenv global 3.10.11`. 

To create your virtual environment run:

```shell 
cd api && virtualenv -p /path/to/python3.10.11 env 
```
If you want your python virtual environment to deactivate when you change directory and activate again when going back into `/api` add this code at the end of your `.bashrc` file located in your home directory:
```shell
# Auto activation and deactivation of virtual env
function cd() {
  builtin cd "$@"

  if [[ -z "$VIRTUAL_ENV" ]] ; then
    ## If env folder is found then activate the virtualenv
    if [[ -d ./env ]] ; then
      source env/bin/activate
    fi
  else
    ## Check if the current folder belongs to an earlier VIRTUAL_ENV folder
    # If yes, then do nothing
    # Else, deactivate
    parentdir="$(dirname "$VIRTUAL_ENV")"
    if [[ "$PWD"/ != "$parentdir"/* ]] ; then
      deactivate
    fi
  fi
}
```
If you want your python virtual environment to activate automatically when you launch Pycharm into a folder or project add this code at the end of your `.bashrc` file located in your home directory:
```shell
# Check if the current directory contains "env" folder
if [[ -d ./env ]]; then
    ## Activate the virtualenv
    source env/bin/activate
fi
```
