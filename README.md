# hash-url
A simple application to create and store distinct shortened URLs using hashid encoding and decoding. Additinally, provides a statistics page with time shortened url was created and number of clicks.

## Setup
Start by activating the virutal environment if it isn't already activated
```
$ . venv/bin/activate
```
Next initialize a new database by running the provided Python script
```
$ Python init_db.py
```
Finally, run the flask App with
```
$ flask run
```
## Usage
To shorten a URL enter it into the text box and click on Submit
![alt text](https://github.com/hundooo/hash-url/blob/main/homePage.png)

To view the stats page visit ```127.0.0.1:5000/stats```
![alt text](https://github.com/hundooo/hash-url/blob/main/StatsPage.png)
