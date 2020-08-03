import pandas as pd

def get_electoral_votes(year):
	df = pd.read_csv('data/elections/country_electoral_votes.csv')

	row = df.loc[df['YEAR'] == year]

	print(row)

	votes = {
		"DEM_VOTES" : str(row['DEM_VOTES'].values[0]),
		'REP_VOTES' : str(row['REP_VOTES'].values[0]),
		'DEM_CANDIDATE' : row['DEM_CANDIDATE'].values[0],
		'REP_CANDIDATE' : row['REP_CANDIDATE'].values[0]
	}

	return votes