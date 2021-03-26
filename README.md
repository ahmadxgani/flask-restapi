# Flask-restapi
## How to use this app :
- Copy and rename file .flaskenv.example to .flaskenv
- Install the requirements by running this command
```bash
pip install -r requirements.txt
flask db init
flask db migrate -m "create user and plugin table"
flask db upgrade
flask run
```
- Edit your email in .flaskenv

## Thanks to <a href="https://github.com/kiddyxyz/flask-todo-list">kiddyxyz</a> for a <a href="https://kiddyxyz.medium.com/tutorial-restful-api-dengan-flask-python-part-1-pengenalan-instalasi-4836478ce651">tutorial</a> :) 

## License
[GNU](https://choosealicense.com/licenses/gpl-3.0/)
