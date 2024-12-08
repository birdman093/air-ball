from service.BettingLine import NbaBettingLine

def test_betting_line():
    '''
    betting_line api return values at function call time
    '''
    betting_line = NbaBettingLine();
    print(betting_line.get_game_lines())