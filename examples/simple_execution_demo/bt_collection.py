_bt_1 = ['s(',
             'DO_PickGearPart[]',
             'DO_MoveGearPart[P: place]',
             'DO_PlaceGearPart[]',
         ')']

_bt_2 = ['f(',
             'CHECK_GearPartPlaced[]',
             's(',
                 'DO_PickGearPart[]',
                 'DO_MoveGearPart[P: place]',
                 'DO_PlaceGearPart[]',
             ')',
         ')']


def select_bt(idx: int):
    collection = [_bt_1, _bt_2]
    return collection[idx]
