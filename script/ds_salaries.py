import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import geopandas as gpd

# load the dataset
df = pd.read_csv('/home/user/Desktop/ds_salaries.csv')
print(df.head())

print('Max salary USD = {}'.format(round(df['salary_in_usd'].max())))
print('Min salary USD = {}'.format(round(df['salary_in_usd'].min())))
print('Mean salary USD = {}'.format(round(df['salary_in_usd'].mean())))

# visuals
# 1 boxplot Experience level vs Salary (stats)
sns.set(font_scale=1.5)
sns.boxplot(data=df, x='experience_level', y='salary_in_usd', order=['EN', 'MI', 'SE', 'EX'])
plt.xlabel('Experience Level')
plt.ylabel('Salary in USD')
plt.title('Salary stats based on experience level')
plt.show()

# 2 bar plot by year and size vs mean salary
df_by_comp_size = df.groupby(['work_year', 'company_size'])['salary_in_usd'].mean()
print(df_by_comp_size)

df_by_comp_size.unstack().plot(kind='bar')
plt.legend()
plt.show()

# load the shapefile with countries
gdf = gpd.read_file('/home/user/filav/PyQGIS work/world-administrative-boundaries.shp')
print(gdf.head())

# find the mean salary for each location
df_countries = df.groupby('company_location')['salary_in_usd'].mean()

df_countries_reset = df_countries.to_frame()
print(df_countries_reset.reset_index(inplace=True))
print(df_countries_reset.head())
