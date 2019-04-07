# Jeff's Blackjack Game - a Udemy Python Bootcamp exercise coded March, 2019

from subprocess import call
import msvcrt
from random import shuffle

call('color a', shell=True)  # this sets the color to light green
player_num_dict = {1: 'one', 2: 'two', 3: 'three', 4: 'four', 5: 'five', 6: 'six', 7: 'seven', 8: 'eight',
                   9: 'nine', 10: 'ten'}
deck = [('A♣', 11), ('2♣', 2), ('3♣', 3), ('4♣', 4), ('5♣', 5), ('6♣', 6), ('7♣', 7), ('8♣', 8), ('9♣', 9),
        ('10♣', 10), ('J♣', 10), ('Q♣', 10), ('K♣', 10),
        ('A♦', 11), ('2♦', 2), ('3♦', 3), ('4♦', 4), ('5♦', 5), ('6♦', 6), ('7♦', 7), ('8♦', 8), ('9♦', 9),
        ('10♦', 10), ('J♦', 10), ('Q♦', 10), ('K♦', 10),
        ('A♥', 11), ('2♥', 2), ('3♥', 3), ('4♥', 4), ('5♥', 5), ('6♥', 6), ('7♥', 7), ('8♥', 8), ('9♥', 9),
        ('10♥', 10), ('J♥', 10), ('Q♥', 10), ('K♥', 10),
        ('A♠', 11), ('2♠', 2), ('3♠', 3), ('4♠', 4), ('5♠', 5), ('6♠', 6), ('7♠', 7), ('8♠', 8), ('9♠', 9),
        ('10♠', 10), ('J♠', 10), ('Q♠', 10), ('K♠', 10)]


class Player:
    hand = ['-']

    def __init__(self, name, hand, chip_bal=10, bet=1, hand_val=0, hand_soft_hard='hard', hand_status='PLAYING',
                 game_status='PLAYING', in_play=True, game_loss_displayed=False, last_hand_stored=False,
                 last_hand_str='', game_status_str='', chip_bal_str='', hand_status_str='', chips_wagered_str='',
                 hand_str='', status_str=''):
        self.name = name
        self.hand = hand
        self.chip_bal = chip_bal
        self.bet = bet
        self.hand_val = hand_val
        # hand_status can be 'in play', 'blackjack', 'busted', 'stand', or 'push'.
        self.hand_status = hand_status
        self.hand_soft_hard = hand_soft_hard
        self.game_status = game_status
        self.in_play = in_play
        self.game_loss_displayed = game_loss_displayed
        self.last_hand_stored = last_hand_stored
        self.last_hand_str = last_hand_str
        self.game_status_str = game_status_str
        self.chip_bal_str = chip_bal_str
        self.hand_status_str = hand_status_str
        self.chips_wagered_str = chips_wagered_str
        self.hand_str = hand_str
        self.status_str = status_str

    def reset_for_play(self):
        if self.chip_bal > 0:
            self.in_play = True
        else:
            self.in_play = False
        self.hand = ['-']
        if not first_hand_played:
            self.chip_bal = 10
        self.bet = 0
        self.hand_val = 0
        self.hand_soft_hard = 'hard'
        self.hand_status = 'PLAYING'
        self.game_status = ''
        self.game_loss_displayed = False
        self.last_hand_stored = False
        self.last_hand_str = ''
        self.game_status_str = ''
        self.chip_bal_str = ''
        self.hand_status_str = ''
        self.chips_wagered_str = ''
        self.hand_str = ''
        self.status_str = ''

    def calc_chip_bal(self):
        self.chip_bal = self.chip_bal - self.bet

    def ace_check(self):
        """ Check for aces in the hand. """
        is_ace = False
        for card in range(0, len(self.hand)):
            if self.hand[card][1] == 11:
                is_ace = True
            return is_ace

    def check_for_soft(self):
        """ A soft hand contains an ace counted as eleven. """
        for card in range(0, len(self.hand)):
            if self.hand[card][1] == 11:
                if self.hand[card][1] == '11':
                    self.hand_soft_hard = 'soft'

    def ace_val_to_one(self):
        """ Change the value of first ace found in the hand to one. """
        ace_found = False
        for card in range(0, len(self.hand)):
            if not ace_found:
                if self.hand[card][1] == 11:
                    ace_found = True
                    self.hand_val -= 10

    def calc_hand_val(self):
        """ Determine the hand value without adjusting ace values. """
        self.hand_val = 0
        for card in range(0, len(self.hand)):
            self.hand_val += self.hand[card][1]
        return self.hand_val

    def __str__(self):
        # todo may not be necessary...
        self.hand_str = ''

        if self.calc_hand_val() > 21 and self.ace_check():
            self.ace_val_to_one()

        self.calc_hand_val()
        self.check_for_soft()

        if self.hand_val < 11:
            hand_val_str = str(player_num_dict[self.hand_val])
            self.hand_status = 'PLAYING'
        else:
            hand_val_str = str(self.hand_val)

        if self.hand_val == 21:
            self.hand_status = 'BLACKJACK'
        elif self.hand_val > 21:
            self.hand_status = 'BUSTED'

        if not self.game_status == '':
            self.game_status_str = self.game_status

        if self.hand_status == 'BLACKJACK' or self.hand_status == 'BUSTED' or self.hand_status == 'PUSH':
            self.hand_status_str = '\n\t' + self.hand_status
        else:
            self.hand_status_str = ''

        if self.bet == 0:
            self.chips_wagered_str = ''
        else:
            self.chips_wagered_str = '\n\tChips wagered: ' + str(self.bet)

        self.hand_str = ''
        self.hand_status_str = ''
        if not self.game_status == 'LOST':
            for card in range(0, len(self.hand)):
                self.hand_str = self.hand_str + ' ' + self.hand[card][0]
            self.status_str = f"{self.name}'s hand is {self.hand_soft_hard} with a value of {hand_val_str}.  "
            self.chip_bal_str = f'\n\tChips available: {self.chip_bal}'
        else:
            if not self.last_hand_stored:
                # self.hand_str = ''
                self.chip_bal_str = ''
                for card in range(0, len(self.hand)):
                    self.hand_str = self.hand_str + ' ' + self.hand[card][0]
                self.status_str = f'{self.name} has lost. The final hand was:{self.hand_str}'
                self.chips_wagered_str = ''
                # self.hand_status = ''
                self.hand_status_str = ''
                self.game_status_str = ''
                self.hand_str = ''
                self.last_hand_stored = True

        return f'\n\t{self.status_str}' \
            f'{self.hand_str}' \
            f'{self.chip_bal_str}' \
            f'{self.chips_wagered_str}' \
            f'{self.hand_status_str}' \
            f'\n\t{self.game_status_str}\n'


class Dealer(Player):
    hand = ['-']

    def __init__(self, name, hand, chip_bal=10, bet=1, hand_val=0, hand_soft_hard='', hand_status='',
                 game_status='', in_play=True):
        self.name = name
        self.hand = hand
        self.chip_bal = chip_bal
        self.bet = bet
        self.hand_val = hand_val
        # Hand_status can be 'in play', 'blackjack', 'busted', 'stand', 'push', 'won', or 'lost'.
        self.hand_status = hand_status
        self.hand_soft_hard = hand_soft_hard
        # game_status can be 'lost' or 'won'.
        self.game_status = game_status
        self.in_play = in_play

    def reset_for_play(self):
        if self.chip_bal > 0:
            self.in_play = True
        else:
            self.in_play = False
        self.hand = ['-']
        self.chip_bal = 9
        self.bet = 1
        self.hand_val = 0
        self.hand_soft_hard = 'hard'
        self.hand_status = ''
        self.game_status = ''

    def dealer_shows_single_card(self):
        return f'\n\t' + 20 * '.  ' + '\n' \
            f"\n\tThe {self.name}'s face-up card is {self.hand[0][0]}.\n"

    def dealer_finishes_hand(self):
        self.hand_val = 0
        ace_in_hand = False

        while self.hand_val < 17:

            for card in range(0, len(self.hand)):
                if self.hand[card][1] == 11:
                    ace_in_hand = True
            if self.hand_val > 21 and ace_in_hand:
                self.hand_val -= 10

            if self.hand_val < 17:
                self.hand.append(tuple(deck.pop(-1)))

            # Hit on a soft 17 (hand containing an ace and one or more other cards totaling six).
            if self.hand_val == 17 and ace_in_hand:
                self.hand.append(tuple(deck.pop(-1)))

            for card in range(0, len(self.hand)):
                self.hand_val += self.hand[card][1]

    def dealer_evaluation(self):
        self.hand_status = 'PLAYING'
        if self.hand_val == 21:
            self.hand_status = 'BLACKJACK'
        elif self.hand_val > 21:
            self.hand_status = 'BUSTED'
            self.game_status = 'LOST'

    def __str__(self):

        hand_str = ''
        for card in range(0, len(self.hand)):
            hand_str = hand_str + ' ' + self.hand[card][0]

        if self.calc_hand_val() > 21 and self.ace_check():
            self.ace_val_to_one()

        self.calc_hand_val()
        self.check_for_soft()

        # Format the hand value.
        if self.hand_val < 11:
            hand_val_str = str(player_num_dict[self.hand_val])
        else:
            hand_val_str = str(self.hand_val)

        self.dealer_evaluation()

        hand_status_str = self.hand_status

        return f'\n\t' + 20 * '.  ' + '\n' \
            f"\n\tThe {self.name}'s hand is {self.hand_soft_hard} with a value of {hand_val_str}. " \
            f'{hand_str}' \
            f'\n\t{hand_status_str}\n'


def count_chips(player_obj_lst_pass):
    total_chip_bal = 0
    for n2 in range(1, num_players + 1):
        total_chip_bal += player_obj_lst_pass[n2].chip_bal
    return total_chip_bal > 0


def initial_deal(player_obj_lst_pass, num_players_pass):
    """ Deal 2 cards to start play. """
    shuffle(deck)
    for i in range(1, num_players_pass + 1):
        # Receive the first two cards.
        player_obj_lst_pass[i].hand = [deck.pop(-2), deck.pop(-1)]
    return player_obj_lst_pass


def initial_deal_dealer(dealer_obj_pass):
    """ Deal 2 cards to start play. The deck was already shuffled. """
    dealer_obj_pass.hand = [deck.pop(-2), deck.pop(-1)]
    return dealer_obj_pass


def evaluate_players_busted_or_blackjack(player_obj_lst_pass_2, num_players_pass_2):
    players_busted_or_blackjack = True
    for n in range(1, num_players_pass_2 + 1):
        if players_busted_or_blackjack:
            if player_obj_lst_pass_2[n].hand_status != 'BUSTED' or player_obj_lst_pass_2[n].hand_status != 'BLACKJACK':
                # Once this triggers false for one player, it must remain false.
                players_busted_or_blackjack = False
    return players_busted_or_blackjack


def print_players(player_obj_lst_pass, num_players_pass, dealer_played_pass):
    call('cls', shell=True)
    for n in range(1, num_players_pass + 1):
        # if player_obj_lst[n].chip_bal > 0 or player_obj_lst[n].bet > 0 and not player_obj_lst[n].game_status == 'LOST':
        # if not player_obj_lst[n].game_loss_displayed:
        print(player_obj_lst_pass[n])
    if not dealer_played_pass:
        print(dealer_obj.dealer_shows_single_card())
    else:
        if not evaluate_players_busted_or_blackjack(player_obj_lst_pass, num_players_pass):
            print(dealer_obj)
        else:
            print("\n\tThe dealer's hand was not completed due to the hand status of players.\n")


call('cls', shell=True)
print(f"\n\tJ E F F' S   B L A C K J A C K   G A M E  - a Python exercise coded March, 2019"
      f"\n\t"
      f"\n\tPlay with one to three players. You will be gambling and will start with ten chips."
      f"\n\t"
      f"\n\tThe object is to beat the automated dealer. This game is played with one deck of 52 cards."
      f"\n\tAfter the dealer shuffles the deck, you will be in initially dealt two cards face up. The"
      f"\n\tdealer will get two cards, but only one will be visible."
      f"\n\t"
      f"\n\tThe winner is whoever has card values totaling closest to 21 without exceeding 21. Tens and"
      f"\n\tface cards are worth ten points, the other cards count as their numerical values, and aces are"
      f"\n\tworth one or 11. You determine the value of the ace and you can change this in mid-hand."
      f"\n\t"
      f"\n\tYou win automatically by receiving a total of 21 in the first two cards. That requires a ten-"
      f"\n\tvalue card and an Ace. This is called a blackjack. If you take a hit that puts your total"
      f"\n\tover 21, you lose."
      f"\n\t"
      f"\n\tA soft hand contains an ace counted as 11. A hard hand will not contain an ace or a hand"
      f"\n\twhere the ace can only be counted as one point."
      f"\n\t"
      f"\n\tOnce all players complete their hands by either exceeding 21 or standing, the dealer will"
      f"\n\treveal the hidden card and hit until the cards total 17 or more points. The exception to this"
      f"\n\tis that the dealer's hand will not be completed if all players have either busted or received"
      f"\n\tblackjacks. The dealer also hits on a soft 17 - a hand containing an ace and one or more other"
      f"\n\tcards totaling six."
      f"\n\t"
      f"\n\tA push happens when a player and the dealer both get a blackjack or a player and the dealer"
      f"\n\thave the same total. No money is won or lost with a push."
      f"\n\t"
      f"\n\tPlayers win by not busting and have a total higher than the dealer, not busting and having"
      f"\n\tthe dealer bust, or getting a blackjack without the dealer getting a blackjack. In the last"
      f"\n\tcase, you receive a two to three payoff (get $15 for a $10 bet). Play as many hands as you"
      f"\n\twant as long as you have chips."
      f"\n\t"
      f"\n\t.  .  .  .  .  .  .  . .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .")

player_obj_lst = ['-']
hand_lst = ['-']
first_hand_played = False
# Determine the number of players (one to three).
print('\n\tHow many players? Enter 1 to 3: ')
while True:
    try:
        num_players = int(msvcrt.getch())
        if num_players in range(1, 4):
            break
    except ValueError:
        print('\n\tHey, enter an integer - the maximum number of players is three.')
        continue
if num_players > 1:
    plural = 's'
else:
    plural = ''
call('cls', shell=True)
print(f"\n\tGreat, there will be {player_num_dict[num_players]} player{plural}. Who's playing?")
# Determine who's playing and create instances of the players.
for n in range(1, num_players + 1):
    name_pass = input(f'\n\tPlayer {n} name: ').title()
    player_obj_lst.append(Player(name_pass, hand_lst, 10))
# WHILE LOOP for play (as long as at least one player has chips).
while count_chips(player_obj_lst):
    #    deck = shuffle(full_deck)
    for n in range(1, num_players + 1):
        if player_obj_lst[n].chip_bal > 0:
            call('cls', shell=True)
            player_obj_lst[n].reset_for_play()
            player_obj_lst[n].calc_chip_bal()
            if player_obj_lst[n].hand_status == 'PLAYING':
                while True:
                    chip_chips = lambda n2: 'chips' if n2 > 1 else 'chip'
                    if player_obj_lst[n].chip_bal < 11:
                        num_str = player_num_dict[player_obj_lst[n].chip_bal]
                    else:
                        num_str = player_obj_lst[n].chip_bal
                    chip_str = chip_chips(player_obj_lst[n].chip_bal)
                    bet_increase = int(input(f'\n\t{player_obj_lst[n].name}, you have {num_str} {chip_str} available.'
                                             f' What is your bet?  '))
                    player_obj_lst[n].bet = bet_increase
                    player_obj_lst[n].calc_chip_bal()
                    # print_players(player_obj_lst, num_players, dealer_played)
                    break

    # Create an instance of Dealer.
    dealer_obj = Dealer('dealer', hand_lst)
    dealer_obj.reset_for_play()
    # Dealer deals two cards to each player (where in_play) and the dealer.
    player_obj_lst = initial_deal(player_obj_lst, num_players)
    dealer_obj = initial_deal_dealer(dealer_obj)
    dealer_played = False
    first_hand_played = True

    for n in range(1, num_players + 1):
        if player_obj_lst[n].chip_bal > 0 or player_obj_lst[n].bet > 0:
            if player_obj_lst[n].chip_bal + player_obj_lst[n].bet > 0:
                # Each player plays until it is the dealer's turn to play (blackjack, busted, or stand).
                print_players(player_obj_lst, num_players, dealer_played)
                # print(dealer_obj.dealer_shows_single_card())
                if player_obj_lst[n].hand_status == 'PLAYING':

                    print_players(player_obj_lst, num_players, dealer_played)
                    hit_once = True
                    while True:
                        if hit_once:
                            print(f'\n\n\t{player_obj_lst[n].name}, do you want a hit?  Y or N...')
                            hit_once = False
                        else:
                            print(f'\n\n\t{player_obj_lst[n].name}, do you want another hit?  Y or N...')
                        hit = str(msvcrt.getch())
                        if 'y' in hit or 'Y' in hit:
                            player_obj_lst[n].hand.append(tuple(deck.pop(-1)))
                            print_players(player_obj_lst, num_players, dealer_played)
                            if player_obj_lst[n].hand_status == 'BLACKJACK' or \
                                    player_obj_lst[n].hand_status == 'BUSTED':
                                break
                            else:
                                continue
                        else:
                            player_obj_lst[n].hand_status = 'STAND'
                            break

    dealer_obj.dealer_finishes_hand()
    dealer_obj.dealer_evaluation()
    print_players(player_obj_lst, num_players, dealer_played)
    for n in range(1, num_players + 1):
        if player_obj_lst[n].hand_status != 'BUSTED' and dealer_obj.hand_status == 'BUSTED':
            player_obj_lst[n].game_status = 'WIN!'
            player_obj_lst[n].chip_bal = player_obj_lst[n].chip_bal + 2 * player_obj_lst[n].bet
            player_obj_lst[n].bet = 0
        elif player_obj_lst[n].hand_status != 'BUSTED' and player_obj_lst[n].hand_val > dealer_obj.hand_val:
            player_obj_lst[n].game_status = 'WIN!'
            player_obj_lst[n].chip_bal = player_obj_lst[n].chip_bal + 2 * player_obj_lst[n].bet
            player_obj_lst[n].bet = 0
        elif player_obj_lst[n].hand_status != 'BUSTED' and dealer_obj.hand_status == 'BUSTED':
            player_obj_lst[n].game_status = 'WIN!'
            player_obj_lst[n].chip_bal = player_obj_lst[n].chip_bal + 2 * player_obj_lst[n].bet
            player_obj_lst[n].bet = 0
        elif player_obj_lst[n].hand_status == 'BLACKJACK' and dealer_obj.hand_status == 'BLACKJACK':
            player_obj_lst[n].game_status = 'PUSH!'
            player_obj_lst[n].chip_bal = player_obj_lst[n].bet + player_obj_lst[n].chip_bal
            player_obj_lst[n].bet = 0
        elif player_obj_lst[n].hand_val == dealer_obj.hand_val:
            player_obj_lst[n].hand_status = 'PUSH'
            player_obj_lst[n].chip_bal = player_obj_lst[n].bet + player_obj_lst[n].chip_bal
            player_obj_lst[n].bet = 0
        elif player_obj_lst[n].hand_status == 'BLACKJACK' and dealer_obj.hand_status != 'BLACKJACK':
            player_obj_lst[n].chip_bal = player_obj_lst[n].chip_bal + 2.5 * player_obj_lst[n].bet
            player_obj_lst[n].bet = 0
        else:
            # No change to the chip balance.
            player_obj_lst[n].game_status = 'LOST'
            player_obj_lst[n].bet = 0
            player_obj_lst[n].chip_bal_str = ''

    dealer_played = True
    print_players(player_obj_lst, num_players, dealer_played)
    if count_chips(player_obj_lst):
        input('\n\tPress enter. The dealer will shuffle the deck and deal a new hand.')
        del dealer_obj
    else:
        # call('cls', shell=True)
        print('\n\tThere are no chips left so this game is over.')
        if num_players == 1:
            print(f"\n\tHey, {player_obj_lst[1].name}, thanks for playing Jeff's blackjack game!")
        elif num_players == 2:
            print(f"\n\tHey, {player_obj_lst[1].name} and {player_obj_lst[2].name}, thanks for playing \
                Jeff's blackjack game!")
        else:
            print(
                f"\n\tHey, {player_obj_lst[1].name} and {player_obj_lst[2].name}, and {player_obj_lst[2].name}, thanks" \
                    f" for playing Jeff's blackjack game!")
        print()
# Pause requiring 'return' keypress for a new hand for players that have chips (press 'Q' or escape to quit)
while True:
    quit_key = str(msvcrt.getch())
    if 'q' or 'Q' or chr(27) in quit_key:
        quit()
    else:
        break
