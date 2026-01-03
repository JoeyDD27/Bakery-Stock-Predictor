"""
New Zealand Calendar Module
Handles NZ-specific public holidays and school holidays for demand forecasting.
"""

import holidays
from datetime import datetime, date


def get_public_holiday_status(check_date):
    """
    Check if a date is a New Zealand public holiday.
    Includes national holidays and regional Anniversary days (Auckland region).
    
    Parameters:
    - check_date: date object or string in 'YYYY-MM-DD' format
    
    Returns:
    - True if the date is a public holiday, False otherwise
    """
    try:
        # Convert string to date if needed
        if isinstance(check_date, str):
            check_date = datetime.strptime(check_date, '%Y-%m-%d').date()
        elif isinstance(check_date, datetime):
            check_date = check_date.date()
        
        # Get NZ holidays including Auckland regional holidays
        nz_holidays = holidays.NewZealand(prov='AUK')  # AUK = Auckland
        
        return check_date in nz_holidays
    
    except Exception as e:
        # Return False on error to avoid breaking the pipeline
        return False


def is_school_holiday(check_date):
    """
    Check if a date falls within New Zealand school holiday periods for 2025.
    
    Hardcoded Term Break dates for 2025:
    - Term 1 Break: April 12 - April 27
    - Term 2 Break: June 28 - July 13
    - Term 3 Break: Sept 20 - Oct 5
    - Summer Break: Dec 17 onwards
    
    Parameters:
    - check_date: date object or string in 'YYYY-MM-DD' format
    
    Returns:
    - True if the date is within a school holiday period, False otherwise
    """
    try:
        # Convert string to date if needed
        if isinstance(check_date, str):
            check_date = datetime.strptime(check_date, '%Y-%m-%d').date()
        elif isinstance(check_date, datetime):
            check_date = check_date.date()
        
        # Define school holiday periods for 2025
        term_breaks = [
            # Term 1 Break: April 12 - April 27
            (date(2025, 4, 12), date(2025, 4, 27)),
            # Term 2 Break: June 28 - July 13
            (date(2025, 6, 28), date(2025, 7, 13)),
            # Term 3 Break: Sept 20 - Oct 5
            (date(2025, 9, 20), date(2025, 10, 5)),
            # Summer Break: Dec 17 onwards (through end of year)
            (date(2025, 12, 17), date(2025, 12, 31)),
        ]
        
        # Check if date falls within any term break
        for start_date, end_date in term_breaks:
            if start_date <= check_date <= end_date:
                return True
        
        return False
    
    except Exception as e:
        # Return False on error to avoid breaking the pipeline
        return False

