import msvcrt
import time
import sys
import math
import string
def printTurn(turn, word):
        print("P" + str(turn) + ": " + word, end = '', flush=True)
def printScores():
    print()
    for x in range(1, len(players)):
        print("P" + str(players[x]) + ": " + "G H O S T"[:2*scores[x]] + "- - - - -"[2*scores[x]:])
    print()
def maketrie(words):
    root = dict()
    for word in words:
        current = root
        for letter in word:
            current = current.setdefault(letter, {})
        current[""] = ""
    return root
def intrie(trie, word):
    current = trie
    for letter in word:
        if letter in current:
            current = current[letter]
        else:
            return False
    else:
        return "" in current
def calculateHints(word, trie):
    current = trie
    if len(word) == 0:
        return set(current.keys())
    for x in range(0, len(word)):
        if word[x] in current:
            current = current[word[x]]
            if x == len(word)-1:
                return set(current.keys())
        else:
            return set()
    return set()    
def analyze(prefix, turn, trie):
    reverse = False
    hints = calculateHints(prefix, trie)
    if "" in hints:
        if len(hints) == 1:
            if len(prefix) != 3:
                return(set([1]), set())
    good, bad = set(), set()
    for letter in hints:
        if letter != "":
            tempgood, tempbad = analyze(prefix+letter, (turn%turns)+1, trie)
            if len(tempgood) == 0 and not (intrie(trie, prefix+letter) and len(prefix) > 3):
                good.add(letter)
            else:
                x = 0
                if len(tempbad) > 0:
                    x = round(len(tempgood)/len(tempbad), 1)
                bad.add((x, letter))
    return (good, bad)
####################################
wordlist = open("ghost.txt").read().split()
wordtrie = maketrie(wordlist)
n = len(wordlist)
word = ""
turns = 0
comps = 0
starter = 1
################
##COMMAND LINE##
################
hinted = False
players = []
scores = []
scores.append("Scores:")
players.append("Players:")
for x in range(1, len(sys.argv)):
    arg = sys.argv[x]
    if arg.isdigit() or arg == 'c':
        if arg.isdigit():
            for x in range(0, int(arg)):
                turns += 1
                players.append(str(turns))
        if arg == 'c':
            turns += 1
            comps += 1
            players.append(str(turns)+'C')
    else:
        sys.exit()
turn = 1
for x in range(1, turns+1):
    scores.append(0)
####################################
while True:
    good, bad = analyze(word, turn%turns, wordtrie)
    for e in good:
        break
    if len(good) != 0:
        if not isinstance(e, str):
            tempg = set([x for x in good])
            good = set([y for y in bad])
            bad = tempg
    if turns == 1:
        print("Game over! Player", players[1], "wins!")
        sys.exit()
    prevturn = (len(word)+ starter - 2)%turns+1
    turn = (len(word)+ starter - 1)%turns+1
    printTurn(turn, word) # AFTER CALC TURN
    hints = calculateHints(word, wordtrie)
    # COMPUTER INPUT
    char = None
    if players[turn].endswith("C"):
        if len(hints) == 0 or (len(word) > 3 and intrie(wordtrie, word)):
            char = ' '
        else:
            if len(good) > 0:
                char = good.pop()
            else:
                print(bad)
                char = max(bad)[1]
    #HUMAN INPUT
    else:
        input_char = msvcrt.getch()
        if input_char == b'\x1b':
            sys.exit()
        if input_char != b'\xe0':
            char = input_char.decode("utf-8")
    ## Process input
    if char != None:
        if char.islower() or char == '-':
            print(char)
            word = word + char
        #Challenge
        if char == ' ':
            if len(word) > 3 or len(hints) == 0:
                if intrie(wordtrie, word):
                    scores[prevturn] = scores[prevturn]+1
                    starter = turn
                    print(" is a complete word.")
                else:
                    if len(hints) == 0:
                        scores[prevturn] = scores[prevturn]+1
                        starter = turn
                        print(" is not a valid prefix.")
                    else:
                        scores[turn] = scores[turn]+1
                        starter = prevturn
                        print(" is a valid prefix, but not a word.")
                printScores()
                word = ""
                index = 0
                ## knocked out
                for x in range(1, len(players)):
                    if scores[x] == 5:
                        r = players[x]
                        if r != 0:
                            scores.pop(x)
                            players.remove(r)
                            turns = turns-1
                        break
            else:
                print()
        if char == '.':
            if not hinted:
                hinted = True
                print()
                if len(hints) > 0:
                    print(hints)
                else:
                    print("No hints remaining.")
            else:
                print()
        else:
            hinted = False
        #time.sleep(0.3)
    ## END OF FILE ##
