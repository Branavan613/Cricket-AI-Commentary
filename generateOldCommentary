import pandas as pd
import json

# Load datasets
commentary_df = pd.read_csv('IPL_Match_Highlights_Commentary.csv')
schedule_df = pd.read_csv('IPL_SCHEDULE_2008_2020.csv')

# Preprocess commentary dataset
commentary_df[['Team', 'Innings']] = commentary_df['Team'].str.extract(r'(.+?)\s+(\d\w+\sInns)')
commentary_df[['Bowler', 'Batsman']] = commentary_df['batsman'].str.extract(r'(.+?)\s+to\s+(.+)')
commentary_df.drop('batsman', axis=1, inplace=True)
commentary_df = commentary_df.dropna()

# Preprocess schedule dataset
schedule_df['Match_Date'] = pd.to_datetime(schedule_df['Match_Date'], errors='coerce')
schedule_df[['Team1', 'Team2']] = schedule_df['Match_Team'].str.split(' vs ', expand=True)
schedule_df.drop(columns=['Match_Cricbuzz_URL', 'Highlights_available'], inplace=True)
schedule_df['Match_Result'] = schedule_df['Match_Result'].fillna('Result Unknown')

# Merge datasets
merged_df = pd.merge(commentary_df, schedule_df, on='Match_id', how='inner')
final_df = merged_df[['Match_id', 'IPL_year', 'Match_Date', 'Stadium', 'Location',
                       'Team1', 'Team2', 'Team', 'Innings', 'Over_num',
                       'Bowler', 'Batsman', 'score', 'Commentary', 'Match_Result']]

# Define commentary function
def generate_commentary(bowler, batsman, outcome, over):
    over_formatted = f"{int(over)}.{int((over % 1) * 10)}"
    if outcome.upper() == "FOUR":
        return f"Over {over_formatted}: {batsman} smashes {bowler} for a boundary!"
    elif outcome.upper() == "SIX":
        return f"Over {over_formatted}: {batsman} launches {bowler} for a huge six!"
    elif outcome.upper() in ["OUT", "WICKET"]:
        return f"Over {over_formatted}: {bowler} gets {batsman} out!"
    elif outcome.isdigit():
        return f"Over {over_formatted}: {batsman} takes {outcome} run(s)."
    return f"Over {over_formatted}: {batsman} faces {bowler}. Outcome: {outcome}."

# Apply AI commentary
target_match = final_df['Match_id'].unique()[0]
match_df = final_df[final_df['Match_id'] == target_match]
match_df['AI_Commentary'] = match_df.apply(
    lambda row: generate_commentary(row['Bowler'], row['Batsman'], row['score'], row['Over_num']), axis=1
)

# Save LLM training data
match_df[['Bowler', 'Batsman', 'score', 'Over_num', 'AI_Commentary']].to_csv('commentary.csv', index=False)

df = pd.read_csv('commentary.csv')
with open('llama_training_data.jsonl', 'w') as f:
    for _, row in df.iterrows():
        json.dump({"instruction": row['Bowler'] + " to " + row['Batsman'], "output": row['AI_Commentary']}, f)
        f.write('\n')

print("Data saved as commentary.csv and llama_training_data.jsonl")
