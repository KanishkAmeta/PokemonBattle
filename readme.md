(make sure you have the necessary python dependencies installed)
dependencies: python pandas fastapi uvicorn

to run server enter this command after going to project directory  :
fastapi run router

access http://127.0.0.1:8000

testing APIs
 API 1/ Get Pagination: In browser enter the following URL
 http://127.0.0.1:8000/api/list/page=2&limit=15 
 it will display the pokemon details till selected page
_________________________________________________________________________________________________________________________________________________
 API 2/ Get Battle Status: Install Postman (free version without subscription) select POST

 and enter the URL http://127.0.0.1:8000/api/battle?pokemon1=Pikachu&pokemon2=Gloom

 the battle id and status will be displayed like this:

 {
    "battleId": "27f7ae3e-89fa-4949-bb52-5eccb96fa5bf",
    "status": "BATTLE_STARTED"
}

___________________________________________________________________________________________________________________________________________________
API 3/ Get Results: carefully copy the above generated battle id and paste it in browser with given query like this

http://127.0.0.1:8000/api/battle/status/27f7ae3e-89fa-4949-bb52-5eccb96fa5bf

the result will be returned like this:

 {"status":"BATTLE_COMPLETED","result":"Pikachu wins"}

###################################################################################################################################################

 unit tests :-
API 1      
   Test                                                Results
 0 0      {"detail":"Pagination not possible, page and limit should be more than 1"}

API 2

'' ''                           "detail": "Invalid Names"

gloom ''                        "detail": "Invalid Names"       

'' ekans                        "detail": "Invalid Names"

gloom ekans                     "battleId": "943706bc-62ea-4e7c-94e9-8e7a6950912e",

                                "status": "BATTLE_STARTED"
gloom ekas                       "battleId": "943706bc-62ea-4e7c-94e9-8e7a6950912e",

                                 "status": "BATTLE_STARTED"
Glooom Ekaans                    "battleId": "943706bc-62ea-4e7c-94e9-8e7a6950912e",

                                 "status": "BATTLE_STARTED"
GLoooM EkAans                    "battleId": "943706bc-62ea-4e7c-94e9-8e7a6950912e",

                                 "status": "BATTLE_STARTED"
Gloom Ekans                      "battleId": "943706bc-62ea-4e7c-94e9-8e7a6950912e",

                                 "status": "BATTLE_STARTED"
pikachu charizard                 "battleId": "480542a5-4342-46ca-84e8-f2eabe7d190a",
                                 

API 3

480542a5-4342-46ca-84e8-f2eabe7d190a   {"status":"BATTLE_COMPLETED","result":"Charizard wins"}

943706bc-62ea-4e7c-94e9-8e7a6950912e   {"status":"BATTLE_COMPLETED","result":"Gloom wins"}


943706bc-62ea-4e7c-94e9-8e7a6950912f   {"detail":"Battle not found"}


