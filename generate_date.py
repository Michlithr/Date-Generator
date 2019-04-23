# Dates generator for etl process in our data warehouse

from datetime import date


# function for writing an insert
def write_insert(file, data):
    for row in data:
        file.write('INSERT INTO termiczna_pora_roku (')
        for i in range(len(row)):
            if i != 0:
                file.write(", ")
            file.write('"' + row[i]['name'] + '"')
        file.write(")\nVALUES (")
        for i in range(len(row)):
            if i != 0:
                file.write(", ")
            if row[i]['value'] is None:
                file.write("NULL")
            elif isinstance(row[i]['value'], str):
                file.write("'" + row[i]['value'] + "'")
            else:
                file.write("'" + str(row[i]['value']) + "'")
        file.write(")\n\n")


# definitions of year are always going to change, months and days are constant because we are
# not taking real thermal seasons of year (according to the simplification we have adopted)
# actual_year is a beginning and ending year for all parts of year
# beginning of winter is the only exception so winter_beginning_year is always in december from actual_year - 1
actual_year = 1899
winter_beginning_year = 1898

# this variables are ready to make some randomization in future if we need this
winter_beginning_month = 12
winter_beginning_day = 7
winter_ending_month = 2
winter_ending_day = 19

prespring_beginning_month = 2
prespring_beginning_day = 20
prespring_ending_month = 3
prespring_ending_day = 20


spring_beginning_month = 3
spring_beginning_day = 21
spring_ending_month = 5
spring_ending_day = 27

summer_beginning_month = 5
summer_beginning_day = 28
summer_ending_month = 9
summer_ending_day = 18

autumn_beginning_month = 9
autumn_beginning_day = 19
autumn_ending_month = 10
autumn_ending_day = 31

prewinter_beginning_month = 11
prewinter_beginning_day = 1
prewinter_ending_month = 12
prewinter_ending_day = 6

first_year = 1898
last_year = 2101
# delta -> diff between first and last year * 6 (because of six seasons of year), this is just our range for loop
delta = 6 * (last_year - first_year)

# season is jut simple helpful int variable for detecting actual part of year in our loop
season = 1
dates = []
# generating thermal seasons in (Start:YYYY-MM-DD, End:YYYY-MM-DD, name_of_season) notation for inserts
for i in range(delta + 1):
    if season == 1:
        dates.append([
            {"name": "Start", "value": date(winter_beginning_year, winter_beginning_month, winter_beginning_day)},
            {"name": "End", "value": date(actual_year, winter_ending_month, winter_ending_day)},
            {"name": "Thermal season of year", "value": "winter"}
        ])
        season = 2
    elif season == 2:
        dates.append([
            {"name": "Start", "value": date(actual_year, prespring_beginning_month, prespring_beginning_day)},
            {"name": "End", "value": date(actual_year, prespring_ending_month, prespring_ending_day)},
            {"name": "Thermal season of year", "value": "pre-spring"}
        ])
        season = 3
    elif season == 3:
        dates.append([
            {"name": "Start", "value": date(actual_year, spring_beginning_month, spring_beginning_day)},
            {"name": "End", "value": date(actual_year, spring_ending_month, spring_ending_day)},
            {"name": "Thermal season of year", "value": "spring"}
        ])
        season = 4
    elif season == 4:
        dates.append([
            {"name": "Start", "value": date(actual_year, summer_beginning_month, summer_beginning_day)},
            {"name": "End", "value": date(actual_year, summer_ending_month, summer_ending_day)},
            {"name": "Thermal season of year", "value": "summer"}
        ])
        season = 5
    elif season == 5:
        dates.append([
            {"name": "Start", "value": date(actual_year, autumn_beginning_month, autumn_beginning_day)},
            {"name": "End", "value": date(actual_year, autumn_ending_month, autumn_ending_day)},
            {"name": "Thermal season of year", "value": "autumn"}
        ])
        season = 6
    else:
        dates.append([
            {"name": "Start", "value": date(actual_year, prewinter_beginning_month, prewinter_beginning_day)},
            {"name": "End", "value": date(actual_year, prewinter_ending_month, prewinter_ending_day)},
            {"name": "Thermal season of year", "value": "pre-winter"}
        ])
        season = 1
        winter_beginning_year = actual_year
        actual_year += 1

# opening file
file_inserts_sql = open('thermal_dates.sql', 'w')
write_insert(file_inserts_sql, dates)



