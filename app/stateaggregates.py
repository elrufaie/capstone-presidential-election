import pandas as pd
from state_details import StateDetails

state_details_df = pd.read_csv('data/elections/state_aggregated_0801.csv')

def init():
	print('loading state aggregates data')
	# global state_details_df = pd.read_csv('data/elections/state_aggregated_0727.csv')

def get_details_for_state(fips, year):
	prev_year = 2000 if year == 2000 else year - 4
	state_details_df.head()
	row = state_details_df.loc[(state_details_df['STATE_FIPS'] == fips) & (state_details_df['YEAR'] == year) ]
	prev_row = state_details_df.loc[(state_details_df['STATE_FIPS'] == fips) & (state_details_df['YEAR'] == prev_year) ]

	state = row['STATE'].values[0]
	top = row['TOP_TOPIC'].values[0]
	winner_str = prev_row['WINNING_PARTY'].values[0]
	prev_winner = 'Democrat' if winner_str == 0 else 'Republican'
	margin = row['ABS_MARGIN_VICTORY'].values[0] * 100
	margin_str = "{:.2f}".format(margin)  + '%'
	votes = row['ELECTORAL_VOTES'].values[0]
	print("votes=" + str(votes))

	return StateDetails(state, top, prev_winner, margin_str, str(votes))

