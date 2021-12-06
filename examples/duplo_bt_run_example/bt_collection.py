_bt_1 = ['s(',
             'apply force 0!',
             'apply force 0!',
             'apply force 0!',
         ')']

_bt_2 = ['f(',
             '0 at pos (0.0, 0.05, 0.0)?',
             's(',
                 'pick 1!',
                 'place on 0!',
                 'pick 2!',
                 'place on 1!',
             ')',
         ')']


def select_bt(idx: int):
    collection = [_bt_1, _bt_2]
    return collection[idx]
