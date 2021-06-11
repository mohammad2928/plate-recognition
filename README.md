
# plate recognition for persian plates 

In this project we extract plate text from persian plates. 

## Plateform:

Windows (These scripts modified for windows version 10)

## Directories:

1- src -->  main scripts folder

2- src/db --> db folder

3- data --> additional data

## Installation: 

1- pip install -r reqierments.txt

(If you are living in the IRAN, for installation maybe you need to use a VPN.)

2- Head over to https://github.com/UB-Mannheim/tesseract/wiki and get the 32-bit or 64-bit version depending on your system architecture and install it like as other  programs. 
(Or you can use direct path in your codes)

3- Put fas-tune-float.traineddata file in the C:\Program Files\Tesseract-OCR\tessdata path 

4- Install the SQL Server drivers for your platform on the client system. 

## Usage:

``` 
cd src;
config parameters.py 
python main.py

```

## Work stages

* Image capture by camera
* Plate recognition
  1. Read image and convert to gray scale
  2. Running threshold
  3. Running two types of erotion 
  4. Extract contours by min and max area for extraction good contours
* OCR
  1. Running OCR over any contours
  2. Check the output is a plate numbers or not
  3. You can set minimum_persian_numbers_count and maximum_persian_numbers_count variables in the parameters.py.  
* Saveing data in the database and save crop plates in the plate_images folder

## Important notes

1- All logs saved in the logs folder. (logs/main.log)

2- When main.py run, temp and plate_images and logs folder will be created.


## Database usage (seperatly)

I have created a database by the name "Plate_table" with three columns (image_path, plate_text, capture_date)
you can change it with the following scripts by yourself. 

``` 
from db import DB
db = DB()
cursor, conn = db.connect()
```

### List of tabls

``` 
db.list_of_tables(cursor, conn)
```

### Create a table

``` 
query = "CREATE TABLE Plate_table(image_path varchar(70), plate_text varchar(70), capture_date date)"
db.create_table(cursor, conn, query)
```

### Remove a table

``` 
query = 'DROP TABLE Plate_table'
db.remove_table(cursor, conn, query)
```

### Insert to a table

``` 
query = "INSERT INTO Plate_table ([image_path], [plate_text],[capture_date]) VALUES (?,?, ?)"
values = ("val", "text plate", datetime.datetime.now())
db.insert(cursor, conn, query, values)
```

### Update a table

``` 
query = "UPDATE Plate_table SET plate_text = ? WHERE capture_date = ?"
values = ("update value", datetime.datetime(2021, 6, 11, 19, 52, 37))
db.update(cursor, conn, query, values)
```

### Read rows of a table

``` 
query = 'select * from {}'.format("Plate_table")
print(db.select_rows(cursor, conn, query))
```

