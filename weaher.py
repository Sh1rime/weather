import math
import sqlite3
con = sqlite3.connect("weather_data.sqlite")
cur = con.cursor()

cur.execute("SELECT * FROM weather_data")
weather_data = cur.fetchall()

cur.execute('PRAGMA table_info("weather_data")')
column_names = tuple([i[1] for i in cur.fetchall()])

country_prefix_list = []
for i in range(1, len(column_names), 3):
    country_prefix_list.append(column_names[i][:2])
country_prefix = tuple(country_prefix_list)

avg_temperature = []
for i in range(len(country_prefix)):
    cur.execute(f"""
                        SELECT AVG({country_prefix[i]}_temperature)
                        FROM weather_data
    """)
    avg_temperature.append([i[0] for i in cur.fetchall()])

min_avg_temperature_year = []
for i in range(len(country_prefix)):
    cur.execute(f"""
                        SELECT year, MIN(avg_temperature)
                        FROM
                        (
                            SELECT strftime('%Y', utc_timestamp) as year, AVG({country_prefix[i]}_temperature) as avg_temperature
                            FROM weather_data
                            GROUP BY strftime('%Y', utc_timestamp)
                        )
    """)
    min_avg_temperature_year.append(cur.fetchall())

min_avg_temperature_month = []
for i in range(len(country_prefix)):
    cur.execute(f"""
                        SELECT month, MIN(avg_temperature)
                        FROM
                        (
                            SELECT strftime('%m', utc_timestamp) as month, AVG({country_prefix[i]}_temperature) as avg_temperature
                            FROM weather_data
                            GROUP BY strftime('%m', utc_timestamp)
                        )

    """)
    min_avg_temperature_month.append(cur.fetchall())

min_avg_temperature_year_month = []
for i in range(len(country_prefix)):
    cur.execute(f"""
                        SELECT year_month, MIN(avg_temperature)
                        FROM
                        (
                            SELECT strftime('%Y %m', utc_timestamp) as year_month, AVG({country_prefix[i]}_temperature) as avg_temperature
                            FROM weather_data
                            GROUP BY strftime('%Y %m', utc_timestamp)
                        )
    """)
    min_avg_temperature_year_month.append(cur.fetchall())

mina = min_avg_temperature_year_month[0]
country = country_prefix[0]
for i in range(len(min_avg_temperature_year_month)):
    if mina[0][1] > min_avg_temperature_year_month[i][0][1]:
        mina = min_avg_temperature_year_month[i]
        country = country_prefix[i]
    else:
        pass

year_avg_temperature = []
spread = []
for i in range(len(country_prefix)):
    cur.execute(f"""
                            SELECT AVG({country_prefix[i]}_temperature)
                            FROM weather_data
                            GROUP BY strftime('%Y', utc_timestamp)
    """)
    year_avg_temperature.append([i[0] for i in cur.fetchall()])
    squared_deviations = [(val - (sum(year_avg_temperature[i]) / len(year_avg_temperature[i]))) ** 2 for val in year_avg_temperature[i]]
    standard_deviation = math.sqrt(sum(squared_deviations) / len(year_avg_temperature))
    spread.append(standard_deviation)
index = spread.index(max(spread))

min_max_temperature = []
for i in range(len(country_prefix)):
    cur.execute(f"""
                        SELECT MIN({country_prefix[i]}_temperature), MAX({country_prefix[i]}_temperature)
                        FROM weather_data
    """)
    min_max_temperature.append(cur.fetchall())
con.close()
class WeatherData:
    info1 = []
    for i in range(len(country_prefix)):
        info1.append(f'{country_prefix[i]}. Температура: {avg_temperature[i][0]}')
    info2 = []
    for i in range(len(country_prefix)):
        info2.append(f'{country_prefix[i]}. Год: {min_avg_temperature_year[i][0][0]}, Температура: {min_avg_temperature_year[i][0][1]}')
    info3 = []
    for i in range(len(country_prefix)):
        info3.append(
            f'{country_prefix[i]}. Месяц: {min_avg_temperature_month[i][0][0]}, Температура: {min_avg_temperature_month[i][0][1]}')
    info4 = f'{country}. Дата: {mina[0][0]}, Температура: {mina[0][1]}'
    info5 = f'{country_prefix[index]}. Отклонение темп-ы: {max(spread)}'
    info6 = []
    for i in range(len(country_prefix)):
        info6.append(f'{country_prefix[i]}. Минимальная темп-а: {min_max_temperature[i][0][0]}, Максимальная темп-а: {min_max_temperature[i][0][1]}')