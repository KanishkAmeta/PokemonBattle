(make sure you have the necessary python dependencies installed)
dependencies: python pandas fastapi uvicorn
_______________________________________________________________________________________________________________________________________________

to run server locally after cloning enter this command after going to project directory  :
fastapi run app

access http://127.0.0.1:8000

testing APIs
 API 1/ Get Pagination: In browser enter the following URL
 http://127.0.0.1:8000/api/list/page=2&limit=15 
 it will display the pokemon details till selected page
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
 API 2/ Get Battle Status: Install Postman (free version without subscription) select POST

 and enter the URL http://127.0.0.1:8000/api/battle?pokemon1=Pikachu&pokemon2=Gloom

 the battle id and status will be displayed like this:

 {
    "battleId": "27f7ae3e-89fa-4949-bb52-5eccb96fa5bf",
    "status": "BATTLE_STARTED"
}

/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
API 3/ Get Results: carefully copy the above generated battle id and paste it in browser with given query like this

http://127.0.0.1:8000/api/battle/status/27f7ae3e-89fa-4949-bb52-5eccb96fa5bf

the result will be returned like this:

 {"status":"BATTLE_COMPLETED","result":"Pikachu wins"}
 ______________________________________________________________________________________________________________________________________________

 Similiarly to access the deployed and hosted API on railway, use the following(you can change the input values):-

 root :  https://pokemonbattlekanishk-047c.up.railway.app/

 API 1: https://pokemonbattlekanishk-047c.up.railway.app/api/list/page=10&limit=25

 API 2: https://pokemonbattlekanishk-047c.up.railway.app/api/battle?pokemon1=pikachu&pokemon2=charizard      // call this API from postman with POST mode 

 API 3: https://pokemonbattlekanishk-047c.up.railway.app/api/battle/status/c1977cc4-e769-4090-b184-4593dda19a23     //feed the response battle_id from calling API2
###################################################################################################################################################

 unit tests :-
API 1      
   Test                                                Results
 0 0      {"detail":"Pagination not possible, page and limit should be more than 1"}
 100 15   {"detail":"Pagination not possible, select correct page values"}
 10  a    {"detail":[{"type":"int_parsing","loc":["path","limit"],"msg":"Input should be a valid integer, unable to parse string as an integer","input":"a"}]}

API 2

'' ''                           {"detail": "Invalid Names"}

gloom ''                        {"detail": "Invalid Names"}       

'' ekans                        {"detail": "Invalid Names"}

gloom ekans                     {"battleId": "943706bc-62ea-4e7c-94e9-8e7a6950912e",
                                  "status": "BATTLE_STARTED"}
                                  
gloom ekas                       {"battleId": "943706bc-62ea-4e7c-94e9-8e7a6950912e",
                                   "status": "BATTLE_STARTED"}
                                   
Glooom Ekaans                    {"battleId": "943706bc-62ea-4e7c-94e9-8e7a6950912e",
                                    "status": "BATTLE_STARTED"}
                                    
GLoooM EkAans                    {"battleId": "943706bc-62ea-4e7c-94e9-8e7a6950912e",
                                   "status": "BATTLE_STARTED"}
                                   
Gloom Ekans                      {"battleId": "943706bc-62ea-4e7c-94e9-8e7a6950912e",
                                  "status": "BATTLE_STARTED"}
                                  
pikachu charizard                 {"battleId": "480542a5-4342-46ca-84e8-f2eabe7d190a",
                                     "status": "BATTLE_STARTED"}

API 3

480542a5-4342-46ca-84e8-f2eabe7d190a   {"status":"BATTLE_COMPLETED","result":"Charizard wins"}

943706bc-62ea-4e7c-94e9-8e7a6950912e   {"status":"BATTLE_COMPLETED","result":"Gloom wins"}


943706bc-62ea-4e7c-94e9-8e7a6950912f   {"detail":"Battle not found"}


