from time import perf_counter
from .utils import time_func
from random import randint
from copy import deepcopy
from copy import copy

# TODO - add testing that cache and alpha beta do not change the result for different player_1 sequences
class Global:
    NUM_CACHES = 0
    NUM_EXTENSIONS = 0
    NUM_CALCULATIONS = 0

    @classmethod
    def reset(cls):
        cls.NUM_CACHES = 0
        cls.NUM_EXTENSIONS = 0
        cls.NUM_CALCULATIONS = 0


class Node:
    def __init__(self, board, player, alpha=None, beta=None, cache=None):
        self.board = board
        self.player = player
        self.id = '{}-{}'.format(board.id(), player.num)
        self.leaves = {}
        self.node_score = None
        self.node_alpha = alpha
        self.node_beta = beta
        self.next_move = None
        if cache is None:
            self.cache = {}
        else:
            self.cache = cache

    def update_cache(self, depth_of_calc):
        self.cache[self.id] = {'depth of calc': depth_of_calc, 'node': self}

    def load_scores_from_cache(self, depth_of_calc):
        if self.id in self.cache:
            if self.cache[self.id]['depth of calc'] == depth_of_calc:
                cache_node = self.cache[self.id]['node']
                self.leaves = cache_node.leaves
                self.node_score = cache_node.node_score
                self.next_move = cache_node.next_move
                Global.NUM_CACHES += 1
                return True
        return False

    def node_leaves(self):
        return self.board.valid_moves()

    def update_alpha_beta(self, score):
        if self.player.num == 1:
            if self.node_alpha:
                self.node_alpha = max(self.node_alpha, score)
            else:
                self.node_alpha = score

        else:
            if self.node_beta:
                self.node_beta = min(self.node_beta, score)
            else:
                self.node_beta = score

    def update_alpha_beta_for_parent_values(self, parent_alpha, parent_beta):
        self.node_alpha = parent_alpha
        self.node_beta = parent_beta

    def within_alpha_beta(self, score):
        if self.player.num == 1:
            if self.node_beta:
                return score <= self.node_beta
            else:
                return True
        if self.player.num == 2:
            if self.node_alpha:
                return score >= self.node_alpha
            else:
                return True

    def calc_leaves_of_the_node(self, target_depth, rel_depth):
        start_time = perf_counter()
        for leaf in self.node_leaves():
            num = randint(0, 1000000)
            # print('{}: *** start (leaf {}):- {}'.format(num, leaf, perf_counter() - start_time))
            leaf_board = self.board.create_child_board()
            # print('{}: create child board:- {}'.format(num, perf_counter() - start_time))
            leaf_board.add_counter(leaf, self.player)
            # print('{}: play move:- {}'.format(num, perf_counter() - start_time))
            leaf_node = Node(leaf_board, self.player.next_player(), alpha=self.node_alpha, beta=self.node_beta,
                                     cache=self.cache)
            # print('{}: create new node (cache empty: {}):- {}'.format(num, len(leaf_node.cache) == 0, perf_counter() - start_time))
            leaf_node.update_alpha_beta_for_parent_values(self.node_alpha, self.node_beta)
            # print('{}: update alpha beta parent:- {}'.format(num, perf_counter() - start_time))
            leaf_node.calc_next_move_and_score(target_depth, rel_depth=rel_depth + 1)
            # print('{}: next next move and score:- {}'.format(num, perf_counter() - start_time))
            self.update_alpha_beta(leaf_node.node_score)
            # print('{}: update alpha beta:- {}'.format(num, perf_counter() - start_time))
            self.leaves[leaf] = leaf_node
            if not self.within_alpha_beta(leaf_node.node_score):
                break
            # print('{}: check alpha beta:- {}'.format(num, perf_counter() - start_time))

    def calc_node_no_extension(self):
        return self.board.score

    def calc_next_move_and_score(self, target_depth, rel_depth=0):
        start_time = perf_counter()
        num = randint(0, 1000000)
        # print('A{}: *** start:- {}'.format(num, perf_counter() - start_time))
        score_cache_success = self.load_scores_from_cache(target_depth - rel_depth)
        # print('A{}: load cache:- {}'.format(num, perf_counter() - start_time))
        if not score_cache_success:
            if rel_depth == target_depth or self.board.winner:
                Global.NUM_CALCULATIONS += 1
                self.node_score = self.calc_node_no_extension()
                # print('A{}: calc no cache:- {}'.format(num, perf_counter() - start_time))
                self.update_cache(target_depth - rel_depth)
                # print('A{}: update cache:- {}'.format(num, perf_counter() - start_time))
            elif rel_depth < target_depth:
                Global.NUM_EXTENSIONS += 1
                self.calc_leaves_of_the_node(target_depth, rel_depth)
                # print('A{}: calc leaves of the node:- {}'.format(num, perf_counter() - start_time))
                self.next_move = self.player.max_min()(self.leaves, key=lambda x: self.leaves[x].node_score)
                # print('A{}: calc next move:- {}'.format(num, perf_counter() - start_time))
                Global.NUM_CALCULATIONS += 1
                self.node_score = self.leaves[self.next_move].node_score
                # print('A{}: calc score:- {}'.format(num, perf_counter() - start_time))
                self.update_cache(target_depth-rel_depth)
                # print('A{}: update cache:- {}'.format(num, perf_counter() - start_time))
            else:
                raise Exception("Depth of calculation has exceed target depth")


@time_func
def calc_next_move(board, player, depth, tree=None):
    Global.reset()
    if tree is None:
        tree = Node(board, player)
    else:
        tree = Node(board, player, cache=tree.cache)
    tree.calc_next_move_and_score(depth)
    print('Num extensions: {}'.format(Global.NUM_EXTENSIONS))
    print('Num calculations: {}'.format(Global.NUM_CALCULATIONS))
    print('Num tree score caches: {}'.format(Global.NUM_CACHES))
    return tree, tree.next_move


