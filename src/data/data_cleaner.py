import pandas as pd
import numpy as np
from typing import Tuple
import logging
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MarketingDataCleaner:
    """Class for cleaning and transforming marketing campaign data."""
    
    def __init__(self):
        """Initialize the data cleaner."""
        self.numeric_columns = [
            'Clicks', 
            'Impressions', 
            'Engagement_Score',
            'Conversion_Rate',
            'ROI'
        ]
        
        self.categorical_columns = [
            'Campaign_Type',
            'Channel_Used',
            'Target_Audience',
            'Location',
            'Language',
            'Customer_Segment'
        ]

    def handle_missing_values(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Handle missing values in the dataset.
        
        Args:
            df (pd.DataFrame): Input dataset
            
        Returns:
            pd.DataFrame: Dataset with handled missing values
        """
        # Handle numeric columns
        for col in self.numeric_columns:
            if df[col].isnull().any():
                median_value = df[col].median()
                df[col].fillna(median_value, inplace=True)
                logger.info(f"Filled missing values in {col} with median: {median_value}")
        
        # Handle categorical columns
        for col in self.categorical_columns:
            if df[col].isnull().any():
                df[col].fillna('Unknown', inplace=True)
                logger.info(f"Filled missing values in {col} with 'Unknown'")
        
        return df

    def remove_duplicates(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Remove duplicate campaign entries.
        
        Args:
            df (pd.DataFrame): Input dataset
            
        Returns:
            pd.DataFrame: Dataset with duplicates removed
        """
        initial_rows = len(df)
        df.drop_duplicates(subset=['Campaign_ID'], keep='first', inplace=True)
        removed_rows = initial_rows - len(df)
        
        if removed_rows > 0:
            logger.warning(f"Removed {removed_rows} duplicate campaign entries")
        
        return df

    def create_derived_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Create derived features from existing data.
        
        Args:
            df (pd.DataFrame): Input dataset
            
        Returns:
            pd.DataFrame: Dataset with additional features
        """
        # Parse duration (e.g., "30 days" to numeric)
        if df['Duration'].dtype == object:
            df['Campaign_Duration'] = df['Duration'].str.extract(r'(\d+)').astype(float)
        else:
            df['Campaign_Duration'] = df['Duration']
        
        # Create campaign duration category
        df['Duration_Category'] = pd.cut(
            df['Campaign_Duration'],
            bins=[0, 7, 30, float('inf')],
            labels=['Short', 'Medium', 'Long']
        )
        
        # Calculate engagement rate
        df['Engagement_Rate'] = df['Clicks'] / df['Impressions']
        
        # Extract time-based features
        df['Month'] = df['Date'].dt.month
        df['Quarter'] = df['Date'].dt.quarter
        df['Year'] = df['Date'].dt.year
        
        # Create engagement category based on Engagement_Score
        df['Engagement_Category'] = pd.cut(
            df['Engagement_Score'],
            bins=[0, 3, 6, 10],
            labels=['Low', 'Medium', 'High']
        )
        
        return df

    def normalize_categorical_values(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Normalize categorical values for consistency.
        
        Args:
            df (pd.DataFrame): Input dataset
            
        Returns:
            pd.DataFrame: Dataset with normalized categories
        """
        # Standardize campaign types
        df['Campaign_Type'] = df['Campaign_Type'].str.title()
        
        # Standardize channels
        df['Channel_Used'] = df['Channel_Used'].str.title()
        
        # Standardize locations
        df['Location'] = df['Location'].str.title()
        
        # Standardize customer segments
        df['Customer_Segment'] = df['Customer_Segment'].str.title()
        
        return df

    def validate_numeric_ranges(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Validate and clean numeric ranges.
        
        Args:
            df (pd.DataFrame): Input dataset
            
        Returns:
            pd.DataFrame: Dataset with validated numeric ranges
        """
        # Ensure all numeric values are positive
        for col in ['Clicks', 'Impressions', 'Engagement_Score']:
            invalid_mask = df[col] < 0
            if invalid_mask.any():
                logger.warning(f"Found {invalid_mask.sum()} negative values in {col}")
                df.loc[invalid_mask, col] = df[col].median()
        
        # Process Acquisition_Cost if it's a string
        if df['Acquisition_Cost'].dtype == object:
            df['Acquisition_Cost'] = df['Acquisition_Cost'].str.replace('$', '').str.replace(',', '').astype(float)
        
        # Ensure conversion rate is between 0 and 1
        invalid_conv_rate = (df['Conversion_Rate'] < 0) | (df['Conversion_Rate'] > 1)
        if invalid_conv_rate.any():
            logger.warning(f"Found {invalid_conv_rate.sum()} invalid conversion rates")
            df.loc[invalid_conv_rate, 'Conversion_Rate'] = df['Conversion_Rate'].median()
        
        return df

    def clean_data(self, df: pd.DataFrame) -> Tuple[pd.DataFrame, dict]:
        """
        Clean and transform the marketing campaign dataset.
        
        Args:
            df (pd.DataFrame): Raw input dataset
            
        Returns:
            Tuple[pd.DataFrame, dict]: Cleaned dataset and cleaning summary
        """
        initial_rows = len(df)
        
        # Apply cleaning steps
        df = self.handle_missing_values(df)
        df = self.remove_duplicates(df)
        df = self.normalize_categorical_values(df)
        df = self.validate_numeric_ranges(df)
        df = self.create_derived_features(df)
        
        # Generate cleaning summary
        cleaning_summary = {
            'initial_rows': initial_rows,
            'final_rows': len(df),
            'rows_removed': initial_rows - len(df),
            'derived_features_added': [
                'Campaign_Duration',
                'Duration_Category',
                'Engagement_Rate',
                'Month',
                'Quarter',
                'Year',
                'Engagement_Category'
            ]
        }
        
        return df, cleaning_summary

def save_cleaned_data(df: pd.DataFrame, output_path: str):
    """
    Save the cleaned dataset to a CSV file.
    
    Args:
        df (pd.DataFrame): Cleaned dataset
        output_path (str): Path to save the cleaned data
    """
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    df.to_csv(output_path, index=False)
    logger.info(f"Saved cleaned dataset to {output_path}")

if __name__ == "__main__":
    # Example usage
    from data_loader import MarketingDataLoader
    
    # Load raw data
    data_loader = MarketingDataLoader("data/raw/marketing_campaign_dataset.csv")
    raw_df = data_loader.load_data()
    
    if raw_df is not None:
        # Clean data
        cleaner = MarketingDataCleaner()
        cleaned_df, summary = cleaner.clean_data(raw_df)
        
        # Save cleaned data
        save_cleaned_data(cleaned_df, "data/processed/cleaned_campaign_data.csv")
        
        # Print cleaning summary
        print("\nCleaning Summary:")
        for key, value in summary.items():
            print(f"{key}: {value}") 