import pandas as pd

df = pd.read_csv('data/elections/top_candidates.csv')

def get_issues_by_candidates(fips, year):
	print('issues_by_candidates: year={}, fips={}'.format(year, fips))

	row = df.loc[(df['year'] == year) & (df['state_fips'] == fips)]

	issues = {
		"Economy" : row['Economy'].values[0],
		'Health Care' : row['Health Care'].values[0],
		'Immigration' : row['Immigration'].values[0],
		'Climate' : row['Climate'].values[0]
	}

	return issues;