# How to operate with the API

### Install MySQL server
https://learn.microsoft.com/en-us/windows/wsl/tutorials/wsl-database#install-mysql
If you get `Failed! Error: SET PASSWORD has no significance for user 'root'@'localhost'`
Check this: https://www.nixcraft.com/t/mysql-failed-error-set-password-has-no-significance-for-user-root-localhost-as-the-authentication-method-used-doesnt-store-authentication-data-in-the-mysql-server-please-consider-using-alter-user/4233

### Install the requirements

```bash
pip install -r requirements.txt
```
### Run the API

```bash
flask run
```
#### If you want to have auto-reload of API when making code changes 

```bash
flask run --debug
```
# Common problems

### Setting up MySQL
For Ubuntu users:

```bash
sudo apt install default-libmysqlclient-dev
```
Then you install “mysqlclient” Package

```bash
pip install mysqlclient
```
