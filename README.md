#WTAPI

WTAPI is Flask based Api.

**For start this project, you have to follow these command:-**
1. Fir you have install all required dependencies.

    	pip install -r requirements.txt

1. Then you have uncomment line 21 for creating database,  then run run.py file

1. After creation of again comment line 21.
    	python run.py

1. After successfully run the code you have to open the **Postman**, you can download postman from here [Download Postman](https://www.postman.com/downloads/ "Download Postman").

1. Then enter these command in url bar:-
	- For create data in Database[PUT]:-
    		http://127.0.0.1:5000/createintent/YourID?name=Your&position=PositionName&experience=ExperienceInYear

	- For List data from Database[GET]:-
		    http://127.0.0.1:5000/listintent/YourId

	- For Update data in Database[PATCH]:
		    http://127.0.0.1:5000/updateintent/YourID?FieldName=Value
