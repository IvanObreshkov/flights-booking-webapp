# How to operate with the API

### Prerequisites:

### Install MySQL server
https://learn.microsoft.com/en-us/windows/wsl/tutorials/wsl-database#install-mysql
If you get `Failed! Error: SET PASSWORD has no significance for user 'root'@'localhost'`
Check this: https://www.nixcraft.com/t/mysql-failed-error-set-password-has-no-significance-for-user-root-localhost-as-the-authentication-method-used-doesnt-store-authentication-data-in-the-mysql-server-please-consider-using-alter-user/4233

### Install the requirements

```bash
pip install -r requirements.txt
```
### .env file

```python
SECRET_KEY="your_secret_key"
MYSQL_DATABASE_URI="mysql+pymysql://youruser:yourpassword@127.0.0.1/flights_users"
ADMIN_EMAIL="admin_email"
ADMIN_PASSWORD="admin_password"
```
You can generate a secret key like this:

```python
python -c 'import secrets; print(secrets.token_hex())'
```
## Database

If you want to create the database and the tables in it with predefined data run:
```bash
python seed.py
```
Making changes to some of the Tables:

* Make changes to the classes located in the `models.py` file

* After you have made a change do: 

```bash
flask db migrate -m "Migration message"
```
 * To apply the changes described by the migration script to the database do:

```bash
flask db upgrade
```

## Run the API

```bash
flask run
```
#### If you want to have auto-reload of API when making code changes 

```bash
flask run --debug
test
```
# Common problems

### Setting up MySQL

If you get `"Can't connect to local MySQL server through socket '/var/lib/mysql/mysql.sock' (2)"`
Make sure your mysql server is running 

```bash
sudo service mysql start
```
If you want to use the MySQL shell run:
```bash
sudo mysql -u root -p
```
Also use `"127.0.0.1"` instead of `localhost` in your code when connecting to MySQL, if your socket connector is not enabled/working.
