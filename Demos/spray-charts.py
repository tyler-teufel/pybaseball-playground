from pybaseball import statcast_batter, spraychart, playerid_lookup

# Get playerid
first_name = input('Enter player name: ')
last_name = input('Enter player last name: ')

playerid = playerid_lookup(last_name, first_name)


# Get spray chart
start_date = input('Enter start date (YYYY-MM-DD): ')
end_date = input('Enter end date (YYYY-MM-DD): ')
data = statcast_batter(start_date, end_date, playerid['key_mlbam'].item())

sub_data = data[data['home_team'] == 'NYM']
spraychart(sub_data, 'mets', title='{first_name} {last_name} Spray Chart'.format(first_name=first_name, last_name=last_name))

