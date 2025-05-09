import pandas as pd
import numpy as np
from typing import Dict, List, Tuple
import logging
from pathlib import Path
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SegmentAnalyzer:
    """Class for analyzing customer segments in marketing campaign data."""
    
    def __init__(self):
        """Initialize the segment analyzer."""
        self.segment_features = [
            'Conversion_Rate',
            'ROI',
            'Engagement_Score',
            'Engagement_Rate'
        ]

    def calculate_rfm_metrics(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Calculate RFM (Recency, Frequency, Monetary) metrics for each audience segment.
        
        Args:
            df (pd.DataFrame): Campaign data
            
        Returns:
            pd.DataFrame: RFM metrics by audience segment
        """
        # Calculate metrics by Target_Audience
        rfm = df.groupby('Target_Audience').agg({
            'Date': lambda x: (pd.Timestamp.now() - x.max()).days,  # Recency
            'Campaign_ID': 'count',  # Frequency
            'Acquisition_Cost': 'sum'  # Monetary
        }).round(2)
        
        # Rename columns
        rfm.columns = ['Recency_Days', 'Campaign_Frequency', 'Total_Spend']
        
        # Add derived metrics
        rfm['Avg_Spend_per_Campaign'] = (rfm['Total_Spend'] / rfm['Campaign_Frequency']).round(2)
        
        return rfm

    def perform_cluster_analysis(self, df: pd.DataFrame, n_clusters: int=5) -> Tuple[pd.DataFrame, Dict]:
        """
        Perform cluster analysis to identify distinct audience segments.
        
        Args:
            df (pd.DataFrame): Campaign data
            n_clusters (int): Number of clusters to create
            
        Returns:
            Tuple[pd.DataFrame, Dict]: Clustered data and cluster characteristics
        """
        # Prepare features for clustering
        features = df[self.segment_features].copy()
        
        # Scale features
        scaler = StandardScaler()
        features_scaled = scaler.fit_transform(features)
        
        # Perform clustering
        kmeans = KMeans(n_clusters=n_clusters, random_state=42)
        df['Cluster'] = kmeans.fit_predict(features_scaled)
        
        # Calculate cluster characteristics
        cluster_stats = {}
        for i in range(n_clusters):
            cluster_data = df[df['Cluster'] == i]
            cluster_stats[f'Cluster_{i}'] = {
                'size': len(cluster_data),
                'avg_conversion_rate': cluster_data['Conversion_Rate'].mean(),
                'avg_roi': cluster_data['ROI'].mean(),
                'avg_acquisition_cost': cluster_data['Acquisition_Cost'].mean(),
                'avg_engagement_score': cluster_data['Engagement_Score'].mean(),
                'avg_engagement_rate': cluster_data['Engagement_Rate'].mean()
            }
        
        return df, cluster_stats

    def analyze_segment_performance(self, df: pd.DataFrame) -> Dict[str, pd.DataFrame]:
        """
        Analyze performance metrics for different audience segments.
        
        Args:
            df (pd.DataFrame): Campaign data
            
        Returns:
            Dict[str, pd.DataFrame]: Dictionary of segment performance metrics
        """
        performance_metrics = {}
        
        # Overall segment performance
        segment_performance = df.groupby('Target_Audience').agg({
            'Conversion_Rate': 'mean',
            'ROI': 'mean',
            'Acquisition_Cost': 'mean',
            'Engagement_Score': 'mean',
            'Engagement_Rate': 'mean',
            'Campaign_ID': 'count'
        }).round(3)
        performance_metrics['overall'] = segment_performance
        
        # Performance by channel
        channel_performance = df.groupby(['Target_Audience', 'Channel_Used']).agg({
            'Conversion_Rate': 'mean',
            'ROI': 'mean',
            'Engagement_Score': 'mean',
            'Campaign_ID': 'count'
        }).round(3)
        performance_metrics['by_channel'] = channel_performance
        
        # Performance by campaign type
        campaign_performance = df.groupby(['Target_Audience', 'Campaign_Type']).agg({
            'Conversion_Rate': 'mean',
            'ROI': 'mean',
            'Engagement_Score': 'mean',
            'Campaign_ID': 'count'
        }).round(3)
        performance_metrics['by_campaign_type'] = campaign_performance
        
        return performance_metrics

    def analyze_segment_trends(self, df: pd.DataFrame) -> Dict[str, pd.DataFrame]:
        """
        Analyze temporal trends in segment performance.
        
        Args:
            df (pd.DataFrame): Campaign data
            
        Returns:
            Dict[str, pd.DataFrame]: Dictionary of segment trends
        """
        trend_metrics = {}
        
        # Monthly trends
        monthly_trends = df.groupby(['Target_Audience', 'Month']).agg({
            'Conversion_Rate': 'mean',
            'ROI': 'mean',
            'Campaign_ID': 'count'
        }).round(3)
        trend_metrics['monthly'] = monthly_trends
        
        # Quarterly trends
        quarterly_trends = df.groupby(['Target_Audience', 'Quarter']).agg({
            'Conversion_Rate': 'mean',
            'ROI': 'mean',
            'Campaign_ID': 'count'
        }).round(3)
        trend_metrics['quarterly'] = quarterly_trends
        
        return trend_metrics

    def create_segment_visualizations(self, df: pd.DataFrame, output_path: str) -> None:
        """
        Create visualizations for segment analysis.
        
        Args:
            df (pd.DataFrame): Campaign data
            output_path (str): Path to save visualizations
        """
        output_path = Path(output_path)
        output_path.mkdir(parents=True, exist_ok=True)
        
        # Segment performance comparison
        plt.figure(figsize=(12, 6))
        sns.scatterplot(data=df, x='ROI', y='Conversion_Rate', 
                       hue='Target_Audience', size='Acquisition_Cost',
                       sizes=(50, 400), alpha=0.6)
        plt.title('Segment Performance: ROI vs Conversion Rate')
        plt.savefig(output_path / 'segment_performance_scatter.png')
        plt.close()
        
        # Channel effectiveness by segment
        plt.figure(figsize=(12, 6))
        sns.barplot(data=df, x='Target_Audience', y='ROI', hue='Channel_Used')
        plt.title('ROI by Segment and Channel')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig(output_path / 'segment_channel_roi.png')
        plt.close()
        
        # Temporal trends
        plt.figure(figsize=(12, 6))
        sns.lineplot(data=df, x='Month', y='Conversion_Rate', 
                    hue='Target_Audience')
        plt.title('Conversion Rate Trends by Segment')
        plt.savefig(output_path / 'segment_trends.png')
        plt.close()

    def save_segment_analysis(self, rfm_metrics: pd.DataFrame, 
                            performance_metrics: Dict[str, pd.DataFrame],
                            trend_metrics: Dict[str, pd.DataFrame],
                            cluster_stats: Dict,
                            output_path: str) -> None:
        """
        Save segment analysis results to CSV files.
        
        Args:
            rfm_metrics (pd.DataFrame): RFM analysis results
            performance_metrics (Dict[str, pd.DataFrame]): Performance metrics
            trend_metrics (Dict[str, pd.DataFrame]): Trend metrics
            cluster_stats (Dict): Cluster analysis results
            output_path (str): Path to save results
        """
        output_path = Path(output_path)
        output_path.mkdir(parents=True, exist_ok=True)
        
        # Save RFM metrics
        rfm_metrics.to_csv(output_path / 'rfm_metrics.csv')
        
        # Save performance metrics
        for metric_name, df in performance_metrics.items():
            df.to_csv(output_path / f'performance_{metric_name}.csv')
        
        # Save trend metrics
        for metric_name, df in trend_metrics.items():
            df.to_csv(output_path / f'trends_{metric_name}.csv')
        
        # Save cluster statistics
        pd.DataFrame(cluster_stats).to_csv(output_path / 'cluster_statistics.csv')
        
        logger.info(f"Saved segment analysis results to {output_path}")

def run_segment_analysis(input_data_path: str, output_path: str) -> None:
    """
    Run the complete segment analysis pipeline.
    
    Args:
        input_data_path (str): Path to the cleaned campaign data
        output_path (str): Path to save the analysis results
    """
    # Load data
    df = pd.read_csv(input_data_path, parse_dates=['Date'])
    
    # Initialize analyzer
    analyzer = SegmentAnalyzer()
    
    # Perform analyses
    rfm_metrics = analyzer.calculate_rfm_metrics(df)
    df_clustered, cluster_stats = analyzer.perform_cluster_analysis(df)
    performance_metrics = analyzer.analyze_segment_performance(df)
    trend_metrics = analyzer.analyze_segment_trends(df)
    
    # Create visualizations
    analyzer.create_segment_visualizations(df, output_path)
    
    # Save results
    analyzer.save_segment_analysis(
        rfm_metrics,
        performance_metrics,
        trend_metrics,
        cluster_stats,
        output_path
    )
    
    logger.info("Completed segment analysis")

if __name__ == "__main__":
    # Example usage
    input_path = "data/processed/cleaned_campaign_data.csv"
    output_path = "data/output/segment_analysis"
    run_segment_analysis(input_path, output_path) 