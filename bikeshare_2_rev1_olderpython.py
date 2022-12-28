import time
import datetime
import calendar
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
        (str) month - name of the month to filter by, or "" to apply no month filter
        (str) day - name of the day of week to filter by, or "" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data! \n')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    cities = ('chicago', 'new york city', 'washington')
    while True:
        city = input('Which of these cities do you want to explore : Chicago, New York City, or Washington? \n').lower()
        if city in cities:
            break
        else:
            print('\n That\'s not a valid entry. \n')

    # get user input for month (january, february, ... , june)
    months = ['january', 'february', 'march', 'april', 'may', 'june']
    print("\nPlease select a month. Months in the dataset:\n")
    print(", ".join(months).title())
    while True:
        month = input("\nLeave blank to look at all months in the dataset.\n").lower()
        if month in months:
            break
        else:
            print('\n That\'s not a valid entry. \n')

    # get user input for day of week (monday, tuesday, ... sunday)
    days = ['sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday']
    print("\nPlease select a day. Days in the dataset:\n")
    print(", ".join(days).title())
    while True:
        day = input("\nLeave blank to look at all months in the dataset.\n").lower()
        if day in days:
            break
        else:
            print('\n That\'s not a valid entry. \n')

    print('\nYou selected:\nCity: {}\nMonth: {}\nDay: {}\n'.format(city,month,day).title())

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
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()
    df['hour'] = df['Start Time'].dt.hour
    # filter by month if applicable
    if month != '':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != '':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    most_common_month = df['month'].mode()[0]
    print("Most common month: ",calendar.month_name[most_common_month])

    # display the most common day of week
    most_common_day_of_week = df['day_of_week'].mode()[0]
    print("Most common day of the week: ",most_common_day_of_week)

    # display the most common start hour
    most_common_start_hour = df['hour'].mode()[0]
    if most_common_start_hour >= 13:
        most_common_start_hour -= 12
        time_value = "PM"
    else:
        time_value = "AM"
    print("Most common start hour: {} {}".format(most_common_start_hour, time_value))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    most_common_start_station = df['Start Station'].mode()[0]
    print("Most common start station:",most_common_start_station)

    # display most commonly used end station
    most_common_end_station = df['End Station'].mode()[0]
    print("Most common end station:",(most_common_end_station))

    # display most frequent combination of start station and end station trip
    most_common_start_and_end_station = df[['Start Station', 'End Station']].mode().loc[0]
    print("Most common start and end station: \n {} \n --> \n {}"\
        .format(most_common_start_and_end_station[0], most_common_start_and_end_station[1]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print("Total travel time: ",pd.to_timedelta(total_travel_time, unit='sec'))

    # display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print("Mean travel time: ", mean_travel_time)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # display counts of user types
    user_count = df['User Type'].value_counts()
    print("Counts of user types:\n{}".format(user_count.to_string()))

    # display counts of gender
    try:
        gender_count = df['Gender'].value_counts()
        print("\nCounts of gender:\n")
        print(gender_count.to_string())
    except KeyError:
        print('\nNo Gender Data')
        pass

    # display earliest, most recent, and most common year of birth
    try:
        birth_year = df['Birth Year']
        earliest_birth_year = birth_year.min()
        print("\nEarliest year of birth: ", int(earliest_birth_year))
        most_recent_birth_year = birth_year.max()
        print("Most recent year of birth: ", int(most_recent_birth_year))
        most_common_birth_year = birth_year.value_counts().idxmax()
        print("Most common year of birth: ", int(most_common_birth_year))
    except KeyError:
        print('\nNo Birth Year Data')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def display_data(city):
    """ Loads the raw data allowing the user to look at the files 5 rows at a time """
    # load data file into a dataframe since we're showing raw data and not filtered
    df = pd.read_csv(CITY_DATA[city])
    answer = ['yes','no']
    start_loc = 0
    # inital loop to see if the user wants to see the first five rows of raw data
    while True:
        answers = input('\nDo you want to see the first 5 rows of data from this city? Enter yes or no\n').lower()
    # displays raw data (first 5 rows)
        if answers == 'yes':
            print('Raw data below',df.iloc[start_loc:(start_loc+5)])
    # breaks loop to last function
        if answers == 'no':
            break
    # check
        elif answers not in answer:
            print('\n That\'s not a valid entry. \n')
    # if the user wants to see an additional 5 rows
        while answers == 'yes':
            answers = input('Do you want to see 5 more rows of data? Enter yes or no\n').lower()
            start_loc += 5
    # print the same information but with the tracker moving up ana dditional 5 rows
            if answers == 'yes':
                print(df.iloc[start_loc:(start_loc+5)])
    # check
            elif answers not in answer:
                print('\n That\'s not a valid entry. \n')
    # if the users is done, this will remove them completely from the function
            elif answers == 'no':
                return

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_data(city)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
