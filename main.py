#!/opt/local/bin/python3
# Main

from game import Game


def main():
    # printIntro()
    game = Game()
    game.playGame()


def printIntro():
    print ('Welcome to Estimation!')
    print ('Do you know the rules? (y/n):')
    rules = input('')
    if (rules == 'n'):
        printRules()
    print ('Good luck!')


def printRules():
    print ('haha nope')


if __name__ == '__main__':
    main()
