import datetime
import pandas as pd
FILE = "ANESTESIOLOGIA.xlsx"

def main():
    holidays()
    month_python, year_python = extract_data()
    day_python = extract_days()
    weekday = identify_weekday(month_python, year_python, day_python)
    work_schedule(weekday)

def extract_data():
    excel_data = pd.read_excel(FILE, dtype=str) # selecting the file and cell then getting the month and year
    desired_line = excel_data.loc[5]
    month_and_year = str(desired_line.iloc[0]).strip().lower()
    
    month_index = month_and_year.find(" ") # spliting month and year in two separate variables
    month_python = month_and_year[0:month_index]
    year_python = int(month_and_year[-4:])
    
    return month_python, year_python # returning year and month to be used in extract_days()

def extract_days():
    excel_data = pd.read_excel(FILE) # selecting the file
    day_python = list()
    
    for line in range(7, 24, 4):
        desired_line = excel_data.loc[line] # selecting the line of the target cell
        for row in range(1,8):
            check_nan = desired_line.iloc[row] # selecting the row of the target cell
            if str(check_nan) != "nan":
                day_python.append(check_nan) # storing the target day in a list
                
    return day_python # returning the list to be used in identify_weekday()

def identify_weekday(month_python, year_python, day_python):    
    days_of_week = ("segunda", "terça", "quarta", "quinta", "sexta", "sabado", "domingo")
    months = {"janeiro": 1, "fevereiro": 2, "março": 3, "abril": 4, "maio": 5, "junho": 6, "julho": 7,
            "agosto": 8, "setembro": 9, "outubro": 10, "novembro": 11, "dezembro": 12}
    calendar = dict()
    
    for cycle in range(len(day_python)): # loop to pass through all the days in the list, use weekday() and save it in dict
        week_date = datetime.date(year_python, months.get(month_python), day_python[cycle])
        weekday_number = week_date.weekday()
        weekday_string = days_of_week[weekday_number]
        calendar[cycle + 1] = weekday_string
    
    return calendar # returning the dict to be used in work_schedule()

def work_schedule(weekday):
    excel_data = pd.read_excel(FILE)
    schedule = list()
    
    for line in range(8, 26, 4): #selecting the first line of the targeted area
        for row in range(1,8): #selecting the rows of the targeted area
            for short_lines in range(line, line+3): # cycling trhough the lines in the targeted row
                desired_line = excel_data.loc[short_lines]
                check_nan = desired_line.iloc[row]
                if str(check_nan) != "nan":
                    first_hour_index = check_nan.find("h")
                    modified_first_hour = check_nan[first_hour_index+1:]
                    first_hour = check_nan[:first_hour_index].strip()
                    
                    modified_first_hour_index = modified_first_hour.find("h")
                    name = modified_first_hour[modified_first_hour_index + 1:] 
                    
                    desired_line = excel_data.loc[line - 1]
                    check_day = desired_line.iloc[row]
                    
                    one_or_two_names(schedule, name, check_day, first_hour, weekday)
    # print(schedule)

def one_or_two_names(schedule, name, check_day, first_hour, weekday):
    if "/" in name:
        slash_index = name.find("/")
        first_name = name[:slash_index]
        second_name = name[slash_index +1:]
        schedule.append({first_name: first_hour, check_day: weekday[check_day]})
        schedule.append({second_name: first_hour, check_day: weekday[check_day]})
    else:
        schedule.append({name: first_hour, check_day: weekday[check_day]})
    
    return schedule

def holidays():
    holiday_data = pd.read_csv('feriados.txt')
    holiday_days = list()
    
    for line in range(20):
        desired_line = holiday_data.loc[line]
        holiday_day = desired_line[:2]
        holiday_month = desired_line[3:5]
        holiday_year = desired_line[6:10]
        holiday_date = holiday_year + "/" + holiday_month + "/" + holiday_day
    
    holiday_days.append(holiday_date)
    
    print(holiday_date)
    print(holiday_days[0])

if __name__ == "__main__":
    main()