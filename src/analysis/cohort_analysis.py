import pandas as pd
import numpy as np
from typing import Dict, Tuple
import logging
from pathlib import Path
import matplotlib.pyplot as plt
import seaborn as sns

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CohortAnalyzer:
    """Class for performing cohort analysis on marketing campaign data."""
    
    def __init__(self):
        """Initialize the cohort analyzer."""
        pass

    def create_cohorts(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Create customer cohorts based on their first campaign interaction.
        
        Args:
            df (pd.DataFrame): Cleaned campaign data
            
        Returns:
            pd.DataFrame: Dataset with cohort information
        """
        # Sort by date and campaign ID
        df = df.sort_values(['Date', 'Campaign_ID'])
        
        # Create cohort groups based on the first interaction month
        df['Cohort_Month'] = df['Date'].dt.to_period('M')
        
        # Calculate months since first interaction
        df['Months_Since_First_Campaign'] = (
            df['Date'].dt.to_period('M') - 
            df.groupby('Target_Audience')['Date'].transform('min').dt.to_period('M')
        ).apply(lambda x: x.n)
        
        return df

    def calculate_cohort_metrics(self, df: pd.DataFrame) -> Dict[str, pd.DataFrame]:
        """
        Calculate key metrics for each cohort.
        
        Args:
            df (pd.DataFrame): Dataset with cohort information
            
        Returns:
            Dict[str, pd.DataFrame]: Dictionary containing different cohort metrics
        """
        metrics = {}
        
        # Retention Matrix
        retention_matrix = (
            df.groupby(['Cohort_Month', 'Months_Since_First_Campaign'])
            .agg({'Target_Audience': 'nunique'})
            .reset_index()
            .pivot(index='Cohort_Month', 
                  columns='Months_Since_First_Campaign', 
                  values='Target_Audience')
        )
        
        # Convert to retention rates
        retention_matrix = retention_matrix.div(retention_matrix[0], axis=0)
        metrics['retention'] = retention_matrix
        
        # Conversion Rate Matrix
        conversion_matrix = (
            df.groupby(['Cohort_Month', 'Months_Since_First_Campaign'])
            .agg({'Conversion_Rate': 'mean'})
            .reset_index()
            .pivot(index='Cohort_Month', 
                  columns='Months_Since_First_Campaign', 
                  values='Conversion_Rate')
        )
        metrics['conversion'] = conversion_matrix
        
        # ROI Matrix
        roi_matrix = (
            df.groupby(['Cohort_Month', 'Months_Since_First_Campaign'])
            .agg({'ROI': 'mean'})
            .reset_index()
            .pivot(index='Cohort_Month', 
                  columns='Months_Since_First_Campaign', 
                  values='ROI')
        )
        metrics['roi'] = roi_matrix
        
        return metrics

    def analyze_cohort_behavior(self, df: pd.DataFrame) -> Dict[str, pd.DataFrame]:
        """
        Analyze behavior patterns within cohorts.
        
        Args:
            df (pd.DataFrame): Dataset with cohort information
            
        Returns:
            Dict[str, pd.DataFrame]: Dictionary containing cohort behavior metrics
        """
        behavior_metrics = {}
        
        # Channel preference by cohort
        channel_pref = (
            df.groupby(['Cohort_Month', 'Channel_Used'])
            .agg({
                'Campaign_ID': 'count',
                'Conversion_Rate': 'mean',
                'ROI': 'mean'
            })
            .round(3)
        )
        behavior_metrics['channel_preference'] = channel_pref
        
        # Campaign type effectiveness by cohort
        campaign_effect = (
            df.groupby(['Cohort_Month', 'Campaign_Type'])
            .agg({
                'Campaign_ID': 'count',
                'Conversion_Rate': 'mean',
                'ROI': 'mean'
            })
            .round(3)
        )
        behavior_metrics['campaign_effectiveness'] = campaign_effect
        
        # Customer segment analysis by cohort
        segment_analysis = (
            df.groupby(['Cohort_Month', 'Customer_Segment'])
            .agg({
                'Campaign_ID': 'count',
                'Conversion_Rate': 'mean',
                'ROI': 'mean',
                'Engagement_Score': 'mean'
            })
            .round(3)
        )
        behavior_metrics['segment_analysis'] = segment_analysis
        
        return behavior_metrics

    def plot_cohort_heatmap(self, matrix: pd.DataFrame, metric_name: str, 
                           title: str, figsize: Tuple[int, int]=(12, 8)) -> None:
        """
        Create a heatmap visualization for cohort analysis.
        
        Args:
            matrix (pd.DataFrame): Cohort matrix to visualize
            metric_name (str): Name of the metric being visualized
            title (str): Plot title
            figsize (Tuple[int, int]): Figure size
        """
        plt.figure(figsize=figsize)
        sns.heatmap(matrix, annot=True, fmt='.2%' if metric_name == 'retention' else '.2f',
                   cmap='YlOrRd', center=0.5 if metric_name == 'retention' else None)
        plt.title(title)
        plt.xlabel('Months Since First Campaign')
        plt.ylabel('Cohort Month')
        plt.tight_layout()

    def save_cohort_analysis(self, metrics: Dict[str, pd.DataFrame], 
                           behavior_metrics: Dict[str, pd.DataFrame], 
                           output_path: str) -> None:
        """
        Save cohort analysis results to CSV files.
        
        Args:
            metrics (Dict[str, pd.DataFrame]): Cohort metrics
            behavior_metrics (Dict[str, pd.DataFrame]): Cohort behavior metrics
            output_path (str): Path to save the results
        """
        output_path = Path(output_path)
        output_path.mkdir(parents=True, exist_ok=True)
        
        # Save cohort metrics
        for metric_name, matrix in metrics.items():
            matrix.to_csv(output_path / f'cohort_{metric_name}_matrix.csv')
            
        # Save behavior metrics
        for metric_name, df in behavior_metrics.items():
            df.to_csv(output_path / f'cohort_{metric_name}.csv')
        
        logger.info(f"Saved cohort analysis results to {output_path}")

def run_cohort_analysis(input_data_path: str, output_path: str) -> None:
    """
    Run the complete cohort analysis pipeline.
    
    Args:
        input_data_path (str): Path to the cleaned campaign data
        output_path (str): Path to save the analysis results
    """
    # Load data
    df = pd.read_csv(input_data_path, parse_dates=['Date'])
    
    # Initialize analyzer
    analyzer = CohortAnalyzer()
    
    # Create cohorts
    df_with_cohorts = analyzer.create_cohorts(df)
    
    # Calculate metrics
    cohort_metrics = analyzer.calculate_cohort_metrics(df_with_cohorts)
    behavior_metrics = analyzer.analyze_cohort_behavior(df_with_cohorts)
    
    # Create visualizations
    for metric_name, matrix in cohort_metrics.items():
        title = f'{metric_name.title()} by Cohort and Months Since First Campaign'
        analyzer.plot_cohort_heatmap(matrix, metric_name, title)
        plt.savefig(Path(output_path) / f'cohort_{metric_name}_heatmap.png')
        plt.close()
    
    # Save results
    analyzer.save_cohort_analysis(cohort_metrics, behavior_metrics, output_path)
    
    logger.info("Completed cohort analysis")

if __name__ == "__main__":
    # Example usage
    input_path = "data/processed/cleaned_campaign_data.csv"
    output_path = "data/output/cohort_analysis"
    run_cohort_analysis(input_path, output_path) 