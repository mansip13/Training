"""
Date utility functions using pendulum library
Handles date parsing, validation, and formatting
"""

import pendulum
from typing import Optional, List, Tuple
from rich.console import Console

console = Console()

class DateUtils:
    """Utility class for date operations using pendulum"""

    @staticmethod
    def parse_date(date_string: str) -> Optional[pendulum.DateTime]:
        """
        Parse various date formats into pendulum DateTime object

        Args:
            date_string: Date string in various formats

        Returns:
            Pendulum DateTime object or None if parsing fails
        """
        date_formats = [
            'YYYY-MM-DD',
            'MM/DD/YYYY', 
            'DD/MM/YYYY',
            'YYYY/MM/DD',
            'MM-DD-YYYY',
            'DD-MM-YYYY'
        ]

        for fmt in date_formats:
            try:
                return pendulum.from_format(date_string, fmt)
            except ValueError:
                continue

        # Try natural language parsing
        try:
            return pendulum.parse(date_string)
        except:
            return None

    @staticmethod
    def validate_date(date_string: str) -> Tuple[bool, Optional[pendulum.DateTime]]:
        """
        Validate if a date string is valid

        Args:
            date_string: Date string to validate

        Returns:
            Tuple of (is_valid, parsed_date)
        """
        parsed_date = DateUtils.parse_date(date_string)
        return parsed_date is not None, parsed_date

    @staticmethod
    def get_date_range(start_date: str, end_date: str) -> Optional[List[pendulum.DateTime]]:
        """
        Generate list of dates between start and end date (inclusive)

        Args:
            start_date: Start date string
            end_date: End date string

        Returns:
            List of pendulum DateTime objects or None if invalid dates
        """
        start = DateUtils.parse_date(start_date)
        end = DateUtils.parse_date(end_date)

        if not start or not end:
            return None

        if start > end:
            start, end = end, start  # Swap if start is after end

        dates = []
        current = start
        while current <= end:
            dates.append(current)
            current = current.add(days=1)

        return dates

    @staticmethod
    def format_date(date_obj: pendulum.DateTime, format_str: str = 'MMMM DD, YYYY') -> str:
        """
        Format pendulum DateTime object to string

        Args:
            date_obj: Pendulum DateTime object
            format_str: Format string

        Returns:
            Formatted date string
        """
        return date_obj.format(format_str)

    @staticmethod
    def get_today() -> pendulum.DateTime:
        """Get current date"""
        return pendulum.now()

    @staticmethod
    def get_yesterday() -> pendulum.DateTime:
        """Get yesterday's date"""
        return pendulum.now().subtract(days=1)

    @staticmethod
    def get_tomorrow() -> pendulum.DateTime:
        """Get tomorrow's date"""
        return pendulum.now().add(days=1)

    @staticmethod
    def is_valid_date_range(start_date: str, end_date: str) -> Tuple[bool, str]:
        """
        Validate date range

        Args:
            start_date: Start date string
            end_date: End date string

        Returns:
            Tuple of (is_valid, error_message)
        """
        start = DateUtils.parse_date(start_date)
        end = DateUtils.parse_date(end_date)

        if not start:
            return False, f"Invalid start date: {start_date}"
        if not end:
            return False, f"Invalid end date: {end_date}"

        if start > end:
            return False, "Start date cannot be after end date"

        # Check if date range is reasonable (not too far in past/future)
        today = pendulum.now()
        max_past = today.subtract(years=1)
        max_future = today.add(days=10)  # Weather forecast limit

        if start < max_past:
            return False, "Start date is too far in the past (max 1 year)"
        if end > max_future:
            return False, "End date is too far in the future (max 10 days)"

        return True, ""

    @staticmethod
    def format_datetime_for_filename(date_obj: pendulum.DateTime) -> str:
        """
        Format datetime for use in filenames

        Args:
            date_obj: Pendulum DateTime object

        Returns:
            Filename-safe date string
        """
        return date_obj.format('YYYY-MM-DD')

    @staticmethod
    def get_time_points(date_obj: pendulum.DateTime) -> List[pendulum.DateTime]:
        """
        Get specific time points for a date (6am, 12pm, 6pm, 12am)

        Args:
            date_obj: Pendulum DateTime object

        Returns:
            List of DateTime objects at specific times
        """
        return [
            date_obj.at(6, 0, 0),   # 6:00 AM
            date_obj.at(12, 0, 0),  # 12:00 PM
            date_obj.at(18, 0, 0),  # 6:00 PM
            date_obj.at(0, 0, 0)    # 12:00 AM (midnight)
        ]

    @staticmethod
    def prompt_for_date(prompt_text: str = "Enter date (YYYY-MM-DD): ") -> Optional[pendulum.DateTime]:
        """
        Interactive date input with validation

        Args:
            prompt_text: Prompt message for user input

        Returns:
            Valid pendulum DateTime or None if cancelled
        """
        while True:
            try:
                date_input = input(prompt_text).strip()
                if not date_input or date_input.lower() == 'cancel':
                    return None

                parsed_date = DateUtils.parse_date(date_input)
                if parsed_date:
                    console.print(f"✅ Parsed date: {DateUtils.format_date(parsed_date)}", style="green")
                    return parsed_date
                else:
                    console.print("❌ Invalid date format. Please use YYYY-MM-DD, MM/DD/YYYY, or DD/MM/YYYY", style="red")

            except KeyboardInterrupt:
                return None
            except Exception as e:
                console.print(f"❌ Error parsing date: {str(e)}", style="red")