# question-place-django
## Creation virtual environment
```bash
$ python -m venv venv   # crezione ambiente virtuale
$ cd venv               # entro nella cartella appena generata dal comando precedente
$ . bin/activate  
```
## Start Django back-end
```bash
$ pip install -r requirements.txt
$ cd RecipePlace                    
$ python manage.py runserver
```
## Start Vue front-end
```bash
$ cd RecipePlace/frontend                   
$ npm i -s
$ npm run serve --fix
```
## Visualize Project
Open chrome on "http://127.0.0.1:8000/home"


