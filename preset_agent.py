import agent
import arena
import mini_expecti_max
import td_learn


PRESET_MAX_AGENTS = [
    (
        'minimax depth 1 - pure builder',
        lambda _: agent.MinimaxAgent(
            'X', arena.MAX_AGENT, mini_expecti_max.eval_pure_builder, 2
        )
    ),
    (
        'minimax depth 2 - pure builder',
        lambda _: agent.MinimaxAgent(
            'X', arena.MAX_AGENT, mini_expecti_max.eval_pure_builder, 4
        )
    ),
    (
        'minimax depth 3 - pure builder',
        lambda _: agent.MinimaxAgent(
            'X', arena.MAX_AGENT, mini_expecti_max.eval_pure_builder, 6
        )
    ),
    (
        'minimax depth 1 - safe builder',
        lambda _: agent.MinimaxAgent(
            'X', arena.MAX_AGENT, mini_expecti_max.eval_builder_with_safeness, 2
        )
    ),
    (
        'minimax depth 2 - safe builder',
        lambda _: agent.MinimaxAgent(
            'X', arena.MAX_AGENT, mini_expecti_max.eval_builder_with_safeness, 4
        )
    ),
    (
        'minimax depth 3 - safe builder',
        lambda _: agent.MinimaxAgent(
            'X', arena.MAX_AGENT, mini_expecti_max.eval_builder_with_safeness, 6
        )
    ),
    (
        'expectimax depth 1 - pure builder',
        lambda _: agent.ExpectimaxAgent(
            'X', arena.MAX_AGENT, mini_expecti_max.eval_pure_builder, 2
        )
    ),
    (
        'expectimax depth 2 - pure builder',
        lambda _: agent.ExpectimaxAgent(
            'X', arena.MAX_AGENT, mini_expecti_max.eval_pure_builder, 4
        )
    ),
    (
        'expectimax depth 3 - pure builder',
        lambda _: agent.ExpectimaxAgent(
            'X', arena.MAX_AGENT, mini_expecti_max.eval_pure_builder, 6
        )
    ),
    (
        'expectimax depth 1 - safe builder',
        lambda _: agent.ExpectimaxAgent(
            'X', arena.MAX_AGENT, mini_expecti_max.eval_builder_with_safeness, 2
        )
    ),
    (
        'expectimax depth 2 - safe builder',
        lambda _: agent.ExpectimaxAgent(
            'X', arena.MAX_AGENT, mini_expecti_max.eval_builder_with_safeness, 4
        )
    ),
    (
        'expectimax depth 3 - safe builder',
        lambda _: agent.ExpectimaxAgent(
            'X', arena.MAX_AGENT, mini_expecti_max.eval_builder_with_safeness, 6
        )
    ),
    (
        'td - trained against minimax depth 1 pure builder',
        lambda _: agent.get_td_agent(
            'X', arena.MAX_AGENT,
            'td_train_output/td_minimax_1_pure_arena_772.json', td_learn.dist_features
        )
    ),
    (
        'td - trained against minimax depth 2 pure builder',
        lambda _: agent.get_td_agent(
            'X', arena.MAX_AGENT,
            'td_train_output/td_minimax_4_pure.json', td_learn.dist_features
        )
    ),

]


PRESET_MIN_AGENTS = [
    (
        'minimax depth 1 - pure builder',
        lambda _: agent.MinimaxAgent(
            'O', arena.MIN_AGENT, mini_expecti_max.eval_pure_builder, 2
        )
    ),
    (
        'minimax depth 2 - pure builder',
        lambda _: agent.MinimaxAgent(
            'O', arena.MIN_AGENT, mini_expecti_max.eval_pure_builder, 4
        )
    ),
    (
        'minimax depth 3 - pure builder',
        lambda _: agent.MinimaxAgent(
            'O', arena.MIN_AGENT, mini_expecti_max.eval_pure_builder, 6
        )
    ),
    (
        'minimax depth 1 - safe builder',
        lambda _: agent.MinimaxAgent(
            'O', arena.MIN_AGENT, mini_expecti_max.eval_builder_with_safeness, 2
        )
    ),
    (
        'minimax depth 2 - safe builder',
        lambda _: agent.MinimaxAgent(
            'O', arena.MIN_AGENT, mini_expecti_max.eval_builder_with_safeness, 4
        )
    ),
    (
        'minimax depth 3 - safe builder',
        lambda _: agent.MinimaxAgent(
            'O', arena.MIN_AGENT, mini_expecti_max.eval_builder_with_safeness, 6
        )
    ),
    (
        'expectimax depth 1 - pure builder',
        lambda _: agent.ExpectimaxAgent(
            'O', arena.MIN_AGENT, mini_expecti_max.eval_pure_builder, 2
        )
    ),
    (
        'expectimax depth 2 - pure builder',
        lambda _: agent.ExpectimaxAgent(
            'O', arena.MIN_AGENT, mini_expecti_max.eval_pure_builder, 4
        )
    ),
    (
        'expectimax depth 3 - pure builder',
        lambda _: agent.ExpectimaxAgent(
            'O', arena.MIN_AGENT, mini_expecti_max.eval_pure_builder, 6
        )
    ),
    (
        'expectimax depth 1 - safe builder',
        lambda _: agent.ExpectimaxAgent(
            'O', arena.MIN_AGENT, mini_expecti_max.eval_builder_with_safeness, 2
        )
    ),
    (
        'expectimax depth 2 - safe builder',
        lambda _: agent.ExpectimaxAgent(
            'O', arena.MIN_AGENT, mini_expecti_max.eval_builder_with_safeness, 4
        )
    ),
    (
        'expectimax depth 3 - safe builder',
        lambda _: agent.ExpectimaxAgent(
            'O', arena.MIN_AGENT, mini_expecti_max.eval_builder_with_safeness, 6
        )
    ),
    (
        'human',
        lambda window: agent.HumanAgent(
            'O', arena.MIN_AGENT, window
        )
    ),
]


def select_agent():
    choice_max_agent = None
    choice_min_agent = None

    print('\nSelect a max agent:\n')
    for i, (name, func) in enumerate(PRESET_MAX_AGENTS):
        print(i, ':', name)
    print('\nType a number:')
    while choice_max_agent == None:
        try:
            choice = input()
            choice_max_agent = PRESET_MAX_AGENTS[int(choice)]
        except KeyboardInterrupt:
            quit()
        except:
            pass
    print('Selected :', choice_max_agent[0])

    print('\nSelect a min agent:\n')
    for i, (name, func) in enumerate(PRESET_MIN_AGENTS):
        print(i, ':', name)
    print('\nType a number:')
    while choice_min_agent == None:
        try:
            choice = input()
            choice_min_agent = PRESET_MIN_AGENTS[int(choice)]
        except KeyboardInterrupt:
            quit()
        except:
            pass
    print('Selected :', choice_min_agent[0])

    return choice_max_agent[1], choice_min_agent[1]


if __name__ == "__main__":
    select_agent()
