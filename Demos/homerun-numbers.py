from pybaseball import batting_stats
from sqlalchemy import create_engine, MetaData, Table
import pandas as pd
import os
from dotenv import load_dotenv, dotenv_values 

# Load the environment variables
load_dotenv()
PASSWORD = os.getenv('PASSWORD')

# Load season long data
data = batting_stats(2024)
season_2024 = pd.DataFrame(data)
# Create a connection to the database

engine = create_engine('mysql+pymysql://root:'+ PASSWORD + '@localhost:3306/fangraphs') # type: ignore

# Create cherrypicked subset of the data
subset = season_2024[['Name', 'Team', 'PA', 'HR', 'FB%', 'HardHit%', 'EV', 'Barrel%', 'SwStr%']]

# Write the DataFrame to a new MySQL table
season_2024.to_sql('hitting_stats', con=engine, if_exists='replace', index=False)
subset.to_sql('homerun_model', con=engine, if_exists='replace', index=False)

#To CSV files
season_2024.to_csv('Demos/Demo-csvs/batting-stats/season_2024.csv', index=False)
subset.to_csv('Demos/Demo-csvs/batting-stats/homerun_model.csv', index=False)


# DELETE TABLE

# metadata = MetaData()
# metadata.reflect(bind=engine)
# table_to_delete = Table('homerun-model', metadata, autoload_with=engine)
# print(f"Table homerun-model has been deleted.")


# Close the engine
engine.dispose()
