import pandas as pd
import numpy as np
from pathlib import Path
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MarketingDataLoader:
    """Class for loading and validating marketing campaign data."""
    
    def __init__(self, data_path: str):
        """
        Initialize the data loader.
        
        Args:
            data_path (str): Path to the raw data file
        """
        self.data_path = Path(data_path)
        self.required_columns = [
            'Campaign_ID',
            'Company',
            'Campaign_Type',
            'Target_Audience',
            'Duration',
            'Channel_Used',
            'Conversion_Rate',
            'Acquisition_Cost',
            'ROI',
            'Location',
            'Language',
            'Clicks',
            'Impressions',
            'Engagement_Score',
            'Customer_Segment',
            'Date'
        ]

    def validate_data(self, df: pd.DataFrame) -> bool:
        """
        Validate the loaded dataset structure and content.
        
        Args:
            df (pd.DataFrame): Loaded dataset
            
        Returns:
            bool: True if validation passes, False otherwise
        """
        # Check for required columns
        missing_cols = set(self.required_columns) - set(df.columns)
        if missing_cols:
            logger.error(f"Missing required columns: {missing_cols}")
            return False
        
        # Check for null values
        null_counts = df.isnull().sum()
        if null_counts.any():
            logger.warning(f"Found null values:\n{null_counts[null_counts > 0]}")
        
        # Validate data types
        try:
            # Convert date columns
            df['Date'] = pd.to_datetime(df['Date'])
            
            # Convert numeric columns
            numeric_cols = ['Clicks', 'Impressions', 'Engagement_Score', 'Conversion_Rate', 'ROI']
            df[numeric_cols] = df[numeric_cols].apply(pd.to_numeric)
            
            # Process currency string (Acquisition_Cost)
            if 'Acquisition_Cost' in df.columns:
                df['Acquisition_Cost'] = df['Acquisition_Cost'].str.replace('$', '').str.replace(',', '').astype(float)
            
        except Exception as e:
            logger.error(f"Error converting data types: {str(e)}")
            return False
        
        return True

    def load_data(self) -> pd.DataFrame:
        """
        Load and validate the marketing campaign dataset.
        
        Returns:
            pd.DataFrame: Loaded and validated dataset
        """
        try:
            logger.info(f"Loading data from {self.data_path}")
            df = pd.read_csv(self.data_path)
            
            if self.validate_data(df):
                logger.info("Data validation successful")
                return df
            else:
                logger.error("Data validation failed")
                return None
                
        except Exception as e:
            logger.error(f"Error loading data: {str(e)}")
            return None

    def get_summary_stats(self, df: pd.DataFrame) -> dict:
        """
        Generate summary statistics for the dataset.
        
        Args:
            df (pd.DataFrame): Input dataset
            
        Returns:
            dict: Summary statistics
        """
        summary = {
            'total_campaigns': len(df),
            'campaign_types': df['Campaign_Type'].value_counts().to_dict(),
            'channels': df['Channel_Used'].value_counts().to_dict(),
            'companies': df['Company'].value_counts().to_dict(),
            'date_range': {
                'start': df['Date'].min(),
                'end': df['Date'].max()
            },
            'avg_acquisition_cost': df['Acquisition_Cost'].mean(),
            'total_clicks': df['Clicks'].sum(),
            'total_impressions': df['Impressions'].sum(),
            'avg_conversion_rate': df['Conversion_Rate'].mean(),
            'avg_roi': df['ROI'].mean(),
            'customer_segments': df['Customer_Segment'].value_counts().to_dict()
        }
        
        return summary

if __name__ == "__main__":
    # Example usage
    data_loader = MarketingDataLoader("data/raw/marketing_campaign_dataset.csv")
    df = data_loader.load_data()
    
    if df is not None:
        summary_stats = data_loader.get_summary_stats(df)
        print("\nDataset Summary:")
        for key, value in summary_stats.items():
            print(f"{key}: {value}") 