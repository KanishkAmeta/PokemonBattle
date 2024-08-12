from abc import ABC, abstractmethod
from fastapi import  HTTPException
import pandas as pd
class DatasetProcessor:
    def __init__(self, csv_file_path):
        self.data = pd.read_csv(csv_file_path)
        self.data = self.data.fillna('')
        self._process_data()

    def _process_data(self):
        # Convert all columns names to lowercase
        self.data.columns = [col.lower() for col in self.data.columns]
        # Convert all string values in the dataframe to lowercase
        self.data = self.data.map(lambda x: x.lower() if isinstance(x, str) else x)

    def get_pokemon_data(self, name):
        # Find the row that matches the Pokémon name
        pokemon_data = self.data[self.data['name'] == name]
        if not pokemon_data.empty:
            return pokemon_data.iloc[0].to_dict()
        else:
            return None
    def get_valid_names(self):
        # Extract the list of Pokémon names
        return self.data['name'].tolist()    
    
    def get_dataframe_dict(self):
        return self.data.to_dict()
    
    def list_pokemon(self, page: int, limit: int):
        start = (page - 1) * limit
        end = start + limit
        return self.data.iloc[start:end].to_dict(orient="records"), len(self.data)
    
class Pokemon:
    def __init__(self, name, type1, type2, attack, data):
        self.name = name
        self.type1 = type1
        self.type2 = type2
        self.attack = attack
        self.data = data

    def get_against(self, type_):
        return self.data.get(f"against_{type_}", 1)
class PokemonFactory:
    def __init__(self, dataset_processor):
        self.dataset_processor = dataset_processor

    def create_pokemon(self, name):
        name = name.lower()
        data = self.dataset_processor.get_pokemon_data(name)
        if not data:
            raise ValueError(f"Pokémon data for {name} not found in dataset")
        return Pokemon(name, data["type1"], data.get("type2"), data["attack"], data)


        
class DamageCalculationStrategy(ABC):
    @abstractmethod
    def calculate_damage(self, attacker, defender):
        pass            

class DefaultDamageCalculationStrategy(DamageCalculationStrategy):
    def calculate_damage(self, attacker, defender):
        type1_effect = defender.get_against(attacker.type1)
        type2_effect = defender.get_against(attacker.type2) if attacker.type2 else 1
        return (attacker.attack / 200) * 100 - (((type1_effect / 4) * 100) + ((type2_effect / 4) * 100))
class Battle:
    def __init__(self, pokemon1, pokemon2, strategy):
        self.pokemon1 = pokemon1
        self.pokemon2 = pokemon2
        self.strategy = strategy

    def determine_winner(self):
        damage1 = self.strategy.calculate_damage(self.pokemon1, self.pokemon2)
        damage2 = self.strategy.calculate_damage(self.pokemon2, self.pokemon1)

        if damage1 > damage2:
            return f"{self.pokemon1.name.capitalize()} wins"
        elif damage2 > damage1:
            return f"{self.pokemon2.name.capitalize()} wins"
        else:
            return "It's a draw"  
class PokemonBattleFacade:
    def __init__(self, csv_file_path, valid_names):
        self.dataset_processor = DatasetProcessor(csv_file_path)
        self.pokemon_factory = PokemonFactory(self.dataset_processor)
        self.spelling_checker = SpellingChecker(valid_names)
        self.strategy = DefaultDamageCalculationStrategy()

    def battle(self, name1, name2):
        name1 = self.spelling_checker.normalize(name1)
        name2 = self.spelling_checker.normalize(name2)
        self.spelling_checker.check_spelling(name1)
        self.spelling_checker.check_spelling(name2)

        pokemon1 = self.pokemon_factory.create_pokemon(name1)
        pokemon2 = self.pokemon_factory.create_pokemon(name2)

        battle = Battle(pokemon1, pokemon2, self.strategy)
        return battle.determine_winner()

class SpellingChecker:
    def __init__(self, valid_names):
        self.valid_names = valid_names

    def normalize(self, name):
        return name.lower()

    def check_spelling(self, name):
        if not self._is_valid_name(name):
            raise HTTPException(status_code=404, detail="Invalid Names")
            #raise ValueError(f"Invalid Pokémon name: {name}")
        return True

    def _is_valid_name(self, name):
        for valid_name in self.valid_names:
            if self._levenshtein_distance(name, valid_name) <= 1:
                return True
        return False

    def _levenshtein_distance(self, a, b):
        dp = [[i + j for j in range(len(b) + 1)] for i in range(len(a) + 1)]
        for i in range(1, len(a) + 1):
            for j in range(1, len(b) + 1):
                dp[i][j] = min(dp[i-1][j] + 1, dp[i][j-1] + 1, dp[i-1][j-1] + (a[i-1] != b[j-1]))
        return dp[-1][-1]    

if __name__=='__main__':
    pokemon_csv_path= 'pokemon.csv'
    dataset_processor = DatasetProcessor(pokemon_csv_path)

    names_list=dataset_processor.get_valid_names()
    battle_system = PokemonBattleFacade(pokemon_csv_path, names_list)
    in_name1=input("Enter the name of first pokemon: ")
    in_name2=input("Enter the name of second pokemon:")
    try:
        result = battle_system.battle(in_name1, in_name2)
        print(result)
    except ValueError as e:
        print(f"Error: {e}")

    