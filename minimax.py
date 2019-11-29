import arena
from direction import Direction, move
from pprint import pprint


def min_dist(arena, start_pos, to_find, to_go_around):
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


def evaluation_factors(agent_char, arena):
    own_pos = arena.agent_pos[agent_char]
    own_territory_pos = arena.agent_territory[agent_char]
    own_trail_pos = arena.agent_trails[agent_char]

    adversary_trail_pos = set()
    for ch in arena.agent_trails:
        if ch == agent_char:
            continue
        for pos in arena.agent_trails[ch]:
            adversary_trail_pos.add(pos)

    adversary_to_own_trail_dist = None
    for adversary in arena.agent_pos:
        if adversary == agent_char:
            continue
        dist = min_dist(
            arena, arena.agent_pos[adversary],
            own_trail_pos, arena.agent_trails[adversary]
        )
        if adversary_to_own_trail_dist == None or dist < adversary_to_own_trail_dist:
            adversary_to_own_trail_dist = dist

    result = {
        'dist_to_own_territory': min_dist(
            arena, own_pos, own_territory_pos, own_trail_pos
        ),
        'dist_to_adversary_trail': min_dist(
            arena, own_pos, adversary_trail_pos, own_trail_pos
        ),
        'dist_adversary_to_own_trail': adversary_to_own_trail_dist,
        'territory_size': arena.get_territory_size(agent_char),
        'own_trail_length': len(own_trail_pos),
    }

    return result


def eval_naive_builder(agent_char, arena):
    factors = evaluation_factors(agent_char, arena)

    if agent_char in arena.dead_agents:
        factors['value'] = float('-inf')
        return factors
    if len(arena.agent_pos) - len(arena.dead_agents) <= 1 and \
            agent_char not in arena.dead_agents:
        factors['value'] = float('inf')
        return factors

    factors['value'] = factors['territory_size']

    return factors


def minimax(agents, curr_agent_idx, arena, eval_func, depth):
    if depth == 0:
        return eval_func(agents[-1], arena)
    curr_agent = agents[curr_agent_idx]

    values = {}
    for direction in Direction.ALL_DIRS:

        arena_copy = arena.get_full_arena_copy()
        arena_copy.move_agent(curr_agent, direction)

        next_agent_idx = (curr_agent_idx + 1) % len(agents)
        new_depth = depth-1 if next_agent_idx == len(agents)-1 else depth

        result = minimax(
            agents, next_agent_idx, arena_copy, eval_func, new_depth
        )
        values[direction] = result

    is_max_agent = curr_agent_idx == len(agents)-1
    if is_max_agent:
        opt_value = float('-inf')
        opt_result = None
        for direction in Direction.ALL_DIRS:
            if values[direction]['value'] > opt_value:
                opt_value = values[direction]['value']
                opt_result = values[direction]
        return opt_result
    else:
        opt_value = float('inf')
        opt_result = None
        for direction in Direction.ALL_DIRS:
            if values[direction]['value'] < opt_value:
                opt_value = values[direction]['value']
                opt_result = values[direction]
        return opt_result
