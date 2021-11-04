import json

def get_stats(file, plays, noredzone, redzone, goalline, formations, men_box, pass_rush, down_conversion,
              drive_conversion):
    f = open(file)
    game = json.load(f)
    periods = game['periods']

    # 0 rush, 1 pass, 2 total, 3 punt, 4 field goal
    hou_plays = plays
    hou_noredzone = noredzone
    hou_redzone = redzone
    hou_goalline = goalline
    hou_formations = formations
    hou_men_box = men_box
    hou_pass_rush = pass_rush
    hou_down_conversion = down_conversion
    hou_drive_conversion = drive_conversion

    for quarter in periods:
        pbp = quarter['pbp']
        for value in pbp:
            if value['type'] == 'drive':
                for event in value['events']:

                    if event['type'] == 'play':
                        if event['start_situation']['possession']['name'] == 'Texans':
                            hou_drive_conversion[1] += 1
                            if value['end_reason'] == 'Touchdown':
                                hou_drive_conversion[0] += 1
                            yfd = event['start_situation']['yfd']
                            if event['play_type'] != 'penalty':
                                stats = event['statistics'][0]
                                down = str(event['start_situation']['down'])
                                end_down = str(event['end_situation']['down'])
                                if str(down) in hou_down_conversion.keys():
                                    hou_down_conversion[str(down)][1] += 1
                                    if end_down == '1':
                                        hou_down_conversion[str(down)][0] += 1

                                if str(down) in hou_plays.keys():
                                    hou_plays[str(down)][2] += 1
                                if event['play_type'] == 'rush':

                                    if stats['kneel_down'] != 1:

                                        index = 0
                                        if stats['scramble'] == 1:
                                            index = 1
                                        hou_plays[str(down)][index] += 1

                                        if 'qb_at_snap' in event.keys():
                                            if event['qb_at_snap'] not in hou_formations.keys():
                                                hou_formations[event['qb_at_snap']] = [0, 0, 0]
                                                hou_formations[event['qb_at_snap']][0] += 1
                                                hou_formations[event['qb_at_snap']][2] += 1
                                            else:
                                                hou_formations[event['qb_at_snap']][0] += 1
                                                hou_formations[event['qb_at_snap']][2] += 1

                                        if 'men_in_box' in event.keys():
                                            if str(event['men_in_box']) not in hou_men_box.keys():

                                                hou_men_box[str(event['men_in_box'])] = [0, 0, 0, 0]
                                                if 'yards' in stats.keys():
                                                    hou_men_box[str(event['men_in_box'])][0] += stats['yards']
                                                    hou_men_box[str(event['men_in_box'])][1] += 1
                                            else:
                                                hou_men_box[str(event['men_in_box'])][1] += 1
                                                if 'yards' in stats.keys():
                                                    hou_men_box[str(event['men_in_box'])][0] += stats['yards']

                                        if yfd >= 10:
                                            key = f'{str(down)} long'
                                            if stats['goaltogo'] == 1:
                                                hou_goalline[key][index] += 1
                                                hou_goalline[key][2] += 1
                                            elif stats['inside_20'] == 1:
                                                hou_redzone[key][index] += 1
                                                hou_redzone[key][2] += 1
                                            else:
                                                hou_noredzone[key][index] += 1
                                                hou_noredzone[key][2] += 1
                                        elif 5 <= yfd <= 9:
                                            key = f'{str(down)} med'
                                            if stats['goaltogo'] == 1:
                                                hou_goalline[key][index] += 1
                                                hou_goalline[key][2] += 1
                                            elif stats['inside_20'] == 1:
                                                hou_redzone[key][index] += 1
                                                hou_redzone[key][2] += 1
                                            else:
                                                hou_noredzone[key][index] += 1
                                                hou_noredzone[key][2] += 1
                                        elif 0 <= yfd <= 4:
                                            key = f'{str(down)} short'
                                            if stats['goaltogo'] == 1:
                                                hou_goalline[key][index] += 1
                                                hou_goalline[key][2] += 1
                                            elif stats['inside_20'] == 1:
                                                hou_redzone[key][index] += 1
                                                hou_redzone[key][2] += 1
                                            else:
                                                hou_noredzone[key][index] += 1
                                                hou_noredzone[key][2] += 1


                                elif event['play_type'] == 'pass':

                                    if 'qb_at_snap' in event.keys():
                                        if event['qb_at_snap'] not in hou_formations.keys():
                                            hou_formations[event['qb_at_snap']] = [0, 0, 0]
                                            hou_formations[event['qb_at_snap']][1] += 1
                                            hou_formations[event['qb_at_snap']][2] += 1
                                        else:
                                            hou_formations[event['qb_at_snap']][1] += 1
                                            hou_formations[event['qb_at_snap']][2] += 1

                                    if 'men_in_box' in event.keys():
                                        if str(event['men_in_box']) not in hou_men_box.keys():
                                            hou_men_box[str(event['men_in_box'])] = [0, 0, 0, 0]
                                            if 'yards' in stats.keys():
                                                hou_men_box[str(event['men_in_box'])][2] += stats['yards']
                                                hou_men_box[str(event['men_in_box'])][3] += 1
                                        else:
                                            hou_men_box[str(event['men_in_box'])][3] += 1
                                            if 'yards' in stats.keys():
                                                hou_men_box[str(event['men_in_box'])][2] += stats['yards']

                                    if 'players_rushed' in event.keys():

                                        if str(event['players_rushed']) not in hou_pass_rush.keys():
                                            hou_pass_rush[str(event['players_rushed'])] = [0, 0]

                                            if 'yards' in stats.keys():
                                                hou_pass_rush[str(event['players_rushed'])][0] += stats['yards']
                                                hou_pass_rush[str(event['players_rushed'])][1] += 1

                                        else:
                                            hou_pass_rush[str(event['players_rushed'])][1] += 1
                                            if 'yards' in stats.keys():
                                                hou_pass_rush[str(event['players_rushed'])][0] += stats['yards']

                                    hou_plays[str(down)][1] += 1
                                    if yfd >= 10:
                                        key = f'{str(down)} long'
                                        if stats['goaltogo'] == 1:
                                            hou_goalline[key][1] += 1
                                            hou_goalline[key][2] += 1
                                        elif stats['inside_20'] == 1:
                                            hou_redzone[key][1] += 1
                                            hou_redzone[key][2] += 1
                                        else:
                                            hou_noredzone[key][1] += 1
                                            hou_noredzone[key][2] += 1
                                    elif 5 <= yfd <= 9:
                                        key = f'{str(down)} med'
                                        if stats['goaltogo'] == 1:
                                            hou_goalline[key][1] += 1
                                            hou_goalline[key][2] += 1
                                        elif stats['inside_20'] == 1:
                                            hou_redzone[key][1] += 1
                                            hou_redzone[key][2] += 1
                                        else:
                                            hou_noredzone[key][1] += 1
                                            hou_noredzone[key][2] += 1
                                    elif 0 <= yfd <= 4:
                                        key = f'{str(down)} short'
                                        if stats['goaltogo'] == 1:
                                            hou_goalline[key][1] += 1
                                            hou_goalline[key][2] += 1
                                        elif stats['inside_20'] == 1:
                                            hou_redzone[key][1] += 1
                                            hou_redzone[key][2] += 1
                                        else:
                                            hou_noredzone[key][1] += 1
                                            hou_noredzone[key][2] += 1

                                elif event['play_type'] == 'punt':

                                    hou_plays[str(down)][3] += 1
                                    if yfd >= 10:
                                        key = f'{str(down)} long'
                                        hou_noredzone[key][3] += 1
                                        hou_noredzone[key][2] += 1
                                    elif 5 <= yfd <= 9:
                                        key = f'{str(down)} med'
                                        hou_noredzone[key][3] += 1
                                        hou_noredzone[key][2] += 1
                                    elif 0 <= yfd <= 4:
                                        key = f'{str(down)} short'
                                        hou_noredzone[key][3] += 1
                                        hou_noredzone[key][2] += 1

                                elif event['play_type'] == 'field_goal':

                                    yardline = event['details'][0]['start_location']['yardline']
                                    yardline = int(yardline)

                                    hou_plays[str(down)][4] += 1
                                    if yfd >= 10:
                                        key = f'{str(down)} long'
                                        if yardline >= 21:
                                            hou_noredzone[key][4] += 1
                                            hou_noredzone[key][2] += 1
                                        elif yardline >= 11:
                                            hou_redzone[key][4] += 1
                                            hou_redzone[key][2] += 1
                                        else:
                                            hou_goalline[key][4] += 1
                                            hou_goalline[key][2] += 1


                                    elif 5 <= yfd <= 9:
                                        key = f'{str(down)} med'

                                        if yardline >= 21:
                                            hou_noredzone[key][4] += 1
                                            hou_noredzone[key][2] += 1
                                        elif yardline >= 11:
                                            hou_redzone[key][4] += 1
                                            hou_redzone[key][2] += 1
                                        else:
                                            hou_goalline[key][4] += 1
                                            hou_goalline[key][2] += 1
                                    elif 0 <= yfd <= 4:
                                        key = f'{str(down)} short'

                                        if yardline >= 21:
                                            hou_noredzone[key][4] += 1
                                            hou_noredzone[key][2] += 1
                                        elif yardline >= 11:
                                            hou_redzone[key][4] += 1
                                            hou_redzone[key][2] += 1
                                        else:
                                            hou_goalline[key][4] += 1
                                            hou_goalline[key][2] += 1
