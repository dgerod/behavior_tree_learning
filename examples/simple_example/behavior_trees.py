bt_1 = ['s(',
            'PickGearPart',
            'MoveGearPart',
            'PlaceGearPart',
        ')']

bt_2 = ['f(',
            'PlaceGearPart',
            's(',
                'PickGearPart',
                'MoveGearPart',
                'PlaceGearPart',
            ')',
        ')']


def select_bt(idx: int):
    behavior_trees = [bt_1, bt_2]
    return behavior_trees[idx]
