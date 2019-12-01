import agent
import direction
import mini_expecti_max
import arena
import td_learn
import curses
import game
import time

SLEEP_TIME = 0
WINNER_ANNOUNCE_TIME = 5


def init():
    window = curses.initscr()
    curses.cbreak()
    window.keypad(True)
    return window


def teardown(window):
    curses.nocbreak()
    window.keypad(False)
    curses.endwin()


def add_str_block(y, x, s, window):
    for line in s.split('\n'):
        window.addstr(y, x, line)
        y += 1


def render(g, window):
    window.clear()

    loser = None
    if g.arena.is_end() and g.arena.winner != None:
        loser = g.arena.other_agent(g.arena.winner)
        g.arena.pos[loser] = None
        g.arena.trail[loser] = set()
        g.arena.territory[loser] = set()

    add_str_block(3, 10, '[ Legend ]', window)
    add_str_block(5, 10, '            MAX_AGENT   MIN_AGENT', window)
    add_str_block(6, 10, 'Position       [X]         [O]', window)
    add_str_block(7, 10, '  Trail        .x.         .o.', window)
    add_str_block(8, 10, 'Territory       x           o',  window)

    add_str_block(11, 10, '[ Legal Move Direction ]', window)
    if loser != arena.MAX_AGENT:
        add_str_block(13, 10, 'MAX_AGENT', window)
        ds = g.arena.get_valid_move_dirs(arena.MAX_AGENT)
        ds = '  '.join([direction.Direction.tostring(d) for d in ds])
        add_str_block(13, 25, ds, window)
    if loser != arena.MIN_AGENT:
        add_str_block(14, 10, 'MIN_AGENT', window)
        ds = g.arena.get_valid_move_dirs(arena.MIN_AGENT)
        ds = '  '.join([direction.Direction.tostring(d) for d in ds])
        add_str_block(14, 25, ds, window)

    add_str_block(3, 60, '[ Arena god view ]', window)
    add_str_block(5, 60, str(g.arena), window)

    add_str_block(3, 110, '[ Arena state ]', window)
    add_str_block(5, 110, f'vision_radius : {g.vision_radius}', window)
    add_str_block(6, 110, f'shape : {(g.arena.height, g.arena.width)}', window)
    add_str_block(
        7, 110, f'remaining_ticks : {g.arena.remaining_ticks}', window)

    add_str_block(
        9, 110, f'MAX_AGENT territory size : {len(g.arena.territory[arena.MAX_AGENT])}', window)
    add_str_block(
        10, 110, f'MIN_AGENT territory size : {len(g.arena.territory[arena.MIN_AGENT])}', window)

    add_str_block(
        12, 110, f'MAX_AGENT trail size : {len(g.arena.trail[arena.MAX_AGENT])}', window)
    add_str_block(
        13, 110, f'MIN_AGENT trail size : {len(g.arena.trail[arena.MIN_AGENT])}', window)

    if loser != arena.MAX_AGENT:
        add_str_block(
            20, 10, f'[ MAX_AGENT : {type(g.arena.agent[arena.MAX_AGENT]).__name__} ]', window)
        add_str_block(
            22, 10, str(g.arena.get_observable_arena(arena.MAX_AGENT, g.vision_radius)), window)

    if loser != arena.MIN_AGENT:
        add_str_block(
            20, 60, f'[ MIN_AGENT : {type(g.arena.agent[arena.MIN_AGENT]).__name__} ]', window)
        add_str_block(
            22, 60, str(g.arena.get_observable_arena(arena.MIN_AGENT, g.vision_radius)), window)

        if g.arena.agent[arena.MIN_AGENT].__class__ == agent.HumanAgent:
            add_str_block(
                33, 60, 'Human agent: use arrows to move ...', window)

    if g.arena.is_end():
        add_str_block(20, 110, '[ Winner ]', window)

        winner_str = 'Tie'
        if g.arena.utility() > 0:
            winner_str = 'MAX_AGENT'
        elif g.arena.utility() < 0:
            winner_str = 'MIN_AGENT'

        add_str_block(
            22, 110, f'Winner : {winner_str}', window)
        add_str_block(
            23, 110, f'Win condition : {"Elimination" if g.arena.winner != None else "Timeout"}', window)
        add_str_block(
            24, 110, f'Utility : {g.arena.utility()}', window)

    add_str_block(33, 140, ' ', window)

    window.refresh()


def run_game(g, window):
    render(g, window)

    while True:
        time.sleep(SLEEP_TIME)
        render(g, window)

        g.tick(quiet=True)
        if g.arena.is_end():
            break
        g.tick(quiet=True)
        if g.arena.is_end():
            break

    render(g, window)

    time.sleep(WINNER_ANNOUNCE_TIME)


if __name__ == "__main__":
    window = init()
    try:
        g = game.Game(7, 7, max_ticks=60, vision_radius=2)
        # max_agent = agent.MinimaxAgent(
        #     'X',
        #     arena.MAX_AGENT,
        #     mini_expecti_max.eval_pure_builder,
        #     4
        # )
        max_agent = agent.get_td_agent(
            'X', arena.MAX_AGENT, 'td_train_output/td_minimax_2_pure.json', td_learn.dist_features)
        g.add_agent(max_agent, arena.MAX_AGENT, (1, 1), 1)
        # min_agent = agent.MinimaxAgent(
        #     'O',
        #     arena.MIN_AGENT,
        #     mini_expecti_max.eval_pure_builder,
        #     4
        # )
        min_agent = agent.HumanAgent('O', arena.MIN_AGENT, window)
        g.add_agent(min_agent, arena.MIN_AGENT, (5, 5), 1)

        run_game(g, window)
    except:
        raise
    finally:
        teardown(window)
