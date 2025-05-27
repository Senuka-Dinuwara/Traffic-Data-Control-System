import part1 as csv
# Task D: Histogram Display
import tkinter as tk


class HistogramApp:
    def __init__(self, traffic_data, date):
        """
        Initializes the histogram application with the traffic data and selected date.
        """
        self.traffic_data = traffic_data  # Traffic data for the histogram
        self.date = date  # Date corresponding to the traffic data
        self.root = tk.Tk()  # Tkinter root window
        self.root.title("Histogram")  # Set the window title
        self.canvas = None  # Will hold the canvas for drawing
        self.hours = [f"{h:02}" for h in range(24)]  # Labels for the 24 hours
        self.bar_width = 17  # Width of each bar in the histogram
        self.bar_spacing = 7  # Spacing between bars
        self.graph_height = 400  # Height of the histogram graph
        self.color = ['#b1ff87',  '#1f8710', '#ff6a6a', '#cf1313']  # Colors for bars and outlines
        self.graph_width = ((self.bar_width + self.bar_spacing) * len(self.hours) * 2) - 124  # Width of the graph
        self.canvas_width = self.graph_width + 100  # Add padding for centering
        self.canvas_height = self.graph_height + 120  # Height of the canvas including padding

    def setup_window(self):
        """
        Sets up the Tkinter window and canvas for the histogram.
        """
        # Center the window on the screen
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x_position = (screen_width - self.canvas_width) // 2
        y_position = (screen_height - self.canvas_height) // 2
        self.root.geometry(f"{self.canvas_width - 50}x{self.canvas_height}+{x_position}+{y_position}")
        self.root.resizable(False, False)  # Disable resizing

        # Create and pack the canvas
        self.canvas = tk.Canvas(self.root, width=self.canvas_width, height=self.canvas_height, bg="white")
        self.canvas.pack()
        # Setup logic for the window and canvas

    def draw_histogram(self):
        """
        Draws the histogram with axes, labels, and bars.
        """
        elm_road_data = self.traffic_data[0]  # Data for Elm Avenue/Rabbit Road
        hanley_road_data = self.traffic_data[1]  # Data for Hanley Highway/Westway
        max_value = max(max(elm_road_data), max(hanley_road_data))  # Find the maximum traffic count
        scale_factor = self.graph_height / (max_value + 5)  # Scaling factor for bar heights

        # Calculate starting x position to center the graph
        x_offset = (self.canvas_width - self.graph_width) // 2

        # Draw baseline
        self.canvas.create_line(
            x_offset - 5, self.graph_height + 61,
                      x_offset + self.graph_width - 45, self.graph_height + 61,
            fill="black", width=2
        )

        # Function to draw bars and add values
        def draw_bar(x, y, height, fill_color, color, value):
            self.canvas.create_rectangle(x, y, x + self.bar_width, y - height, fill=fill_color, outline=color)
            self.canvas.create_text(x + 1 + self.bar_width // 2, y - height - 6, text=str(value), font=("Arial", 8),
                                    fill=color)

        # Draw the bars for both roads
        for i, (elm, hanley) in enumerate(zip(elm_road_data, hanley_road_data)):
            x_elm = x_offset + i * (2 * self.bar_width + self.bar_spacing)
            x_hanley = x_elm + self.bar_width
            draw_bar(x_elm, self.graph_height + 60, elm * scale_factor, self.color[0], self.color[1], elm)  # Elm Avenue/Rabbit Road
            draw_bar(x_hanley, self.graph_height + 60, hanley * scale_factor, self.color[2], self.color[3], hanley)  # Hanley Highway/Westway

        # Add x-axis labels
        for i, hour in enumerate(self.hours):
            x_label = x_offset + i * (2 * self.bar_width + self.bar_spacing) + self.bar_width // 2 + 8
            self.canvas.create_text(x_label, self.graph_height + 64, text=hour, font=("Arial", 8), anchor=tk.N)

        self.canvas.create_text(x_offset + 425, self.graph_height + 90, text="Hours 00:00 to 24:00", anchor=tk.W, font=("Arial", 10))

    def add_legend(self):
        """
        Adds a legend to the histogram to indicate which bar corresponds to which junction.
        """
        x_offset = (self.canvas_width - self.graph_width) // 2
        self.canvas.create_text(x_offset + 240, 20, text=f"Histogram of Vehicle Frequency per Hour ({self.date})",
                                font=("Arial", 15))
        self.canvas.create_rectangle(x_offset, 40, x_offset + 20, 60, fill=self.color[0], outline=self.color[1])
        self.canvas.create_text(x_offset + 30, 50, text="Elm Avenue/Rabbit Road", anchor=tk.W, font=("Arial", 10))
        self.canvas.create_rectangle(x_offset, 70, x_offset + 20, 90, fill=self.color[2], outline=self.color[3])
        self.canvas.create_text(x_offset + 30, 80, text="Hanley Highway/Westway", anchor=tk.W, font=("Arial", 10))

    def run(self):
        """
        Runs the Tkinter main loop to display the histogram.
        """
        self.setup_window()  # Setup the window and canvas
        self.draw_histogram()  # Draw the histogram
        self.add_legend()  # Add the legend
        self.root.mainloop()  # Start the Tkinter event loop


# Task E: Code Loops to Handle Multiple CSV Files
class MultiCSVProcessor:
    def __init__(self):
        """
        Initializes the application for processing multiple CSV files.
        """
        self.data = []  # Holds the raw data from the CSV file
        self.current_data = None  # Processed data for the current file
        self.file_path = None  # Path of the current CSV file
        self.date = None  # Date associated with the current file

    def load_csv_file(self, file_path):
        """
        Loads a CSV file and processes its data.
        """
        with open(file_path, 'r') as csv_file:
            file = csv_file.read().splitlines()
            for line in file:
                self.data.append(line.split(','))

        hanley_highway = {f"{x:02}": 0 for x in range(24)}  # Initialize hourly data for Hanley Highway
        elm_avenue = hanley_highway.copy()  # Initialize hourly data for Elm Avenue

        for T0 in range(3):  # Process hours
            for T1 in range(10):
                hour = str(T0) + str(T1)
                if int(hour) > 23:  # Stop if the hour exceeds 23
                    break
                for row in self.data[1:]:  # Skip header row
                    if row[0] == 'Hanley Highway/Westway':
                        if row[2].startswith(hour):  # Match the hour prefix
                            hanley_highway[hour] += 1
                    else:
                        if row[2].startswith(hour):  # Match the hour prefix
                            elm_avenue[hour] += 1

        self.current_data = [list(elm_avenue.values()), list(hanley_highway.values())]

    def clear_previous_data(self):
        """
        Clears data from the previous run to process a new dataset.
        """
        self.data = []  # Clear raw data
        self.current_data = None  # Clear processed data
        self.file_path = None  # Clear file path
        self.date = None  # Clear associated date

    def handle_user_interaction(self):
        """
        Handles user input for processing multiple files.
        """
        data = csv.validate_date_input()  # Prompt user for date input
        self.file_path = f'traffic_data{data[0]}{data[1]}{data[2]}.csv'  # Generate file path
        self.date = f'{data[0]}/{data[1]}/{data[2]}'  # Format the date

    def process_files(self):
        """
        Main loop for handling multiple CSV files until the user decides to quit.
        """
        while True:
            print('')  # Blank line for better formatting
            self.handle_user_interaction()
            outcome = csv.process_csv_data(self.file_path)  # Process the file
            if outcome == -1:  # Handle file not found
                continue
            elif outcome != 0:  # Handle other outcomes
                csv.display_outcomes(outcome)  # Display outcomes
                csv.save_results_to_file(outcome)  # Save results to file
                self.load_csv_file(self.file_path)  # Load the CSV file
                histogram = HistogramApp(self.current_data, self.date)  # Create a histogram
                histogram.run()  # Display the histogram
            if csv.validate_continue_input() == 'n':  # Check if the user wants to exit
                print('End of run')  # Print exit message
                break
            self.clear_previous_data()  # Clear previous data for the next run


# run = MultiCSVProcessor()
# run.process_files()
