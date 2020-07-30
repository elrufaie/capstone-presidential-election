import pandas as pd
from state_details import StateDetails

state_details_df = pd.read_csv('data/elections/state_aggregated_0727.csv')

def init():
	print('loading state aggregates data')
	# global state_details_df = pd.read_csv('data/elections/state_aggregated_0727.csv')

def get_details_for_state(fips, year):
	state_details_df.head()
	row = state_details_df.loc[(state_details_df['STATE_FIPS'] == fips) & (state_details_df['YEAR'] == year) ]

	state = row['STATE'].values[0]
	top = row['TOP_TOPIC'].values[0]
	prev = "TBD"
	# margin = row['']

	return StateDetails(state, top, prev, '1.8%')