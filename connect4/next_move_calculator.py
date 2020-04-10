import copy
from utils import time_func


class Global:
    NUM_CACHES = 0
    NUM_EXTENSIONS = 0
    NUM_CALCULATIONS = 0

    @classmethod
    def reset(cls):
        cls.NUM_CACHES = 0
        cls.NUM_EXTENSIONS = 0
        cls.NUM_CALCULATIONS = 0


@time_func
def calc_next_move(board, player, depth):
    Global.reset()
    new_board = copy.deepcopy(board)
    score_tree = _calc_leaves(new_board, player, depth)
    if player.num == 1:
        suggested_entry = max(score_tree.keys(), key=lambda x: score_tree[x]['Base'])
    else:
        suggested_entry = min(score_tree.keys(), key=lambda x: score_tree[x]['Base'])
    print('Num extensions: {}'.format(Global.NUM_EXTENSIONS))
    print('Num calculations: {}'.format(Global.NUM_CALCULATIONS))
    print('Num caches: {}'.format(Global.NUM_CACHES))
    return suggested_entry


def _calc_score_from_leaves(leaf_scores, player):
    if player.num == 1:
        return min(value['Base'] for value in leaf_scores.values())
    else:
        return max(value['Base'] for value in leaf_scores.values())


def _calc_leaves(base_board, player, depth, curr_depth=1, alpha_above=None, beta_above=None, cache=None):
    if cache is None:
        cache = {}
    score_dict = {}
    alpha_this_level = alpha_above
    beta_this_level = beta_above
    for entry in base_board.valid_moves():
        score_dict[entry] = {}
        h_board = copy.deepcopy(base_board)
        h_board.add_counter(entry, player)
        if (h_board.id(), curr_depth) not in cache:
            if curr_depth < depth and h_board.winner is None:
                Global.NUM_EXTENSIONS += 1
                score_dict[entry]['Next_level'] = _calc_leaves(h_board, player.next_player(), depth, curr_depth=curr_depth + 1,
                                                               alpha_above=alpha_this_level, beta_above=beta_this_level,
                                                               cache=cache)
            if curr_depth == depth or h_board.winner:
                Global.NUM_CALCULATIONS += 1
                score_dict[entry]['Base'] = h_board.score
                if player.num == 1:
                    if beta_above:
                        if score_dict[entry]['Base'] > beta_above:
                            break
                if player.num == 2:
                    if alpha_above:
                        if score_dict[entry]['Base'] < alpha_above:
                            break
            else:
                if len(score_dict[entry]['Next_level']) > 0:
                    Global.NUM_CALCULATIONS += 1
                    score_dict[entry]['Base'] = _calc_score_from_leaves(score_dict[entry]['Next_level'], player)
                else:
                    score_dict[entry]['Base'] = 0
            cache[(h_board.id(), curr_depth)] = score_dict[entry]
        else:
            score_dict[entry] = cache[(h_board.id(), curr_depth)]
            Global.NUM_CACHES += 1

        # Set alpha and beta
        # if player.num == 1:
        #     if alpha_this_level is None:
        #         alpha_this_level = score_dict[entry]['Base']
        #     else:
        #         alpha_this_level = min(score_dict[entry]['Base'], alpha_this_level)
        # else:
        #     if beta_this_level is None:
        #         beta_this_level = score_dict[entry]['Base']
        #     else:
        #         beta_this_level = max(score_dict[entry]['Base'], beta_this_level)
    return score_dict















