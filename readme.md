OCR Reciept project

upload receipt picture as `formdata` with `file` keyword

will receive parsed result as json response

#USAGE

1. cd OCR_Receipt
   
2. pipenv install

3. pipenv shell

4. ./src/manage.py migrate

5. ./src/manage.py runserver

6. `endpoint`: "127.0.0.1:8000/api/predictor/"

##TODO:

    - make better and strict serializer.
    
    - use model for saving results if required.
