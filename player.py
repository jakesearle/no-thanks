import random

import const
from enumerations import DecisionResult


class Player:
    def __init__(self, num_counters=11):
        self.num_counters = num_counters
        self.cards = []
        self.display_name = 'Player'

    def add_counters(self, num_counters):
        self.num_counters += num_counters

    def get_num_counters(self):
        return self.num_counters

    # Scores may be optional
    def decide(self, curr_card, curr_card_counters, ownership, player_index):
        pass

    def reduce_counters(self):
        self.num_counters -= 1


class HumanPlayer(Player):
    def __init__(self):
        super().__init__()
        self.display_name = 'HumanPlayer'

    def decide(self, curr_card, curr_card_counters, ownership, player_index):
        self.print_game(curr_card, curr_card_counters, ownership, player_index)
        if not self.num_counters:
            print(f"Unfortunately you have no counters so you must take it")
            return DecisionResult.TAKE
        while True:
            resp = input("Take (t) or pass? (p):\n").strip()[0].lower()
            if resp == 't':
                return DecisionResult.TAKE
            elif resp == 'p':
                return DecisionResult.PASS
            print("Please input a valid value")

    def print_game(self, curr_card, curr_card_counters, ownership, player_index):
        # Assuming there are five players
        players_ownership = [[] for _ in range(const.NUM_PLAYERS)]
        for val, owner in enumerate(ownership):
            if owner != -1:
                card_val = val + const.MIN_CARD_VAL
                players_ownership[owner].append(card_val)

        for i, player in enumerate(players_ownership):
            # Don't print out what I have, save that till the end
            if i != player_index:
                print(f"Player #{i + 1} has: {players_ownership[i]}")
        print(
            f"You (player #{player_index + 1} have {players_ownership[player_index]}, and {self.num_counters} counters")
        print(f"The card's value is {curr_card} and it has {curr_card_counters} counters on it")


class CoinFlipPlayer(Player):
    def __init__(self):
        super().__init__()
        self.display_name = 'CoinFlipPlayer'

    def decide(self, curr_card, curr_card_counters, ownership, player_index):
        if not self.num_counters or random.random() < (1 / 2):
            return DecisionResult.TAKE
        return DecisionResult.PASS


class OneInFivePlayer(Player):
    def __init__(self):
        super().__init__()
        self.display_name = 'OneInFivePlayer'

    def decide(self, curr_card, curr_card_counters, ownership, player_index):
        if not self.num_counters or random.random() < (1 / const.NUM_PLAYERS):
            return DecisionResult.TAKE
        return DecisionResult.PASS


class NetGainPlayer(Player):
    def __init__(self):
        super().__init__()
        self.display_name = 'NetGainPlayer'

    def decide(self, curr_card, curr_card_counters, ownership, player_index):
        if not self.num_counters or random.random() < (curr_card_counters / curr_card):
            return DecisionResult.TAKE
        return DecisionResult.PASS


class NNPlayer(Player):
    def __init__(self, genome, net):
        super().__init__()
        self.display_name = 'NNPlayer'
        self.net = net
        self.genome = genome

    def decide(self, curr_card, curr_card_counters, ownership, player_index):
        input_list = [_ for _ in ownership] + [curr_card] + [curr_card_counters] + [player_index]
        output = self.net.activate(input_list)
        if output[0] > 0.5 or not self.num_counters:
            return DecisionResult.TAKE
        else:
            return DecisionResult.PASS
