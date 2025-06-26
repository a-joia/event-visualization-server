import datetime
import os
import time
import pickle
import hashlib
import random

test_data = {
    "x": [1, 2, 3, 4, 5]*10,
    "y": [1, 7, 2, 4, 7]*10,
    "z": [3, 2, 1, 2, 3]*10,
    "j": [6, 1, 8, 5, 6]*10,
    "timestamp": [datetime.datetime.now() - datetime.timedelta(days=i) for i in range(5*10)]
}

# Test data for bar plot with categorical features
bar_test_data = {
    "timestamp": [
        datetime.datetime.now() - datetime.timedelta(days=i) 
        for i in range(30)  # 30 days of data
    ],
    "status": [
        random.choice(["active", "pending", "completed", "failed", "cancelled"]) 
        for _ in range(30)
    ],
    "priority": [
        random.choice(["low", "medium", "high", "critical"]) 
        for _ in range(30)
    ],
    "category": [
        random.choice(["meeting", "review", "workshop", "planning", "break", "deployment"]) 
        for _ in range(30)
    ],
    "user": [
        random.choice(["alice", "bob", "charlie", "diana", "eve", "frank"]) 
        for _ in range(30)
    ],
    "location": [
        random.choice(["office", "remote", "meeting_room", "conference_center"]) 
        for _ in range(30)
    ]
}

class KustoHandler():
    def __init__(self):
        self.data = None
        self.bar_data = None
        self.last_load_time = None
        self.bar_last_load_time = None
        self.cache_duration = 600  # 10 minutes in seconds
        pass

    def _is_cache_valid(self, last_load_time):
        """Check if cache is still valid (less than 10 minutes old)"""
        if last_load_time is None:
            return False
        return (datetime.datetime.now() - last_load_time).total_seconds() < self.cache_duration

    def _update_cache(self, data_type="line"):
        """Update cache and timestamp"""
        if data_type == "line":
            self.data = test_data
            self.last_load_time = datetime.datetime.now()
        elif data_type == "bar":
            self.bar_data = bar_test_data
            self.bar_last_load_time = datetime.datetime.now()

    def get_data(self, query: str):
        """Get line chart data with caching"""
        # Check if cache is valid
        if self._is_cache_valid(self.last_load_time):
            if self.last_load_time:
                print(f"Using cached line data (loaded {self.last_load_time.strftime('%H:%M:%S')})")
            return self.data
        
        # Cache expired or doesn't exist, reload data
        print(f"Loading fresh line data at {datetime.datetime.now().strftime('%H:%M:%S')}")
        self._update_cache("line")
        return self.data

    def get_data_from_table(self, table: str, filters: dict):
        """Get data from table with caching"""
        return self.get_data("table_query")

    def get_bar_data(self, feature: str, start_date: str | None = None, end_date: str | None = None, bin_size: str = "1D"):
        """Get data for bar plot with specified feature and date range"""
        # Check if cache is valid
        if self._is_cache_valid(self.bar_last_load_time) and self.bar_data:
            if self.bar_last_load_time:
                print(f"Using cached bar data (loaded {self.bar_last_load_time.strftime('%H:%M:%S')})")
            filtered_data = self.bar_data.copy()
        else:
            # Cache expired or doesn't exist, reload data
            print(f"Loading fresh bar data at {datetime.datetime.now().strftime('%H:%M:%S')}")
            self._update_cache("bar")
            # Ensure bar_data is not None after update
            if self.bar_data:
                filtered_data = self.bar_data.copy()
            else:
                # Fallback to original data if cache update failed
                filtered_data = bar_test_data.copy()
        
        if start_date and end_date and self.bar_data:
            start_dt = datetime.datetime.fromisoformat(start_date)
            end_dt = datetime.datetime.fromisoformat(end_date)
            end_dt = end_dt.replace(hour=23, minute=59, second=59)
            
            # Filter timestamps and corresponding feature values
            filtered_indices = [
                i for i, ts in enumerate(self.bar_data["timestamp"])
                if start_dt <= ts <= end_dt
            ]
            
            filtered_data["timestamp"] = [self.bar_data["timestamp"][i] for i in filtered_indices]
            filtered_data[feature] = [self.bar_data[feature][i] for i in filtered_indices]
        
        # Group by bin size and count unique values
        if bin_size == "1H":
            # Group by hour
            bins = {}
            for i, ts in enumerate(filtered_data["timestamp"]):
                hour_key = ts.strftime("%Y-%m-%d %H:00")
                if hour_key not in bins:
                    bins[hour_key] = {}
                
                value = filtered_data[feature][i]
                bins[hour_key][value] = bins[hour_key].get(value, 0) + 1
            
            result = []
            for hour, counts in bins.items():
                for value, count in counts.items():
                    result.append({
                        "date": hour,
                        "value": value,
                        "count": count
                    })
            
            return result
        
        elif bin_size == "1D":
            # Group by day
            bins = {}
            for i, ts in enumerate(filtered_data["timestamp"]):
                day_key = ts.strftime("%Y-%m-%d")
                if day_key not in bins:
                    bins[day_key] = {}
                
                value = filtered_data[feature][i]
                bins[day_key][value] = bins[day_key].get(value, 0) + 1
            
            # Convert to list format for frontend
            result = []
            for day, counts in bins.items():
                for value, count in counts.items():
                    result.append({
                        "date": day,
                        "value": value,
                        "count": count
                    })
            
            return result
        
        elif bin_size == "1W":
            # Group by week
            bins = {}
            for i, ts in enumerate(filtered_data["timestamp"]):
                # Get the start of the week (Monday)
                week_start = ts - datetime.timedelta(days=ts.weekday())
                week_key = week_start.strftime("%Y-%m-%d")
                if week_key not in bins:
                    bins[week_key] = {}
                
                value = filtered_data[feature][i]
                bins[week_key][value] = bins[week_key].get(value, 0) + 1
            
            result = []
            for week, counts in bins.items():
                for value, count in counts.items():
                    result.append({
                        "date": week,
                        "value": value,
                        "count": count
                    })
            
            return result
        
        elif bin_size == "1M":
            # Group by month
            bins = {}
            for i, ts in enumerate(filtered_data["timestamp"]):
                month_key = ts.strftime("%Y-%m")
                if month_key not in bins:
                    bins[month_key] = {}
                
                value = filtered_data[feature][i]
                bins[month_key][value] = bins[month_key].get(value, 0) + 1
            
            result = []
            for month, counts in bins.items():
                for value, count in counts.items():
                    result.append({
                        "date": month,
                        "value": value,
                        "count": count
                    })
            
            return result
        
        elif bin_size == "3M":
            # Group by quarter (3 months)
            bins = {}
            for i, ts in enumerate(filtered_data["timestamp"]):
                year = ts.year
                quarter = (ts.month - 1) // 3 + 1
                quarter_key = f"{year}-Q{quarter}"
                if quarter_key not in bins:
                    bins[quarter_key] = {}
                
                value = filtered_data[feature][i]
                bins[quarter_key][value] = bins[quarter_key].get(value, 0) + 1
            
            result = []
            for quarter, counts in bins.items():
                for value, count in counts.items():
                    result.append({
                        "date": quarter,
                        "value": value,
                        "count": count
                    })
            
            return result
        
        else:
            # Default to daily bins
            return self.get_bar_data(feature, start_date, end_date, "1D")

    def get_available_features(self):
        """Get list of available categorical features"""
        return [key for key in bar_test_data.keys() if key != "timestamp"]

    def clear_cache(self):
        """Clear all cached data"""
        self.data = None
        self.bar_data = None
        self.last_load_time = None
        self.bar_last_load_time = None
        print("Cache cleared")

    def get_cache_status(self):
        """Get cache status information"""
        line_cache_valid = self._is_cache_valid(self.last_load_time)
        bar_cache_valid = self._is_cache_valid(self.bar_last_load_time)
        
        return {
            "line_cache": {
                "valid": line_cache_valid,
                "last_load": self.last_load_time.strftime('%Y-%m-%d %H:%M:%S') if self.last_load_time else None,
                "age_minutes": round((datetime.datetime.now() - self.last_load_time).total_seconds() / 60, 1) if self.last_load_time else None
            },
            "bar_cache": {
                "valid": bar_cache_valid,
                "last_load": self.bar_last_load_time.strftime('%Y-%m-%d %H:%M:%S') if self.bar_last_load_time else None,
                "age_minutes": round((datetime.datetime.now() - self.bar_last_load_time).total_seconds() / 60, 1) if self.bar_last_load_time else None
            },
            "cache_duration_minutes": self.cache_duration / 60
        }



