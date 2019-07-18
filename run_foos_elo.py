import pandas as pd
import numpy as np
import re
import foos


# Pull the specific data, make it single-player only
results_df = pd.read_csv('Table football (Responses) - Form.csv')

# Get rid of the ridiculous Google Forms brackets things
def mapper(old_name):
    match = re.search('\[(.*)\]$', old_name)
    if match:
        return match.group(1)
    else:
        return old_name
    
results_df.rename(columns=mapper, inplace=True)

# Single player only (for now)
results_df = results_df[results_df['PlayerCount'] == 2]


cols = ['winner_name', 'loser_name', 'winning_score', 'winner_starting_elo', 
        'loser_starting_elo', 'winner_ending_elo', 'loser_ending_elo']
results_df = results_df.assign(**{col: np.nan for col in cols})
results_df['losing_score'] = results_df['Losing score']

# Update dataframes with winners and losers
results_df['winner_name'] = results_df.apply(foos.status_to_player, axis=1, status='Winning')
results_df['loser_name'] = results_df.apply(foos.status_to_player, axis=1, status='Losing')

# Create empty Elo table with names of all players
elo_df = pd.DataFrame(columns=np.unique(results_df[['winner_name', 'loser_name']]))

# Set winning scores
results_df['winning_score'] = results_df['Tick if this was played to five, leave blank otherwise'].replace({'We played to five': 5, np.nan: 10})


# Reset the index so 
results_df = results_df.reset_index()


# Iterate over the rows
# This could be faster/better by using the 'apply' method on entire columns
# and filtering the Elo table by date
for i, row in results_df.iterrows():
    # Starting Elos
    row_starting_elo = foos.start_elo(row, 'winner_name', elo_df, default_elo=20)
    results_df['winner_starting_elo'].at[i] = row_starting_elo
    row_starting_elo = foos.start_elo(row, 'loser_name', elo_df, default_elo=20)
    results_df['loser_starting_elo'].at[i] = row_starting_elo

    # Ending Elos
    winner_score = foos.calc_score(row['winning_score'], row['losing_score'])
    loser_score = foos.calc_score(row['losing_score'], row['winning_score'])

    winner_exp = foos.calc_expected(results_df['winner_starting_elo'].at[i], results_df['loser_starting_elo'].at[i])
    loser_exp = foos.calc_expected(results_df['loser_starting_elo'].at[i], results_df['winner_starting_elo'].at[i])

    winner_ending_elo = foos.elo(results_df['winner_starting_elo'].at[i], winner_exp, winner_score)
    results_df['winner_ending_elo'].at[i] = winner_ending_elo
    loser_ending_elo = foos.elo(results_df['loser_starting_elo'].at[i], loser_exp, loser_score)
    results_df['loser_ending_elo'].at[i] = loser_ending_elo

    # Assign new Elos in elo_table
    new_results = results_df.loc[i][['winner_ending_elo', 'loser_ending_elo']]
    new_results.index = results_df.loc[i][['winner_name', 'loser_name']]
    elo_df = elo_df.append(new_results)
    
elo_df = elo_df.ffill()

results_df.to_csv('results.csv')
elo_df.to_csv('elo.csv')