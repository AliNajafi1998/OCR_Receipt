OCR Reciept project


upload receipt picture as `formdata` with `file` keyword

will receive parsed result as json response

# USAGE


1. install tesseract

### Installing tesseract on Ubuntu

```sudo apt-get update
sudo apt-get install libleptonica-dev 
sudo apt-get install tesseract-ocr
sudo apt-get install libtesseract-dev
```
[Traindata for Tesseract](https://tesseract-ocr.github.io/tessdoc/Data-Files.html)


2. cd OCR_Receipt
   
3. pipenv install

4. pipenv shell

5. ./src/manage.py migrate

6. ./src/manage.py runserver

7. `endpoint`: "127.0.0.1:8000/api/predictor/"



# Sample

![Sample](https://github.com/AliNajafi1998/OCR_Receipt/blob/master/sample.png)


## TODO:

    - make better and strict serializer.
    
    - use model for saving results if required.
