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
and replace with a service account key

To run the server
```
source ./.venv/bin/activate
cd ./llamaapi
python manage.py createsuperuser
./llamaapi/manage.py runserver
```