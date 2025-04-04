from databases import Database

def newSeason():
    '''Set Daily Script parameters for new season'''
    db: Database = Database(reset_parameters=True)
    