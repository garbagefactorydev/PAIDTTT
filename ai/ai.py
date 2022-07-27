import random
from copy import deepcopy


class AiPlayer:
    def __init__(self, game):
        self.game = game

    def make_move(self):
        if not self.game.ai_positions and not self.game.player_positions:
            return random.choice(self.game.display.empty_fields)
        best_moves = self.consider_options()
        return best_moves[0][0]

    def consider_options(self):
        game_state = {"available_moves": self.game.display.empty_fields,
                      "player_positions": self.game.player_positions,
                      "ai_positions": self.game.ai_positions,
                      "game_over": self.game.game_over}
        best_moves = []
        for position in game_state["available_moves"]:
            test_game_state = deepcopy(game_state)
            self.simulate_move(position, test_game_state, "ai")
            rating = self.minimax(test_game_state, False)
            best_moves.append((position, rating))
        return sorted(best_moves, key=lambda x: x[1], reverse=True)

    def simulate_move(self, position, game_state, player):
        player_positions = game_state["ai_positions"] if player == "ai" else game_state["player_positions"]
        game_state["available_moves"].remove(position)
        player_positions.append(self.game.board[position])
        player_won, _ = self.game.is_win_position(player_positions)
        draw = self.game.is_draw(game_state["available_moves"])
        if player_won or draw:
            game_state["game_over"] = True

    def minimax(self, game_state, maximizing_player, alpha=-100, beta=100):
        if game_state["game_over"]:
            return self.evaluate_situation(game_state)

        if maximizing_player:
            max_eval = -100
            for position in game_state["available_moves"]:
                new_game_state = deepcopy(game_state)
                self.simulate_move(position, new_game_state, "ai")
                evaluation = self.minimax(new_game_state, False, alpha, beta)
                max_eval = max(max_eval, evaluation)
                alpha = max(alpha, evaluation)
                if beta <= alpha:
                    break
            return max_eval

        else:
            min_eval = 100
            for position in game_state["available_moves"]:
                new_game_state = deepcopy(game_state)
                self.simulate_move(position, new_game_state, "player")
                evaluation = self.minimax(new_game_state, True, alpha, beta)
                min_eval = min(min_eval, evaluation)
                beta = min(beta, evaluation)
                if beta <= alpha:
                    break
            return min_eval

    def evaluate_situation(self, game_state):
        ai, _ = self.game.is_win_position(game_state["ai_positions"])
        player, _ = self.game.is_win_position(game_state["player_positions"])
        if ai: return 1
        if player: return -1
        else: return 0
