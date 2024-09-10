from pybaseball import batting_stats_range

# retrieve all players' batting stats for the month of May, 2017 
#data = batting_stats_range("2017-05-01", "2017-05-28")

# retrieve batting stats for only August 24, 2016
#data = batting_stats_range("2016-08-24",)

first_name = input('Enter player\'s first name: ')
last_name = input('Enter player\'s last name: ')
begin = input('Enter start date of the range (YYYY-MM-DD): ')
end = input('Enter end date of the range (YYYY-MM-DD): ')

# get war stats from baseball reference 
data = batting_stats_range(begin,end)
#data = batting_stats_range("2016-05-01", "2019-05-28")
player = data.loc[lambda df: (df['Name'] == '{first_name} {last_name}'.format(first_name=first_name, last_name=last_name))]
print(player)