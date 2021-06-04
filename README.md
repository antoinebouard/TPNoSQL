# TPNoSQL

python3 -m venv venv
venv\Scripts\activate
pip install flask
pip install pymongo
$env:FLASK_ENV = "development"
$env:FLASK_APP = "application.py"
flask run