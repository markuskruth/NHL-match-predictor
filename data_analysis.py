import numpy as np
import pandas as pd

df = pd.read_csv("all_teams.csv")

columns_to_keep = ["gameId","season","playerTeam","opposingTeam","home_or_away","goalsFor","goalsAgainst"]
df = df[columns_to_keep]
df = df[df["season"] > 2018]

def calculate_normalized_team_winrates(df):
	# collect the names of every team
	all_teams = df["playerTeam"].unique()

	# calculate winrates for every team
	# recent games have more weight
	team_winrates = {}
	for team in all_teams:
		# filter the df for the current team
		team_data = df[df["playerTeam"] == team]
		total_games = len(team_data)

		total_wins = 0
		weighted_total_games = 0
		for i in range(len(team_data)):
			recency_weight = i/total_games
			game = team_data.iloc[i]
			if game["goalsFor"] > game["goalsAgainst"]:
				total_wins += recency_weight

			weighted_total_games += recency_weight

		win_rate = total_wins / weighted_total_games
		team_winrates[team] = win_rate

	# get the max and min values of winrates
	smallest_winrate = 100
	biggest_winrate = 0
	for team, winrate in team_winrates.items():
		if winrate < smallest_winrate:
			smallest_winrate = winrate
		if winrate > biggest_winrate:
			biggest_winrate = winrate

	# normalize the winrates between 0 and 1
	difference = biggest_winrate - smallest_winrate
	for team, winrate in team_winrates.items():
		team_winrates[team] = (winrate - smallest_winrate) / difference

	return team_winrates

def calculate_predictions(df):
	team_winrates = calculate_normalized_team_winrates(df)
	predictions = []
	for i in range(len(df)):
		game = df.iloc[i]
		
		if game["home_or_away"] == "HOME":
			home = game["playerTeam"]
			away = game["opposingTeam"]
			goalDifference = game["goalsFor"] - game["goalsAgainst"]
		else:
			home = game["opposingTeam"]
			away = game["playerTeam"]
			goalDifference = game["goalsAgainst"] - game["goalsFor"]

		
		winrate_difference = team_winrates[home] - team_winrates[away]
		predictions.append(round(goalDifference + winrate_difference, 2))

	df["prediction"] = predictions

calculate_predictions(df)
columns_to_keep = ["playerTeam","opposingTeam","home_or_away","prediction"]
df = df[columns_to_keep]

labels = df.columns
data = df.iloc[11]


for i in range(len(data)):
	print(labels[i],":",data[i])