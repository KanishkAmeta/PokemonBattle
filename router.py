from fastapi import FastAPI, HTTPException
from battle import *
from pydantic import BaseModel
from typing import Optional
import uuid
import asyncio

app = FastAPI()

#create object of DatasetProcessor from csv path
pokemon_csv_path= 'pokemon.csv'
pokemon_processor = DatasetProcessor(pokemon_csv_path)
valid_names = pokemon_processor.get_valid_names()


@app.get("/")
def root():
    #return pokemon_processor.get_pokemon_data('charizard')
    return {'Pokemon':'Gotta catch\'em all',
            'listing with pagination':'api/list/page={num\}&list={num\}',
            'begin battle':'battle/name1&&name2'
            }


@app.get("/api/list/page={page}&limit={limit}")
def list_pokemon(page: int = 1, limit: int = 20):
    if page<1 or limit<1:
        raise HTTPException(status_code=404, detail="Pagination not possible, page and limit should be more than 1")
    pokemons, total_items = pokemon_processor.list_pokemon(page, limit)
    total_pages = (total_items + limit - 1) // limit
    if total_pages<1:
        raise HTTPException(status_code=404, detail="Pagination not possible")
    return {
        "page": page,
        "limit": limit,
        "total_items": total_items,
        "total_pages": total_pages,
        "pokemons": pokemons
    }



pokemon_battle_facade = PokemonBattleFacade(pokemon_csv_path, valid_names)

# Store ongoing battles in a dictionary with battle_id as the key
battles = {}

@app.post("/api/battle")
async def start_battle(pokemon1: str, pokemon2: str):
    # Normalize Pokémon names
    pokemon1 = pokemon1.lower()
    pokemon2 = pokemon2.lower()
    spelling_checker = SpellingChecker(valid_names)
    # Check for Pokémon validity
    if not(spelling_checker.check_spelling(pokemon1) and spelling_checker.check_spelling(pokemon2)):
        raise HTTPException(status_code=404, detail="Invalid Names")
    try:
        battle_id = str(uuid.uuid4())
        battles[battle_id] = {"status": "BATTLE_INPROGRESS", "result": None}
        
        # Run battle asynchronously
        asyncio.create_task(run_battle(battle_id, pokemon1, pokemon2))

        return {"battleId": battle_id, "status": "BATTLE_STARTED"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

async def run_battle(battle_id, pokemon1, pokemon2):
    try:
        # Simulate battle execution time
        await asyncio.sleep(2)  # Simulate delay

        # Execute battle
        result = pokemon_battle_facade.battle(pokemon1, pokemon2)
        battles[battle_id] = {"status": "BATTLE_COMPLETED", "result": result}
    except Exception as e:
        battles[battle_id] = {"status": "BATTLE_FAILED", "result": None}

@app.get("/api/battle/status/{battle_id}")
async def get_battle_status(battle_id: str):
    if battle_id not in battles:
        raise HTTPException(status_code=404, detail="Battle not found")
    return battles[battle_id]        

    
