import pandas as pd
from urllib.request import urlopen
from scipy import stats

import warnings

warnings.filterwarnings('ignore')


def betting_data():
    fd_fix = urlopen('https://www.football-data.co.uk/fixtures.csv')
    filesLoad = ['e0.csv', 'e1.csv', 'e2.csv', 'e3.csv', 'ec.csv', 'b1.csv', 'd2.csv', 'f1.csv', 'f2.csv',
                 'n1.csv', 'p1.csv', 'sc0.csv', 'sc1.csv', 'sc2.csv', 'sc3.csv', 'sp2.csv', 't1.csv',
                 'd1.csv', 'sp1.csv', 'i1.csv', 'i2.csv', 'g1.csv']
    league_path = 'https://www.football-data.co.uk/mmz4281/1920/'

    # Will append the dataframes from below into list_.
    list_ = []
    for files in filesLoad:
        fd = urlopen(league_path + files)
        df = pd.read_csv(fd, encoding="ISO-8859-1")
        list_.append(df)
    frame = pd.concat(list_)
    fix_df = pd.read_csv(fd_fix)

    # Set the avergages by division and then by home team and away team
    df_avg = frame.groupby(['Div']).mean()
    df_HT_avg = frame.groupby(['HomeTeam']).mean()
    df_AT_avg = frame.groupby(['AwayTeam']).mean()
    div_avg = df_avg[['FTHG', 'FTAG']]
    df_HT_avg = df_HT_avg.reset_index()
    df_AT_avg = df_AT_avg.reset_index()
    output = frame[['Div', 'HomeTeam']].drop_duplicates()
    output1 = frame[['Div', 'AwayTeam']].drop_duplicates()
    df_new = pd.merge(output, df_HT_avg, left_on='HomeTeam', right_on='HomeTeam')
    df_away = pd.merge(output1, df_AT_avg, left_on='AwayTeam', right_on='AwayTeam')
    div = df_avg[['FTHG', 'FTAG']].reset_index().rename(columns={'FTHG': 'DFTHG', 'FTAG': 'DFTAG'})
    df = pd.merge(df_new, div, left_on='Div', right_on='Div')
    df1 = pd.merge(df_away, div, left_on='Div', right_on='Div')
    df_home = df[['Div', 'HomeTeam', 'FTHG', 'FTAG', 'DFTHG', 'DFTAG']]
    df_away = df1[['Div', 'AwayTeam', 'FTHG', 'FTAG', 'DFTHG', 'DFTAG']]
    df_home['HTAS'] = df['FTHG'] / df['DFTHG']
    df_home['HTDS'] = df['FTAG'] / df['DFTAG']
    df_away['ATAS'] = df1['FTAG'] / df1['DFTAG']
    df_away['ATDS'] = df1['FTHG'] / df1['DFTHG']
    final_frame = pd.merge(fix_df, df_home, left_on=['Div', 'HomeTeam'], right_on=['Div', 'HomeTeam'])
    final_frame = pd.merge(final_frame, df_away, left_on=['Div', 'AwayTeam'], right_on=['Div', 'AwayTeam'])
    final_frame[
        ['Div', 'Date', 'HomeTeam', 'AwayTeam', 'B365H', 'B365D', 'B365A', 'HTAS', 'HTDS', 'ATAS', 'ATDS', 'DFTHG_x',
         'DFTAG_x']]
    final_frame['HTGE'] = final_frame['HTAS'] * final_frame['ATDS'] * final_frame['DFTHG_x']
    final_frame['ATGE'] = final_frame['ATAS'] * final_frame['HTDS'] * final_frame['DFTAG_x']
    data = final_frame[
        ['Div', 'Date', 'HomeTeam', 'AwayTeam', 'B365H', 'B365D', 'B365A', 'HTAS', 'HTDS', 'ATAS', 'ATDS', 'DFTHG_x',
         'DFTAG_x', 'HTGE', 'ATGE']]
    # Home team to nil
    data['nil_nil'] = stats.poisson.pmf(0, data['HTGE']) * stats.poisson.pmf(0, data['ATGE'])
    data['one_nil'] = stats.poisson.pmf(1, data['HTGE']) * stats.poisson.pmf(0, data['ATGE'])
    data['two_nil'] = stats.poisson.pmf(2, data['HTGE']) * stats.poisson.pmf(0, data['ATGE'])
    data['three_nil'] = stats.poisson.pmf(3, data['HTGE']) * stats.poisson.pmf(0, data['ATGE'])
    data['four_nil'] = stats.poisson.pmf(4, data['HTGE']) * stats.poisson.pmf(0, data['ATGE'])
    data['five_nil'] = stats.poisson.pmf(5, data['HTGE']) * stats.poisson.pmf(0, data['ATGE'])
    # away team to nil
    data['nil_one'] = stats.poisson.pmf(0, data['HTGE']) * stats.poisson.pmf(1, data['ATGE'])
    data['nil_two'] = stats.poisson.pmf(0, data['HTGE']) * stats.poisson.pmf(2, data['ATGE'])
    data['nil_three'] = stats.poisson.pmf(0, data['HTGE']) * stats.poisson.pmf(3, data['ATGE'])
    data['nil_four'] = stats.poisson.pmf(0, data['HTGE']) * stats.poisson.pmf(4, data['ATGE'])
    data['nil_five'] = stats.poisson.pmf(0, data['HTGE']) * stats.poisson.pmf(5, data['ATGE'])
    # home team away team to score one
    data['one_one'] = stats.poisson.pmf(1, data['HTGE']) * stats.poisson.pmf(1, data['ATGE'])
    data['two_one'] = stats.poisson.pmf(2, data['HTGE']) * stats.poisson.pmf(1, data['ATGE'])
    data['three_one'] = stats.poisson.pmf(3, data['HTGE']) * stats.poisson.pmf(1, data['ATGE'])
    data['four_one'] = stats.poisson.pmf(4, data['HTGE']) * stats.poisson.pmf(1, data['ATGE'])
    data['five_one'] = stats.poisson.pmf(5, data['HTGE']) * stats.poisson.pmf(1, data['ATGE'])
    # home team away team to score two
    data['one_two'] = stats.poisson.pmf(1, data['HTGE']) * stats.poisson.pmf(2, data['ATGE'])
    data['two_two'] = stats.poisson.pmf(2, data['HTGE']) * stats.poisson.pmf(2, data['ATGE'])
    data['three_two'] = stats.poisson.pmf(3, data['HTGE']) * stats.poisson.pmf(2, data['ATGE'])
    data['four_two'] = stats.poisson.pmf(4, data['HTGE']) * stats.poisson.pmf(2, data['ATGE'])
    data['five_two'] = stats.poisson.pmf(5, data['HTGE']) * stats.poisson.pmf(2, data['ATGE'])
    # home team away team to score three
    data['one_three'] = stats.poisson.pmf(1, data['HTGE']) * stats.poisson.pmf(3, data['ATGE'])
    data['two_three'] = stats.poisson.pmf(2, data['HTGE']) * stats.poisson.pmf(3, data['ATGE'])
    data['three_three'] = stats.poisson.pmf(3, data['HTGE']) * stats.poisson.pmf(3, data['ATGE'])
    data['four_three'] = stats.poisson.pmf(4, data['HTGE']) * stats.poisson.pmf(3, data['ATGE'])
    data['five_three'] = stats.poisson.pmf(5, data['HTGE']) * stats.poisson.pmf(3, data['ATGE'])
    # home team away team to score four
    data['one_four'] = stats.poisson.pmf(1, data['HTGE']) * stats.poisson.pmf(4, data['ATGE'])
    data['two_four'] = stats.poisson.pmf(2, data['HTGE']) * stats.poisson.pmf(4, data['ATGE'])
    data['three_four'] = stats.poisson.pmf(3, data['HTGE']) * stats.poisson.pmf(4, data['ATGE'])
    data['four_four'] = stats.poisson.pmf(4, data['HTGE']) * stats.poisson.pmf(4, data['ATGE'])
    data['five_four'] = stats.poisson.pmf(5, data['HTGE']) * stats.poisson.pmf(4, data['ATGE'])
    # home team away team to score five
    data['one_five'] = stats.poisson.pmf(1, data['HTGE']) * stats.poisson.pmf(5, data['ATGE'])
    data['two_five'] = stats.poisson.pmf(2, data['HTGE']) * stats.poisson.pmf(5, data['ATGE'])
    data['three_five'] = stats.poisson.pmf(3, data['HTGE']) * stats.poisson.pmf(5, data['ATGE'])
    data['four_five'] = stats.poisson.pmf(4, data['HTGE']) * stats.poisson.pmf(5, data['ATGE'])
    data['five_five'] = stats.poisson.pmf(5, data['HTGE']) * stats.poisson.pmf(5, data['ATGE'])
    data['home_win'] = data['one_nil'] + data['two_nil'] + data['three_nil'] + data['four_nil'] + data['five_nil'] + \
                       data['two_one'] + data['three_one'] + data['four_one'] + data['five_one'] + data['three_two'] + \
                       data['four_two'] + data['five_two'] + data['four_three'] + data['five_three'] + data['five_four']
    data['draw'] = data['nil_nil'] + data['one_one'] + data['two_two'] + data['three_three'] + data['four_four'] + data[
        'five_five']
    data['away_win'] = 1 - (
            data['home_win'] + data['draw'])
    data['Fixture'] = data['HomeTeam'] + ' vs. ' + data['AwayTeam']
    data.to_csv("test.csv", index=False)
    return data


path_set = 'C://tmp//'
betting_data().to_csv(path_set + 'results_today.csv', index=False)
