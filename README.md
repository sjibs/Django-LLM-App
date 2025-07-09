# Django LLM App

Django App that provides a REST interface and backend access to manage prompts

To install requirements

```
pip install -r requirements.txt.
```

Navigate to

```
service-accounts/service-account-key.json
```

and replace with a service account

To run the server

```
source ./.venv/bin/activate
./llamaapi/manage.py  createsuperuser #first time only
./llamaapi/manage.py runserver
```
