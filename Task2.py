import bs4
import httpx
from datetime import datetime

def process_date(date):
    date_day, date_month, date_year = date.split(".")

    if len(date_day) > 2 or len(date_day) < 1:
        raise ValueError("Incorrect day format")
    if len(date_month) > 2 or len(date_month) < 1:
        raise ValueError("Incorrect month format")
    if len(date_year) != 4:
        raise ValueError("Incorrect year format")

    if date_day[0] == "0":
        date_day = date_day[1:]
    if date_month[0] == "0":
        date_month = date_month[1:]

    if int(date_day) > 31 or int(date_day) < 1:
        raise ValueError("Incorrect day value")
    if int(date_month) > 12 or int(date_month) < 1:
        raise ValueError("Incorrect month value")
    if int(date_year) < 1 or int(date_year) > datetime.now().year:
        raise ValueError("Incorrect year value")
    return int(date_day), int(date_month), int(date_year)

def process_time(time):
    time_hour, time_minute = time.split(":")

    if len(time_hour) > 2 or len(time_hour) < 1:
        raise ValueError("Incorrect hour format")
    if len(time_minute) > 2 or len(time_minute) < 1:
        raise ValueError("Incorrect minute format")

    if time_hour[0] == "0":
        time_hour = time_hour[1:]
    if time_minute[0] == "0":
        time_minute = time_minute[1:]

    if int(time_hour) > 23 or int(time_hour) < 0:
        raise ValueError("Incorrect hour value")
    if int(time_minute) > 59 or int(time_minute) < 0:
        raise ValueError("Incorrect minute value")
    return int(time_hour), int(time_minute)

def is_weekend(date_time):
    url = 'https://www.consultant.ru/law/ref/calendar/proizvodstvennye/2024/'
    date, time = date_time.split(" ")
    date_day, date_month, date_year = process_date(date)
    time_hour, time_minute = process_time(time)

    try:
        response = httpx.get(url)
        soup = bs4.BeautifulSoup(response.text, 'html.parser')
        calendars = soup.find_all('div', class_='col-md-3')
        month_count = 1

        # iterating through all calendar tables
        for calendar in calendars:
            calendar_table = calendar.find_all('table', class_='cal')

            # iterating through one table
            for row in calendar_table:
                weeks = row.find_all('tr')

                # iterating through a week
                for day in weeks:
                    cells = day.find_all('td')

                    # iterating through each day
                    for cell in cells:
                        day_number = cell.text.strip()
                        if day_number == "":
                            continue
                        day_number = int(day_number.replace("*", ""))

                        cell_class = cell.get('class')
                        day_status = " ".join(cell_class)
                        if month_count == date_month and day_number == date_day: # day is weekend
                            if day_status == "holiday weekend" or day_status == "weekend":
                                return True
                            else: # day is working
                                if time_hour >= 9 and time_hour <= 18:
                                    return False
                                else:
                                    return "Это рабочий день, но время не рабочее"

                month_count += 1

    except httpx.RequestError as exc:
        print(f"An error occurred: {exc}")
    except httpx.HTTPError as exc:
        print(f"An error occurred: {exc}")
    except httpx.InvalidURL as exc:
        print(f"An error occurred: {exc}")



def main():
    date = input("Write date in format (DD.MM.YY) and time in format (HH:MM): ")
    print(is_weekend(date))

if __name__ == "__main__":
    main()


