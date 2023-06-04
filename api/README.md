# How to operate with the API
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
And to connect to the DB you need a connector:
```bash
pip install mysql-connector-python
```
