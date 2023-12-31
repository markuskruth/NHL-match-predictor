import tkinter as tk
from tkinter import ttk

import ml_model 

home_team = None
away_team = None
prediction = [None, None]

def predict(home, away):
	odds = ml_model.get_odds(home, away)
	return odds

def predict_collect():
	global prediction
	home,away = get_teams()
	prediction = predict(home, away)
	update_odds(prediction[0], prediction[1])

def get_teams():
	home_team = home_n.get().strip()
	away_team = away_n.get().strip()

	return home_team, away_team

def update_odds(home_odds, away_odds):
	odds_home_variable.set(home_odds)
	odds_away_variable.set(away_odds)

if __name__ == "__main__":

	win = tk.Tk()
	win.title("NHL match odds predictor") 
	win.geometry("600x200")

	home_row = 5
	home_column = 0

	away_row = 6
	away_column = 0

	# home team label
	home_label = ttk.Label(win, text = "Home team: ", 
				font = ("Times New Roman", 15))

	# away team label
	away_label = ttk.Label(win, text = "Away team: ", 
				font = ("Times New Roman", 15))

	home_n = tk.StringVar()
	away_n = tk.StringVar()
	home_chosen = ttk.Combobox(win, width = 27, textvariable = home_n)
	away_chosen = ttk.Combobox(win, width = 27, textvariable = away_n)
	home_chosen["values"] = (" NYR"," SJS"," PIT"," EDM"," WPG"," PHI",
							" DAL"," N.J"," T.B"," MIN"," COL"," ANA",
							" VGK"," TOR"," NYI"," MTL"," SEA"," STL",
							" FLA"," BUF"," LAK"," ARI"," OTT"," WSH",
							" NJD"," TBL"," CBJ"," CHI"," NSH"," CGY",
							" BOS"," DET"," VAN"," CAR"," S.J"," L.A")

	away_chosen["values"] = (" NYR"," SJS"," PIT"," EDM"," WPG"," PHI",
							" DAL"," N.J"," T.B"," MIN"," COL"," ANA",
							" VGK"," TOR"," NYI"," MTL"," SEA"," STL",
							" FLA"," BUF"," LAK"," ARI"," OTT"," WSH",
							" NJD"," TBL"," CBJ"," CHI"," NSH"," CGY",
							" BOS"," DET"," VAN"," CAR"," S.J"," L.A")

	button = ttk.Button(win, text="Predict", command=predict_collect, width = 15)

	odds_home_variable = tk.StringVar()
	odds_away_variable = tk.StringVar()

	odds_home = ttk.Label(win, textvariable=odds_home_variable,
		foreground="white",
	    background="Green",
		font = ("Times New Roman", 25))

	odds_away = ttk.Label(win, textvariable=odds_away_variable,
		foreground="white",
	    background="Green",
		font = ("Times New Roman", 25))

	odds_home_label = ttk.Label(win, text="Home odds:",
								font = ("Times New Roman", 15))
	odds_home_variable.set(prediction[0])

	odds_away_label = ttk.Label(win, text="Away odds:",
								font = ("Times New Roman", 15))
	odds_away_variable.set(prediction[1])

	home_label.grid(column = home_column, row = home_row, padx = 10, pady = 25)
	home_chosen.grid(column = home_column+1, row = home_row)
	away_label.grid(column = away_column, row = away_row, padx = 10, pady = 25)
	away_chosen.grid(column = away_column+1, row = away_row)
	#team_chosen.current(0)
	button.grid(column = 0, row = 7, padx = 5)
	odds_home_label.grid(column = 2, row = home_row, padx = 20)
	odds_home.grid(column = 3, row = home_row)
	odds_away_label.grid(column = 2, row = away_row, padx = 20)
	odds_away.grid(column = 3, row = away_row)

	win.mainloop()