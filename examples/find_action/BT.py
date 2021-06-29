behavior_tree_1 = ['s(',
                       'CHECK_anchored(gear_1: gear)',
                       'DO_move_arm_to(E: place)',
                   ')']

behavior_tree_2 = ['f(',
                       'CHECK_anchored[gear_1: gear]',
                       's(',
                            'DO_move_arm_to[E: place]',
                            'DO_retrive_objects[] => [objects]',                            
                        ')',
                   ')']
