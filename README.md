# WTAPI

WTAPI is Flask based Api.

**For start this project, you have to follow these command:-**
1. Fir you have install all required dependencies.

    	pip install -r requirements.txt

1. Then you have uncomment line 161 for creating database,  then run run.py file

1. After creation of again comment line 161.
    	python run.py

1. After successfully run the code you have to open the **Postman**, you can download postman from here [Download Postman](https://www.postman.com/downloads/ "Download Postman").

1. We'll also share with you postman json api open it in postman collections.

**Right Now 6 Apis is thier :-**

1. **Create Bot** :-
In create bot you have to pass bot_id and bot_name. 

1. **Create Intent** :-
In create intent you have to pass intent_id, intent_name, intent_description and bot_id (Which is you created first).

1. ** List Intent By Id** :-
In list intent you have to pass just only intent_id.

1. **Create Stories** :-
In create story you have pass story_id, story_name, intent_id, action_name, action_reply and bot_id (Which is you created first).

1. **Train Bot** :-
In train bot you have to pass just only bot_id.

1. **Deploy Bot** :-
In Deploy bot you have to pass just only bot_id.






