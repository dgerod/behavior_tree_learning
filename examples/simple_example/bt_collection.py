_bt_1 = ['s(',
             'PickGearPart',
             'MoveGearPart',
             'PlaceGearPart',
         ')']

_bt_2 = ['f(',
             'PlaceGearPart',
             's(',
                 'PickGearPart',
                 'MoveGearPart',
                 'PlaceGearPart',
             ')',
         ')']


def select_bt(idx: int):
    collection = [_bt_1, _bt_2]
    return collection[idx]
