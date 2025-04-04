from externalApi import NbaBettingLineApi

def test_betting_line():
    '''
    betting_line api return values at function call time
    '''
    betting_line = NbaBettingLineApi();
    print(betting_line.get_game_lines())