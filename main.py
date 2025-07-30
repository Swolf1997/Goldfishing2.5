"""
Create on July 30, 2025

@author: Seth

@description: This program is based off of DanielsWorlds single player Commander game called Goldfishing.
"""
import random

def welcome():
    """Simple welcome screen for the player. Used to explain the rules."""
    print("")
    print(" Welcome to the Goldfishing Game! ".center(150, '*'))
    print("")
    print(" RULES ".center(150, '*'))
    print("")
    print('''Deal 70 damage to win the game
The game has 2 phases, phase 1 is when you have dealt between 0-30 damage. 
In this phase play as if there are 3 other players alive, use the D6 table below.
Phase 2 is once you have dealt between 30-70 damage.
In this phase assume there are 2 players alive, use the D8 table below.

Each turn after your end step, gain a time counter. 
Then you lose life equal to the amount of time counters you currently have.
Time counters can be removed by playing interaction beyond when forced.
-1 counter for single target interaction, -2 for mass interaction.
You gain +1 time counter for every 20 damage you deal.
Giving an opponent an advantage gains +1 time counter. (Giving a card or permanent, demonstrating a spell.)
Ending a turn with 0 Blockers gains +1 time counters.
As soon as a player hits 7 Time counters for the first time in this game, Destroy all creatures. 
(this can be responded to if able) This happens again at 10 time counters. 

Attacking and Blocking -  All creatures you control are able to freely attack in phase 1.
In phase 2 all creatures may attack, whenever one or more creatures smaller than 3/3 attack destroy a number of 
those creatures equal to the current number of time counters before the damage step. 
(This is intended to simulate blocking in the late game, and prevent small utility creatures for getting in for damage that are not meant to.)
Dealing more than 20 damage in a single attack, -1 Time counters. 


Starting at the end of any turn where you were able to produce 3 mana you roll the dice. 
Follow the result on the charts below. If you are unable to meet the conditions for a roll you gain +1 time counter. 
(this does not apply if you counter the effect with a spell of your own.)
Phase 1 - D6
1. Nothing
2. Destroy a single permanent that would be the most detrimental to your current board.
3. Sacrifice a nonland permanent of your choice.  
4. Exile all graveyards, tap then place a stun counter on a creature at random.
5. Discard a card of your choice.
6. Return the permanent with the highest mana value to your hand.
Phase 2 - D8
1. Nothing
2. Destroy a single permanent that would be the most detrimental to your current board.
3. Sacrifice a nonland permanent at random.
4. Exile all graveyards, tap then place a stun counter on a creature at random.
5. Discard a card at random.
6. Return the permanent with the highest mana value to your hand.
7. Put the nonland nontoken permanent with the lowest converted mana cost on top of your library. 
8. Destroy all creatures. -1 Time counters''')
    print("".center(150, '*'))


class Player:
    """Where all the player's information is stored.

    Keywords:
        lifeTotal -- Player's life total
        turn -- Player turn count
        oppLifeTotal -- Opponents' life total
        numOpp -- Number of opponents left
        timeSeven -- player reached 7 time counters for the first time.
        timeTen -- player reached 10 time counters for the first time.
        time -- Time counters
        checkpoint -- Opponents' life total checkpoint for if the player needs to increment time counter
    """
    lifeTotal = 40
    turn = 1
    oppLifeTotal = 70
    numOpp = 3
    time = 0
    timeSeven = False
    timeTen = False
    checkpoint = 50

    def display(self):
        """Display the player's stats before each action is taken."""
        print()
        print("".center(150, "*"))
        print("Current life total: {}".format(self.lifeTotal).center(150, " "))
        print("Current number of time counters: {}".format(self.time).center(150, " "))
        print("Current turn: {}".format(self.turn).center(150, " "))
        print("Current opponents' life total: {}".format(self.oppLifeTotal).center(150, " "))
        print("Current number of opponents: {}".format(self.numOpp).center(150, " "))
        print("".center(150, "*"))


    def play(self):
        """Tracking the game for the player. Will take an input from the player and act accordingly.

        Keywords:
            action -- the player's input.
            damage -- how much damage the player has dealt to the opponents.
            blockers -- if blockers is 0, increase time counter.
        """
        print("")
        print("Let's Play!".center(150, '*'))
        while self.oppLifeTotal > 0 and self.lifeTotal > 0:
            self.display()
            print("")
            print(" TURN ACTION! ".center(150, '*'))
            action = input("\nWhen you are finsh [P]ass the turn.\n"
                           "What did you do this turn? [S]ingle Target Interaction, "
                            "[M]ass Interaction, [D]elt Damage, or gave an [A]dvantage?: ").upper()
            if action not in "SMDAP" or len(action) != 1:
                print("Please enter a valid action.")
                continue
            if action == 'S':
                self.time -= 1
            elif action == 'M':
                self.time -= 2
            elif action == 'D':
                try:
                    damage = int(input("How much damage did you deal?: "))
                    self.oppLifeTotal -= damage
                    if self.oppLifeTotal <= 40:
                        self.numOpp -= 1
                    if self.oppLifeTotal < self.checkpoint:
                        self.checkpoint -= 20
                        self.time += 1
                except ValueError:
                    print("Please enter a number.")
            elif action == 'A':
                self.time += 1
            elif action == 'P':
                self.end_turn()
            if self.time >= 10 and self.timeTen == False:
                print("*** WIPE THE BOARD OF ALL CREATURES!!! TIME COUNTERS HAS REACHED 10! ***".center(150, '*'))
                self.timeTen = True
            elif self.time >= 7 and self.timeSeven == False:
                print("*** WIPE THE BOARD OF ALL CREATURES!!! TIME COUNTERS HAS REACHED 7! ***".center(150, '*'))
                self.timeSeven = True

    def end_turn(self):
        """Handling the end of the turn.
        Keywords:
        blockers -- if blockers is 0, increase time counter.
        mana -- if mana is 3 or greater, roll dice"""
        try:
            blockers = int(input("How many blockers do you have?: "))
            mana = int(input("How much mana can you produce?: "))
            if blockers == 0:
                self.time += 1
            if mana >= 3:
                self.roll()
            self.time += 1
            self.turn += 1
            self.lifeTotal -= self.time
        except ValueError:
            print("Please enter a number.")

    def roll(self):
        """Roll dice. This handles the dice rolling for depending on the phase.
        Keywords:
        random_num -- Simulate rolling either a d6 or a d8"""
        print("")
        print("*** Rolling Dice! ***".center(150, '*'))
        if self.oppLifeTotal <= 30:
            random_num = random.randint(1, 8)
            print("\nYou rolled a {}".format(random_num))
            if random_num == 1:
                print("Nothing happened.")
            elif random_num == 2:
                print("Destroy a single permanent that would be the most detrimental to your current board.")
            elif random_num == 3:
                print("Sacrifice a nonland permanent at random.")
            elif random_num == 4:
                print("Exile all graveyards, tap then place a stun counter on a creature at random.")
            elif random_num == 5:
                print("Discard a card at random.")
            elif random_num == 6:
                print("Return the permanent with the highest mana value to your hand.")
            elif random_num == 7:
                print("Put the nonland nontoken permanent with the lowest converted mana cost on top of your library.")
            elif random_num == 8:
                print("Destroy all creatures. -1 Time counters.")
                self.time -= 1
        else:
            random_num = random.randint(1, 6)
            print("\nYou rolled a {}".format(random_num))
            if random_num == 1:
                print("Nothing happened.")
            elif random_num == 2:
                print("Destroy a single permanent that would be the most detrimental to your current board.")
            elif random_num == 3:
                print("Sacrifice a nonland permanent of your choice.")
            elif random_num == 4:
                print("Exile all graveyards, tap then place a stun counter on a creature at random.")
            elif random_num == 5:
                print("Discard a card of your choice.")
            elif random_num == 6:
                print("Return the permanent with the highest mana value to your hand.")
        print()

if __name__ == '__main__':

    player = Player()

    welcome()
    while True:
        try:
            userInput = input("\nDo you want to play? [Y]es or [N]o? ").upper()
            if userInput not in "YN" or len(userInput) != 1:
                raise ValueError("Please enter a valid input.")
            if userInput == 'Y':
                break
            elif userInput == 'N':
                exit()
        except ValueError:
            print("Please enter a valid input.")
    player.play()
    if player.oppLifeTotal == 0:
        print()
        print("*** CONGRATULATIONS!!! YOU WON!!! ***".center(150, '*'))
        exit()
    print()
    print("*** You Lost. Better luck next time! ***".center(150, '*'))
