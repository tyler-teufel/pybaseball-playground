# -*- coding: utf-8 -*-
"""
Created on Thu Sep 26 15:05:32 2024

@author: brendan
"""

"""
Version 1.0 of the MLB Hitter Power Index (HPI)
Date Completed: 9/25/24
Description: Using baseball metrics from statcast and other platforms in an
attempt to predict the best home run hitters for the impending season

to start this analysis, here are links to statcast custom leaderboards you need

2024_stats.csv = https://baseballsavant.mlb.com/leaderboard/custom?year=2024&type=batter&filter=&min=300&selections=xwobacon%2Cexit_velocity_avg%2Cbarrel_batted_rate%2Chard_hit_percent%2Cavg_best_speed%2Coz_contact_percent%2Cwhiff_percent%2Cflyballs_percent&chart=false&x=xwobacon&y=xwobacon&r=no&chartType=beeswarm&sort=1&sortDir=desc
descr: custom leaderboard from baseball savant with most stats we will use
2024_bbe.csv = https://baseballsavant.mlb.com/leaderboard/statcast?type=batter&year=2024&position=&team=&min=q&sort=barrels_per_pa&sortDir=desc
descr: this leaderboard just used to make sure every batter had 300 BBE's,
        which is the minimum we chose for "qualified" hitters
fg_fb60.csv = https://www.fangraphs.com/leaders/splits-leaderboards?splitArr=12&splitArrPitch=&autoPt=false&splitTeams=false&statType=player&statgroup=3&startDate=2024-3-1&endDate=2024-11-1&players=&filter=PA%7Cgt%7C60&groupBy=season&wxTemperature=&wxPressure=&wxAirDensity=&wxElevation=&wxWindSpeed=&position=B&sort=16,1&pageitems=2000000000&pg=0
descr: used to get pulled flyball rate, the last stat we needed for our data

P.S - we have omitted bat tracking data from the HPI due to not
being able to test for year-to-year correlation
"""
#%% creating dataframe
import pandas as pd
import pybaseball as bb
from scipy.stats import pearsonr
from statistics import stdev

#%% 2024 version

'''
* bbe_24: Pulling the 2024 bbe.csv file from the power-index-data folder.
*
* Contains 10 columns, 252 rows not including header:
*
* "last_name, first_name","player_id","attempts","avg_hit_angle","anglesweetspotpercent",
* "max_hit_speed","avg_hit_speed","ev50","fbld","gb","max_distance","avg_distance",
* "avg_hr_distance", "ev95plus","ev95percent","barrels","brl_percent","brl_pa"
*
*
'''
bbe_24 = pd.read_csv('Demos/Demo-csvs/power-index-data/2024/2024_bbe.csv')
bbe_24 = bbe_24[['player_id','attempts']]
bbe_24 = bbe_24.query("attempts >= 300")



'''
* stats24: Pulling the 2024 stats.csv file from the power-index-data folder.
*
*
* Contains 14 Columns, 286 rows not including header:
*
* "last_name, first_name","player_id","year","pa","home_run","xwobacon",
* "exit_velocity_avg","barrel_batted_rate","hard_hit_percent","avg_best_speed",
* "oz_contact_percent","whiff_percent","flyballs_percent"

'''
stats24 = pd.read_csv('Demos/Demo-csvs/power-index-data/2024/2024_stats.csv')

stats24 = stats24.merge(bbe_24,on='player_id')
stats24['hr/pa']=round((stats24['home_run']/stats24['pa'])*100,3)
stats24=stats24.drop(columns=['home_run','pa'])
stats24['name']=stats24['last_name, first_name']
stats24=stats24.drop(columns=['last_name, first_name'])

stats24[['lname', 'fname']] =stats24['name'].str.split(',', n=1, expand=True).fillna('')
stats24['fname'] = stats24['fname'].str.lstrip()
stats24 = stats24.drop(columns='name')
stats24['playerId'] = 0 #establishing column for fangraphs ID's



fgfb = pd.read_csv('Demos/Demo-csvs/power-index-data/2024/2024_fg_fb60.csv')
fgfb=fgfb[['Pull%','playerId']]
for i in range(0,len(stats24)-1): #fangraphs id's needed for mergeing pulledfb%
    p_id=bb.playerid_lookup(stats24.iloc[:,13][i],stats24.iloc[:,14][i],fuzzy=True)
    p_id = p_id.iloc[:,2:6]
    check = p_id[p_id['key_mlbam'].isin(stats24['player_id'])]
    check = check.drop_duplicates()
    stats24.at[i,'playerId']=int(check.iloc[:,3])
stats24 = stats24.merge(fgfb,on='playerId')
reorder = ['lname','fname','player_id','playerId','hr/pa','xwobacon','hard_hit_percent',
           'barrel_batted_rate','exit_velocity_avg','avg_best_speed','flyballs_percent',
           'whiff_percent','oz_contact_percent','Pull%']
stats24=stats24[reorder]

"""
from here, you'll want to perform the same operations, but with 2023 hitters.
It is as simple as changing the year on the website leaderboards and downloading
those new CSV's. Once that's complete, you should merge the two dataframes 
on id number, so you have only hitters who recorded 300 BBE's in both 2023 
and 2024. At the time I did this there were 100 hitters in my merged df, but
there is likely to be more than that if performed after the conclusion of the 
2024 season.
"""
#%% 2023 version
bbe_23 = pd.read_csv('Demos/Demo-csvs/power-index-data/2023/2023_bbe.csv')
bbe_23 = bbe_23[['player_id','attempts']]
bbe_23 = bbe_23.query("attempts >= 300") #300 BBE's was the minimum we selected
stats23 = pd.read_csv('Demos/Demo-csvs/power-index-data/2023/2023_stats.csv')
stats23 = stats23.merge(bbe_23,on='player_id') 
stats23['hr/pa']=round((stats23['home_run']/stats23['pa'])*100,3)
stats23=stats23.drop(columns=['home_run','pa'])
stats23['name']=stats23['last_name, first_name']
stats23=stats23.drop(columns='last_name, first_name')
stats23[['lname', 'fname']] =stats23['name'].str.split(',', n=1, expand=True).fillna('')
stats23['fname'] = stats23['fname'].str.lstrip()
stats23 = stats23.drop(columns='name')
stats23['playerId'] = 0 #establishing column for fangraphs ID's
fgfb = pd.read_csv('Demos/Demo-csvs/power-index-data/2023/2023_fg_fb60.csv')
fgfb=fgfb[['Pull%','playerId']]
for i in range(0,len(stats23)): #getting fangraphs id's for all players in current df
    p_id=bb.playerid_lookup(stats23.iloc[:,13][i],stats23.iloc[:,14][i],fuzzy=True)
    p_id = p_id.iloc[:,2:6]
    check = p_id[p_id['key_mlbam'].isin(stats23['player_id'])]
    check = check.drop_duplicates()
    stats23.at[i,'playerId']=int(check.iloc[:,3])
stats23 = stats23.merge(fgfb,on='playerId')
stats23=stats23[reorder]
stats = stats24.merge(stats23,on=['player_id','playerId','lname','fname'])
del([bbe_24,bbe_23,check,fgfb,reorder,p_id])

"""
Now that we have all hitters who qualified in both seasons, we can use 
the pearsonr function from scipy.stats to find the year-to-year correlation
coefficients for our chosen stats. After finding those, I also found the
correlation from our stats to hr rate in both seasons, and too the average
of those two numbers. Once you multiply these together, that will be our
coefficient to assign a weight to each of the stats
"""

#%% Coefficients for power index
coefs = pd.DataFrame()
for i in range(5,14): #testing for year-over-year correlation
    r_sq = pearsonr(stats.iloc[:,i],stats.iloc[:,(i+10)])
    r_sq= pd.Series(round(r_sq[0],2))
    coefs = coefs.append(r_sq,ignore_index=True)
coefs = coefs.rename(columns={0:'y2y'})
coefs['2023'] = 0
for i in range(15,24): #testing for correlation to home-run rate in 2023
    r_sq = pearsonr(stats.iloc[:,i],stats.iloc[:,14])
    r_sq= float(round(r_sq[0],2))
    coefs.at[i-15,'2023'] = r_sq
coefs['2024'] = 0
for i in range(5,14): #same in 2024
    r_sq = pearsonr(stats.iloc[:,i],stats.iloc[:,4])
    r_sq= float(round(r_sq[0],2))
    coefs.at[i-5,'2024'] = r_sq
coefs['hr_avg'] = round((coefs['2023']+coefs['2024'])/2,2) #finding average
coefs = coefs.drop(columns=['2023','2024'])
coefs['coef'] = round(coefs['y2y']*coefs['hr_avg'],3)
coefs = coefs.drop(columns=['y2y','hr_avg']).T    
coefs.columns = stats24.columns[5:14]
"""
Now that we have our coefficients, it's time to create the power index. We will
first have to find the z score for each player's stat, so all numbers will
be on a similar scale. Once that's complete, we take our stat coefficients and
multiply them by our stat columns to get the weighted values, before finally
adding all columns together to get the index.

Also note we are back to using the original dataframes. Since the power index
is a single season metric, we no longer require players that are qualified in
both seasons.
"""
#%% Power Index
stats24['year'] = 2024
stats23['year'] = 2023
stats_all = stats24.append(stats23)
stats_all = stats_all.reset_index().drop(columns='index')
from scipy.stats import zscore
# gets z-scores for all player stats
for i in range(5,14):
    stats_all.iloc[:,i] = zscore(stats_all.iloc[:,i])
    stats_all.iloc[:,i] = stats_all.iloc[:,i]*coefs.iloc[:,(i-5)][0]
stats_all['power_index'] = stats_all.iloc[:,5:14].sum(axis=1)
stats_all = stats_all.sort_values(by='power_index',ascending=False).reset_index().drop(columns='index')

""" code to put index on 0-100 scale
stats_all['power_index'] = stats_all['power_index']+((-1)*stats_all.iloc[:,15][len(stats_all)-1])
mult = 100/stats_all.iloc[:,15][0]
stats_all['power_index'] = round(stats_all['power_index']*mult,0)
"""
#%% Final Notes
"""
pearson coefficient for power index year-over-year: 0.88
pearson coefficient for power index on same year hr/pa: 0.81
pearson coefficient for power index on next year hr/pa: 0.66

the 0.66 coefficient for power index on next year home-run rate indicates that
this metric has some predictive power, promising given that this is only v-1.
For some perspective, that value is higher than avg exit velo, hard hit rate,
xwobacon, and EV50 at predicting next year hr/pa, as none of those stats eclipse
0.60. However, it is marginally worse than straight up barrel rate, which has a
coefficient of 0.68. Perhaps it would be prudent to add in bat-tracking data,
but I am hesistent to do so until we can get reliable data for year-over-year
correlation.
"""