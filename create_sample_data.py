import pandas as pd
import os

# Sample data
data = {
    'Campaign_ID': [1, 2, 3, 4, 5],
    'Company': ['Innovate Industries', 'NexGen Systems', 'Alpha Innovations', 'DataTech Solutions', 'NexGen Systems'],
    'Campaign_Type': ['Email', 'Email', 'Influencer', 'Display', 'Email'],
    'Target_Audience': ['Men 18-24', 'Women 35-44', 'Men 25-34', 'All Ages', 'Men 25-34'],
    'Duration': ['30 days', '60 days', '30 days', '60 days', '15 days'],
    'Channel_Used': ['Google Ads', 'Google Ads', 'YouTube', 'YouTube', 'YouTube'],
    'Conversion_Rate': [0.04, 0.12, 0.07, 0.11, 0.05],
    'Acquisition_Cost': ['$16,174.00', '$11,566.00', '$10,200.00', '$12,724.00', '$16,452.00'],
    'ROI': [6.29, 5.61, 7.18, 5.55, 6.5],
    'Location': ['Chicago', 'New York', 'Los Angeles', 'Miami', 'Los Angeles'],
    'Language': ['Spanish', 'German', 'French', 'Mandarin', 'Mandarin'],
    'Clicks': [506, 116, 584, 217, 379],
    'Impressions': [1922, 7523, 7698, 1820, 4201],
    'Engagement_Score': [6, 7, 1, 7, 3],
    'Customer_Segment': ['Health & Wellness', 'Fashionistas', 'Outdoor Adventurers', 'Health & Wellness', 'Health & Wellness'],
    'Date': ['2021-01-01', '2021-01-02', '2021-01-03', '2021-01-04', '2021-01-05']
}

# Create DataFrame
df = pd.DataFrame(data)

# Create directory if it doesn't exist
os.makedirs('data/raw', exist_ok=True)

# Save to CSV
df.to_csv('data/raw/marketing_campaign_dataset.csv', index=False)
print("Sample dataset created successfully!") 