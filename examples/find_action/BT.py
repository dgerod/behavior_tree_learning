behavior_tree_1 = ['s(',
                       'CHECK_picked(gear_1: gear)',
                       'DO_move_arm_to(E: place)',
                   ')']

behavior_tree_2 = ['f(',
                       'CHECK_picked[gear_1: gear]',
                       's(',
                            'DO_move_arm_to[A: place]',
                            'DO_move_arm_to[B: place]',
                            'DO_move_arm_to[C: place]',
                            'DO_move_arm_to[D: place]',
                        ')',
                   ')']
