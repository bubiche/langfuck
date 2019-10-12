# LangFuck

Simple Django website to encode your source code in Javascript/Python the least amount of characters as possible

Demo: https://bubiche.pythonanywhere.com/


## Setup
- Create a file named `.env`, an example can be found in `.env.sample`, change DJANGO_SETTINGS_MODULE between `dev` and `prod` depending on the environment

- If you are deploying this application, remember to add your domain name to `ALLOWED_HOSTS` in `langfuck/settings/prod.py`

- Run the following commands:
```python
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic
python manage.py runserver
```


## The ideas for this are shamelessly taken from
- https://github.com/wanqizhu/pyfuck
- https://github.com/aemkei/jsfuck
