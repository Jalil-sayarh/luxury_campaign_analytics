import pandas as pd
import numpy as np
from datetime import datetime
from typing import Dict, List, Optional
import logging
import json
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MarketingDataProcessor:
    """
    Handles the processing of marketing campaign data according to project requirements.
    """
    
    def __init__(self, input_file: str):
        """
        Initialize the data processor.
        
        Args:
            input_file (str): Path to the input CSV file
        """
        self.input_file = input_file
        self.data = None
        self.required_columns = [
            'Campaign_ID', 'Company', 'Campaign_Type', 'Target_Audience', 'Duration',
            'Channel_Used', 'Conversion_Rate', 'Acquisition_Cost', 'ROI', 'Location',
            'Language', 'Clicks', 'Impressions', 'Engagement_Score', 'Customer_Segment', 'Date'
        ]

    def validate_data(self) -> bool:
        """
        Validate the data structure and content.
        
        Returns:
            bool: True if validation passes, False otherwise
        """
        try:
            # Check for required columns
            missing_cols = set(self.required_columns) - set(self.data.columns)
            if missing_cols:
                logger.error(f"Missing required columns: {missing_cols}")
                return False
            
            # Validate data types
            expected_types = {
                'Campaign_ID': 'object',
                'Impressions': 'number',
                'Clicks': 'number',
                'Engagement_Score': 'number'
            }
            
            for col, expected_type in expected_types.items():
                if expected_type == 'number':
                    if not pd.to_numeric(self.data[col], errors='coerce').notna().all():
                        logger.error(f"Invalid data type in column {col}")
                        return False
            
            return True
            
        except Exception as e:
            logger.error(f"Validation error: {str(e)}")
            return False

    def load_data(self) -> bool:
        """
        Load the CSV file and perform initial validation.
        
        Returns:
            bool: True if loading succeeds, False otherwise
        """
        try:
            # Read CSV in chunks for memory efficiency
            chunks = []
            for chunk in pd.read_csv(self.input_file, chunksize=50000):
                chunks.append(chunk)
            self.data = pd.concat(chunks, ignore_index=True)
            
            logger.info(f"Successfully loaded data with {len(self.data)} rows")
            return self.validate_data()
        except Exception as e:
            logger.error(f"Error loading data: {str(e)}")
            return False

    def clean_data(self) -> None:
        """
        Clean the data according to project requirements.
        """
        # Convert dates
        self.data['Date'] = pd.to_datetime(self.data['Date'])
        
        # Process Duration (can be a string with format like "30 days")
        if self.data['Duration'].dtype == object:
            self.data['Duration_Days'] = self.data['Duration'].str.extract(r'(\d+)').astype(float)
        
        # Process Acquisition_Cost (can be a string with format like "$16,174.00")
        if self.data['Acquisition_Cost'].dtype == object:
            self.data['Acquisition_Cost'] = self.data['Acquisition_Cost'].str.replace('$', '').str.replace(',', '').astype(float)
        
        # Handle missing values for numeric columns
        numeric_cols = ['Clicks', 'Impressions', 'Engagement_Score']
        for col in numeric_cols:
            median_value = self.data[col].median()
            self.data[col] = self.data[col].fillna(median_value)
        
        # Handle missing values for categorical columns
        categorical_cols = ['Channel_Used', 'Target_Audience', 'Location', 'Language', 'Customer_Segment']
        for col in categorical_cols:
            self.data[col] = self.data[col].fillna('Unknown')
        
        # Remove duplicates
        self.data = self.data.drop_duplicates(subset=['Campaign_ID'], keep='first')
        
        # Add derived features
        # Create month, quarter, year columns from Date
        self.data['Month'] = self.data['Date'].dt.month
        self.data['Quarter'] = self.data['Date'].dt.quarter
        self.data['Year'] = self.data['Date'].dt.year
        
        # Calculate click-through rate (CTR)
        self.data['CTR'] = self.data['Clicks'] / self.data['Impressions']
        
        # Create engagement categories
        self.data['Engagement_Category'] = pd.cut(
            self.data['Engagement_Score'], 
            bins=[0, 3, 6, 10], 
            labels=['Low', 'Medium', 'High']
        )
        
        logger.info("Data cleaning completed successfully")

    def transform_data(self) -> None:
        """
        Transform data and create additional features.
        """
        # Add time-based features
        self.data = self.data.assign(
            Campaign_Month=self.data['Date'].dt.month,
            Campaign_Quarter=self.data['Date'].dt.quarter,
            Campaign_Year=self.data['Date'].dt.year
        )
        
        # Calculate campaign duration
        self.data = self.data.assign(
            Campaign_Duration=(self.data['Date'].max() - self.data['Date'].min()).days
        )
        
        # Create duration categories
        self.data = self.data.assign(
            Duration_Category=pd.cut(
                self.data['Campaign_Duration'],
                bins=[0, 7, 30, float('inf')],
                labels=['Short', 'Medium', 'Long']
            )
        )
        
        # Calculate CTR (Click-Through Rate)
        self.data['CTR'] = self.data['Clicks'] / self.data['Impressions']
        
        logger.info("Data transformation completed successfully")

    def prepare_dashboard_data(self) -> Dict:
        """
        Prepare aggregated data for the dashboard.
        
        Returns:
            Dict: Dashboard data in the required format
        """
        # Calculate summary metrics
        total_acquisition_cost = float(self.data['Acquisition_Cost'].sum())
        total_clicks = int(self.data['Clicks'].sum())
        total_impressions = int(self.data['Impressions'].sum())
        total_campaigns = len(self.data)
        
        dashboard_data = {
            'summary': {
                'avg_conversion_rate': float(self.data['Conversion_Rate'].mean()),
                'avg_roi': float(self.data['ROI'].mean()),
                'total_acquisition_cost': total_acquisition_cost,
                'total_clicks': total_clicks,
                'total_impressions': total_impressions,
                'total_campaigns': total_campaigns,
                'avg_engagement_score': float(self.data['Engagement_Score'].mean())
            },
            'campaign_types': self.data.groupby('Campaign_Type').agg({
                'Conversion_Rate': 'mean',
                'ROI': 'mean',
                'Acquisition_Cost': 'mean',
                'Campaign_ID': 'count',
                'Engagement_Score': 'mean'
            }).reset_index().to_dict('records'),
            'channel_performance': self.data.groupby('Channel_Used').agg({
                'Impressions': 'sum',
                'Clicks': 'sum',
                'Conversion_Rate': 'mean',
                'ROI': 'mean',
                'Engagement_Score': 'mean'
            }).reset_index().to_dict('records'),
            'segment_performance': self.data.groupby('Customer_Segment').agg({
                'Conversion_Rate': 'mean',
                'ROI': 'mean',
                'Engagement_Score': 'mean',
                'Acquisition_Cost': 'sum'
            }).reset_index().to_dict('records'),
            'geographic_data': self.data.groupby('Location').agg({
                'Conversion_Rate': 'mean',
                'ROI': 'mean',
                'Campaign_ID': 'count',
                'Engagement_Score': 'mean'
            }).reset_index().to_dict('records'),
            'monthly_trends': self.data.groupby(['Month', 'Channel_Used']).agg({
                'ROI': 'mean',
                'Conversion_Rate': 'mean',
                'Engagement_Score': 'mean'
            }).reset_index().to_dict('records'),
            'duration_metrics': self.data.groupby('Duration_Category').agg({
                'ROI': 'mean',
                'Engagement_Score': 'mean',
                'Conversion_Rate': 'mean',
                'Campaign_ID': 'count'
            }).reset_index().to_dict('records')
        }
        
        return dashboard_data

    def save_dashboard_data(self, output_file: str) -> None:
        """
        Save the processed dashboard data to JSON and CSV files.
        
        Args:
            output_file (str): Path to save the JSON file
        """
        # Save dashboard data as JSON
        dashboard_data = self.prepare_dashboard_data()
        
        with open(output_file, 'w') as f:
            json.dump(dashboard_data, f, indent=2)
        
        logger.info(f"Dashboard data saved to {output_file}")
        
        # Save processed data as CSV
        csv_output = 'data/processed/marketing_campaign_processed.csv'
        self.data.to_csv(csv_output, index=False)
        logger.info(f"Processed data saved to {csv_output}")

    def process(self) -> bool:
        """
        Execute the complete data processing pipeline.
        
        Returns:
            bool: True if processing succeeds, False otherwise
        """
        try:
            if not self.load_data():
                return False
            
            self.clean_data()
            self.transform_data()
            
            return True
            
        except Exception as e:
            logger.error(f"Processing error: {str(e)}")
            return False

def main():
    # Set up paths
    input_file = "data/raw/marketing_campaign_dataset.csv"
    output_file = "dashboard/data/dashboard_data.json"
    
    # Create processor instance
    processor = MarketingDataProcessor(input_file)
    
    # Run processing pipeline
    if processor.process():
        processor.save_dashboard_data(output_file)
        logger.info("Data processing completed successfully")
    else:
        logger.error("Data processing failed")

if __name__ == "__main__":
    main() 