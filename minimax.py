import arena
from direction import Direction, move
from pprint import pprint
import random


def arena_end_utility(a):
    if a.winner == None:
        print('[WARN] arena_end_utility called not is_end')
        return 0
    elif a.winner == arena.MAX_AGENT:
        return float('inf')
    elif a.winner == arena.MIN_AGENT:
        return float('-inf')

    return None


def arena_bfs(arena, start_pos, to_find, to_go_around):
    touched = set()
    queue = [(start_pos, 0)]
    while queue:
        pos, dist = queue.pop(0)
        if pos in touched:
            continue
        touched.add(pos)

        if pos == None:
            continue
        if not arena.is_within_bounds(*pos):
            continue
        if pos in to_find:
            return dist

        for newpos in [
            move(pos, Direction.LEFT),
            move(pos, Direction.RIGHT),
            move(pos, Direction.UP),
            move(pos, Direction.DOWN),
        ]:
            if newpos not in to_go_around:
                queue.append((newpos, dist + 1))
    return None


def arena_features(arena, agent):
    start_pos = arena.pos[agent]
    other_agent = arena.other_agent(agent)

    result = {
        # 'dist_to_own_territory': arena_bfs(
        #     arena,
        #     start_pos,
        #     arena.territory[agent],
        #     arena.trail[agent]
        # ),
        # 'dist_to_adversary_trail': arena_bfs(
        #     arena,
        #     start_pos,
        #     arena.trail[other_agent],
        #     arena.trail[agent]
        # ),
        # 'adversary_dist_to_own_trail': arena_bfs(
        #     arena,
        #     arena.pos[other_agent],
        #     arena.trail[agent],
        #     arena.trail[other_agent],
        # ),
        'territory_size': arena.get_territory_size(agent),
        'own_trail_length': len(arena.trail[agent]),
    }

    return result


def eval_builder(a, agent):
    features = arena_features(a, agent)
    features['value'] = features['territory_size']

    if agent == arena.MIN_AGENT:
        features['value'] *= -1

    return features


def minimax(a, depth, eval_func, alpha=float('-inf'), beta=float('inf')):
    if a.is_end():
        return {
            'value': arena_end_utility(a)
        }
    if depth == 0:
        return eval_func(a, a.curr_agent)

    directions = a.get_valid_move_dirs(a.curr_agent)
    if len(directions) == 0:
        return {
            'value': float('-inf' if a.curr_agent == arena.MAX_AGENT else 'inf')
        }

    minimax_values = []
    minimax_results = []
    minimax_dirs = []
    for direction in directions:
        succ = a.get_full_arena_copy()
        succ.move_agent(succ.curr_agent, direction)

        results = minimax(succ, depth-1, eval_func, alpha, beta)
        results['dir'] = direction
        results['dir_str'] = Direction.tostring(direction)
        minimax_results.append(results)
        minimax_values.append(results['value'])

        if a.curr_agent == arena.MAX_AGENT:
            if results['value'] > beta:
                return {'value': float('inf')}
            alpha = max(alpha, results['value'])
        elif a.curr_agent == arena.MIN_AGENT:
            if results['value'] < alpha:
                return {'value': float('-inf')}
            beta = min(beta, results['value'])

    optimal_val = max(minimax_values) \
        if a.curr_agent == arena.MAX_AGENT \
        else min(minimax_values)
    results_of_choice = []
    for i in range(len(minimax_values)):
        if minimax_values[i] == optimal_val:
            results_of_choice.append(minimax_results[i])

    return random.choice(results_of_choice)
