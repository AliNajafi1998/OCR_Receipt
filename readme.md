OCR Reciept project


upload receipt picture as `formdata` with `file` keyword

will receive parsed result as json response

# USAGE


## Step 1. install tesseract

### Installing tesseract on Ubuntu

```sudo apt-get update
sudo apt-get install libleptonica-dev 
sudo apt-get install tesseract-ocr
sudo apt-get install libtesseract-dev
```
[Traindata for Tesseract](https://tesseract-ocr.github.io/tessdoc/Data-Files.html)


### Installing tesseract on Windows

To install Tesseract 4  on Windows use this informative article on MEDIUM:<br>
[Installing and using Tesseract 4 on windows 10](https://medium.com/quantrium-tech/installing-and-using-tesseract-4-on-windows-10-4f7930313f82)


### Step 2. ```cd OCR_Receipt```
   
### Step 3. ```pipenv install```

### Step 4. ```pipenv shell```

### Step 5. ```./src/manage.py migrate```

### Step 6. ```./src/manage.py runserver```

### Step 7. `endpoint`: "127.0.0.1:8000/api/predictor/"



# Sample:

![Sample](https://github.com/AliNajafi1998/OCR_Receipt/blob/master/sample.png)


## TODO:

    - make better and strict serializer.
    
    - use model for saving results if required.
