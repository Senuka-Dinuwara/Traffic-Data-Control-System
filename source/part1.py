# Author: Senuka Dinuwara
# Date: 12/10/2024

# Task A: Input Validation
def validate_date_input():
    """
    Prompts the user for a date in DD MM YYYY format, validates the input for:
    - Correct data type
    - Correct range for day, month, and year
    """
    day = month = year = None

    # Function to check if the input can be converted to an integer
    def check_type(value):
        try:
            value = int(value)
            return 1
        except ValueError:
            print('Integer required')
            return 0

    # Validate day input (1-31)
    def check_day(input_value):
        if check_type(input_value) == 0:
            return 0
        if len(input_value) > 2 and len(str(int(input_value))) < 3:
            print('Error: Input must be at most two digits.')
            return 0
        if int(input_value) < 1 or int(input_value) > 31:
            print('Out of range - values must be in the range 1 and 31.')
            return 0
        return 1

    # Validate month input (1-12)
    def check_month(input_value):
        if check_type(input_value) == 0:
            return 0
        if len(input_value) > 2 and len(str(int(input_value))) < 3:
            print('Error: Input must be at most two digits.')
            return 0
        if int(input_value) < 1 or int(input_value) > 12:
            print('Out of range - values must be in the range 1 to 12.')
            return 0
        return 1

    # Validate year input (2000-2024)
    def check_year(input_value):
        if check_type(input_value) == 0:
            return 0
        if len(input_value) != 4:
            print('Error: Input must consist of exactly four digits.')
            return 0
        if int(input_value) < 2000 or int(input_value) > 2024:
            print('Out of range - values must range from 2000 and 2024.')
            return 0
        return 1

    # Main loop for date input validation
    while True:
        for i in [['day', 'dd'], ['month', 'MM'], ['year', 'YYYY']]:
            while True:
                user_input = input(f'Please enter the {i[0]} of the survey in the format {i[1]}: ')
                if i[1] == 'dd':
                    check = check_day(user_input)
                    if check == 1:
                        day = str(int(user_input)).zfill(2)
                        break
                elif i[1] == 'MM':
                    check = check_month(user_input)
                    if check == 1:
                        month = str(int(user_input)).zfill(2)
                        break
                elif i[1] == 'YYYY':
                    check = check_year(user_input)
                    if check == 1:
                        year = str(int(user_input))
                        break

        # Additional validation for February and months with fewer days
        if int(month) == 2:
            if int(year) % 4 == 0:
                if int(day) > 29:
                    print("\nError: The date you entered is not valid.\n")
                    continue
            else:
                if int(day) > 28:
                    print("\nError: The date you entered is not valid.\n")
                    continue
        else:
            if int(month) in [4, 6, 9, 11]:
                if int(day) > 30:
                    print("\nError: The date you entered is not valid.\n")
                    continue

        return day, month, year  # Validation logic goes here


def validate_continue_input():
    """
    Prompts the user to decide whether to load another dataset:
    - Validates "Y" or "N" input
    """
    validate = input('\nDo you want to select another data file for a different date? Y/N : ').lower()
    while len(validate) == 0 or validate not in ['n', 'y']:
        validate = input('Please enter “Y” or “N” : ').lower()
    return validate  # Validation logic goes here


# Task B: Processed Outcomes
def process_csv_data(file_path):
    """
    Processes the CSV data for the selected date and extracts:
    - Total vehicles
    - Total trucks
    - Total electric vehicles
    - Two-wheeled vehicles, and other requested metrics
    """
    csv_data = []
    try:
        with open(file_path, 'r') as csv:
            file = csv.read().splitlines()
            for line in file:
                csv_data.append(line.split(','))
    except FileNotFoundError:
        print(f"\nError: The file '{file_path}' does not exist.")
        return 0

    # Prompt to process another dataset if needed
    if validate_continue_input() == 'y':
        return -1

    # Initialize report list
    report = []

    # Extract specific data to lists for processing
    data = csv_data[1:]  # Exclude header row

    # File name
    file_name = file_path[-24:]
    report.append(file_name)

    # Total number of vehicles recorded
    t_vehicles = len(data)
    report.append(t_vehicles)

    # Initialize counts
    t_trucks = 0
    t_electric = 0
    t_2wheel_vehicles = 0
    t_buses_north = 0
    t_no_turn = 0
    over_speed_limit = 0
    t_elm = 0
    t_hanley = 0
    t_scooters_elm = 0
    hour_rain = 0
    bicycle_count = 0

    # Direction list for no-turn logic
    direction = ['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW']

    # Process each row
    for row in data:
        # Count trucks
        if row[-2] == 'Truck':
            t_trucks += 1

        # Count electric vehicles
        if row[-1] == 'True':
            t_electric += 1

        # Count two-wheeled vehicles
        if row[-2] in ['Bicycle', 'Scooter', 'Motorcycle']:
            t_2wheel_vehicles += 1

        # Count Buses heading North at Elm Avenue/Rabbit Road
        if row[0] == 'Elm Avenue/Rabbit Road' and row[4] == 'N' and row[-2] == 'Buss':
            t_buses_north += 1

        # Count vehicles not turning left or right
        for i in range(4):
            if (row[3] == direction[i] and row[4] == direction[i]) or (
                    row[3] == direction[i + 4] and row[4] == direction[i + 4]):
                t_no_turn += 1
                break

        # Count over-speeding vehicles
        if int(row[7]) > int(row[6]):
            over_speed_limit += 1

        # Count vehicles at Elm Avenue/Rabbit Road
        if row[0] == 'Elm Avenue/Rabbit Road':
            t_elm += 1
            # Count scooters at Elm Avenue/Rabbit Road
            if row[-2] == 'Scooter':
                t_scooters_elm += 1

        # Count vehicles at Hanley Highway/Westway
        if row[0] == 'Hanley Highway/Westway':
            t_hanley += 1

        # Count hours of rain
        if row[5].endswith('Rain') or "Rain" in row[5]:
            hour_rain += 1

        # Count bicycles
        if row[-2] == 'Bicycle':
            bicycle_count += 1

    # Append values to the list
    report.append(t_trucks)  # Total trucks
    report.append(t_electric)  # Total electric vehicles
    report.append(t_2wheel_vehicles)  # Total two-wheeled vehicles
    report.append(t_buses_north)  # Total buses heading North at Elm Avenue/Rabbit Road
    report.append(t_no_turn)  # Total vehicles not turning left or right
    report.append(over_speed_limit)  # Total over-speeding vehicles
    report.append(t_elm)  # Total vehicles at Elm Avenue/Rabbit Road
    report.append(t_hanley)  # Total vehicles at Hanley Highway/Westway
    report.append(hour_rain)  # Total hours of rain

    # Calculate averages and percentages
    ave_bicycle = round(bicycle_count / 24)
    report.insert(7, ave_bicycle)  # Average bicycles per hour

    if t_elm > 0:
        per_scooter_elm = int((t_scooters_elm / t_elm) * 100)
    else:
        per_scooter_elm = 0
    report.insert(-1, per_scooter_elm)  # Percentage of scooters at Elm Avenue/Rabbit Road

    if t_vehicles > 0:
        pre_truck = round((t_trucks / t_vehicles) * 100)
    else:
        pre_truck = 0
    report.insert(7, pre_truck)  # Percentage of trucks

    report_hours = {}
    for T0 in range(3):
        for T1 in range(10):
            hour = str(T0) + str(T1)
            if int(hour) > 23:
                break
            for row in data:
                if row[0] == 'Hanley Highway/Westway':
                    if row[2].startswith(hour):
                        if hour in report_hours:
                            report_hours[hour] += 1
                        else:
                            report_hours[hour] = 1
    higher_key, higher_value, higher_items, hour_range = '', 0, [], ''
    for key, value in report_hours.items():
        if higher_value < value:
            higher_items = []
            higher_key, higher_value = key, value
            higher_items.append([higher_key, higher_value])
        elif higher_value == value:
            higher_items.append([key, value])
    for place, hour in enumerate(higher_items):
        start_time = hour[0] + ':00'
        end_time = str(int(hour[0]) + 1)
        if len(end_time) != 2:
            end_time = '0' + end_time
        if end_time == '24':
            end_time = '00'
        end_time += ':00'
        if place != 0:
            hour_range += ', '
        hour_range += start_time + ' and ' + end_time

    report.insert(-1, higher_value)
    report.insert(-1, hour_range)
    return report  # Logic for processing data goes here


def display_outcomes(outcomes):
    """
    Displays the calculated outcomes in a clear and formatted way.
    """
    display = f"""
*************************** 
data file selected is {outcomes[0]}
*************************** 
The total number of vehicles recorded for this date is {outcomes[1]} 
The total number of trucks recorded for this date is {outcomes[2]}
The total number of electric vehicles for this date is {outcomes[3]} 
The total number of two-wheeled vehicles for this date is {outcomes[4]}
The total number of Busses leaving Elm Avenue/Rabbit Road heading North is {outcomes[5]} 
The total number of Vehicles through both junctions not turning left or right is {outcomes[6]} 
The percentage of total vehicles recorded that are trucks for this date is {outcomes[7]}%
The average number of Bikes per hour for this date is {outcomes[8]} 
 
The total number of Vehicles recorded as over the speed limit for this date is {outcomes[9]}  
The total number of vehicles recorded through Elm Avenue/Rabbit Road junction is {outcomes[10]}
The total number of vehicles recorded through Hanley Highway/Westway junction is {outcomes[-5]}  
{outcomes[-4]}% of vehicles recorded through Elm Avenue/Rabbit Road are scooters. 
 
The highest number of vehicles in an hour on Hanley Highway/Westway is {outcomes[-3]}
The most vehicles through Hanley Highway/Westway were recorded between {outcomes[-2]}  
The number of hours of rain for this date is {outcomes[-1]} """
    print(display)
    return  # Printing outcomes to the console


# Task C: Save Results to Text File
def save_results_to_file(outcomes, file_name="results.txt"):
    """
    Saves the processed outcomes to a text file and appends if the program loops.
    """
    write = f"""data file selected is {outcomes[0]}
The total number of vehicles recorded for this date is {outcomes[1]} 
The total number of trucks recorded for this date is {outcomes[2]}
The total number of electric vehicles for this date is {outcomes[3]} 
The total number of two-wheeled vehicles for this date is {outcomes[4]}
The total number of Busses leaving Elm Avenue/Rabbit Road heading North is {outcomes[5]} 
The total number of Vehicles through both junctions not turning left or right is {outcomes[6]} 
The percentage of total vehicles recorded that are trucks for this date is {outcomes[7]}%
The average number of Bikes per hour for this date is {outcomes[8]} 
The total number of Vehicles recorded as over the speed limit for this date is {outcomes[9]}  
The total number of vehicles recorded through Elm Avenue/Rabbit Road junction is {outcomes[10]}
The total number of vehicles recorded through Hanley Highway/Westway junction is {outcomes[-5]}  
{outcomes[-4]}% of vehicles recorded through Elm Avenue/Rabbit Road are scooters. 
The highest number of vehicles in an hour on Hanley Highway/Westway is {outcomes[-3]}
The most vehicles through Hanley Highway/Westway were recorded between {outcomes[-2]}  
The number of hours of rain for this date is {outcomes[-1]} """

    with open(file_name, 'a+') as f0:
        f0.seek(0)
        if f0.read(1):  # Add separation if file is not empty
            f0.write('\n\n***************************\n\n')
        f0.write(write)
    return  # File writing logic goes here
