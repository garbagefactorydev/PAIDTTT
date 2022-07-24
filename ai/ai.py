class AiPlayer:
    def __init__(self, game):
        self.game = game

    def consider_options(self):
        available_options = []
        for position in self.game.display.empty_fields:
            option = self.consider_position(position)
            available_options.append(option)
        return sorted(available_options, key=lambda x: x[0], reverse=True)

    def make_move(self):
        available_moves = self.consider_options()
        return available_moves[0][1]

    def consider_position(self, position):
        center = '4'
        corners = ['0', '2', '6', '8']
        rating = 0
        position_on_board = self.game.board[position]
        oponent_positions_on_board = self.game.player_positions
        new_situation = self.game.ai_positions[:]
        new_situation.append(position_on_board)
        if position_on_board == center:
            rating += self.rate_position('center')
        if position_on_board in corners:
            rating += self.rate_position('corner')
        if self.game.is_win_position(new_situation)[0]:
            rating += self.rate_position('win')
        if position_on_board in self.two_in_a_row_check(oponent_positions_on_board):
            rating += self.rate_position('block player')
        rating += len(self.two_in_a_row_check(new_situation))
        return rating, position

    def two_in_a_row_check(self, situation):
        two_in_a_row = []
        for combination in self.game.win_combinations:
            missing = [i for i in combination if i not in situation]
            if len(missing) == 1:
                if missing[0] not in self.game.player_positions:
                    two_in_a_row.append(missing[0])
        return two_in_a_row

    @staticmethod
    def rate_position(position):
        position_rating = {
            'win': 10,
            'block player': 8,
            'center': 2,
            'corner': 1,
        }
        return position_rating[position]
