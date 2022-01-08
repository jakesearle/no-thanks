import const
import player
from player import Player, HumanPlayer
from enumerations import DecisionResult
import random


class Game:
    def __init__(self, num_players=const.NUM_PLAYERS, players=None):
        self.curr_card = None
        self.curr_card_counters = 0
        self.winner_index = None

        self.num_players = num_players
        if players is None:
            self.players = [Player() for _ in range(num_players)]
        else:
            self.players = players

        # Reset number of counters
        for p in self.players:
            p.num_counters = 11

        # See if there's a human player
        self.has_human_player = any([isinstance(p, HumanPlayer) for p in self.players])
        self.curr_player_index = 0
        self.curr_player = self.players[self.curr_player_index]

        self.deck = [_ for _ in range(const.MIN_CARD_VAL, const.MAX_CARD_VAL + 1)]
        self.ownership = [-1 for _ in self.deck]
        random.shuffle(self.deck)
        self.remove_cards()

    def play(self):
        self.draw_card()
        while self.deck:
            result = self.curr_player.decide(self.curr_card,
                                             self.curr_card_counters,
                                             self.ownership,
                                             self.curr_player_index)
            if result == DecisionResult.TAKE:
                self.ownership[self.curr_card - const.MIN_CARD_VAL] = self.curr_player_index
                self.curr_player.add_counters(self.curr_card_counters)
                self.curr_card_counters = 0
                self.draw_card()
            elif result == DecisionResult.PASS:
                assert self.curr_player.num_counters > 0
                self.curr_player.reduce_counters()
                self.curr_card_counters += 1
                self.next_player()
            else:
                raise Exception('That\'s our ball?')
        if self.has_human_player:
            self.print_results()
        self.determine_winner()

    def print_results(self):
        scores = self.get_scores()
        for i, score in enumerate(scores):
            print(f"Player {i + 1}: {score}")

        print(f"Player #{scores.index(min(scores)) + 1} wins!")

    def get_scores(self):
        # Get initial scores
        scores = [0 for _ in self.players]
        previous_owner = None
        for score, owner in enumerate(self.ownership):
            # Don't count the ones after
            if previous_owner != owner and owner != -1:
                scores[owner] += score + const.MIN_CARD_VAL
            previous_owner = owner

        # Subtract the counters
        for i, p in enumerate(self.players):
            scores[i] -= p.get_num_counters()
        return scores

    def determine_winner(self):
        # TODO: confirm game is over
        assert not self.deck
        scores = self.get_scores()
        self.winner_index = scores.index(min(scores))
        # return winner_index, self.players[winner_index].display_name

    def get_winner(self):
        return self.players[self.winner_index]

    # Removes the starting cards from the game
    def remove_cards(self):
        for i in range(const.CARDS_TO_REMOVE):
            self.deck.pop()

    def draw_card(self):
        self.curr_card = self.deck.pop()

    def next_player(self):
        self.curr_player_index = (self.curr_player_index + 1) % self.num_players
        self.curr_player = self.players[self.curr_player_index]

    def award_winner(self):
        winner = self.players[self.winner_index]
        if isinstance(winner, player.NNPlayer):
            # TODO: tweak this?
            winner.genome.fitness += 1.0

    def punish_losers(self):
        for i, loser in enumerate(self.players):
            if i != self.winner_index:
                loser.genome.fitness -= 0.1
