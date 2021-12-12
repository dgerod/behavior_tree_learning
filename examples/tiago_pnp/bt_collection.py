_scenario_1 = ['f(',
               'task_done?',
                    's(',
                        'localise!',
                        'head [up]!',
                        'f(',
                            'have_block?',
                            's(',
                                'arm [tucked]!',
                                'move_to_pick [0]!',
                            ')',
                        ')',
                    'head [down]!',
                    'pick!',
                    'move_to_place!',
                    'place!',
                    ')',
               ')']


def select_bt(name: str):
    collection = {'scenario_1': _scenario_1}
    return collection[name]
