# verifies whether the string a user enters is a valid 
# day. The valid_day() function takes as 
# input a String, and returns either a valid 
# Int or None. If the passed in String is 
# not a valid day, return None. 
# If it is a valid day, then return 
# the day as an Int, not a String. Don't 
# worry about months of different length. 
# Assume a day is valid if it is a number 
# between 1 and 31.
# Be careful, the input can be any string 
# at all, you don't have any guarantees 
# that the user will input a sensible 
# day.
def valid_day(day):
    if day and day.isdigit():
        if 1 <= int(day) <=31:
            return int(day)


# print valid_day('1');
# print valid_day(None)    
# valid_day('1') => 1
# valid_day('15') => 15
# valid_day('500') => None


# verifies whether the data a user enters is a valid 
# month. If the passed in parameter 'month' 
# is not a valid month, return None. 
# If 'month' is a valid month, then return 
# the name of the month with the first letter 
# capitalized.
months = ['January',
          'February',
          'March',
          'April',
          'May',
          'June',
          'July',
          'August',
          'September',
          'October',
          'November',
          'December']
          
def valid_month(month):
    if month:
        month = month.title()
        if month in months:
          return month
        else:
          return None

# print valid_month("january")
# => "January"
# print valid_month("January") 
# => "January"
# print valid_month("foo")
# => None
# print valid_month("")
# => None
 
# verifies whether the string a user enters is a valid 
# year. If the passed in parameter 'year' 
# is not a valid year, return None. 
# If 'year' is a valid year, then return 
# the year as a number. Assume a year 
# is valid if it is a number between 1900 and 
# 2020.
def valid_year(year):
	if year and year.isdigit():
		year = int(year)
		if 1900 <= year <= 2020:
			return year

# print valid_year('0')    
# print valid_year('-11')
# print valid_year('1950')
# print valid_year('2000')
# print valid_year("notanumber")
# print valid_year(None)