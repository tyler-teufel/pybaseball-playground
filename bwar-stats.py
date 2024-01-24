from pybaseball import statcast_batter, bwar_bat, playerid_lookup

# Get playerid
first_name = input('Enter player\'s first name: ')
last_name = input('Enter player\'s last name: ')
year = input('Enter year: ')
# get war stats from baseball reference 
data = bwar_bat()
player = data.loc[lambda df: (df['name_common'] == '{first_name} {last_name}'.format(first_name=first_name, last_name=last_name)) & (df['year_ID'] == int(year))]


print(player[['name_common', 'year_ID', 'WAR']])


