#!/usr/bin/env python
# coding: utf-8

# ### Project :   Game Streamer Analysis
# ### Author :    Sanjoy Kumar
# ### Email :      sanjoy.eee32@gmail.com
# ### Portfolio : imsanjoykb.github.io

# ## Import Necessary Libraries


import pandas as pd
import numpy as np
import matplotlib.pylab as plt
import datetime
import missingno as msno
from collections import Counter


# ## Import Data Source


data_source =  'Maingames_DS_dataset.csv'
df = pd.read_csv(data_source, index_col="Unnamed: 0")
df.head(5)


# ## Data Internal Insights


df.shape
df.isnull().sum()
df.describe()


# ## Data Cleaning


# Drop NA value (value = '-')
df = df[df.Game != '-']
df = df[df.Game != 'No MLBB Video']
# Merge same game name
 # Arena of Valor
df['Game'] = df['Game'].replace(['Garena Liên Quân Mobile','Liên Quân Mobile'],'Arena of Valor')
 # Age of Empires
df['Game'] = df['Game'].replace(['Agge of Empires'],'Age of Empires')
 # Audition online
df['Game'] = df['Game'].replace(['Audition'],'Audition Online')
df['Game'] = df['Game'].replace(['Call of Duty: Mobile VN'],'Call of Duty: Mobile')
df['Total Follower'] = df['Total Follower'].replace(['250,98'],25098)

# change datatype
df['Total Follower'] = pd.to_numeric(df['Total Follower'])

# Other
df['PaidStarPerWatchedHourPerFollower'] = df['PaidStarPerWatchedHour']/df['Total Follower']


# Show all games
for game in df.groupby('Game').groups.keys():
  print(game)
df.groupby('Game').groups.keys()
df.groupby('Game').count().iloc[:,0].shape


# Generate game count
df_game_count = df.groupby('Game').count().sort_values('Country', ascending=False).iloc[:, 0:1].rename(columns={'Country':'Count'})
# df_game_count.head(10)


# ## Check Per Followers

cols = ['Total Follower','PaidStarPerWatchedHour'] # The columns you want to search for outliers in

# Calculate quantiles and IQR
Q1 = df[cols].quantile(0.25) # Same as np.percentile but maps (0,1) and not (0,100)
Q3 = df[cols].quantile(0.75)
IQR = Q3 - Q1

# Return a boolean array of the rows with (any) non-outlier column values
condition = ~((df[cols] < (Q1 - 1.5 * IQR)) | (df[cols] > (Q3 + 1.5 * IQR))).any(axis=1)

# Filter our dataframe based on condition
filtered_df = df[condition]
filtered_df.shape

filtered_df[['Total Follower', 'PaidStarPerWatchedHourPerFollower']].plot(x='Total Follower', y='PaidStarPerWatchedHourPerFollower', grid=True, kind='scatter')


# select data of PaidStarPerWatchedHourPerFollower in Q3-Q4
cols = ['PaidStarPerWatchedHourPerFollower']
Q1 = df[cols].quantile(0.25)
Q3 = df[cols].quantile(0.75)
condition = (df[cols]>Q3).any(axis=1)
df_filtered_by_PSPWPF = df[condition]


c = df_filtered_by_PSPWPF.corr()
c['PSPW_abs'] = c['PaidStarPerWatchedHour'].apply(lambda x: abs(x))
c_rank = c[['PaidStarPerWatchedHour', 'PSPW_abs']].sort_values('PSPW_abs', ascending=False)[c['PSPW_abs'] > c['PSPW_abs'].mean()]
c_rank = c_rank.iloc[3:]
c_rank.head(10)


# ## Correlation Matrix with General Data 


corr_matrix = df.corr()
corr_matrix['PSPW_abs'] = corr_matrix['PaidStarPerWatchedHour'].apply(lambda x: abs(x))
corr_core = corr_matrix[['PaidStarPerWatchedHour', 'PSPW_abs']]


corr_core.sort_values('PSPW_abs', ascending=False).head(10)


# ## Divide into several group: Country, Game, Genger

# Distribution of VN, PUBG, Male
vpm = df.loc[df['Game'] == 'PUBG'].loc[df['Country'] == 'VN'].loc[df['Gender'] == 'Male']
test_corr = vpm.corr()
test_corr['PSPW_abs'] = test_corr['PaidStarPerWatchedHour'].apply(lambda x: abs(x))
test_corr = test_corr[['PaidStarPerWatchedHour', 'PSPW_abs']]
test_corr


# select data of PaidStarPerWatchedHourPerFollower in Q3-Q4
cols = ['PSPW_abs']
Q3 = test_corr[cols].quantile(0.75)
condition = (test_corr[cols]>Q3).any(axis=1)
test_corr = test_corr[condition]
test_corr = test_corr.sort_values('PSPW_abs',ascending= False).iloc[3:,1:]
test_corr
test_corr.head(5).plot(kind='barh')


# Distribution of VN, PUBG, Female
vpf = df.loc[df['Game'] == 'PUBG'].loc[df['Country'] == 'VN'].loc[df['Gender'] == 'Female']
test_corr_f = vpf.corr()
test_corr_f['PSPW_abs'] = test_corr_f['PaidStarPerWatchedHour'].apply(lambda x: abs(x))
test_corr_f = test_corr_f[['PaidStarPerWatchedHour', 'PSPW_abs']]
test_corr_f

# select data of PaidStarPerWatchedHourPerFollower in Q3-Q4
cols = ['PSPW_abs']
Q3 = test_corr_f[cols].quantile(0.75)
condition = (test_corr_f[cols]>Q3).any(axis=1)
test_corr_f = test_corr_f[condition]
test_corr_f = test_corr_f.sort_values('PSPW_abs',ascending= False)[test_corr_f['PSPW_abs'] > test_corr_f['PSPW_abs'].mean()].iloc[3:,1:]
test_corr_f.plot(kind='barh')


# print(df.groupby('Country').mean()['PaidStarPerWatchedHour'])
print(df.groupby('Country').mean()['PaidStarPerWatchedHour']/df.groupby('Country').count()['PaidStarPerWatchedHour'])
(df.groupby('Country').mean()['PaidStarPerWatchedHour']/df.groupby('Country').count()['PaidStarPerWatchedHour']).plot(kind='barh')

df[df['Gender'] == 'Male'].groupby('Country').mean()['PaidStarPerWatchedHour'].plot(kind='barh')

df[df['Gender'] == 'Female'].groupby('Country').mean()['PaidStarPerWatchedHour'].plot(kind='barh')

df.groupby('Gender').mean()['PaidStarPerWatchedHour'].plot(kind='barh')

df[df['Country'] == 'PH'].groupby('Gender').mean()['PaidStarPerWatchedHour'].plot(kind='barh')

print(df.groupby('Gender').mean()['PaidStarPerWatchedHour']/df.groupby('Gender').count()['PaidStarPerWatchedHour'])
(df.groupby('Gender').mean()['PaidStarPerWatchedHour']/df.groupby('Gender').count()['PaidStarPerWatchedHour']).plot(kind='barh')

df[df['Country'] == 'VN'].groupby('Gender').mean()['PaidStarPerWatchedHour'].plot(kind='barh')

df[df['Country'] == 'ID'].groupby('Gender').mean()['PaidStarPerWatchedHour'].plot(kind='barh')


# ## Thank you







# In[ ]:




