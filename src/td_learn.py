import arena
from direction import Direction, move
from pprint import pprint
import random
import mini_expecti_max
import agent
import game


EXPLORE_EPSILON = 0.03
LEARNING_RATE = 0.002

GAMMA = 0.6


def dot(v, w):
    r = 0
    for key in v:
        r += v[key] * w[key]
    return r


def init_weights(feature_extractor):
    w = {}
    a = arena.Arena(10, 10, 10)
    a.add_agent(agent.RandomAgent('A', arena.MAX_AGENT),
                arena.MAX_AGENT, (1, 1))
    a.add_agent(agent.RandomAgent('B', arena.MIN_AGENT),
                arena.MIN_AGENT, (8, 8))
    a.curr_agent = arena.MAX_AGENT
    features = feature_extractor(a)
    for key in features:
        w[key] = 0
    return w


def dist_features(a):
    if a.curr_agent != arena.MAX_AGENT:
        print(f'[WARN] td_learn.dist_features called on not MAX_AGENT')

    agent = a.curr_agent
    start_pos = a.pos[agent]
    other_agent = a.other_agent(agent)

    features = {
        'dist_to_own_territory': mini_expecti_max.arena_bfs(
            a, start_pos,
            a.territory[agent], a.trail[agent]
        ),
        'dist_to_adversary_trail': mini_expecti_max.arena_bfs(
            a,
            start_pos,
            a.trail[other_agent],
            a.trail[agent]
        ),
        'adversary_dist_to_own_trail': mini_expecti_max.arena_bfs(
            a,
            a.pos[other_agent],
            a.trail[agent],
            a.trail[other_agent],
        ),
        'adversary_dist_to_adversary_territory': mini_expecti_max.arena_bfs(
            a,
            a.pos[other_agent],
            a.territory[other_agent],
            a.trail[other_agent],
        ),
        'territory_size': a.get_territory_size(agent),
    }

    arena_max_dist = a.width + a.height
    if features['dist_to_own_territory'] == None:
        features['dist_to_own_territory'] = arena_max_dist
    if features['dist_to_adversary_trail'] == None:
        features['dist_to_adversary_trail'] = arena_max_dist
    if features['adversary_dist_to_own_trail'] == None:
        features['adversary_dist_to_own_trail'] = a.height
    if features['adversary_dist_to_adversary_territory'] == None:
        features['adversary_dist_to_adversary_territory'] = 0

    features['trail_size'] = len(a.trail[agent])
    features['adversary_trail_size'] = len(a.trail[other_agent])

    features['num_tick_remain'] = a.remaining_ticks

    row, col = start_pos
    dist_from_wall = [
        abs(row), abs(col), abs(row-a.height), abs(col-a.width)
    ]
    features['min_dist_from_wall'] = min(dist_from_wall)

    features['is_self_win'] = 100 if a.winner == arena.MAX_AGENT else 0
    features['is_adversary_win'] = 100 if a.winner == arena.MIN_AGENT else 0

    return features


def get_max_value_dir(a, w, feature_extractor):
    if a.curr_agent != arena.MAX_AGENT:
        print(f'[WARN] td_learn.get_max_move_value called on not MAX_AGENT')

    # epsilon greedy exploration
    if random.uniform(0, 1) < EXPLORE_EPSILON:
        return (-a.width * a.height, random.choice(Direction.ALL_DIRS))

    directions = a.get_valid_move_dirs(a.curr_agent)
    if len(directions) == 0:
        return (-a.width * a.height, random.choice(Direction.ALL_DIRS))

    value_direction = []
    for direction in directions:
        succ = a.get_full_arena_copy()
        succ.move_agent(succ.curr_agent, direction)
        succ.curr_agent = arena.MAX_AGENT

        succ_features = feature_extractor(succ)
        v = dot(succ_features, w)
        value_direction.append((v, direction))

    value_direction = sorted(value_direction, key=lambda x: x[0])
    return value_direction[-1]


def update_weight(episode, util, w, feature_extractor):
    new_weights = {}

    for i in range(len(episode) - 1):
        curr = episode[i]
        curr_feat = feature_extractor(curr)
        succ = episode[i + 1]
        succ.curr_agent = arena.MAX_AGENT
        succ_feat = feature_extractor(succ)

        reward = util if succ.is_end() else 0
        v_curr = dot(curr_feat, w)
        # maybe v_succ needs not to be 0 for end state
        v_succ = dot(succ_feat, w)

        for key in w:
            new_weights[key] = w[key] - (
                LEARNING_RATE *
                (v_curr - (reward + GAMMA * v_succ)) *
                curr_feat[key]
            )

    for key in new_weights:
        w[key] = new_weights[key]
