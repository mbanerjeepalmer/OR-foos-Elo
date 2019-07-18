# coding: utf-8
import numpy as np

class Tidying:
    """ For cleaning the messy data.
    """
    pass

class Rating:
    pass


def status_to_player(row, status):
    """
     
    Parameters
    ----------

    status : str
        Value to search for. Expected to be 'Winning' or 'Losing'.
    """
    # 
    return row[row == status].index[0]

def start_elo(row, player_name_col, elo_df, default_elo=2000):
    """For a row and a DataFrame, find the starting Elo for a given player name.
    
    Parameters:
    -----------
    row : Pandas Series
    player_name_col : string
        Represents the name of the column to be used to get the name from, assuming this uses 'apply' or 'iterrows'.
    elo_df : Pandas DataFrame
    default_elo : int or float
    """
    name = row[player_name_col]
    if elo_df[name].isnull().all():
        return default_elo
    # Return the latest value if they are.
    else:
        # TODO take the index of the current row and filter the Elo table using that as an explicit index instead.
		# Remember that `last_valid_index()` doesn't work when there are duplicate indices.
        return elo_df[name][elo_df[name].notna()].iloc[-1]

def get_loser(row_int, columns, df):
    loser_name = columns[df.iloc[row_int] =='Losing'][0]
    return loser_name

def get_winner(row_int, columns, df):
    winner_name = columns[df.iloc[row_int] =='Winning'][0]
    return winner_name
    
def set_all_losers(df):
    for r in df.index:
        df.loc[r, 'loser'] = get_loser(df, r, df.columns)

def set_all_winners(df):
    for r in df.index:
        df.loc[r, 'winner'] = get_winner(df, r, df.columns)

def get_player_elo():
    # get player unique name
    # look in table for name
    # get most recent value
    pass

def set_player_elo():
    # get player unique name
    # look in table for name
    # set new value
    pass


def calc_expected(player, opponent):
    """
    Calculate expected score of `player` in a match against `opponent`.
    
    Parameters:
    -----------
    player : int or float
        Elo rating for player we're rating
    opponent : int or float
        Elo rating for their opponent
    """
    return 1 / (1 + 10 ** ((opponent - player) / 400))

def calc_score(player, opponent):
    """
    Get score to pass in to an Elo function.
    
    Parameters:
    -----------
    player : into / float
        
    """
    # margin of loss / victory
    margin = (player - opponent) / max(player, opponent)
    # make this elo-friendly
    score = margin / 2 + 0.5
    return score

def elo(old, exp, score, k=32):
    """
    Calculate the new Elo rating for a player
    :param old: The previous Elo rating
    :param exp: The expected score for this match
    :param score: The actual score for this match
    :param k: The k-factor for Elo (default: 32)
    """
    return old + k * (score - exp)


def get_latest_elo(player, default_elo, df):
    if player not in df.columns:
        return default_elo
    else:
        latest_elo = df[['win_result_elo', 'lose_result_elo']][df['carl'].notna()].iloc[-1].dropna()
        if latest_elo.empty:
            return default_elo
        else:
            return latest_elo[0]