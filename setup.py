import pandas as pd
from main_func import get_stats


def setup_df():
    hou_plays = {'1': [0, 0, 0, 0, 0], '2': [0, 0, 0, 0, 0], '3': [0, 0, 0, 0, 0], '4': [0, 0, 0, 0, 0]}
    hou_noredzone = {'1 long': [0, 0, 0, 0, 0], '1 med': [0, 0, 0, 0, 0], '1 short': [0, 0, 0, 0, 0],
                     '2 long': [0, 0, 0, 0, 0], '2 med': [0, 0, 0, 0, 0], '2 short': [0, 0, 0, 0, 0],
                     '3 long': [0, 0, 0, 0, 0], '3 med': [0, 0, 0, 0, 0], '3 short': [0, 0, 0, 0, 0],
                     '4 long': [0, 0, 0, 0, 0], '4 med': [0, 0, 0, 0, 0], '4 short': [0, 0, 0, 0, 0]}
    hou_redzone = {'1 long': [0, 0, 0, 0, 0], '1 med': [0, 0, 0, 0, 0], '1 short': [0, 0, 0, 0, 0],
                   '2 long': [0, 0, 0, 0, 0], '2 med': [0, 0, 0, 0, 0], '2 short': [0, 0, 0, 0, 0],
                   '3 long': [0, 0, 0, 0, 0], '3 med': [0, 0, 0, 0, 0], '3 short': [0, 0, 0, 0, 0],
                   '4 long': [0, 0, 0, 0, 0], '4 med': [0, 0, 0, 0, 0], '4 short': [0, 0, 0, 0, 0]}
    hou_goalline = {'1 long': [0, 0, 0, 0, 0], '1 med': [0, 0, 0, 0, 0], '1 short': [0, 0, 0, 0, 0],
                    '2 long': [0, 0, 0, 0, 0], '2 med': [0, 0, 0, 0, 0], '2 short': [0, 0, 0, 0, 0],
                    '3 long': [0, 0, 0, 0, 0], '3 med': [0, 0, 0, 0, 0], '3 short': [0, 0, 0, 0, 0],
                    '4 long': [0, 0, 0, 0, 0], '4 med': [0, 0, 0, 0, 0], '4 short': [0, 0, 0, 0, 0]}
    formations = {}

    men_box = {}
    pass_rush = {}
    drive_conversion = [0, 0]

    down_conversion = {'1': [0, 0], '2': [0, 0], '3': [0, 0]}

    for i in range(1, 17):
        file = f'Hou 2020 Games/2020 Hou Game {i}.json'
        get_stats(file, hou_plays, hou_noredzone, hou_redzone, hou_goalline, formations, men_box, pass_rush,
                  down_conversion, drive_conversion)

    play_list = [hou_noredzone, hou_redzone, hou_goalline]

    play_df = pd.DataFrame.from_dict(hou_plays)
    play_df.rename(index={0: 'Run', 1: 'Pass', 2: 'Total', 3: 'Punt', 4: 'Field Goal'}, inplace=True)
    play_df = (play_df / play_df.iloc[2]) * 100
    play_df = play_df.drop(['Total'])
    play_df = play_df.stack().reset_index(level=1, name='Percentage').rename(columns={'level_1': 'Down'})
    play_df = play_df.reset_index().rename(columns={'index': 'Play Type'})

    output_play_list = []
    for value in play_list:
        df = pd.DataFrame.from_dict(value)
        df.rename(index={0: 'Run', 1: 'Pass', 2: 'Total', 3: 'Punt', 4: 'Field Goal'}, inplace=True)
        df = (df / df.iloc[2]) * 100
        df = df.fillna(0)
        df = df.drop('Total')
        df = df.stack().reset_index(level=1, name='Percentage').rename(columns={'level_1': 'Down'})
        df = df.reset_index().rename(columns={'index': 'Play Type'})
        mask1 = df['Down'].str.contains('1')
        mask2 = df['Down'].str.contains('2')
        mask3 = df['Down'].str.contains('3')
        mask4 = df['Down'].str.contains('4')
        df1 = df[mask1]
        df2 = df[mask2]
        df3 = df[mask3]
        df4 = df[mask4]
        final_list = [df1, df2, df3, df4]
        output_play_list.append(final_list)

    form_df = pd.DataFrame.from_dict(formations)
    form_df.rename(index={0: 'Run', 1: 'Pass', 2: 'Total'}, inplace=True)
    form_df = (form_df / form_df.iloc[2]) * 100
    form_df = form_df.drop(['Total'])
    form_df = form_df.stack().reset_index(level=1, name='Percentage').rename(columns={'level_1': 'Formation'})
    form_df = form_df.reset_index().rename(columns={'index': 'Play Type'})

    men_df = pd.DataFrame.from_dict(men_box)
    men_df.rename(index={0: 'Run Yards', 1: 'Run Total', 2: 'Pass Yards', 3: 'Pass Total'}, inplace=True)
    men_df = men_df.reindex(sorted(men_df.columns), axis=1)
    men_df.iloc[0] = men_df.iloc[0] / men_df.iloc[1]
    men_df.iloc[2] = men_df.iloc[2] / men_df.iloc[3]
    men_df = men_df.drop(['Pass Total'])
    men_df = men_df.drop(['Run Total'])
    men_df = men_df.fillna(0)
    men_df = men_df.stack().reset_index(level=1, name='Avg Yards').rename(columns={'level_1': 'Men in Box'})
    men_df = men_df.reset_index().rename(columns={'index': 'Play Type'})

    rushed_df = pd.DataFrame.from_dict(pass_rush)
    rushed_df.rename(index={0: 'Avg Yards', 1: 'Plays'}, inplace=True)
    rushed_df = rushed_df.reindex(sorted(rushed_df.columns), axis=1)
    rushed_df = rushed_df / rushed_df.iloc[1]
    rushed_df = rushed_df.drop(['Plays'])
    rushed_df = rushed_df.stack().reset_index(level=1, name='Avg Yards').rename(columns={'level_1': 'Players Rushed'})
    rushed_df = rushed_df.reset_index().rename(columns={'index': 'Legend'})

    down_con_df = pd.DataFrame.from_dict(down_conversion)
    down_con_df.rename(index={0: 'Converted', 1: 'Drives'}, inplace=True)
    down_con_df = (down_con_df / down_con_df.iloc[1]) * 100
    down_con_df = down_con_df.drop(['Drives'])
    down_con_df = down_con_df.stack().reset_index(level=1, name='Conversion %').rename(columns={'level_1': 'Down'})
    down_con_df = down_con_df.reset_index().rename(columns={'index': 'Legend'})

    return play_df, output_play_list, form_df, men_df, rushed_df, down_con_df
