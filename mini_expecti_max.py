import arena
from direction import Direction, move
from pprint import pprint
import random


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


def eval_pure_builder(a, agent):
    result = {
        'territory_size': a.get_territory_size(agent),
    }
    result['value'] = result['territory_size']
    return result


UNSAFE_PENALTY = -2  # per step


def eval_builder_with_safeness(a, agent):
    start_pos = a.pos[agent]
    other_agent = a.other_agent(agent)

    result = eval_pure_builder(a, agent)

    dist_to_own_territory = arena_bfs(
        a,
        start_pos,
        a.territory[agent],
        a.trail[agent]
    )
    dist_to_adversary_trail = arena_bfs(
        a,
        start_pos,
        a.trail[other_agent],
        a.trail[agent]
    )
    adversary_dist_to_own_trail = arena_bfs(
        a,
        a.pos[other_agent],
        a.trail[agent],
        a.trail[other_agent],
    )

    if dist_to_own_territory != None and dist_to_adversary_trail != None and adversary_dist_to_own_trail != None:
        if dist_to_own_territory <= adversary_dist_to_own_trail:
            # if we can get home quicker than adversary can get to our trail, we're safe
            return result
        if adversary_dist_to_own_trail > dist_to_adversary_trail:
            # if we can kill adversary before they can kill us, we're safe
            return result

        adversary_advantage = dist_to_adversary_trail - adversary_dist_to_own_trail
        result['value'] += adversary_advantage * UNSAFE_PENALTY
    return result


def minimax(a, depth, eval_func, alpha=float('-inf'), beta=float('inf')):
    if a.is_end():
        return {
            'value': a.utility()
        }
    if depth == 0:
        results = eval_func(a, a.curr_agent)
        if a.curr_agent == arena.MIN_AGENT:
            results['value'] *= -1
        return results

    directions = a.get_valid_move_dirs(a.curr_agent)
    if len(directions) == 0:
        # dont trap yourself with tail
        return {
            'value': float('-inf' if a.curr_agent == arena.MAX_AGENT else 'inf')
        }

    minimax_values = []
    minimax_results = []
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


def expectimax(a, depth, eval_func):

    if a.is_end():
        return {
            'value': a.utility()
        }
    if depth == 0:
        results = eval_func(a, a.curr_agent)
        if a.curr_agent == arena.MIN_AGENT:
            results['value'] *= -1
        return results

    directions = a.get_valid_move_dirs(a.curr_agent)
    if len(directions) == 0:
        return {
            'value': float('-inf' if a.curr_agent == arena.MAX_AGENT else 'inf')
        }

    values = []
    results = []
    for direction in directions:
        succ = a.get_full_arena_copy()
        succ.move_agent(succ.curr_agent, direction)

        result = expectimax(succ, depth-1, eval_func)
        result['dir'] = direction
        result['dir_str'] = Direction.tostring(direction)
        results.append(result)
        values.append(result['value'])

    use_expect = (depth % 2) != 0
    if use_expect:
        return {
            'value': sum(values) / len(values)
        }

    optimal_val = max(values) \
        if a.curr_agent == arena.MAX_AGENT \
        else min(values)
    results_of_choice = []
    for i in range(len(values)):
        if values[i] == optimal_val:
            results_of_choice.append(results[i])

    return random.choice(results_of_choice)
