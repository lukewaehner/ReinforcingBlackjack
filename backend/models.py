import numpy as np


class RLModel:
    def __init__(self):
        self.reset_game()

    def reset_game(self):
        self.deck = self.initialize_deck()
        np.random.shuffle(self.deck)
        self.state = {
            "player_hand": [],
            "ai_hand": [],
            "current_player": "player",
            "game_over": False,
            "winner": None,
            "deck_count": len(self.deck),
            "player_score": 0,
            "ai_score": 0
        }
        self.model_trained = False

    def initialize_deck(self):
        ranks = [2, 3, 4, 5, 6, 7, 8, 9, 10, "Jack", "Queen", "King", "Ace"]
        suits = ['hearts', 'diamonds', 'clubs', 'spades']
        return [(rank, suit) for suit in suits for rank in ranks]

    def draw_card(self):
        if len(self.deck) == 0:
            self.deck = self.initialize_deck()
            np.random.shuffle(self.deck)
        card = self.deck.pop()
        self.state['deck_count'] = len(self.deck)
        return card

    def initialize_game(self):
        if len(self.deck) < 4:
            self.deck = self.initialize_deck()
            np.random.shuffle(self.deck)
        self.state["player_hand"] = []
        self.state["ai_hand"] = []
        self.state["current_player"] = "player"
        self.state["game_over"] = False
        self.state["winner"] = None
        for _ in range(2):
            self.state['player_hand'].append(self.draw_card())
            self.state["ai_hand"].append(self.draw_card())
        return self.state

    def play(self, user_move):
        if user_move == 'draw':
            self.state["player_hand"].append(self.draw_card())
            if self.calculate_hand_value(self.state["player_hand"]) > 21:
                self.state["game_over"] = True
                self.state["winner"] = "AI"
                self.state["ai_score"] += 1
                self.state["current_player"] = "ai"
            return self.state, None

    def ai_turn(self):
        while self.calculate_hand_value(self.state["ai_hand"]) < 17:
            self.state["ai_hand"].append(self.draw_card())
        if self.calculate_hand_value(self.state["ai_hand"]) > 21 or self.calculate_hand_value(self.state["player_hand"]) > self.calculate_hand_value(self.state["ai_hand"]):
            self.state["winner"] = "Player"
            self.state["player_score"] += 1
        else:
            self.state["winner"] = "AI"
            self.state["ai_score"] += 1
        self.state["game_over"] = True
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

        return value

    def train(self):
        # placeholder for training logic
        self.model_trained = True
        pass

    def reset_deck(self):
        self.deck = self.initialize_deck()
        np.random.shuffle(self.deck)
        self.state['deck_count'] = len(self.deck)
        self.state['player_hand'] = []
        self.state['ai_hand'] = []
        self.state['current_player'] = 'player'
        self.state['game_over'] = False
        self.state['winner'] = None
        for _ in range(2):
            self.state['player_hand'].append(self.draw_card())
            self.state['ai_hand'].append(self.draw_card())
        return self.state
