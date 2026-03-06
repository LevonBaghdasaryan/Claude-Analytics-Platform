import json
import pandas as pd
import sqlite3
import os

def process_telemetry():
    """
    ETL Script: Extracts telemetry data from JSONL, 
    merges with employee CSV, and loads into SQLite.
    """
    
    # Define file paths
    csv_file = 'employees.csv'
    jsonl_file = 'telemetry_logs.jsonl'
    db_file = 'claude_analytics.db'

    # 1. Check if source files exist
    if not os.path.exists(csv_file) or not os.path.exists(jsonl_file):
        print(f"Error: Required files ({csv_file} or {jsonl_file}) not found.")
        return

    print("Step 1: Loading and validating employee metadata...")
    employees_df = pd.read_csv(csv_file)
    
    # Basic Validation: Ensure no duplicate emails
    employees_df = employees_df.drop_duplicates(subset=['email'])

    print("Step 2: Parsing telemetry logs (JSONL)...")
    telemetry_data = []

    try:
        with open(jsonl_file, 'r') as f:
            for line_num, line in enumerate(f, 1):
                try:
                    batch = json.loads(line)
                    for event_wrapper in batch.get('logEvents', []):
                        # Parse the nested message string into JSON
                        event = json.loads(event_wrapper['message'])
                        attrs = event.get('attributes', {})
                        
                        # Extract necessary fields
                        row = {
                            'timestamp': attrs.get('event.timestamp'),
                            'event_type': event.get('body'),
                            'email': attrs.get('user.email'),
                            'model': attrs.get('model'),
                            'input_tokens': int(attrs.get('input_tokens', 0)),
                            'output_tokens': int(attrs.get('output_tokens', 0)),
                            'cost': float(attrs.get('cost_usd', 0.0)),
                            'duration_ms': int(attrs.get('duration_ms', 0)),
                            'tool_name': attrs.get('tool_name')
                        }
                        telemetry_data.append(row)
                except Exception as e:
                    print(f"Skipping malformed line {line_num}: {e}")

        # 3. Create DataFrame and Data Cleaning
        df_telemetry = pd.DataFrame(telemetry_data)
        
        # Validation: Remove rows with missing critical data (timestamp or email)
        df_telemetry = df_telemetry.dropna(subset=['timestamp', 'email'])

        print("Step 3: Merging datasets...")
        # Left Join with employees metadata
        final_df = pd.merge(df_telemetry, employees_df, on='email', how='left')

        print("Step 4: Saving to SQLite database...")
        conn = sqlite3.connect(db_file)
        final_df.to_sql('telemetry_usage', conn, if_exists='replace', index=False)
        conn.close()

        print("-" * 30)
        print("SUCCESS: Data processing completed!")
        print(f"Total rows processed: {len(final_df):,}")
        print(f"Database created: {db_file}")
        print("-" * 30)

    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    process_telemetry()