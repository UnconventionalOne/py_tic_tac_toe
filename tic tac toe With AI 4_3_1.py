# Tic Tac Toe With "AI" version 4.3
# Original design from: http://code.activestate.com/recipes/578816-the-game-of-tic-tac-toe-in-python/
# with ridiculous edits and "AI" implementation by Unconventional.
# Currently can only play as 'X' and nothing is logged between games.
# Level 1 and level 5 might be a little extreme ^_^

import random, time

def print_board(board):
    # The game board: 1 = X, 0 = O, -1 = emptry space
    if board != [2,3,4,5,6,7,8,9,10]:
        print "The board looks like this: \n"
    for i in range(3):
        print " ",
        for j in range(3):
            if board[i*3+j] == 1:
                print 'X',
            elif board[i*3+j] == 0:
                print 'O',
            elif board[i*3+j] != -1:
                print board[i*3+j]-1,
            else:
                print ' ',
            if j != 2:
                print " | ",
        print
        if i != 2:
            print "-----+-----+-----"
        else:
            print


def print_instruction():
    print "Please use the following cell numbers to make your move:"
    print_board([2,3,4,5,6,7,8,9,10])


def comp_response(board, move, numbers, level, check):
    # When check == 10, comp_response checks for tie.
    win_cond = ((1,2,3),(4,5,6),(7,8,9),(1,4,7),(2,5,8),(3,6,9),(1,5,9),(3,5,7))
    corners = [1, 3, 7, 9]
    sides = [2, 4, 6, 8]
    # Following conditions are for catching the two possible "garanteed win" moves.
    trap_cond1 = ((board[4] == 1 and board[0] == 1 and board[8] == 0) or \
        (board[4] == 1 and board[2] == 1 and board[6] == 0) or \
        (board[4] == 1 and board[6] == 1 and board[2] == 0) or \
        (board[4] == 1 and board[8] == 1 and board[0] == 0))
    trap_cond2 = ((board[4] == 0 and board[0] == 1 and board[8] == 1) or \
          (board[4] == 0 and board[2] == 1 and board[6] == 1))

    # If fist X move is center, comp chooses corner. Else chooses center.
    if move == 1 and (level == 4 or level == 5):
        if board[4] == 1:
            rand1 = random.choice(corners)
            return rand1 - 1
        else:
            return 5-1
    # Following prevents X from doing a particular "guaranteed" win move.
    elif move == 3 and (level == 5) and trap_cond1:
        move3a = True
        while move3a:
            rand3a = random.choice(corners) - 1
            if board[rand3a] == -1:
                return rand3a
    # Following prevents X from executing the other "guaranteed" win move.
    elif move == 3 and (level == 5) and trap_cond2:
        move3b = True
        while move3b:
            rand3b = random.choice(sides) - 1
            if board[rand3b] == -1:
                return rand3b
    # Only check for tie when move >= 7. Was set to 6, but that was more annoying than helpful.       
    elif move < 7 and check == 10:
        return 'notend'
            
    else:
        cond = False
        offensive = False
        # Following checks for two in a row and takes the third spot. After lvl 2, prioritizes offense.
        # Lvl 1 skips all this. Lvl 2 only uses defensive portion.
        for win in win_cond:
            if level !=1 or check == 10:
                # First 3 for offense.
                if (level !=2 or check == 10) and (board[win[0]-1] == 0) and (board[win[1]-1] == 0) and (board[win[2]-1] != 1):
                    cond = True
                    offensive = True
                    value = win[2]-1
                elif (level !=2 or check == 10) and (board[win[1]-1] == 0) and (board[win[2]-1] == 0) and (board[win[0]-1] != 1):
                    cond = True
                    offensive = True
                    value = win[0]-1
                elif (level !=2 or check == 10) and (board[win[0]-1] == 0) and (board[win[2]-1] == 0) and (board[win[1]-1] != 1):
                    cond = True
                    offensive = True
                    value = win[1]-1
                # Last 3 for defense. Only executes if not offensive.
                elif offensive == False and (board[win[0]-1] == 1) and (board[win[1]-1] == 1) and (board[win[2]-1] != 0):
                    cond = True
                    value =win[2]-1
                elif offensive == False and (board[win[1]-1] == 1) and (board[win[2]-1] == 1) and (board[win[0]-1] != 0):
                    cond = True
                    value = win[0]-1
                elif offensive == False and (board[win[0]-1] == 1) and (board[win[2]-1] == 1) and (board[win[1]-1] != 0):
                    cond = True
                    value = win[1]-1

        if check != 10 and cond == False:
            rand2 = random.choice(numbers) -1
            # Following attempts to implement "true" offense. 
            if level in [3,4,5]:
                off = [] # Offensive moves
                trap = [] # See trap_moves in weighted_rand
                for win in win_cond: # Check where possible for O to get 3 in a row
                    if (board[win[0]-1] == 0) and (board[win[1]-1] == -1) and (board[win[2]-1] == -1):
                        off.append(win[1]-1), off.append(win[2]-1)
                    elif (board[win[1]-1] == 0) and (board[win[2]-1] == -1) and (board[win[0]-1] == -1):
                        off.append(win[2]-1), off.append(win[0]-1)
                    elif (board[win[2]-1] == 0) and (board[win[0]-1] == -1) and (board[win[1]-1] == -1):
                        off.append(win[0]-1), off.append(win[1]-1)
##                print 'off: ' + str(off)
                # Following uses weighted_rand function to allow all moves, but prefer some over others
                if move == 3 and (level == 4 or level == 3) and (trap_cond1 or trap_cond2):
                    if trap_cond1:
                        trap = [x for x in off if x+1 in sides]
                    elif trap_cond2:
                        trap = [x for x in off if x+1 in corners]
##                    print "Offensive choices are: " + str([x+1 for x in off]) + ". Trap moves are: " + str([x+1 for x in trap])
                    value = weighted_rand(off, trap, level, numbers)
                elif off != []: # Offense where no trap possible
                    if level ==4 or level == 3: # Stil using wieghted_rand so comp can make "mistakes"
                        value = weighted_rand(off, trap, level, numbers)
                    else:
                        value = random.choice(off)
##                    print "Offensive choices are: " + str([x+1 for x in off]) + ". Trap moves are: " + str([x+1 for x in trap])
                elif board[rand2] == -1:
                    value = rand2
            elif board[rand2] == -1:
                value = rand2
        elif move >= 7 and check == 10 and cond == False and offensive == False:
            value = 'end'
        elif move >= 7 and check == 10 and cond == True:
            value = 'notend'

        return value


def weighted_rand(open_offensive_moves, trap_moves, level, numbers):
    # Best way I could think to deal with garanteed win moves on lvl 4.
    # Extended for use with lvl 3 and for generally less scripted looking play on 3 & 4.
    weighted = []
    if level == 4:
        x = 5
        y = 25
        z = 1
    else: # Not yet decided on how this lvl (3) should be weighted. Ditto 4, I guess.
        x = 2
        y = 2
        z = 3
    for number in [f-1 for f in numbers]:
        w = []
        if number not in open_offensive_moves: # Neutral moves
            w = [number] * x
        elif number in trap_moves: # "Offensive" moves that ironically force X into a "guaranteed" win
            w = [number] * z
        else:
            w = [number] * y 
        weighted.extend(w)
##    print "weighted list: " + str([x+1 for x in weighted])
    return random.choice(weighted)


def get_count(count):
    # For special ending.
    counting = count - 1
    return counting


def noob(blarb):
    # Because...why not?
    if 'noob' in blarb.lower() or 'newb' in blarb.lower():
        print "\nTakes one to know one, noob ^_^"
    else:
        pass


def get_input(turn, board, count):
    valid = False
    while not valid:
        try:
            user = raw_input("Where would you like to place " + turn + " (1-9)? ")
            user = int(user)
            if user >= 1 and user <= 9:
                return user-1
            else:
                counting = get_count(count)
                print_instruction()
                print_board(board)
                print "\n" + str(user) + " is not a valid move! Please try again.\n"
                return counting
        except:# Exception as e:
            counting = get_count(count)
            print_instruction()
            print_board(board)
            noob(user)
            print "\n" + user + " is not a valid move! Please try again.\n"
            return counting


def check_win(board):
    win_cond = ((1,2,3),(4,5,6),(7,8,9),(1,4,7),(2,5,8),(3,6,9),(1,5,9),(3,5,7))
    value = -1
    for each in win_cond:
        if board[each[0]-1] == board[each[1]-1] and board[each[1]-1] == board[each[2]-1]:
            value = board[each[0]-1]
    return value


def quit_game(board,msg):
        try:
            gameend = raw_input(msg + "\nDo you wish to continue? Type Y or N:")
            if gameend in ['n', 'N', 'No', 'no', 'NO']:
                quit()
            elif gameend in ['y', 'Y', 'yes', 'Yes', 'YES']:
                main()
            else:
                print "\n" + gameend + " is not a valid response! Please type Y or N.\n"
        # Not sure if all try-excepts in script are necessary...
        except:# Exception as e:
            print "\n" + gameend + " is not a valid response! Please type Y or N.\n"
            

def level_select():
    while True:
        try:
            level = raw_input("Select difficulty level. (1-5):")
            level = int(level)
            if level >= 1 and level <= 5:
                return level
            else:
                print "\n" + str(level) + " is not a valid respose! Please input 1-5.\n"
        except:# Exception as e:
            print "\n" + str(level) + " is not a valid respose! Please input 1-5.\n"


def count_to_break(count, board):
    # Path to special ending.
    if count == -3:
        print "You entered a lot of invalid responses. Is something wrong?\n"
    elif count == -5:
        print "Are you perhaps trying to break the game?\n"
    elif count == - 8:
        print "You are trying to break the game arent you!?\n"
    elif count == - 9:
        print "I warn you! You might not like what lies ahead if you continue down this path!\n"
    elif count == -10:
        print "Does my warning mean nothing to you?\n"
    elif count == -11:
        print "This is your final warning! Stop trying to break the game or there may be consequences!\n"
    elif count == -12:
        get_break(board)
    else:
        pass

    
def get_break(board):
    # Special ending with options.
    print "Game over!!!"
    time.sleep(3)
    print "You broke it!!!!!"
    time.sleep(3)
    print "Are you happy now?!!!!!!"
    time.sleep(3)
    broken = raw_input("Respond darn it!!!!!!!!!!")
    if broken in ['n', 'N', 'No', 'no', 'NO']:
        print "Good..."
        time.sleep(3)
        print "If you were happy, I would have been very mad.\nI might even have been mad enough to punish you..."
        time.sleep(6)
        print "\nBut if you feel remorseful, then I suppose I can forgive you just this once...",\
              "and will let you play again...\n"
        time.sleep(8)
        print "but next time I might not be so forgiving...\n"
        time.sleep(5)
        msg1 = "So..."
        quit_game(board, msg1) # For continue option

    else:
        if broken in ['y', 'Y', 'yes', 'Yes', 'YES']:
            print "So this does make you happy?!!!"
        else:
            print "Computer takes your improper response as a yes!"
            time.sleep(3)
            print "So this does make you happy..."
        time.sleep(3)
        print "\nWell guess what? Computer not happy!!!!!!"
        time.sleep(4)
        print "\nComputer very not happy!!!!!"
        time.sleep(3)
        print "\nComputer so very not happy, computer not able speak proper anymore!!!!!!"
        time.sleep(5)
        print "\nComputer punish!!!!!!!\n"
        time.sleep(2)
        # Following (minus text) is from http://www.asciiworld.com/-Robots,24-.html
        print r'''      _n____n__
     /         \---||--<
    /___________\ 
    _|____|____|_   EXTERMINATE!
    _|____|____|_   EXTERMINATE!!
     |    |    |    EXTERMINATE!!!
    --------------  
    | || || || ||\
    | || || || || \++++++++------<
    ===============  
    |   |  |  |   |
   (| O | O| O| O |)
   |   |   |   |   |
  (| O | O | O | O |)
   |   |   |   |    |
 (| O |  O | O  | O |)
  |   |    |    |    |
 (| O |  O |  O |  O |)
 ======================'''
        time.sleep(6)
        quit()


def main():
    level = level_select()
    print_instruction()
    board = []
    count = -1
    numbers = range(1, 9+1) # Possible locations on board for random move. See below
    for i in range(9):
        board.append(-1)

    win = False
    move = 0
    while not win:
        user = "null"
        print_board(board)
        if move % 2 == 0:
            turn = 'X'
        else:
            turn = 'O'
        print "Turn number " + str(move+1) + ".\n" + turn + "'s move."
        if turn == 'X':
            user0 = get_input(turn, board, count)
            while user0 < 0:
                count = user0
                count_to_break(count, board)
                user0 = get_input(turn, board, count)
            if user0 >= 0:
                user = user0
        elif turn == 'O':
            user = comp_response(board, move, numbers, level, 0)
        if user != "null":
            while board[user] != -1:
                print "\nInvalid move! Cell already taken. Please try again.\n"
                user0 = get_input(turn, board, count)
                if user0 >= 0:
                    user = user0
                else: # If count trigered here, will continue to print "Cell already taken", but whatever.
                    count = user0
                    count_to_break(count, board)
            numbers.remove(user+1)# So numbers represents remaining spots on board
            board[user] = 1 if turn == 'X' else 0

        move += 1
        if move > 4:
            winner = check_win(board)
            tie = comp_response(board, move, numbers, level, 10)
            if winner != -1 and tie != 'end':
                gameover = True
                print_board(board)
                out = "Game over. The winner is "
                out += "X. " if winner == 1 else "O, "
                out += "\nCongratulations! You beat the game on level " if \
                       winner == 1 else "sorry.\nYou lost on level "
                out += str(level) + "!" if winner == 1 else str(level) + "."
                out += "\nMaybe you should try again on a "
                out += "higher level!\n" if winner ==1 else "lower level.\n"
                while gameover:
                    quit_game(board,out)
            elif (move == 9 and winner == -1) or tie == 'end':
                gameover = True
                print_board(board)
                if move == 9:
                    out = "Game over. It's a tie."
                else:
                    out = "Tie game. It's impossible for either side to win."
                while gameover:
                    quit_game(board, out)

if __name__ == "__main__":
    main()
            
