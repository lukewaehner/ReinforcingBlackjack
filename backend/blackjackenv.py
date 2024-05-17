import numpy as np
import random
from collections import defaultdict


class BlackjackEnv:
    def __init__(self):
        self.reset_game()

    def reset_game(self):
        self.deck = self.initialize_deck()
        random.shuffle(self.deck)
        self.state = {
            "player_hand": [],
            "dealer_hand": [],
            "current_player": "player",
            "game_over": False,
            "winner": None,
            "deck_count": len(self.deck)
        }

    def initialize_deck(self):
        ranks = [2, 3, 4, 5, 6, 7, 8, 9, 10, "Jack", "Queen", "King", "Ace"]
        suits = ['hearts', 'diamonds', 'clubs', 'spades']
        return [(rank, suit) for suit in suits for rank in ranks]

    def draw_card(self):
        if len(self.deck) == 0:
            self.deck = self.initialize_deck()
            random.shuffle(self.deck)
        card = self.deck.pop()
        self.state['deck_count'] = len(self.deck)
        return card

    def start_new_round(self):
        self.state["player_hand"] = [self.draw_card(), self.draw_card()]
        self.state["dealer_hand"] = [self.draw_card(), self.draw_card()]
        self.state["current_player"] = "player"
        self.state["game_over"] = False
        self.state["winner"] = None
        return self.state

    def calculate_hand_value(self, hand):
        value = 0
        num_aces = 0
        for rank, suit in hand:
            if rank == "Ace":
                num_aces += 1
                value += 11
            elif rank in ["Jack", "Queen", "King"]:
                value += 10
            else:
                value += rank

        # Adjust for aces
        while value > 21 and num_aces:
            value -= 10
            num_aces -= 1

        return value, num_aces

    def get_state(self):
        player_value, player_aces = self.calculate_hand_value(
            self.state["player_hand"])
        dealer_visible_value = self.state["dealer_hand"][0][0]
        if dealer_visible_value in ["Jack", "Queen", "King"]:
            dealer_visible_value = 10
        elif dealer_visible_value == "Ace":
            dealer_visible_value = 11
        return (player_value, dealer_visible_value, player_aces)

    def dealer_play(self):
        dealer_value, _ = self.calculate_hand_value(self.state["dealer_hand"])
        while dealer_value < 17:
            self.state["dealer_hand"].append(self.draw_card())
            dealer_value, _ = self.calculate_hand_value(
                self.state["dealer_hand"])
        return dealer_value

    def step(self, action):
        if action == "draw":
            self.state["player_hand"].append(self.draw_card())
            player_value, _ = self.calculate_hand_value(
                self.state["player_hand"])
            if player_value > 21:
                self.state["game_over"] = True
                self.state["winner"] = "Dealer"
                reward = -1
            else:
                reward = -0.1 if player_value > 17 else 0.1
        elif action == "stand":
            self.state["game_over"] = True
            player_value, _ = self.calculate_hand_value(
                self.state["player_hand"])
            dealer_value = self.dealer_play()
            if dealer_value > 21 or player_value > dealer_value:
                self.state["winner"] = "Player"
                reward = 1
            else:
                self.state["winner"] = "Dealer"
                reward = -1
        return self.state, reward, self.state["game_over"]
