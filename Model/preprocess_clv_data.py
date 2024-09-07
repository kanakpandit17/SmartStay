# preprocess_clv_data.py
import os
import pandas as pd
from datetime import datetime

def process_clv_data():
    # Directory for saving CSV files
    csv_folder = 'csv_files'

    # Create the directory if it doesn't exist
    if not os.path.exists(csv_folder):
        os.makedirs(csv_folder)

    # Current time
    current_time = datetime.now()

    # Load the CSV file
    file_name = 'csv_files/final-rectfied-clv-data.csv'
    df1 = pd.read_csv(file_name)

    # Ensure check_out_date is in datetime format
    df1['check_out_date'] = pd.to_datetime(df1['check_out_date'], errors='coerce')

    # Step 1: Compute frequency of bookings for each guest
    df1['frequency_of_bookings'] = df1.groupby('guest_id')['guest_id'].transform('count')

    # Step 2: Calculate time since last booking based on the latest check_out_date in the dataset
    df1['days_since_last_booking'] = df1.groupby('guest_id')['check_out_date'].transform(
        lambda x: (pd.to_datetime(current_time) - x.iloc[-1]).days if pd.notna(x.iloc[-1]) else None
    )

    # Step 3: Calculate total revenue generated for each guest
    df1['total_revenue_generated'] = df1.groupby('guest_id')['grand_total_amount'].transform('sum')

    # Step 4: Calculate average stay duration for each guest
    df1['average_stay_duration'] = df1.groupby('guest_id')['duration_of_stay'].transform('mean')

    # Step 5: Calculate total amount spent on meals by each guest
    df1['total_meal_charges'] = df1.groupby('guest_id')['meal_charges'].transform('sum')

    # Step 6: Round values to 2 decimal places for the following
    df1['total_revenue_generated'] = df1['total_revenue_generated'].round(2)
    df1['average_stay_duration'] = df1['average_stay_duration'].round(2)
    df1['total_meal_charges'] = df1['total_meal_charges'].round(2)

    # Updated dataframe
    result_df = df1[['guest_id', 'guest_name', 'email_id', 'frequency_of_bookings', 
                     'days_since_last_booking', 
                     'average_stay_duration', 'total_meal_charges','total_revenue_generated']].drop_duplicates().reset_index(drop=True)

    # Save the modified dataframe to csv_files directory
    result_df.to_csv(os.path.join(csv_folder, 'condensed-clv-data.csv'), index=False)
    df1.to_csv(os.path.join(csv_folder, 'final-clv-data.csv'), index=False)