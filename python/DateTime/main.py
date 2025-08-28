import time as t
#from datetime import datetime
#from pytz import timezone 
import pendulum 
# basic printing current time that has passed in unix calendar(time passed since jan1st 1970). floating point value
def main()-> None:
    
    #print(time.time()) #floating point value
    #print(t.time_ns()) #time in nanoseconds. more precise. Integer value
    
    #2038 year problem. curr sys -> 32bit to store the date. will overflow in 2038 
    
    #utc = gmt = ztime = zulu 
    
    #some_date = datetime.fromisoformat("2022-08-27T14:05:30")
    #print(some_date)
    
    
    #print(some_date<datetime.now())
    
    #https://onezero.medium.com/the-largely-untold-story-of-how-one-guy-in-california-keeps-the-worlds-computers-on-the-right-time-a97a5493bf73 : tz database - the og database maintaining all date and time 
    
    '''
    utc = timezone("UTC")
    loc = utc.localize(some_date)
    print(loc)
    
    sydney = timezone("Australia/Sydney")
    print(loc.astimezone(sydney))
    
    
    amsterdam=timezone("Europe/Amsterdam")
    print(loc.astimezone(amsterdam))
   
   datetime has limitations primarily in its handling of advanced and high-precision timekeeping. While sufficient for most basic date and time manipulation, developers often need external libraries for more complex scenarios.
    Time zone and DST complications
    Naive vs. aware objects: A naive datetime object lacks time zone information, making it prone to errors when run across different geographical locations.
    Daylight saving time (DST) issues: The module doesn't automatically handle the complex and changing rules of DST transitions. This can lead to calculations that produce nonexistent or ambiguous times.
    Third-party reliance: For robust time zone support, including DST, developers must use external libraries like pytz, dateutil, or the built-in zoneinfo module (Python 3.9+).
    Limited precision and date range
    Precision: Standard datetime objects are limited to microsecond precision. For applications requiring nanosecond-level accuracy, such as high-performance or scientific computing, a different tool is needed.
    Date range: The module's range is restricted to the Gregorian calendar from year 1 to 9999, which is insufficient for astronomical or deep historical calculations.
    Performance overhead
    Slower operations: For tasks that involve a large number of time-related operations, the overhead of creating and manipulating datetime objects can be a performance bottleneck.
    Timestamp efficiency: Using simple integer timestamps from the time module is often faster for applications that perform numerous calculations.
    '''
    
    #alternate packages : Arrrow, Delorean, Pendulum
    #pendulum 
    some_date = pendulum.datetime(2022,10,9,18,0,tz="UTC")
    print(some_date)
    print(some_date.in_timezone("Australia/SYdney"))

if __name__ == "__main__":
    main()
