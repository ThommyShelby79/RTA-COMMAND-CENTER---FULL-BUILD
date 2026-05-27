"""
RTA Calculations Module - Real-Time Adherence Math
Production-Ready Code with Full Error Handling
Author: Hatem Shalaby
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Optional
from datetime import datetime, timedelta

class RTACalculations:
    """Encapsulates all adherence calculations"""
    
    @staticmethod
    def time_to_minutes(time_str: str) -> int:
        """
        Convert HH:MM time string to total minutes since midnight.
        
        Args:
            time_str: Time in "HH:MM" format (24-hour)
            
        Returns:
            Total minutes from midnight
            
        Raises:
            ValueError: If time format is invalid
            
        Example:
            >>> RTACalculations.time_to_minutes("09:30")
            570  # 9*60 + 30
        """
        try:
            if not isinstance(time_str, str) or ':' not in time_str:
                raise ValueError(f"Invalid time format: {time_str}. Use HH:MM")
            
            hours, minutes = map(int, time_str.split(':'))
            
            if not (0 <= hours <= 23) or not (0 <= minutes <= 59):
                raise ValueError(f"Invalid time values: {time_str}")
            
            return hours * 60 + minutes
        except ValueError as e:
            raise ValueError(f"Time conversion error for '{time_str}': {str(e)}")
    
    @staticmethod
    def calculate_adherence(df: pd.DataFrame) -> pd.DataFrame:
        """
        Calculate Real-Time Adherence percentage for each agent.
        
        BUSINESS LOGIC:
        Adherence % = (Actual Productive Time / Scheduled Productive Time) × 100
        
        Where:
        - Productive Time = Total Work Time - Break Time
        - Status color-coded: Green ≥95%, Yellow 90-95%, Red <90%
        
        Args:
            df: DataFrame with columns:
                - agent_id (str): Unique agent identifier
                - agent_name (str): Agent display name
                - scheduled_start (str): "HH:MM" format
                - scheduled_end (str): "HH:MM" format
                - actual_start (str): "HH:MM" format
                - actual_end (str): "HH:MM" format
                - break_scheduled (int): Minutes
                - break_actual (int): Minutes
        
        Returns:
            DataFrame with added columns:
                - scheduled_time (int): Scheduled minutes (work only)
                - actual_time (int): Actual minutes (work only)
                - adherence_pct (float): 0-100 percentage
                - variance_minutes (int): Positive=extra, Negative=missing
                - status (str): "✅ Adherent", "⚠️ At Risk", "❌ Out"
                - color (str): "green", "yellow", "red"
        
        Raises:
            ValueError: If required columns missing
            
        Example:
            >>> data = {
            ...     'agent_id': ['A001'],
            ...     'agent_name': ['John'],
            ...     'scheduled_start': ['09:00'],
            ...     'scheduled_end': ['17:00'],
            ...     'actual_start': ['09:00'],
            ...     'actual_end': ['17:00'],
            ...     'break_scheduled': [60],
            ...     'break_actual': [60]
            ... }
            >>> df = pd.DataFrame(data)
            >>> result = RTACalculations.calculate_adherence(df)
            >>> print(result['adherence_pct'].iloc[0])
            100.0
        """
        
        # Validate required columns
        required_cols = ['agent_id', 'agent_name', 'scheduled_start', 'scheduled_end',
                        'actual_start', 'actual_end', 'break_scheduled', 'break_actual']
        missing_cols = [col for col in required_cols if col not in df.columns]
        if missing_cols:
            raise ValueError(f"Missing required columns: {missing_cols}")
        
        results = []
        
        for idx, row in df.iterrows():
            try:
                # Convert time strings to minutes
                scheduled_start = RTACalculations.time_to_minutes(str(row['scheduled_start']))
                scheduled_end = RTACalculations.time_to_minutes(str(row['scheduled_end']))
                actual_start = RTACalculations.time_to_minutes(str(row['actual_start']))
                actual_end = RTACalculations.time_to_minutes(str(row['actual_end']))
                
                # Get break times (handle various input types)
                break_scheduled = int(row['break_scheduled']) if pd.notna(row['break_scheduled']) else 0
                break_actual = int(row['break_actual']) if pd.notna(row['break_actual']) else 0
                
                # Calculate scheduled productive time (excluding breaks)
                scheduled_time = (scheduled_end - scheduled_start) - break_scheduled
                
                # Calculate actual productive time (excluding breaks)
                actual_time = (actual_end - actual_start) - break_actual
                
                # Handle negative times (shift spans midnight or invalid data)
                if scheduled_time < 0 or actual_time < 0:
                    adherence_pct = 0
                elif scheduled_time == 0:
                    adherence_pct = 0
                else:
                    adherence_pct = (actual_time / scheduled_time) * 100
                    adherence_pct = max(0, min(100, adherence_pct))  # Cap between 0-100
                
                # Determine status and color
                if adherence_pct >= 95:
                    status = "✅ Adherent"
                    color = "green"
                elif adherence_pct >= 90:
                    status = "⚠️ At Risk"
                    color = "yellow"
                else:
                    status = "❌ Out of Adherence"
                    color = "red"
                
                # Calculate variance in minutes
                variance_minutes = actual_time - scheduled_time
                
                results.append({
                    'agent_id': str(row['agent_id']),
                    'agent_name': str(row['agent_name']),
                    'scheduled_start': str(row['scheduled_start']),
                    'scheduled_end': str(row['scheduled_end']),
                    'actual_start': str(row['actual_start']),
                    'actual_end': str(row['actual_end']),
                    'scheduled_time': scheduled_time,
                    'actual_time': actual_time,
                    'adherence_pct': round(adherence_pct, 2),
                    'variance_minutes': variance_minutes,
                    'status': status,
                    'color': color
                })
            
            except Exception as e:
                # Log error but continue processing
                print(f"Error processing agent {row.get('agent_id', 'unknown')}: {str(e)}")
                results.append({
                    'agent_id': str(row['agent_id']),
                    'agent_name': str(row['agent_name']),
                    'adherence_pct': 0,
                    'status': '❌ Error',
                    'color': 'red',
                    'error': str(e)
                })
        
        return pd.DataFrame(results)
    
    @staticmethod
    def calculate_summary_metrics(df: pd.DataFrame) -> Dict:
        """
        Calculate summary statistics for the entire team.
        
        Args:
            df: DataFrame with adherence calculations
            
        Returns:
            dict with metrics:
            - total_agents (int)
            - avg_adherence (float)
            - adherent_count (int): ≥95%
            - at_risk_count (int): 90-95%
            - out_of_adherence_count (int): <90%
            - total_variance_hours (float)
        """
        
        total_agents = len(df)
        
        if total_agents == 0:
            return {
                'total_agents': 0,
                'avg_adherence': 0,
                'adherent_count': 0,
                'at_risk_count': 0,
                'out_of_adherence_count': 0,
                'total_variance_hours': 0
            }
        
        avg_adherence = df['adherence_pct'].mean()
        
        adherent_count = len(df[df['adherence_pct'] >= 95])
        at_risk_count = len(df[(df['adherence_pct'] >= 90) & (df['adherence_pct'] < 95)])
        out_of_adherence_count = len(df[df['adherence_pct'] < 90])
        
        total_variance_hours = df['variance_minutes'].sum() / 60
        
        return {
            'total_agents': total_agents,
            'avg_adherence': round(avg_adherence, 2),
            'adherent_count': adherent_count,
            'at_risk_count': at_risk_count,
            'out_of_adherence_count': out_of_adherence_count,
            'total_variance_hours': round(total_variance_hours, 2)
        }
    
    @staticmethod
    def generate_alerts(df: pd.DataFrame, threshold_minutes: int = 10) -> List[Dict]:
        """
        Generate alerts for agents significantly out of adherence.
        
        Args:
            df: DataFrame with adherence calculations
            threshold_minutes: Alert if variance exceeds this threshold
            
        Returns:
            List of alert dictionaries with:
            - agent_id
            - agent_name
            - alert_type: "Early Departure" or "Extended Time"
            - variance_minutes
            - adherence_pct
        """
        
        alerts = []
        
        for idx, row in df.iterrows():
            if abs(row['variance_minutes']) >= threshold_minutes:
                alert_type = "Early Departure" if row['variance_minutes'] < 0 else "Extended Time"
                
                alerts.append({
                    'agent_id': row['agent_id'],
                    'agent_name': row['agent_name'],
                    'alert_type': alert_type,
                    'variance_minutes': row['variance_minutes'],
                    'adherence_pct': row['adherence_pct'],
                    'severity': 'critical' if abs(row['variance_minutes']) >= 20 else 'warning'
                })
        
        return sorted(alerts, key=lambda x: abs(x['variance_minutes']), reverse=True)
    
    @staticmethod
    def calculate_daily_trend(daily_data: List[Dict]) -> pd.DataFrame:
        """
        Calculate adherence trends over multiple days.
        
        Args:
            daily_data: List of daily adherence records
            
        Returns:
            DataFrame with daily trend data
        """
        
        if not daily_data:
            return pd.DataFrame()
        
        df = pd.DataFrame(daily_data)
        
        if 'date' in df.columns and 'adherence_pct' in df.columns:
            df['date'] = pd.to_datetime(df['date'])
            return df.sort_values('date')
        
        return df

# Test functions
def test_calculations():
    """Unit tests for adherence calculations"""
    
    print("Running RTA Calculation Tests...")
    
    # Test 1: Basic adherence (100%)
    test_data_1 = {
        'agent_id': ['A001'],
        'agent_name': ['John'],
        'scheduled_start': ['09:00'],
        'scheduled_end': ['17:00'],
        'actual_start': ['09:00'],
        'actual_end': ['17:00'],
        'break_scheduled': [60],
        'break_actual': [60]
    }
    df = pd.DataFrame(test_data_1)
    result = RTACalculations.calculate_adherence(df)
    assert result['adherence_pct'].iloc[0] == 100.0, "Test 1 Failed"
    print("✅ Test 1 Passed: Basic adherence (100%)")
    
    # Test 2: Late arrival (adherence <100%)
    test_data_2 = {
        'agent_id': ['A002'],
        'agent_name': ['Jane'],
        'scheduled_start': ['09:00'],
        'scheduled_end': ['17:00'],
        'actual_start': ['09:15'],
        'actual_end': ['17:00'],
        'break_scheduled': [60],
        'break_actual': [60]
    }
    df = pd.DataFrame(test_data_2)
    result = RTACalculations.calculate_adherence(df)
    assert result['adherence_pct'].iloc[0] < 100.0, "Test 2 Failed"
    print("✅ Test 2 Passed: Late arrival detected")
    
    # Test 3: Out of adherence (<90%)
    test_data_3 = {
        'agent_id': ['A003'],
        'agent_name': ['Mike'],
        'scheduled_start': ['09:00'],
        'scheduled_end': ['17:00'],
        'actual_start': ['09:00'],
        'actual_end': ['16:30'],
        'break_scheduled': [60],
        'break_actual': [60]
    }
    df = pd.DataFrame(test_data_3)
    result = RTACalculations.calculate_adherence(df)
    assert result['adherence_pct'].iloc[0] < 90.0, "Test 3 Failed"
    assert result['status'].iloc[0] == "❌ Out of Adherence", "Test 3 Status Failed"
    print("✅ Test 3 Passed: Out of adherence detection")
    
    # Test 4: Summary metrics
    test_data_4 = pd.DataFrame({
        'agent_id': ['A001', 'A002', 'A003'],
        'agent_name': ['John', 'Jane', 'Mike'],
        'scheduled_start': ['09:00', '09:00', '09:00'],
        'scheduled_end': ['17:00', '17:00', '17:00'],
        'actual_start': ['09:00', '09:05', '09:10'],
        'actual_end': ['17:00', '17:00', '16:40'],
        'break_scheduled': [60, 60, 60],
        'break_actual': [60, 60, 60]
    })
    result = RTACalculations.calculate_adherence(test_data_4)
    summary = RTACalculations.calculate_summary_metrics(result)
    assert summary['total_agents'] == 3, "Test 4 Failed"
    assert summary['avg_adherence'] > 0, "Test 4 Summary Failed"
    print("✅ Test 4 Passed: Summary metrics calculated")
    
    # Test 5: Alerts
    alerts = RTACalculations.generate_alerts(result, threshold_minutes=10)
    assert len(alerts) > 0, "Test 5 Failed"
    print(f"✅ Test 5 Passed: {len(alerts)} alerts generated")
    
    print("\n✅ ALL TESTS PASSED - Code is production-ready\n")

if __name__ == "__main__":
    test_calculations()
