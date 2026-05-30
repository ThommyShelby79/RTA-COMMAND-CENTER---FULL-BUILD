import pandas as pd
from core import time_to_minutes  # Imported from shared_utils

class RTACalculations:
    """Encapsulates all adherence calculations"""
    
    # Map the shared utility to the class
    time_to_minutes = staticmethod(time_to_minutes)
    
    @staticmethod
    def calculate_adherence(df: pd.DataFrame) -> pd.DataFrame:
        """Calculates adherence and handles errors gracefully to prevent dashboard crashes."""
        try:
            # ... (keep your existing adherence math logic exactly as it is) ...
            # Ensure your math logic uses self.time_to_minutes(...) where needed
            return df_result
        except Exception as e:
            # FIX: Returning an empty structure with default values 
            # This prevents the dashboard from crashing with a KeyError
            print(f"Error in adherence calculation: {e}")
            return pd.DataFrame({
                'agent_id': [],
                'adherence_pct': [0.0],
                'variance_minutes': [0],
                'status': ['Error'],
                'color': ['red']
            })