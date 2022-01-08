import game
import player
import random
import time
import os
import neat
import visualize


NUM_GENERATIONS = 300
NUM_GAMES = 100


def chunker(seq, size):
    return (seq[pos:pos + size] for pos in range(0, len(seq), size))


def eval_genomes(genomes, config):
    # Make players
    random.shuffle(genomes)
    players = [player.NNPlayer(genome, neat.nn.FeedForwardNetwork.create(genome, config)) for genome_id, genome in genomes]
    for p in players:
        p.genome.fitness = 0.0
    winners = players
    # For each round
    while len(winners) > 1:
        winners = []
        # For each match
        for group in chunker(players, 5):
            if len(group) != 5:
                continue
            play_games(group, NUM_GAMES)
            best_player = max(group, key=lambda x: x.genome.fitness)
            # print(best_player)
            winners.append(best_player)
        players = winners


def run(config_file):
    # Load configuration.
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_file)

    # Create the population, which is the top-level object for a NEAT run.
    p = neat.Population(config)

    # Add a stdout reporter to show progress in the terminal.
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    p.add_reporter(neat.Checkpointer(5))

    # Run for up to NUM_GENERATIONS generations.
    winner_genome = p.run(eval_genomes, NUM_GENERATIONS)

    # Display the winning genome.
    print('\nBest genome:\n{!s}'.format(winner_genome))

    # TODO: Play a game against the most fit genome
    winner_player = player.NNPlayer(winner_genome, neat.nn.FeedForwardNetwork.create(winner_genome, config))
    top_players = [winner_player,
                   winner_player,
                   winner_player,
                   winner_player,
                   player.HumanPlayer()]
    winner_game = game.Game(players=top_players)
    winner_game.play()

    node_names = {
        -1: '#3 ownership',
        -2: '#4 ownership',
        -3: '#5 ownership',
        -4: '#6 ownership',
        -5: '#7 ownership',
        -6: '#8 ownership',
        -7: '#9 ownership',
        -8: '#10 ownership',
        -9: '#11 ownership',
        -10: '#12 ownership',
        -11: '#13 ownership',
        -12: '#14 ownership',
        -13: '#15 ownership',
        -14: '#16 ownership',
        -15: '#17 ownership',
        -16: '#18 ownership',
        -17: '#19 ownership',
        -18: '#20 ownership',
        -19: '#21 ownership',
        -20: '#22 ownership',
        -21: '#23 ownership',
        -22: '#24 ownership',
        -23: '#25 ownership',
        -24: '#26 ownership',
        -25: '#27 ownership',
        -26: '#28 ownership',
        -27: '#29 ownership',
        -28: '#30 ownership',
        -29: '#31 ownership',
        -30: '#32 ownership',
        -31: '#33 ownership',
        -32: '#34 ownership',
        -33: '#35 ownership',
        -34: 'card number',
        -35: 'num counters',
        -36: 'player index',
        0: 'take?'
    }
    visualize.draw_net(config, winner_genome, True, node_names=node_names)
    visualize.plot_stats(stats, ylog=False, view=True)
    visualize.plot_species(stats, view=True)


def play_games(players, num_games=1, shuffle=True):
    for i in range(num_games):
        if shuffle:
            random.shuffle(players)
        curr_game = game.Game(players=players)
        curr_game.play()
        # Award winner
        curr_game.award_winner()
        # Punish loser
        curr_game.punish_losers()


def main():
    # Determine path to configuration file. This path manipulation is
    # here so that the script will run successfully regardless of the
    # current working directory.
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config-feedforward.txt')
    run(config_path)


if __name__ == '__main__':
    main()
