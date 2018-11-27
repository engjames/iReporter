# iReporter
iReporter enables any/every citizen to bring any form of corruption to the notice of appropriate authorities and the general public. Users can also report on things that needs government intervention
## Travis
```
http......
```
## coveralls
```
http.....
```
## code climate
```
http.......
```
## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. 


### Prerequisites for API

Things you need to install for the API to work

* Python 

### Installing

To deploy this application follow these steps;
* clone/download this project from git hub
```
 git clone...........

```
* Extract the project and open it in an Editor forexample Vs code ,Pycharm or any editor of your choice.
* create a python virtual environment using the following command
```
 virtualenv  env 

``` 
* In windows, navigate to scripts in the env folder where the virtual environment exists.
```
 cd env\scripts

```
*  Activate the virtual environment using the following command ;
```
activate.bat

```
* In linux, activate the virtual environment using ;
```
source bin/activate

```
* Execute the application by running a a given command

```
 python run.py

``` 

* After running that command the server will start running at http://127.0.0.1:5000/ which is the default URI 

API Endpoints currently available are;

|__Http header__| __Endpoint__ | __Functionality__ | 
|------|-------------|------------|
|POST|  /api/v1/redflags/      | Create a ​red-flag​ record     |
|GET|  /api/v1/redflags/      | Get all ​red-flag​ records  |
|GET|  /api/v1/redflags/<id>    | Get a specific ​red-flag​ record    |
|PUT| /api/v1/redflags/<id>        |  Edit a specific ​red-flag​ record| 
|PUT| /api/v1/update-red-flags/<id>       |  Admin update status of redflg records|
|DELETE|  /api/v1/redflags/<id>   | Delete a ​red-flag​ record  |

## Testing 

Tests can be run by running by installing pytest using the command below ;
```
 pip install pytest

```
Then after installing pytest, type the command below to run the tests
```
 pytest

```

You can also get the test coverage though this requires you to have installed pytest --cov by running the command below.
```
pip install pytest-cov
```
To get the test coverage, you type the command below.
```
 pytest --cov .
```

## Built With

* [Flask](http://flask.pocoo.org/docs/1.0/) - Python web framework used

## Versioning

* URL Versioning has been used to version this applications endpoint 

* Currently only version:1 is available 

## Deployment

* The app is deployed on heroku  https://