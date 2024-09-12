from pybaseball import batting_stats
from sqlalchemy import create_engine
import pandas as pd
import os
from dotenv import load_dotenv, dotenv_values 

# Load the environment variables
load_dotenv()

PASSWORD = os.getenv('PASSWORD')

data = batting_stats(2024)

season_2024 = pd.DataFrame(data)
# Create a connection to the database

engine = create_engine('mysql+pymysql://root:'+ PASSWORD + '@localhost:3306/fangraphs') # type: ignore


#subset = season_2024[['Name', 'Team', 'PA', 'HR', 'HR/PA', 'FB%', 'HardHit%', 'ExitVelo', 'Barrel%', 'SwStr%', ]]

# Write the DataFrame to a new MySQL table
season_2024.to_sql('hitting_stats', con=engine, if_exists='replace', index=False)
#subset.to_sql('homerun-model', con=engine, if_exists='replace', index=False)
season_2024.to_csv('season_2024.csv', index=False)


# Close the engine
engine.dispose()
