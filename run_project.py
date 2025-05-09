import os
import logging
from pathlib import Path
import subprocess
import sys
import time

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('project_execution.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

def run_command(command: str, cwd: str = None) -> None:
    """
    Run a shell command and log its output.
    
    Args:
        command (str): Command to run
        cwd (str, optional): Working directory
    """
    try:
        process = subprocess.run(
            command,
            shell=True,
            cwd=cwd,
            check=True,
            capture_output=True,
            text=True
        )
        logger.info(f"Successfully ran: {command}")
        if process.stdout:
            logger.info(process.stdout)
    except subprocess.CalledProcessError as e:
        logger.error(f"Command failed: {command}")
        logger.error(f"Error: {e.stderr}")
        raise

def create_directory_structure():
    """Create the required directory structure for the project."""
    directories = [
        'data/processed',
        'data/output',
        'notebooks',
        'src/data',
        'src/analysis',
        'src/visualization',
        'dashboard/css',
        'dashboard/js',
        'dashboard/data',
        'docs/images'
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        logger.info(f"Created directory: {directory}")

def run_data_processing():
    """Process the marketing campaign data."""
    try:
        logger.info("Processing marketing campaign data...")
        subprocess.run([sys.executable, 'src/data/data_processor.py'], check=True)
        logger.info("Data processing completed successfully")
    except subprocess.CalledProcessError as e:
        logger.error(f"Error processing data: {str(e)}")
        raise

def setup_dashboard():
    """Set up the dashboard environment."""
    try:
        logger.info("Setting up dashboard...")
        
        # Ensure dashboard directories exist
        os.makedirs('dashboard/data', exist_ok=True)
        
        # Copy processed data to dashboard directory
        if os.path.exists('dashboard/data/dashboard_data.json'):
            logger.info("Dashboard data is ready")
        else:
            logger.error("Dashboard data not found")
            raise FileNotFoundError("dashboard_data.json not found")
            
    except Exception as e:
        logger.error(f"Error setting up dashboard: {str(e)}")
        raise

def run_analysis():
    """Run the complete analysis pipeline."""
    logger.info("Running analysis pipeline...")
    
    try:
        # Create analysis directory if it doesn't exist
        os.makedirs('src/analysis', exist_ok=True)
        
        # Create a basic analysis script if it doesn't exist
        analysis_script = 'src/analysis/run_analysis.py'
        if not os.path.exists(analysis_script):
            with open(analysis_script, 'w') as f:
                f.write("""
import pandas as pd
import numpy as np
import logging

logger = logging.getLogger(__name__)

def run_analysis():
    \"\"\"Run basic analysis on the processed data.\"\"\"
    try:
        # Load processed data
        data = pd.read_csv('data/processed/marketing_campaign_processed.csv')
        
        # Perform basic analysis
        summary = {
            'total_campaigns': len(data),
            'avg_roi': data['ROI'].mean(),
            'avg_conversion_rate': data['Conversion_Rate'].mean(),
            'total_revenue': data['Revenue'].sum(),
            'total_budget': data['Budget'].sum()
        }
        
        logger.info("Analysis completed successfully")
        return summary
        
    except Exception as e:
        logger.error(f"Analysis error: {str(e)}")
        raise

if __name__ == '__main__':
    run_analysis()
""")
        
        # Run the analysis script
        run_command(f"{sys.executable} {analysis_script}")
        logger.info("Analysis completed successfully")
        
    except Exception as e:
        logger.error(f"Error in analysis: {str(e)}")
        raise

def start_dashboard():
    """Start the dashboard server."""
    logger.info("Starting dashboard server...")
    
    try:
        # Check if package.json exists
        if not os.path.exists('dashboard/package.json'):
            logger.error("Dashboard package.json not found")
            return
            
        # Install dependencies if needed
        if not os.path.exists('dashboard/node_modules'):
            run_command("npm install", cwd="dashboard")
        
        # Start the dashboard
        run_command("npm start", cwd="dashboard")
        
    except Exception as e:
        logger.error(f"Error starting dashboard: {str(e)}")
        raise

def main():
    """Run the complete project pipeline."""
    start_time = time.time()
    
    try:
        # Create project structure
        create_directory_structure()
        
        # Process data
        run_data_processing()
        
        # Set up dashboard
        setup_dashboard()
        
        # Run analysis
        run_analysis()
        
        # Start dashboard
        start_dashboard()
        
        execution_time = time.time() - start_time
        logger.info(f"Project execution completed in {execution_time:.2f} seconds")
        
    except Exception as e:
        logger.error(f"Project pipeline failed: {str(e)}")
        sys.exit(1)

if __name__ == '__main__':
    main() 