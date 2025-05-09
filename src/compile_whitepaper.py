import pandas as pd
import json
from pathlib import Path
import shutil
import logging
from datetime import datetime
import matplotlib.pyplot as plt
import seaborn as sns

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class WhitepaperCompiler:
    """Class for compiling the marketing campaign analysis whitepaper."""
    
    def __init__(self):
        """Initialize the whitepaper compiler."""
        self.data_path = Path("data")
        self.docs_path = Path("docs")
        self.output_path = self.docs_path / "whitepaper.md"
        self.image_path = self.docs_path / "images"
        
        # Ensure image directory exists
        self.image_path.mkdir(parents=True, exist_ok=True)

    def load_analysis_results(self) -> dict:
        """
        Load all analysis results from the data directory.
        
        Returns:
            dict: Dictionary containing all analysis results
        """
        results = {}
        
        # Load data summary
        with open(self.data_path / "processed/data_summary.json", "r") as f:
            results['summary'] = json.load(f)
            
            # Convert string values to appropriate types
            results['summary']['total_budget'] = float(results['summary']['total_budget'])
            results['summary']['avg_conversion_rate'] = float(results['summary']['avg_conversion_rate'])
            results['summary']['avg_roi'] = float(results['summary']['avg_roi'])
        
        # Load cohort analysis results
        cohort_files = (self.data_path / "output/cohort_analysis").glob("*.csv")
        results['cohort'] = {
            f.stem: pd.read_csv(f) for f in cohort_files
        }
        
        # Load segment analysis results
        segment_files = (self.data_path / "output/segment_analysis").glob("*.csv")
        results['segment'] = {
            f.stem: pd.read_csv(f) for f in segment_files
        }
        
        # Load channel analysis results
        channel_files = (self.data_path / "output/channel_analysis").glob("*.csv")
        results['channel'] = {
            f.stem: pd.read_csv(f) for f in channel_files
        }
        
        return results

    def copy_visualizations(self):
        """Copy analysis visualizations to the whitepaper images directory."""
        # Copy cohort analysis visualizations
        for img in (self.data_path / "output/cohort_analysis").glob("*.png"):
            shutil.copy2(img, self.image_path / img.name)
        
        # Copy segment analysis visualizations
        for img in (self.data_path / "output/segment_analysis").glob("*.png"):
            shutil.copy2(img, self.image_path / img.name)
        
        # Copy channel analysis visualizations
        for img in (self.data_path / "output/channel_analysis").glob("*.png"):
            shutil.copy2(img, self.image_path / img.name)

    def generate_executive_summary(self, results: dict) -> str:
        """
        Generate the executive summary section.
        
        Args:
            results (dict): Analysis results
            
        Returns:
            str: Executive summary markdown text
        """
        summary = results['summary']
        
        return f"""## Executive Summary

This analysis examines {summary['total_campaigns']} marketing campaigns across multiple channels and segments, 
spanning from {summary['date_range']['start']} to {summary['date_range']['end']}. Key findings include:

1. **Overall Performance**
   - Average Conversion Rate: {summary['avg_conversion_rate']:.2%}
   - Average ROI: {summary['avg_roi']:.2f}
   - Total Budget Utilized: ${summary['total_budget']:,.2f}

2. **Channel Performance**
   - Top performing channels identified by ROI and conversion rate
   - Significant variation in cost efficiency across channels
   - Clear patterns in channel effectiveness by audience segment

3. **Customer Segmentation**
   - Distinct customer segments identified through clustering analysis
   - Segment-specific channel preferences and behaviors observed
   - Opportunities for targeted optimization identified

4. **Strategic Recommendations**
   - Channel budget reallocation opportunities
   - Segment-specific targeting improvements
   - Temporal optimization strategies
"""

    def generate_methodology_section(self) -> str:
        """
        Generate the methodology section.
        
        Returns:
            str: Methodology section markdown text
        """
        return """## Methodology

### Data Processing and Analysis Framework

1. **Data Preparation**
   - Comprehensive data validation and cleaning
   - Feature engineering and derived metrics
   - Temporal aggregation and segmentation

2. **Analysis Components**
   - Cohort Analysis: Customer lifecycle and behavior patterns
   - Segment Analysis: RFM metrics and clustering
   - Channel Analysis: Performance metrics and statistical testing

3. **Statistical Methods**
   - ANOVA for channel performance comparison
   - Clustering for customer segmentation
   - Time series analysis for temporal patterns

4. **Visualization Techniques**
   - Interactive dashboards for exploration
   - Statistical plots for pattern identification
   - Comparative visualizations for insights
"""

    def generate_findings_section(self, results: dict) -> str:
        """
        Generate the key findings section.
        
        Args:
            results (dict): Analysis results
            
        Returns:
            str: Key findings section markdown text
        """
        return f"""## Key Findings

### Channel Performance Analysis

![Channel ROI Comparison](images/channel_roi_comparison.png)

1. **Channel Effectiveness**
   - Detailed performance metrics by channel
   - Cost efficiency analysis
   - Conversion funnel analysis

### Customer Segmentation Insights

![Segment Performance](images/segment_performance_scatter.png)

1. **Segment Characteristics**
   - Behavioral patterns by segment
   - Channel preferences
   - Response to campaign types

### Cohort Analysis Results

![Cohort Retention](images/cohort_retention_heatmap.png)

1. **Temporal Patterns**
   - Customer lifecycle analysis
   - Retention patterns
   - Value evolution
"""

    def generate_recommendations_section(self, results: dict) -> str:
        """
        Generate the recommendations section.
        
        Args:
            results (dict): Analysis results
            
        Returns:
            str: Recommendations section markdown text
        """
        return """## Strategic Recommendations

### Channel Optimization

1. **Budget Allocation**
   - Redistribute budget based on ROI performance
   - Focus on high-performing channels
   - Test new channel combinations

2. **Targeting Improvements**
   - Segment-specific channel strategies
   - Temporal optimization
   - Creative optimization

### Implementation Plan

1. **Short-term Actions (0-3 months)**
   - Immediate budget adjustments
   - Quick-win optimizations
   - Testing framework setup

2. **Medium-term Strategy (3-6 months)**
   - Channel mix optimization
   - Segment-specific campaigns
   - Performance monitoring system

3. **Long-term Development (6+ months)**
   - Advanced analytics implementation
   - Automated optimization
   - Continuous improvement framework
"""

    def compile_whitepaper(self):
        """Compile the complete whitepaper."""
        try:
            # Load analysis results
            results = self.load_analysis_results()
            
            # Copy visualizations
            self.copy_visualizations()
            
            # Generate whitepaper sections
            sections = [
                self.generate_executive_summary(results),
                self.generate_methodology_section(),
                self.generate_findings_section(results),
                self.generate_recommendations_section(results)
            ]
            
            # Combine sections
            whitepaper_content = "\n\n".join(sections)
            
            # Add metadata
            metadata = f"""# Marketing Campaign Performance Analysis
*Generated on {datetime.now().strftime('%Y-%m-%d')}*

"""
            
            # Write whitepaper
            with open(self.output_path, "w") as f:
                f.write(metadata + whitepaper_content)
            
            logger.info(f"Successfully compiled whitepaper at {self.output_path}")
            
        except Exception as e:
            logger.error(f"Error compiling whitepaper: {str(e)}")
            raise

def main():
    """Main function to compile the whitepaper."""
    compiler = WhitepaperCompiler()
    compiler.compile_whitepaper()

if __name__ == "__main__":
    main() 