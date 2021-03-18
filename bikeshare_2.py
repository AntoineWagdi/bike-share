import time
import pandas as pd
import numpy as np

CITY_DATA = { 'Chicago': 'chicago.csv',
              'New York City': 'new_york_city.csv',
              'Washington': 'washington.csv' }

month_list = {"January", "February","March", "April", "May","June", "All"}

day_list ={"Monday","Tuesday", "Wednesday", "Thursday", "Friday","Saturday", "Sunday","All"}

def get_filters():

    print('Hello! Let\'s explore some US bikeshare data!')
    city_query, month_query, day_query = False , False ,False
    while True:
        # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
        if not city_query:
            city=input('Where do you like to ride Chicago New York City or Washington:')
            city=city.title()
            if city not in CITY_DATA:
                print ("City is not found please choose on from above(T.C.case sensitive)")
                continue
            else:
                city_query= True
                # get user input for month (all, january, february, ... , june)
        if not month_query:
            month= input('What month do you search for please January, February, March, April,May and June type All if you want to see it All :')
            month=month.title()
            if month not in month_list:
                print("Month is not found please choose on from above(T.C.case sensitive)")
                continue
            else:
                month_query=True
        # get user input for day of week (all, monday, tuesday, ... sunday)
        if not day_query:
            day=input('What day are you looking for? type All if you want to see all week: ')
            day=day.title()
            if day not in day_list:
                print('This not a week day please enter you desire day:')
                continue
            else:
                break
    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "All" to apply no month filter
        (str) day - name of the day of week to filter by, or "All" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    start_time=time.time()
    print('Loading data')

    df = pd.read_csv(CITY_DATA.get(city),parse_dates=["Start Time","End Time"])
    
    df["Start Month"], df["Start Day"], df["Start Hour"]= (df["Start Time"].dt.month_name(),df["Start Time"].dt.day_name(),df["Start Time"].dt.hour)

    if month!="All":
        df =df[df["Start Month"]==month]
    if day!="All":
        df=df[df["Start Day"]==day]
    print("Done")
    print("\nThis took %s seconds." % (time.time() - start_time))
    return df


def time_stats(df, month, day):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    if month == "All":
        best_month=df["Start Month"].dropna()
        if best_month.empty:
            print("No suggested month please choose one!")
        else:
            best_month=best_month.mode()[0]
            print("Your best chance is:{}".format(best_month))
    else:
        print("Type All to get your best chance month instead of {}".format(month))

    # display the most common day of week
    if day == "All":
        best_day=df["Start Day"].dropna()
        if best_day.empty:
           print("No suggested day please choose one!")
        else:
            best_day=best_day.mode()[0]
            print("Your best chance is:{}".format(best_day))
    else:
        print("Type All to get your best chance day instead of {}".format(day))
    # display the most common start hour
        best_hour = df["Start Hour"].dropna()
        if best_hour.empty:
            print("No best hour due to your choises please try again")
        else:
            best_hour=best_hour.mode()[0]
            print("Your best hour is:{}:00h.".format(best_hour))
    print("Done")
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    most_popular_start_station=df["Start Station"]
    if most_popular_start_station.empty:
        print("No start station availble please try again!")
    else:
        most_popular_start_station=most_popular_start_station.mode()[0]
        print("Most popular start station is:{}".format(most_popular_start_station))

    # display most commonly used end station
    most_popular_end_station=df["End Station"]
    if most_popular_end_station.empty:
        print("No end station availble please try again!")
    else:
        most_popular_end_station=most_popular_end_station.mode()[0]
        print("Most popular end station is:{}".format(most_popular_end_station))
    # display most frequent combination of start station and end station trip
    most_frequent_start_and_end_station =df[["Start Station","End Station"]].dropna()
    if most_frequent_start_and_end_station.empty:
        print("No data found, try again!")
    else:
        most_frequent_start_and_end_station=(most_frequent_start_and_end_station.groupby(["Start Station","End Station"]).size().sort_values(ascending=False))
        trip_count = most_frequent_start_and_end_station.iloc[0]
        stations= most_frequent_start_and_end_station[most_frequent_start_and_end_station==trip_count].index[0]
        start_station, end_station =stations
        print("Most frequent start station is {} and end station is {} which take time about {}.".format(start_station,end_station,trip_count))
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    valid_time = df["Trip Duration"].dropna()
    if valid_time.empty:
        print("No record found, try again!")
    else:
        total_time=valid_time.sum()
        print("Total travel time:{}".format(total_time))

    # display mean travel time
    mean_time=valid_time.mean()
    print("Mean travel time:{}".format(mean_time))
    print("Done")
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_type = df["User Type"].dropna()
    if user_type.empty:
        print("No data availble try again!")
    else:
        user_type=user_type.value_counts()
        print("User type details:{}".format(user_type))

    # Display counts of gender
    if "Gender"in df:
        user_gender= df["Gender"].dropna()
        if user_gender.empty:
            print("No data availble try again!")
        else:
            user_gender=user_gender.value_counts()
            print("User gender count is {}".format(user_gender))

    # Display earliest, most recent, and most common year of birth
    if "Birth Year" in df:
        user_birth_year= df["Birth Year"].dropna()
        if user_birth_year.empty:
            print("No data found try again!")
        else:
            oldest_user=user_birth_year.min()
            print("The oldest useris{}".format(oldest_user))
            yongest_user=user_birth_year.max()
            print("The youngest user is :{}".format(yongest_user))
            com_user=user_birth_year.mode()[0]
            print("The most commun user are:{}".format(com_user))
        print("Done")
        print("\nThis took %s seconds." % (time.time() - start_time))
        print('-'*40)

def show_raw_data(df):
    """prints the selected data fram, 5 at a time"""
    choise= input( "Do you like to see raw data? [y/n]: ")
    count = 0
    if choise.lower()=="y":
        for raw in df.iterrows():
            print(raw)
            count+=1
            if count!=0 and count %5 ==0:
                choise = input("would you like to see raw data?[y/n]:")
                if choise.lower()!="y":
                    break

def main():
    while True:
        city, month, day = get_filters()
        print("Inputs are:\n City:{}, Month:{}, day:{}".format(city,month,day))
        df =load_data(city, month, day)
        if df.empty:
            print("No data availble please enter your request")
            continue
    
        time_stats(df, month, day)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        show_raw_data(df)

        restart = input('\nWould you like to restart? [y/n]\n')
        if restart.lower() != 'y':
            break


if __name__ == "__main__":
	main()
 