import pandas as pd
import numpy as np
from typing import Dict, List, Tuple
import logging
from pathlib import Path
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ChannelAnalyzer:
    """Class for analyzing marketing channel performance."""
    
    def __init__(self):
        """Initialize the channel analyzer."""
        self.performance_metrics = [
            'Impressions',
            'Clicks',
            'Conversion_Rate',
            'ROI',
            'Acquisition_Cost',
            'Engagement_Score',
            'Engagement_Rate'
        ]

    def calculate_channel_metrics(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Calculate comprehensive metrics for each channel.
        
        Args:
            df (pd.DataFrame): Campaign data
            
        Returns:
            pd.DataFrame: Channel performance metrics
        """
        channel_metrics = df.groupby('Channel_Used').agg({
            'Campaign_ID': 'count',
            'Impressions': 'sum',
            'Clicks': 'sum',
            'Acquisition_Cost': 'sum',
            'Conversion_Rate': 'mean',
            'ROI': 'mean',
            'Engagement_Score': 'mean',
            'Engagement_Rate': 'mean'
        }).round(3)
        
        # Add derived metrics
        channel_metrics['Click_Through_Rate'] = (
            channel_metrics['Clicks'] / channel_metrics['Impressions']
        ).round(3)
        
        channel_metrics['Cost_per_Click'] = (
            channel_metrics['Acquisition_Cost'] / channel_metrics['Clicks']
        ).round(3)
        
        return channel_metrics

    def analyze_channel_effectiveness(self, df: pd.DataFrame) -> Dict[str, pd.DataFrame]:
        """
        Analyze channel effectiveness across different dimensions.
        
        Args:
            df (pd.DataFrame): Campaign data
            
        Returns:
            Dict[str, pd.DataFrame]: Dictionary of channel effectiveness metrics
        """
        effectiveness_metrics = {}
        
        # Performance by campaign type
        campaign_type_perf = df.groupby(['Channel_Used', 'Campaign_Type']).agg({
            'Conversion_Rate': 'mean',
            'ROI': 'mean',
            'Campaign_ID': 'count'
        }).round(3)
        effectiveness_metrics['by_campaign_type'] = campaign_type_perf
        
        # Performance by target audience
        audience_perf = df.groupby(['Channel_Used', 'Target_Audience']).agg({
            'Conversion_Rate': 'mean',
            'ROI': 'mean',
            'Campaign_ID': 'count'
        }).round(3)
        effectiveness_metrics['by_audience'] = audience_perf
        
        # Performance by customer segment
        segment_perf = df.groupby(['Channel_Used', 'Customer_Segment']).agg({
            'Conversion_Rate': 'mean',
            'ROI': 'mean',
            'Engagement_Score': 'mean',
            'Campaign_ID': 'count'
        }).round(3)
        effectiveness_metrics['by_segment'] = segment_perf
        
        return effectiveness_metrics

    def analyze_channel_trends(self, df: pd.DataFrame) -> Dict[str, pd.DataFrame]:
        """
        Analyze temporal trends in channel performance.
        
        Args:
            df (pd.DataFrame): Campaign data
            
        Returns:
            Dict[str, pd.DataFrame]: Dictionary of channel trends
        """
        trend_metrics = {}
        
        # Monthly trends
        monthly_trends = df.groupby(['Channel_Used', 'Month']).agg({
            'Conversion_Rate': 'mean',
            'ROI': 'mean',
            'Acquisition_Cost': 'sum',
            'Campaign_ID': 'count'
        }).round(3)
        trend_metrics['monthly'] = monthly_trends
        
        # Quarterly trends
        quarterly_trends = df.groupby(['Channel_Used', 'Quarter']).agg({
            'Conversion_Rate': 'mean',
            'ROI': 'mean',
            'Acquisition_Cost': 'sum',
            'Campaign_ID': 'count'
        }).round(3)
        trend_metrics['quarterly'] = quarterly_trends
        
        return trend_metrics

    def perform_statistical_analysis(self, df: pd.DataFrame) -> Dict[str, Dict]:
        """
        Perform statistical analysis on channel performance.
        
        Args:
            df (pd.DataFrame): Campaign data
            
        Returns:
            Dict[str, Dict]: Statistical analysis results
        """
        statistical_results = {}
        
        # ANOVA test for channel performance differences
        for metric in ['Conversion_Rate', 'ROI', 'Engagement_Score']:
            channel_groups = [group for _, group in df.groupby('Channel_Used')[metric]]
            f_stat, p_value = stats.f_oneway(*channel_groups)
            
            statistical_results[f'{metric}_anova'] = {
                'f_statistic': round(f_stat, 3),
                'p_value': round(p_value, 3),
                'significant': p_value < 0.05
            }
        
        # Correlation analysis
        correlation_matrix = df[self.performance_metrics].corr().round(3)
        statistical_results['correlations'] = correlation_matrix.to_dict()
        
        return statistical_results

    def create_channel_visualizations(self, df: pd.DataFrame, output_path: str) -> None:
        """
        Create visualizations for channel analysis.
        
        Args:
            df (pd.DataFrame): Campaign data
            output_path (str): Path to save visualizations
        """
        output_path = Path(output_path)
        output_path.mkdir(parents=True, exist_ok=True)
        
        # Channel performance comparison
        plt.figure(figsize=(12, 6))
        sns.barplot(data=df, x='Channel_Used', y='ROI')
        plt.title('ROI by Channel')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig(output_path / 'channel_roi_comparison.png')
        plt.close()
        
        # Impression and click metrics by channel
        plt.figure(figsize=(12, 6))
        channel_funnel = df.groupby('Channel_Used').agg({
            'Impressions': 'sum',
            'Clicks': 'sum'
        })
        channel_funnel.plot(kind='bar', width=0.8)
        plt.title('Impressions and Clicks by Channel')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig(output_path / 'channel_metrics.png')
        plt.close()
        
        # Cost efficiency analysis
        plt.figure(figsize=(12, 6))
        sns.scatterplot(data=df, x='Acquisition_Cost', y='Conversion_Rate',
                       hue='Channel_Used', size='Engagement_Score', sizes=(50, 400))
        plt.title('Channel Cost Efficiency')
        plt.tight_layout()
        plt.savefig(output_path / 'channel_cost_efficiency.png')
        plt.close()
        
        # ROI and Engagement Score relationship
        plt.figure(figsize=(12, 6))
        sns.scatterplot(data=df, x='ROI', y='Engagement_Score', 
                      hue='Channel_Used', alpha=0.7)
        plt.title('ROI vs Engagement Score by Channel')
        plt.tight_layout()
        plt.savefig(output_path / 'channel_roi_engagement.png')
        plt.close()

    def calculate_channel_recommendations(self, df: pd.DataFrame) -> Dict[str, List[str]]:
        """
        Generate channel-specific recommendations based on analysis.
        
        Args:
            df (pd.DataFrame): Campaign data
            
        Returns:
            Dict[str, List[str]]: Recommendations for each channel
        """
        recommendations = {}
        
        for channel in df['Channel_Used'].unique():
            channel_data = df[df['Channel_Used'] == channel]
            recommendations[channel] = []
            
            # ROI-based recommendations
            avg_roi = channel_data['ROI'].mean()
            if avg_roi > df['ROI'].mean():
                recommendations[channel].append(
                    f"High ROI performer (ROI: {avg_roi:.2f}). Consider increasing budget allocation."
                )
            else:
                recommendations[channel].append(
                    f"Below average ROI (ROI: {avg_roi:.2f}). Review campaign strategy and targeting."
                )
            
            # Conversion rate recommendations
            avg_conv_rate = channel_data['Conversion_Rate'].mean()
            if avg_conv_rate < df['Conversion_Rate'].mean():
                recommendations[channel].append(
                    f"Below average conversion rate ({avg_conv_rate:.2%}). Review targeting and creative strategy."
                )
            
            # Cost efficiency recommendations
            avg_cost = channel_data['Acquisition_Cost'].mean()
            if avg_cost > df['Acquisition_Cost'].mean():
                recommendations[channel].append(
                    f"High acquisition cost (${avg_cost:.2f}). Optimize bidding strategy and targeting."
                )
            
            # Engagement recommendations
            avg_engagement = channel_data['Engagement_Score'].mean()
            if avg_engagement < df['Engagement_Score'].mean():
                recommendations[channel].append(
                    f"Low engagement score ({avg_engagement:.2f}). Improve content quality and engagement factors."
                )
            
            # Engagement rate recommendations
            avg_engagement_rate = channel_data['Engagement_Rate'].mean()
            if avg_engagement_rate < df['Engagement_Rate'].mean():
                recommendations[channel].append(
                    f"Low engagement rate ({avg_engagement_rate:.2%}). Review content strategy and audience targeting."
                )
        
        return recommendations

    def save_channel_analysis(self, channel_metrics: pd.DataFrame,
                            effectiveness_metrics: Dict[str, pd.DataFrame],
                            trend_metrics: Dict[str, pd.DataFrame],
                            statistical_results: Dict[str, Dict],
                            recommendations: Dict[str, List[str]],
                            output_path: str) -> None:
        """
        Save channel analysis results to files.
        
        Args:
            channel_metrics (pd.DataFrame): Overall channel metrics
            effectiveness_metrics (Dict[str, pd.DataFrame]): Channel effectiveness metrics
            trend_metrics (Dict[str, pd.DataFrame]): Channel trend metrics
            statistical_results (Dict[str, Dict]): Statistical analysis results
            recommendations (Dict[str, List[str]]): Channel recommendations
            output_path (str): Path to save results
        """
        output_path = Path(output_path)
        output_path.mkdir(parents=True, exist_ok=True)
        
        # Save channel metrics
        channel_metrics.to_csv(output_path / 'channel_metrics.csv')
        
        # Save effectiveness metrics
        for metric_name, df in effectiveness_metrics.items():
            df.to_csv(output_path / f'effectiveness_{metric_name}.csv')
        
        # Save trend metrics
        for metric_name, df in trend_metrics.items():
            df.to_csv(output_path / f'trends_{metric_name}.csv')
        
        # Save statistical results
        pd.DataFrame(statistical_results).to_csv(output_path / 'statistical_analysis.csv')
        
        # Save recommendations
        pd.DataFrame.from_dict(recommendations, orient='index').to_csv(
            output_path / 'channel_recommendations.csv'
        )
        
        logger.info(f"Saved channel analysis results to {output_path}")

def run_channel_analysis(input_data_path: str, output_path: str) -> None:
    """
    Run the complete channel analysis pipeline.
    
    Args:
        input_data_path (str): Path to the cleaned campaign data
        output_path (str): Path to save the analysis results
    """
    # Load data
    df = pd.read_csv(input_data_path, parse_dates=['Date'])
    
    # Initialize analyzer
    analyzer = ChannelAnalyzer()
    
    # Perform analyses
    channel_metrics = analyzer.calculate_channel_metrics(df)
    effectiveness_metrics = analyzer.analyze_channel_effectiveness(df)
    trend_metrics = analyzer.analyze_channel_trends(df)
    statistical_results = analyzer.perform_statistical_analysis(df)
    recommendations = analyzer.calculate_channel_recommendations(df)
    
    # Create visualizations
    analyzer.create_channel_visualizations(df, output_path)
    
    # Save results
    analyzer.save_channel_analysis(
        channel_metrics,
        effectiveness_metrics,
        trend_metrics,
        statistical_results,
        recommendations,
        output_path
    )
    
    logger.info("Completed channel analysis")

if __name__ == "__main__":
    # Example usage
    input_path = "data/processed/cleaned_campaign_data.csv"
    output_path = "data/output/channel_analysis"
    run_channel_analysis(input_path, output_path) 