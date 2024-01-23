from pybaseball import statcast_batter, bwar_bat, playerid_lookup

# get war stats from baseball reference 
data = bwar_bat()
player = data.loc[lambda df: (df['name_common'] == 'Mike Trout') & (df['year_ID'] == 2016)]

#.loc[lambda df: df['shield'] == 8]
#print(data.loc[lambda df: (df['name_common'] == 'Mike Trout') & (df['year_ID'] == 2023)])
print(player[['name_common', 'year_ID', 'WAR']])
# get war stats plus additional fields from this table 
data = bwar_bat()



