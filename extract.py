import datetime
import pandas as pd

def main():
    # month_python, year_python = extract_data()
    # day_python = extract_days()
    #  identify_weekday(month_python, year_python, day_python)
    work_schedule()

def extract_data():
    excel_data = pd.read_excel("ANESTESIOLOGIA.xlsx", dtype=str)
    desired_line = excel_data.loc[5]
    month_and_year = str(desired_line.iloc[0]).strip().lower()
    
    month_index = month_and_year.find(" ")
    month_python = month_and_year[0:month_index]
    year_python = int(month_and_year[-4:])
    
    print(month_python)
    print(year_python)
    
    return month_python, year_python

def extract_days():
    excel_data = pd.read_excel("ANESTESIOLOGIA.xlsx")
    day_python = list()
    
    for line in range(7, 24, 4):
        desired_line = excel_data.loc[line]
        for row in range(1,8):
            check = desired_line.iloc[row]
            if str(check) != "nan":
                day_python.append(check)
                
    return day_python

def identify_weekday(month_python, year_python, day_python):    
    days_of_week = ("segunda", "terça", "quarta", "quinta", "sexta", "sabado", "domingo")
    months = {"janeiro": 1, "fevereiro": 2, "março": 3, "abril": 4, "maio": 5, "junho": 6, "julho": 7,
            "agosto": 8, "setembro": 9, "outubro": 10, "novembro": 11, "dezembro": 12}
    calendar = dict()
    
    for cycle in range(len(day_python)):
        week_date = datetime.date(year_python, months.get(month_python), day_python[cycle])
        weekday_number = week_date.weekday()
        weekday_string = days_of_week[weekday_number]
        calendar[cycle + 1] = weekday_string
    
    print(calendar)

def work_schedule():
    excel_data = pd.read_excel("ANESTESIOLOGIA.xlsx")
    schedule = list()
    
    for line in range(8, 26, 4):
        for row in range(1,8):
            for short_lines in range(line, line+3):
                desired_line = excel_data.loc[short_lines]
                check = desired_line.iloc[row]
                if str(check) != "nan":
                    first_hour_index = check.find("h")
                    modified_first_hour = check[first_hour_index+1:]
                    first_hour = check[:first_hour_index].strip()
                    
                    modified_first_hour_index = modified_first_hour.find("h")
                    name = modified_first_hour[modified_first_hour_index + 1:] 
                    
                    if "/" in name:
                        slash_index = name.find("/")
                        first_name = name[:slash_index]
                        second_name = name[slash_index +1:]
                        schedule.append({first_name: first_hour})
                        schedule.append({second_name: first_hour})
                    else:
                        schedule.append({name: first_hour})
    print(schedule)

if __name__ == "__main__":
    main()