import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import geopandas as gpd
import numpy as np

# load the dataset
df = pd.read_csv('../data/ds_salaries.csv')
print(df.info())
print(df.describe())  # basic stats of the data
print(df['experience_level'].value_counts())  # check number of unique levels of experience, 4 in total

# select the data to work on
features = ['work_year', 'experience_level', 'salary_in_usd']

df_gr = df[features].groupby(['work_year', 'experience_level'], sort=True).mean()
df_gr['salary_in_usd'] = round(df_gr['salary_in_usd'])
print(df_gr)

# sample histogram
sns.histplot(df['salary_in_usd'], bins=50)
plt.title('Histogram of the salaries in USD')
plt.show()

# additional KDE plot to check distribution by level (very low Executives)
sns.kdeplot(data=df, x='salary_in_usd', hue='experience_level')
plt.show()

# barplot of the salary by experience level
# df_gr.unstack().plot(kind='bar')
# plt.legend()
# plt.show()

print(df['company_location'].unique())  # check number of locations in the dataset

# min, max, mean for the salaries for the whole dataset
print('Max salary USD = {}'.format(round(df['salary_in_usd'].max())))
print('Min salary USD = {}'.format(round(df['salary_in_usd'].min())))
print('Mean salary USD = {}'.format(round(df['salary_in_usd'].mean())))

sns.set(font_scale=1.5)
sns.boxplot(data=df, x='experience_level', y='salary_in_usd', order=['EN', 'MI', 'SE', 'EX'])
plt.xlabel('Experience Level')
plt.ylabel('Salary in USD')
plt.title('Salary stats based on experience level')
plt.show()

df_by_comp_size = df.groupby(['work_year', 'company_size'])['salary_in_usd'].mean()
print(df_by_comp_size)

# plot the mean salaries based on the company sizes and the work year
df_by_comp_size.unstack().plot(kind='bar')
plt.legend()
plt.show()

df_countries = df.groupby('company_location')['salary_in_usd'].mean()
print(df_countries.head())
df_countries_reset = df_countries.to_frame()
print(df_countries_reset.reset_index(inplace=True))
print(df_countries_reset.head())
print('Datatypes : ', df_countries_reset.info())

df_countr_sorted = df_countries_reset.sort_values(by='salary_in_usd', ascending=False)
print(df_countr_sorted.head())

sns.set(font_scale=0.8)
fig, ax = plt.subplots(figsize=(20,8))
ax = sns.barplot(data=df_countr_sorted, x='company_location', y='salary_in_usd', color='lightblue')
ax.set_xticklabels(labels=df_countr_sorted['company_location'], rotation = 90)
ax.set_xlabel('Country')
ax.set_ylabel('Mean Salary USD')
plt.axhline(y=df['salary_in_usd'].mean(), color='red', ls='--', lw=0.8)
plt.text(x=len(df_countr_sorted)*0.5, y = df['salary_in_usd'].mean() + 1000, s='Mean salary = {} USD'.format(round(df['salary_in_usd'].mean(),2)))
plt.show()

# remove Israel as the salary there is bigger by 50% than the 2nd country
df_countr_sorted_revised = df_countr_sorted[df_countr_sorted['company_location'] != 'IL']

sns.set(font_scale=0.8)
fig, ax = plt.subplots(figsize=(20,8))
ax = sns.barplot(data=df_countr_sorted_revised, x='company_location', y='salary_in_usd', color='lightblue')
ax.set_xticklabels(labels=df_countr_sorted_revised['company_location'], rotation = 90)
ax.set_xlabel('Country')
ax.set_ylabel('Mean Salary USD')
plt.axhline(y=df_countr_sorted_revised['salary_in_usd'].mean(), color='red', ls='--', lw=0.8)
plt.text(x=len(df_countr_sorted_revised)*0.5, y = df_countr_sorted_revised['salary_in_usd'].mean() + 1000, s='Mean salary = {} USD'.format(round(df_countr_sorted_revised['salary_in_usd'].mean(),2)))
plt.show()

# load the shapefile with world countries
gdf = gpd.read_file('../data/world-administrative-boundaries.shp')
print(gdf.head())

gdf = gdf.merge(df_countries_reset, left_on='iso_3166_1_', right_on='company_location', how='left')

# replace missing values with 0 (no data)
gdf['salary_in_usd'].fillna(0, inplace=True)
gdf['salary_in_usd_log'] = np.log(gdf['salary_in_usd'])  # log could be used for plotting in the folium.Map

m = gdf.explore('salary_in_usd',
vmin=10000, vmax=200000,
cmap='viridis_r', style_kwds=dict(weight=1, color='black', fillOpacity=0.8), k=12)  # viridis_r - reversed cmap
m.show_in_browser()
