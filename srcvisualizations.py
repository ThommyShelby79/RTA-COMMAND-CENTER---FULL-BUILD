"""
Visualization Module - Plotly Charts for RTA Dashboard
Production-Ready Visualizations
"""

import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
from typing import List

class RTAVisualizations:
    """Encapsulates all RTA visualization logic"""
    
    @staticmethod
    def create_adherence_bar_chart(df: pd.DataFrame):
        """
        Create horizontal bar chart showing adherence by agent.
        Color-coded by status (green/yellow/red).
        
        Args:
            df: DataFrame with adherence calculations
            
        Returns:
            Plotly figure object
        """
        
        if df.empty:
            return go.Figure().add_annotation(text="No data available")
        
        # Sort by adherence percentage
        df_sorted = df.sort_values('adherence_pct', ascending=True)
        
        # Create color mapping
        colors = []
        for color in df_sorted['color']:
            if color == 'green':
                colors.append('#00AA00')
            elif color == 'yellow':
                colors.append('#FFAA00')
            else:
                colors.append('#FF0000')
        
        fig = go.Figure(data=[go.Bar(
            x=df_sorted['adherence_pct'],
            y=df_sorted['agent_name'],
            orientation='h',
            marker_color=colors,
            text=df_sorted['adherence_pct'],
            texttemplate='%{text:.1f}%',
            textposition='outside',
            hovertemplate='<b>%{y}</b><br>Adherence: %{x:.2f}%<extra></extra>'
        )])
        
        # Add target line at 95%
        fig.add_vline(x=95, line_dash="dash", line_color="blue", 
                     annotation_text="Target: 95%", annotation_position="top right")
        
        fig.update_layout(
            title='Agent Adherence Overview',
            xaxis_title='Adherence %',
            yaxis_title='Agent',
            height=max(400, len(df) * 25),
            showlegend=False,
            xaxis_range=[0, 105],
            hovermode='closest'
        )
        
        return fig
    
    @staticmethod
    def create_status_pie_chart(summary: dict):
        """
        Create pie chart showing distribution of adherence statuses.
        
        Args:
            summary: Dictionary with adherence counts
            
        Returns:
            Plotly figure object
        """
        
        labels = ['✅ Adherent (≥95%)', '⚠️ At Risk (90-95%)', '❌ Out (<90%)']
        values = [
            summary['adherent_count'],
            summary['at_risk_count'],
            summary['out_of_adherence_count']
        ]
        colors = ['#00AA00', '#FFAA00', '#FF0000']
        
        fig = go.Figure(data=[go.Pie(
            labels=labels,
            values=values,
            marker_colors=colors,
            hole=0.4,
            textinfo='label+percent',
            textposition='outside',
            hovertemplate='<b>%{label}</b><br>Count: %{value}<extra></extra>'
        )])
        
        fig.update_layout(
            title='Team Adherence Distribution',
            height=400
        )
        
        return fig
    
    @staticmethod
    def create_variance_chart(df: pd.DataFrame):
        """
        Create chart showing time variance (over/under schedule).
        Positive = extended time, Negative = early departure.
        
        Args:
            df: DataFrame with variance_minutes column
            
        Returns:
            Plotly figure object
        """
        
        if df.empty:
            return go.Figure().add_annotation(text="No data available")
        
        df_sorted = df.sort_values('variance_minutes')
        
        # Color by direction
        colors = ['#FF0000' if x < 0 else '#00AA00' for x in df_sorted['variance_minutes']]
        
        fig = go.Figure(data=[go.Bar(
            x=df_sorted['variance_minutes'],
            y=df_sorted['agent_name'],
            orientation='h',
            marker_color=colors,
            text=df_sorted['variance_minutes'],
            texttemplate='%{text:.0f} min',
            textposition='outside',
            hovertemplate='<b>%{y}</b><br>Variance: %{x:.0f} minutes<extra></extra>'
        )])
        
        # Add zero line
        fig.add_vline(x=0, line_dash="solid", line_color="black", annotation_text="On Schedule")
        
        fig.update_layout(
            title='Schedule Variance (Minutes)',
            xaxis_title='Minutes (Negative = Under Schedule, Positive = Over)',
            yaxis_title='Agent',
            height=max(400, len(df) * 25),
            hovermode='closest'
        )
        
        return fig
    
    @staticmethod
    def create_summary_metrics_chart(summary: dict):
        """
        Create KPI indicator cards for summary metrics.
        
        Args:
            summary: Dictionary with summary metrics
            
        Returns:
            Plotly figure object
        """
        
        fig = make_subplots(
            rows=1, cols=4,
            subplot_titles=('Total Agents', 'Avg Adherence', 'Adherent', 'Out of Adherence'),
            specs=[[{'type': 'indicator'}, {'type': 'indicator'}, 
                    {'type': 'indicator'}, {'type': 'indicator'}]]
        )
        
        # Total Agents
        fig.add_trace(go.Indicator(
            mode="number",
            value=summary['total_agents'],
            title={'text': 'Total Agents'},
            number={'font': {'size': 30}}
        ), row=1, col=1)
        
        # Average Adherence
        avg_adh = summary['avg_adherence']
        delta_color = 'green' if avg_adh >= 95 else 'red'
        fig.add_trace(go.Indicator(
            mode="number+delta",
            value=avg_adh,
            delta={'reference': 95, 'relative': False, 'valueformat': '.1f'},
            title={'text': 'Avg Adherence %'},
            number={'suffix': '%', 'font': {'size': 30}, 'valueformat': '.1f'},
            domain={'x': [0.25, 0.5], 'y': [0, 1]}
        ), row=1, col=2)
        
        # Adherent Count
        fig.add_trace(go.Indicator(
            mode="number",
            value=summary['adherent_count'],
            title={'text': 'Adherent (≥95%)'},
            number={'font': {'size': 30, 'color': 'green'}}
        ), row=1, col=3)
        
        # Out of Adherence Count
        fig.add_trace(go.Indicator(
            mode="number",
            value=summary['out_of_adherence_count'],
            title={'text': 'Out of Adherence (<90%)'},
            number={'font': {'size': 30, 'color': 'red'}}
        ), row=1, col=4)
        
        fig.update_layout(height=200, showlegend=False)
        
        return fig
    
    @staticmethod
    def create_alerts_display(alerts: List[dict]) -> str:
        """
        Create HTML display for alerts.
        
        Args:
            alerts: List of alert dictionaries
            
        Returns:
            HTML string for rendering
        """
        
        if not alerts:
            return "<p style='color: green;'>✅ No alerts - All agents within acceptable variance</p>"
        
        html = ""
        
        for alert in alerts:
            if alert['severity'] == 'critical':
                color_class = "background-color: #ff4444; color: white;"
                icon = "🚨"
            else:
                color_class = "background-color: #ffaa00; color: black;"
                icon = "⚠️"
            
            html += f"""
            <div style="padding: 1rem; border-radius: 0.5rem; margin: 0.5rem 0; {color_class}">
                <strong>{icon} {alert['agent_name']}</strong> ({alert['agent_id']})<br>
                {alert['alert_type']}: {abs(alert['variance_minutes'])} minutes<br>
                Adherence: {alert['adherence_pct']}%
            </div>
            """
        
        return html

def test_visualizations():
    """Test visualization functions"""
    
    print("Testing visualization functions...")
    
    # Create sample data
    test_df = pd.DataFrame({
        'agent_id': ['A001', 'A002', 'A003'],
        'agent_name': ['John', 'Jane', 'Mike'],
        'adherence_pct': [96.5, 92.3, 88.1],
        'color': ['green', 'yellow', 'red'],
        'variance_minutes': [5, -8, -25]
    })
    
    # Test bar chart
    fig = RTAVisualizations.create_adherence_bar_chart(test_df)
    assert fig is not None, "Bar chart failed"
    print("✅ Bar chart created successfully")
    
    # Test pie chart
    summary = {
        'adherent_count': 1,
        'at_risk_count': 1,
        'out_of_adherence_count': 1
    }
    fig = RTAVisualizations.create_status_pie_chart(summary)
    assert fig is not None, "Pie chart failed"
    print("✅ Pie chart created successfully")
    
    # Test variance chart
    fig = RTAVisualizations.create_variance_chart(test_df)
    assert fig is not None, "Variance chart failed"
    print("✅ Variance chart created successfully")
    
    # Test metrics
    summary['total_agents'] = 3
    summary['avg_adherence'] = 92.3
    fig = RTAVisualizations.create_summary_metrics_chart(summary)
    assert fig is not None, "Metrics chart failed"
    print("✅ Metrics chart created successfully")
    
    print("\n✅ ALL VISUALIZATION TESTS PASSED\n")

if __name__ == "__main__":
    test_visualizations()
