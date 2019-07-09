#URL Shortener

## Details

The Shortener takes a long url and shortens it, generating a four-character token. You can choose category for shortened link, short many urls in one time - you get 
csv file [long_url;short_url] or try out your own token. All operations are saved in the database.
<br><br>
If you create 'superuser' and log in on http://127.0.0.1:8000/admin/ you'll see additional options on home page. 
You can updating/deleting URLs or categories, deactivating/activating links, view details about number of clicks on short links, details about the user clicking - his browser and the IP address. 

## Installation

Before run this workshop, please install all necessary libraries.

It's good idea to install them in own virtualenv.

First, clone repository :
```
git clone https://github.com/Bartecky/Shortener.git
```

Create and active virtualenv:

```
virtualenv -p python3.7 [your env-name]
source [your env-name]/bin/activate
```
Install necessary libraries (when your env is activated):
```
cd [directory where requirements.txt is located]
pip install -r requirements.txt
```

Find location of manage.py in cloned repository and run:
```
cd .../src
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```
Remember that superuser allows you to look at the entire functionality of the project.<br>
Open browser at http://127.0.0.1:8000/ and try Shortener.


