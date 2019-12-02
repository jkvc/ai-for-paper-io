import td_learn
import mini_expecti_max
import game
import arena
import agent
import json
import os
import sys
from pprint import pprint

NUM_EPISODE = 20000

OPPONENT_TYPE = agent.MinimaxAgent
OPPONENT_DEPTH = 4
EVAL_FUNC = mini_expecti_max.eval_pure_builder

FILENAME = 'td_minimax_2_pure_arena_772'
DEFAULT_MAX_POS = (1, 1)
ARENA_SIZE = (7, 7)
DEFAULT_MIN_POS = (ARENA_SIZE[0]-2, ARENA_SIZE[1]-2)
VISION_RADIUS = 2
MAX_TICKS = 50

DIRNAME = 'td_train_output'
WEIGHT_FILENAME = os.path.join(DIRNAME, FILENAME+'.json')
OUTCOME_RECORD_FILENAME = os.path.join(DIRNAME, FILENAME+'.outcome.json')
FEATURE_EXTRACTOR = td_learn.dist_features


def simulate_one_game(w, opponent, feature_extractor):
    g = game.Game(
        *ARENA_SIZE,
        max_ticks=MAX_TICKS,
        vision_radius=VISION_RADIUS)
    max_agent = agent.TDAgent(
        'X',
        arena.MAX_AGENT,
        w,
        feature_extractor
    )
    g.add_agent(max_agent, arena.MAX_AGENT,
                DEFAULT_MAX_POS, init_territory_radius=1)
    min_agent = opponent
    g.add_agent(min_agent, arena.MIN_AGENT,
                DEFAULT_MIN_POS, init_territory_radius=1)

    g.run(quiet=True)
    max_agent_history = []
    for i, h in enumerate(g.history):
        if h.curr_agent == arena.MAX_AGENT or i == len(g.history) - 1:
            max_agent_history.append(h)
    return (max_agent_history, g.history[-1].utility())


def load_or_init_weight():
    if os.path.exists(WEIGHT_FILENAME):
        with open(WEIGHT_FILENAME) as f:
            print(f'Loading weights from {WEIGHT_FILENAME}')
            w = json.load(f)
    else:
        print(f'Init new weights')
        w = td_learn.init_weights(FEATURE_EXTRACTOR)
    return w


if __name__ == "__main__":
    if sys.argv[1] == 'train':
        assert td_learn.EXPLORE_EPSILON != 0
        assert td_learn.LEARNING_RATE != 0
    elif sys.argv[1] == 'play':
        td_learn.EXPLORE_EPSILON = 0
        td_learn.LEARNING_RATE = 0
    else:
        print('Usage: python td_train.py train|play')

    w = load_or_init_weight()

    outcomes = []
    if os.path.exists(OUTCOME_RECORD_FILENAME):
        with open(OUTCOME_RECORD_FILENAME) as f:
            outcomes = json.load(f)

    for i in range(NUM_EPISODE):
        episode, util = simulate_one_game(
            w,
            OPPONENT_TYPE(
                'O',
                arena.MIN_AGENT,
                EVAL_FUNC,
                OPPONENT_DEPTH
            ),
            FEATURE_EXTRACTOR
        )

        td_learn.update_weight(episode, util, w, FEATURE_EXTRACTOR)
        print(i, util, '+'*20 if util >= 0 else '')
        outcomes.append(util)

        if i % 1000 == 0 or i == NUM_EPISODE-1:
            with open(WEIGHT_FILENAME, 'w') as f:
                json.dump(w, f)
            with open(OUTCOME_RECORD_FILENAME, 'w') as f:
                json.dump(outcomes, f)

    print('[Outcomes]')
    print(outcomes[-NUM_EPISODE:])
    print('[Average outcome]')
    print(sum(outcomes[-NUM_EPISODE:]) / len(outcomes[-NUM_EPISODE:]))
