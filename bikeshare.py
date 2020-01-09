import time
import calendar
import csv
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs

    while True:
        try:
            city = input("Enter the name of the city you want to explore the data of (chicago, new york city, or washington): ")
            if city not in dict.keys(CITY_DATA):
                raise Exception ('Invalid city name')
            print ("You have selected: {}.\n".format(city.title()))
            break
        except Exception :
            print ("Invalid name of city, please choose chicago, new york city, or washington (writtent in this format)\n")

    # TO DO: get user input for month (all, january, february, ... , june)

    while True:
        valid_months_names =('all', 'january', 'february', 'march', 'april', 'may', 'june')
        try:
            month = input("Enter the month that you wish to explore (use 'all' for the entire timeframe): ")
            if month not in valid_months_names:
                raise Exception ('Invalid month name')
            print ("You have selected: {}.\n".format(month.title()))
            break
        except Exception :
            print ("Invalid month: Please choose from all, january, february, march, april, may, june\n")

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)

    while True:
        valid_day_names =('all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday')
        try:
            day = input("Enter the day that you wish to explore (use 'all' for exploring all days): ")
            if day not in valid_day_names:
                raise Exception ('Invalid day name')
            print ("You have selected: {}.\n".format(day.title()))
            break
        except Exception :
            print ("Invalid day: Please choose from all, monday, tuesday, wednesday, thursday, friday, saturday, sunday\n")

    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    df = pd.read_csv(CITY_DATA[city])
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['hour'] = df['Start Time'].dt.hour
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    #filter by month if needed and create a new frame
    if month != 'all':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
        df = df[df['month'] == month]
    # filter by day of week if needed
    if day != 'all':
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df, month, day):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    if month == 'all':
        most_common_month = df['month'].mode()[0]
        print ("The most frequent month of travel is: ", calendar.month_name[most_common_month])

    # TO DO: display the most common day of week
    if day == 'all':
        most_common_day = df['day_of_week'].mode()[0]
        print ("The most frequent day of travel is: ", most_common_day)

    # TO DO: display the most common start hour
    most_common_hour = df['hour'].mode()[0]
    print ("The most frequent hour of travel is: ", most_common_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    most_common_start_station = df['Start Station'].mode()[0]
    print ("The most frequent start station is:\n ->", most_common_start_station)

    # TO DO: display most commonly used end station
    most_common_end_station = df['End Station'].mode()[0]
    print ("The most frequent end station is:\n ->", most_common_end_station)

    # TO DO: display most frequent combination of start station and end station trip
    df['combinaison_start_end'] = df['Start Station'] + ' to ' + df['End Station']
    most_common_combinaison = df['combinaison_start_end'].mode()[0]
    print ("The most frequent itinerary (combinaison of start and end station) is:\n ->", most_common_combinaison)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    total_travel_time = round(np.sum(df['Trip Duration'])/60/60,2)
    print ('Total travel time over the selected period (in hours) is: ', total_travel_time)

    # TO DO: display mean travel time
    mean_travel_time = round(np.mean(df['Trip Duration'])/60,2)
    print ('The mean travel time over the selected period (in minutes) is: ', mean_travel_time)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    df['User Type'] = df['User Type'].fillna('Type Unknown')
    user_types = df['User Type'].unique()
    for user_type in user_types:
        count_user_type = (df['User Type'].values == user_type).sum()
        print ('The count of ', user_type, ' is ', count_user_type)
    print('\n')


    # TO DO: Display counts of gender
    try:
        df['Gender'] = df['Gender'].fillna('Gender Unknown')
        gender_types = df['Gender'].unique()
        for gender_type in gender_types:
            count_gender_type = (df['Gender'].values == gender_type).sum()
            print ('The count of ', gender_type, ' is ', count_gender_type)
    except:
        print('No gender data available for', city)
    print('\n')

    # TO DO: Display earliest, most recent, and most common year of birth
    try:
        df['Birth Year'] = df['Birth Year'].dropna()
        earliest_dob = int(df['Birth Year'].min())
        most_recent_dob = int(df['Birth Year'].max())
        most_common_dob = int(df['Birth Year'].mode()[0])

        print ('The earliest DoB in the dataset is ', earliest_dob)
        print ('The most recent DoB in the dataset is ', most_recent_dob)
        print ('The most common date of birth in the dataset is ', most_common_dob)
    except:
        print('No birth date data available for ', city)



    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def see_raw_data(city):
    """Allow to scroll through the raw data of the csv file selected"""
    
    while True:
        try:
            see_raw_data_input = input('\nIn addition of the stats above, would you like to scroll through the raw data? (y/n)\n')
            if see_raw_data_input not in ('y', 'n'):
                raise Exception ('Invalid answer')
            if see_raw_data_input == 'n':
                break
            if see_raw_data_input == 'y':
                with open (CITY_DATA[city], 'r') as f:
                    reader = csv.reader(f)
                    count_row_start_iteration = 0
                    count_row_read = 0
                    for row in reader:
                        print(row)
                        count_row_read += 1
                        if count_row_read == count_row_start_iteration +5:
                            continue_scroll = input('\nDo you want to continue scrolling 5 more rows through the raw data? (y/n): ')
                            if continue_scroll == 'n':
                                break
                            else:
                                count_row_start_iteration +=5      
        except Exception :
            print ("Please answer 'y' or 'n'\n")

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df, month, day)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)
        see_raw_data(city)
        
        
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
