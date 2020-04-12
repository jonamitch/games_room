import pandas as pd
import pickle
import os
from football_predictor.utils import get_from_pickle_cache, add_to_pickle_cache

LEAGUES = ('E0', 'E1')
YEARS = range(2002, 2020)
DATA_FOLDER = './data/'
PICKLE_CACHE_FOLDER = './data/pickle_cache/'


class FootballData:
    @classmethod
    def __getCache(cls, league_list, year_list, add_goals_scored_model_odds, create_team_series, override_cache):
        """ Return cached object """
        if override_cache:
            return
        cache_id = '{}-{}-{}-{}'.format(league_list, year_list, add_goals_scored_model_odds, create_team_series)
        o = get_from_pickle_cache(cache_id)
        if o:
            return o

    def __new__(cls, league_list=LEAGUES, year_list=YEARS, specified_folder=DATA_FOLDER,
                add_goals_scored_model_odds=True,
                create_team_series=True,
                override_cache=False):
        """ Initilize the class and start processing """
        existing = cls.__getCache(league_list, year_list, add_goals_scored_model_odds, create_team_series,
                                  override_cache)
        if existing:
            return existing
        football_data = super(FootballData, cls).__new__(cls)
        return football_data

    def __init__(self, league_list=LEAGUES, year_list=YEARS, specified_folder=DATA_FOLDER,
                 add_goals_scored_model_odds=True,
                 create_team_series=True,
                 override_cache=False):
        cache_id = '{}-{}-{}-{}'.format(league_list, year_list, add_goals_scored_model_odds, create_team_series)
        cache_success = get_from_pickle_cache(cache_id)
        if cache_success and not override_cache:
            print('Data loaded from cache')
            return
        self.full_df = self.get_raw_data_frame(league_list, year_list, specified_folder)
        self.team_series = None

        if add_goals_scored_model_odds:
            self.full_df = self.add_goals_scored_odds_model_column()

        if create_team_series:
            self.team_series = self.create_team_series_dict()

        print('Data loaded from raw files')

        add_to_pickle_cache(self, cache_id)
        print('Data saved to cache: {}'.format(cache_id))

    def get_raw_data_frame(self, league_list, year_list, specified_folder,
                           add_goals_scored_model_odds=True):
        league_df_list = []

        def dateparse(dates):
            parsed_dates = []
            for date in dates:
                if len(date) == 8:
                    parsed_dates.append(pd.datetime.strptime(date, '%d/%m/%y'))
                else:
                    parsed_dates.append(pd.datetime.strptime(date, '%d/%m/%Y'))
            return parsed_dates

        file_names = ['{}-{}'.format(league, year) for league in league_list for year in year_list]

        for file_name in file_names:
            file_path = os.path.join(specified_folder, '{}.csv'.format(file_name))
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
        df = self.full_df
        for season in df.index.get_level_values('season_id').unique():
            team_series[season] = {}
            season_df = df.loc[season]
            for team in season_df['HomeTeam'].unique():
                team_df = season_df.loc[(season_df['HomeTeam'] == team) | (season_df['AwayTeam'] == team)].sort_values(
                    'Date')
                team_home_df = season_df.loc[season_df['HomeTeam'] == team].sort_values('Date')
                team_away_df = season_df.loc[season_df['AwayTeam'] == team].sort_values('Date')
                team_series[season][team] = {'home': team_home_df,
                                             'away': team_away_df,
                                             'all': team_df}
        return team_series


if __name__ == '__main__':
    DATA = FootballData()

    print(DATA.full_df)
