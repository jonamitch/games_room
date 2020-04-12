from football_predictor.data_loader import FootballDataFactory


class BackTesting:
    def __init__(self, football_data, profit_function):
        self.football_data = football_data
        self.profit_function = profit_function
        self.profit_summary = None

    def run_back_test(self):
        print('Running back test...')
        full_df = self.football_data.full_df

        full_df['profit'] = full_df.apply(self.profit_function, axis=1)
        print('Finished back test, producing results...')

        full_df.reset_index(inplace=True)
        self.profit_summary = full_df.groupby(['season_id'])['profit'].sum()
        print('Back test complete')


if __name__ == '__main__':
    FOOTBALL_DATA = FootballDataFactory().create_football_data(override_cache=False)
    BACK_TESTING = BackTesting(FOOTBALL_DATA, lambda row: 1)
    BACK_TESTING.run_back_test()

    print(BACK_TESTING.profit_summary)

