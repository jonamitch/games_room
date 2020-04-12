import pandas as pd
import numpy as np
from datetime import datetime
import os
from football_predictor.utils import get_from_pickle_cache, add_to_pickle_cache

LEAGUES = ('E0', 'E1')
YEARS = range(2002, 2020)
DATA_FOLDER = './data/'
PICKLE_CACHE_FOLDER = './data/pickle_cache/'


class FootballDataFactory:
    def __init__(self):
        return

    @staticmethod
    def create_football_data(league_list=LEAGUES, year_list=YEARS, specified_folder=DATA_FOLDER,
                             add_goals_scored_model_odds=True,
                             create_team_series=True,
                             override_cache=False):
        cache_id = '{}-{}-{}-{}'.format(league_list, year_list, add_goals_scored_model_odds, create_team_series)
        if override_cache:
            football_data = FootballData(league_list, year_list, specified_folder, add_goals_scored_model_odds,
                                         create_team_series)
            print('Data loaded from raw files')
            add_to_pickle_cache(football_data, cache_id)
            print('Data saved to cache: {}'.format(cache_id))
        else:
            football_data = get_from_pickle_cache(cache_id)
            print('Data loaded from cache')
        return football_data


class FootballData:
    def __init__(self, league_list, year_list, specified_folder,
                 add_goals_scored_model_odds,
                 create_team_series):
        self.league_list = league_list
        self.year_list = year_list
        self.raw_data_folder = specified_folder
        self.full_df = self.get_raw_data_frame()
        self.team_series = None

        if add_goals_scored_model_odds:
            self.full_df = self.add_goals_scored_odds_model_column()

        if create_team_series:
            self.team_series = self.create_team_series_dict()

    def get_raw_data_frame(self):
        league_df_list = []

        def dateparse(dates):
            parsed_dates = []
            for date in dates:
                if len(date) == 8:
                    parsed_dates.append(datetime.strptime(date, '%d/%m/%y'))
                else:
                    parsed_dates.append(datetime.strptime(date, '%d/%m/%Y'))
            return parsed_dates

        file_names = ['{}-{}'.format(league, year) for league in self.league_list for year in self.year_list]

        for file_name in file_names:
            file_path = os.path.join(self.raw_data_folder, '{}.csv'.format(file_name))
            league_df = pd.read_csv(file_path, sep=',', parse_dates=['Date'], date_parser=dateparse)
            league_df_list.append(league_df)

        # Create combined DF of all league data throughout the years
        combined_df = pd.concat(league_df_list, keys=file_names)
        combined_df.index.rename(['season_id', 'row_num'], inplace=True)

        return combined_df

    def add_goals_scored_odds_model_column(self):
        # Investigate the goals scored odds columns
        df = self.full_df
        goals_scored_df = df.loc[:, [col for col in df.columns if '2.5' in col]]
        goals_scored_df.reset_index(inplace=True)
        goals_scored_df_groupby = goals_scored_df.groupby(['season_id']).count()

        # Based on the above, we create the a standard goals scored odds column
        for metric in ['GB>2.5', 'BbAv>2.5', 'Avg>2.5', 'GB<2.5', 'BbAv<2.5', 'Avg<2.5']:
            if metric not in df:
                df[metric] = np.nan
        df['model>2.5'] = df['GB>2.5'].fillna(0) + \
                          df['BbAv>2.5'].fillna(0) + \
                          df['Avg>2.5'].fillna(0)
        df['model<2.5'] = df['GB<2.5'].fillna(0) + \
                          df['BbAv<2.5'].fillna(0) + \
                          df['Avg<2.5'].fillna(0)

        # Recreate analysis of the goals scored odds columns
        goals_scored_df = df.loc[:, [col for col in df.columns if '2.5' in col]]
        goals_scored_df.reset_index(inplace=True)
        goals_scored_df_groupby = goals_scored_df.groupby(['season_id']).agg(['mean', 'count'])

        return df

    def create_team_series_dict(self):
        team_series = {}
        full_df = self.full_df
        for season in full_df.index.get_level_values('season_id').unique():
            team_series[season] = {}
            season_df = full_df.loc[season]
            for team in season_df['HomeTeam'].unique():
                team_df = season_df.loc[(season_df['HomeTeam'] == team) | (season_df['AwayTeam'] == team)].sort_values(
                    'Date')
                team_home_df = season_df.loc[season_df['HomeTeam'] == team].sort_values('Date')
                team_away_df = season_df.loc[season_df['AwayTeam'] == team].sort_values('Date')
                team_series[season][team] = {'home': team_home_df,
                                             'away': team_away_df,
                                             'all': team_df}
        return team_series

    def get_team_form(self, season, date, team, num_prev_matches=None, fixture='all'):
        team_form = self.team_series[season][team][fixture]
        if date is None:
            recent_team_form = team_form
        else:
            recent_team_form = team_form.loc[team_form['Date'] < date]
        if num_prev_matches is None:
            return recent_team_form
        if recent_team_form.shape[0] < num_prev_matches:
            return None
        return recent_team_form[-num_prev_matches:]


if __name__ == '__main__':
    DATA = FootballDataFactory().create_football_data(override_cache=True)

    print(DATA.full_df)
