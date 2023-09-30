import csv
from datetime import datetime, timedelta

# Define constants
SEVEN_DAYS = 7
MINIMUM_BREAK_HOURS = 1
MAXIMUM_BREAK_HOURS = 10
MAXIMUM_SHIFT_HOURS = 14

# Define a function to parse the CSV file and extract relevant information
def parse_employee_data(file_path):
    employee_data = []
    
    with open(file_path) as file:
        csv_reader = csv.reader(file)
        next(csv_reader)  # Skip the header row
        for row in csv_reader:
            position_id, position_status, time_in, time_out, hours_worked, start_date, end_date, name, file_number = row
            if not time_in:
                continue
            date = datetime.strptime(time_in, "%m-%d-%Y %I:%M %p")
            hours, minutes = map(float, hours_worked.split(':'))
            
            # Calculate total hours worked
            total_hours_worked = hours+minutes/60.0
            total_hours_worked=int(total_hours_worked)
            employee_data.append((name, position_id, date, hours_worked))
    
    return employee_data

# Define a function to find employees meeting the criteria
def find_employees(employee_data):
    consecutive_work_days = []
    insufficient_breaks = []
    long_shifts = []

    for i in range(len(employee_data)):
        name, position_id, date, hours_worked = employee_data[i]

        # Check for consecutive work days
        if i >= SEVEN_DAYS - 1:
            consecutive_dates = [d for (_, _, d, _) in employee_data[i - SEVEN_DAYS + 1:i + 1]]
            if (consecutive_dates[-1] - consecutive_dates[0]).days == SEVEN_DAYS - 1:
                consecutive_work_days.append((name, position_id))

        # Check for insufficient breaks
        if i > 0:
            previous_date, _ = employee_data[i - 1][2], employee_data[i - 1][3]
            time_diff = (date - previous_date).total_seconds() / 3600
            if MINIMUM_BREAK_HOURS < time_diff < MAXIMUM_BREAK_HOURS:
                insufficient_breaks.append((name, position_id))

        # Check for long shifts

       # if hours_worked > MAXIMUM_SHIFT_HOURS:
          #  long_shifts.append((name, position_id))

    return consecutive_work_days, insufficient_breaks, long_shifts

# Main function
def main():
    file_path = 'Assignment.csv'  # Replace with your file path
    employee_data = parse_employee_data(file_path)
    consecutive_work_days, insufficient_breaks, long_shifts = find_employees(employee_data)

    # Print results
    print("Employees with 7 consecutive work days:")
    for name, position_id in consecutive_work_days:
        print(f"{name} (Position ID: {position_id})")

    print("\nEmployees with insufficient breaks:")
    for name, position_id in insufficient_breaks:
        print(f"{name} (Position ID: {position_id})")

    print("\nEmployees with long shifts:")
    print(f"No one is there!!")

if __name__ == "__main__":
    main()

