import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os

def generate_sample_data(num_campaigns: int = 1000) -> pd.DataFrame:
    """
    Generate sample marketing campaign data.
    
    Args:
        num_campaigns (int): Number of campaigns to generate
        
    Returns:
        pd.DataFrame: Generated sample data
    """
    # Set random seed for reproducibility
    np.random.seed(42)
    
    # Define possible values for categorical columns
    companies = ['Innovate Industries', 'NexGen Systems', 'Alpha Innovations', 'DataTech Solutions', 'FutureBrands']
    campaign_types = ['Email', 'Influencer', 'Display', 'Social Media', 'Search']
    target_audiences = ['Men 18-24', 'Women 35-44', 'Men 25-34', 'All Ages', 'Women 25-34']
    channels = ['Google Ads', 'YouTube', 'Facebook', 'Instagram', 'TikTok']
    locations = ['Chicago', 'New York', 'Los Angeles', 'Miami', 'San Francisco']
    languages = ['English', 'Spanish', 'French', 'German', 'Mandarin']
    customer_segments = ['Health & Wellness', 'Fashionistas', 'Outdoor Adventurers', 'Tech Enthusiasts', 'Foodies']
    
    # Generate dates
    start_date = datetime(2021, 1, 1)
    dates = [
        start_date + timedelta(days=i)
        for i in range(num_campaigns)
    ]
    
    # Generate durations (as strings like "30 days")
    durations = [f"{np.random.choice([15, 30, 45, 60, 90])} days" for _ in range(num_campaigns)]
    
    # Generate metrics with realistic relationships
    impressions = np.random.uniform(1000, 10000, num_campaigns).astype(int)
    
    # CTR between 0.5% and 20%
    clicks = np.random.uniform(100, 1000, num_campaigns).astype(int)
    
    # Conversion rate between 1% and 15%
    conversion_rates = np.random.uniform(0.01, 0.15, num_campaigns)
    
    # Engagement scores (1-10)
    engagement_scores = np.random.randint(1, 11, num_campaigns)
    
    # Acquisition costs with currency format
    acquisition_costs = [f"${np.random.uniform(5000, 20000):.2f}".replace('.00', '') for _ in range(num_campaigns)]
    
    # ROI values
    roi_values = np.random.uniform(1.0, 10.0, num_campaigns)
    
    # Create DataFrame
    data = pd.DataFrame({
        'Campaign_ID': range(1, num_campaigns + 1),
        'Company': np.random.choice(companies, num_campaigns),
        'Campaign_Type': np.random.choice(campaign_types, num_campaigns),
        'Target_Audience': np.random.choice(target_audiences, num_campaigns),
        'Duration': durations,
        'Channel_Used': np.random.choice(channels, num_campaigns),
        'Conversion_Rate': conversion_rates,
        'Acquisition_Cost': acquisition_costs,
        'ROI': roi_values,
        'Location': np.random.choice(locations, num_campaigns),
        'Language': np.random.choice(languages, num_campaigns),
        'Clicks': clicks,
        'Impressions': impressions,
        'Engagement_Score': engagement_scores,
        'Customer_Segment': np.random.choice(customer_segments, num_campaigns),
        'Date': dates
    })
    
    # Format the Acquisition_Cost to include commas for thousands
    data['Acquisition_Cost'] = data['Acquisition_Cost'].apply(
        lambda x: "${:,.2f}".format(float(x.replace('$', '').replace(',', '')))
    )
    
    return data

def main():
    """Generate and save sample marketing campaign data."""
    # Create directories if they don't exist
    os.makedirs('data/raw', exist_ok=True)
    
    # Generate sample data
    data = generate_sample_data(num_campaigns=1000)
    
    # Save to CSV
    output_file = 'data/raw/marketing_campaign_dataset.csv'
    data.to_csv(output_file, index=False)
    print(f"Sample data generated and saved to {output_file}")
    print(f"Generated {len(data)} campaign records")
    
    # Display a sample of the data
    print("\nSample of generated data:")
    print(data.head(3).to_string())


if __name__ == "__main__":
    main() 