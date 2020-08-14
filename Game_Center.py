from Blackjack import Blackjack

class Player:
    def __init__(self, money=1000):
        self.cardlist = []
        self.money = money
        self.pot = 0


class BlackjackPlayer(Player):
    def __init__(self):
        super(BlackjackPlayer, self).__init__()
        self.sum = 0
        self.blackjack = False


class GameCenter:
    def __init__(self):
        self.gamelist = ['b']
        self.player_list = []
        self.game_start()
        
    def game_start(self):
        print("Welcome to the Game Center!")
        print("Please select a game and type its hotkey to begin:")
        print("Blackjack: <b>")
        game_choice = input()

        while game_choice not in self.gamelist:
            print("This game does not exist, please input a valid hotkey:")
            game_choice = input()

        self.player_list = self.spawn_players(game_choice)

        if game_choice == 'b':
            Blackjack(self.player_list, BlackjackPlayer())
            self.play_again()
        
    def play_again(self):
        exit_game = True
        for player_num in range(len(self.player_list)):
            if self.player_list[player_num].money != 0:
                exit_game = False

        if exit_game:
            print("All players have run out of money. Please restart!")
            print("Goodbye!")
            exit()

        yes_or_no_list = ["y", "n"]
        
        yes_or_no = input("Would you like to play again? <y>/<n>: ")
        while yes_or_no not in yes_or_no_list:
            yes_or_no = input("That is not a valid answer. Please input <y> or <n>: ")
        
        if yes_or_no == "n":
            print("Are you sure? You will lose all your progress.")
            yes_or_no = input("<y>/<n>: ")

        if yes_or_no == "n":
            print("Thank you for playing with us! Goodbye!")
            exit()

        if yes_or_no == "y":
            self.game_start()

    def spawn_players(self, game_type):
        while True:
            try:
                player_count = int(input("How many players?: "))
            
            except ValueError:
                print("That is not a valid number:")
                continue

            else:
                break

        player_list = []
        for player in range(player_count):
            player_list.append(PlayerFactory().player_type(game_type))
        return player_list


class PlayerFactory():
    def __init__(self):
        pass

    def player_type(self, player_type):
        if player_type == "b":
            return BlackjackPlayer()





if __name__ == "__main__":
    game = GameCenter()