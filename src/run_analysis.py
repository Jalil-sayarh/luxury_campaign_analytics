import logging
from pathlib import Path
import pandas as pd
import json
from datetime import datetime

# Import analysis modules
from data.data_loader import MarketingDataLoader
from data.data_cleaner import MarketingDataCleaner, save_cleaned_data
from analysis.cohort_analysis import run_cohort_analysis
from analysis.segment_analysis import run_segment_analysis
from analysis.channel_analysis import run_channel_analysis

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def setup_directories():
    """Create necessary directories for the analysis."""
    directories = [
        'data/processed',
        'data/output/cohort_analysis',
        'data/output/segment_analysis',
        'data/output/channel_analysis',
        'docs/images'
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        logger.info(f"Created directory: {directory}")

def run_analysis_pipeline():
    """Run the complete marketing campaign analysis pipeline."""
    try:
        # Setup directories
        setup_directories()
        
        # Step 1: Load and clean data
        logger.info("Starting data loading and cleaning...")
        data_loader = MarketingDataLoader("data/raw/marketing_campaign_dataset.csv")
        raw_df = data_loader.load_data()
        
        if raw_df is None:
            raise ValueError("Failed to load raw data")
        
        cleaner = MarketingDataCleaner()
        cleaned_df, cleaning_summary = cleaner.clean_data(raw_df)
        cleaned_data_path = "data/processed/cleaned_campaign_data.csv"
        save_cleaned_data(cleaned_df, cleaned_data_path)
        
        # Save data summary
        summary_stats = data_loader.get_summary_stats(cleaned_df)
        with open("data/processed/data_summary.json", "w") as f:
            json.dump({**summary_stats, **cleaning_summary}, f, indent=4, default=str)
        
        # Step 2: Run cohort analysis
        logger.info("Running cohort analysis...")
        run_cohort_analysis(
            input_data_path=cleaned_data_path,
            output_path="data/output/cohort_analysis"
        )
        
        # Step 3: Run segment analysis
        logger.info("Running segment analysis...")
        run_segment_analysis(
            input_data_path=cleaned_data_path,
            output_path="data/output/segment_analysis"
        )
        
        # Step 4: Run channel analysis
        logger.info("Running channel analysis...")
        run_channel_analysis(
            input_data_path=cleaned_data_path,
            output_path="data/output/channel_analysis"
        )
        
        # Step 5: Prepare dashboard data
        logger.info("Preparing dashboard data...")
        dashboard_data = {
            'last_updated': datetime.now().isoformat(),
            'summary_metrics': summary_stats,
            'cleaning_summary': cleaning_summary
        }
        
        with open("dashboard/data/dashboard_data.json", "w") as f:
            json.dump(dashboard_data, f, indent=4, default=str)
        
        logger.info("Analysis pipeline completed successfully")
        
    except Exception as e:
        logger.error(f"Error in analysis pipeline: {str(e)}")
        raise

def main():
    """Main function to run the analysis."""
    try:
        run_analysis_pipeline()
    except Exception as e:
        logger.error(f"Failed to run analysis pipeline: {str(e)}")
        raise

if __name__ == "__main__":
    main() 