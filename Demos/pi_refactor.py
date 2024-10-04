#%% creating dataframe
import pandas as pd
import pybaseball as bb
from scipy.stats import pearsonr
from statistics import stdev

# Function for adding bbe data to the general stats df.
def add_bbe(stats, bbe):
    bbe = bbe[['player_id','attempts']]
    bbe = bbe.query("attempts >= 300")
    stats = stats.merge(bbe,on='player_id')
    return stats

# Function for splitting the name column into two columns for first and last name.
def name_split(stats):
    stats['name']=stats['last_name, first_name']
    stats=stats.drop(columns=['last_name, first_name'])
    stats[['lname', 'fname']] =stats['name'].str.split(',', n=1, expand=True).fillna('')
    stats['fname'] = stats['fname'].str.lstrip()
    stats = stats.drop(columns='name')
    return stats

# Function for calculating HR/PA.
def hr_per_pa(stats):
    stats['hr/pa']=round((stats['home_run']/stats['pa'])*100,3)
    stats=stats.drop(columns=['home_run','pa'])
    return stats

# Function for merging the fgfb data with the general stats df, by mapping fangraphs ids to baseball savant / mlbam.
def merge_fg(bs_stats, fg_stats):
    fg = fg_stats['playerId'].tolist()
    fg_stats=fg_stats[['Pull%','playerId']]

    ids = bb.playerid_reverse_lookup(fg, key_type='fangraphs')
    ids = ids[['key_fangraphs', 'key_mlbam']]

    bs_stats = bs_stats.merge(ids, left_on='player_id', right_on='key_mlbam')
    bs_stats = bs_stats.merge(fg_stats, left_on='key_fangraphs', right_on='playerId')
    bs_stats.drop(columns=['key_mlbam'], inplace=True)
    bs_stats.drop(columns=['playerId'], inplace=True)
    bs_stats.rename(columns={'key_fangraphs': 'fangraphs_id'}, inplace=True)
    bs_stats.rename(columns={'player_id': 'mlbam_id'}, inplace=True)
    reorder = ['lname','fname','mlbam_id','fangraphs_id','hr/pa','xwobacon','hard_hit_percent',
            'barrel_batted_rate','exit_velocity_avg','avg_best_speed','flyballs_percent',
            'whiff_percent','oz_contact_percent','Pull%']
    bs_stats=bs_stats[reorder]

    return bs_stats

def merge_years(stats_yr1, stats_yr2):
    stats = stats_yr1.merge(stats_yr2, on=['mlbam_id','fangraphs_id','lname','fname'], suffixes=('_23', '_24'))
    return stats


#%% 2024 version

# Create df based on the  spreadsheets collected for 2024.
bbe24 = pd.read_csv('Demos/Demo-csvs/power-index-data/2024/2024_bbe.csv')
stats24 = pd.read_csv('Demos/Demo-csvs/power-index-data/2024/2024_stats.csv')
fgfb24 = pd.read_csv('Demos/Demo-csvs/power-index-data/2024/2024_fg_fb60.csv')


# Add bbe data from bbe24 to stats24.
stats24 = add_bbe(stats24, bbe24)

# Calculate HR/PA.
stats24 = hr_per_pa(stats24)

# Split name into two columns for first and last name.
stats24 = name_split(stats24)

# Merge fgfb data with stats24.
stats24 = merge_fg(stats24, fgfb24)

# Print the columns and the first 5 rows of the df.
# print(stats24.columns)
# print(stats24.head())


############################################################################################
############################################################################################


#%% 2023 version
bbe23 = pd.read_csv('Demos/Demo-csvs/power-index-data/2023/2023_bbe.csv')
stats23 = pd.read_csv('Demos/Demo-csvs/power-index-data/2023/2023_stats.csv')
fgfb23 = pd.read_csv('Demos/Demo-csvs/power-index-data/2023/2023_fg_fb60.csv')



# Add bbe data from bbe24 to stats24.
stats23 = add_bbe(stats23, bbe23)

# Calculate HR/PA.
stats23 = hr_per_pa(stats23)

# Split name into two columns for first and last name.
stats23 = name_split(stats23)

# Merge fgfb data with stats24.
stats23 = merge_fg(stats23, fgfb23)

# Print the columns and the first 5 rows of the df.
print(stats23.columns)
print(stats23.head())

# Merge the two years' dataframes.
total = merge_years(stats23, stats24)
print(total.head())

