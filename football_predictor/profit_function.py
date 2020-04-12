from math import exp, factorial
from football_predictor.utils import convert_odds_to_dec_probability


class NumGoalsProfit:
    def __init__(self, football_data):
        self.football_data = football_data

    def _calculate_recent_results(self, season, date, teams):
        recent_results = {}
        for team in ['home', 'away']:
            recent_results[team] = {}
            for form in ['home', 'away']:
                team_form = self.football_data.team_series[season][teams[team]][form]
                recent_team_form = team_form.loc[team_form['Date'] < date]
                if recent_team_form.shape[0] < 3:
                    return None
                recent_team_form = recent_team_form[-3:]
                recent_results[team][form] = recent_team_form
        return recent_results

    @staticmethod
    def _calc_probability_goals_under_x(x, mean):
        return exp(-mean) * ((mean ** x) / factorial(x))

    def _predict_probability_under_x(self, row, x=3, lookback_period=3):
        date = row['Date']
        data = {'home': {'team': row['HomeTeam']},
                'away': {'team': row['AwayTeam']}}
        for fixture in data:
            recent_results = self.football_data.get_team_form(row.name[0], date, data[fixture]['team'],
                                                              fixture=fixture, num_prev_matches=lookback_period)
            season_results = self.football_data.get_team_form(row.name[0], date, data[fixture]['team'],
                                                              fixture=fixture)
            if recent_results is None:
                return None
            data[fixture]['FTHG_recent'] = recent_results['FTHG'].mean()
            data[fixture]['FTAG_recent'] = recent_results['FTAG'].mean()
            data[fixture]['FTHG_season'] = season_results['FTHG'].mean()
            data[fixture]['FTAG_season'] = season_results['FTAG'].mean()

        average_recent_home_goals = (data['home']['FTHG_recent'] + data['away']['FTHG_recent']) / 2
        average_recent_away_goals = (data['home']['FTAG_recent'] + data['away']['FTAG_recent']) / 2

        average_home_goals = (average_recent_home_goals + data['home']['FTHG_season'] + data['away']['FTHG_season']) / 3
        average_away_goals = (average_recent_away_goals + data['home']['FTAG_season'] + data['away']['FTAG_season']) / 3

        prob_under_x = 0
        for home_goals in range(x):
            for away_goals in range(x):
                if home_goals + away_goals < x:
                    home_goal_prob = self._calc_probability_goals_under_x(home_goals, average_recent_home_goals)
                    away_goal_prob = self._calc_probability_goals_under_x(away_goals, average_recent_away_goals)
                    prob_under_x += home_goal_prob * away_goal_prob

        return prob_under_x

    def _make_bet_decision_under_3(self, row, prob_under_3, buffer=0.2):
        if prob_under_3 is None:
            return None
        odds_under = row['model<2.5']
        odds_over = row['model>2.5']

        try:
            if (prob_under_3 - convert_odds_to_dec_probability(odds_under)) > buffer:
                return ('under', 1)
            elif (1 - prob_under_3) - convert_odds_to_dec_probability(odds_over) > buffer:
                return ('over', 1)
            else:
                return None
        except TypeError:
            return None

    def _calculate_profit(self, place_bet, row):
        if place_bet:
            outcome = 'under' if row['FTHG'] + row['FTAG'] < 3 else 'over'
            if outcome == place_bet[0]:
                odds = row['model<2.5'] if outcome == 'under' else row['model>2.5']
                return place_bet[1] * (odds - 1)
            else:
                return place_bet[1] * (-1)
        return 0

    def profit_function(self, row):
        prob_under_3 = self._predict_probability_under_x(row, lookback_period=10)
        place_bet = self._make_bet_decision_under_3(row, prob_under_3)
        profit = self._calculate_profit(place_bet, row)
        return profit
