import pandas as pd
import math
from scipy.stats import norm

def process_data(filename):
	df = pd.read_csv(filename)

	columns_to_keep = ["gameId","season","playerTeam","opposingTeam","home_or_away","goalsFor","goalsAgainst","shotsOnGoalFor","shotsOnGoalAgainst","iceTime"]
	df = df[columns_to_keep]
	df = df[df["season"] > 2019]	# only include the matches from 2019 onward
	df = df[df["iceTime"] == 3600]	# only include the ending stats of each match
	df = df.sort_values(by="season")

	# Duplicate the most recent 33% of the data to give it more weight
	recent_data = df.iloc[-int(0.33 * len(df)):].copy()
	df = pd.concat([df, recent_data])

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

	# calculates a prediction-value for each match
	# higher value to either positive or negative direction indicates a higher likelihood of winning
	# for home (positive) or away (negative) team 
	def calculate_predictions(df):
		team_winrates = calculate_normalized_team_winrates(df)
		predictions = []
		for i in range(len(df)):
			game = df.iloc[i]
			
			if game["home_or_away"] == "HOME":
				home = game["playerTeam"]
				away = game["opposingTeam"]
				goalDifference = game["goalsFor"] - game["goalsAgainst"]
				shotsOnGoalDif = (game["shotsOnGoalFor"] - game["shotsOnGoalAgainst"])/20
			else:
				home = game["opposingTeam"]
				away = game["playerTeam"]
				goalDifference = game["goalsAgainst"] - game["goalsFor"]
				shotsOnGoalDif = (game["shotsOnGoalAgainst"] - game["shotsOnGoalFor"])/20

			
			winrate_difference = team_winrates[home] - team_winrates[away]


			predictions.append(round((goalDifference + winrate_difference*1.25 + shotsOnGoalDif), 2))

		df["prediction"] = predictions

	calculate_predictions(df)
	columns_to_keep = ["playerTeam","opposingTeam","home_or_away","prediction"]
	df = df[columns_to_keep]

	STD = calculate_std(df) 						# calculate standard deviation for the predictions-data
	confidences = calculate_confidences(df, STD)	# and use that to calculate confidences for each matches winner to actually have won
	odds_home,odds_away = calculate_bookmarker_odds(confidences)	# transform confidence-odds to bookmaker-odds
	df["oddsHome"] = odds_home
	df["oddsAway"] = odds_away

	columns_to_keep = ["playerTeam","opposingTeam","home_or_away","oddsHome", "oddsAway"]
	df = df[columns_to_keep]

	return df

def print_teams():
	df = process_data("all_teams.csv")
	all_teams = df["playerTeam"].unique()
	for team in all_teams:
		print(team)

def print_labels():
	df = pd.read_csv("all_teams.csv")
	data = df.iloc[-124]
	for i in range(len(df.columns)):
		print(df.columns[i],":",data[i])

def calculate_std(df):
	# calculate EV
	predictions = df["prediction"].values.tolist()
	EV = sum(predictions) / len(predictions)

	# calculate variance
	squared_differences = []
	for p in predictions:
		squared_differences.append((p - EV)**2)
	VAR = sum(squared_differences) / len(squared_differences)

	# calculate standard deviation
	STD = math.sqrt(VAR)

	return STD

def calculate_confidences(df, STD):
	predictions = df["prediction"].values.tolist()
	confidences = []
	# assume the predictions are following a normal distribution
	for p in predictions:
		# z = (EV-p) / (STD/sqrt(n))
		# here we calculate the difference to a draw, which is the prediction
		# we divide it by 2 to because we only want to go down not up (not +-, just -)
		z = (p/2) / STD
		confidence = norm.cdf(z)
		confidences.append(confidence)

	return confidences

def calculate_bookmarker_odds(confidences):
	oddsHome = []
	oddsAway = []
	for p in confidences:
		home_odds = 1/p
		away_odds = 1/(1-p)

		# add some extra to the odds to get nearer to the real-world betting odds
		home_ratio = home_odds / away_odds
		away_ratio = away_odds / home_odds
		scaler = home_ratio + away_ratio

		home_odds += (home_ratio / scaler) * 0.5
		away_odds += (away_ratio / scaler) * 0.5

		oddsHome.append(home_odds)
		oddsAway.append(away_odds)

	return oddsHome, oddsAway
