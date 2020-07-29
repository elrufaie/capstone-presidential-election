import pandas as pd
from state_details import StateDetails

state_details_df = None

def init():
	print('loading state aggregates data')
	state_details_df = pd.read_csv('data/elections/state_aggregated_0727.csv')

def get_details_for_state(fips):
	return StateDetails('Flordia', 'Economy', 'Republican', '1.8%')