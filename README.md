# Traffic Data Control System

This project is developed as part of the coursework. It provides an interface to process traffic data, extract meaningful insights, and visualize hourly traffic patterns using Python.

---

## ✅ Objective

The objective of this project is to read traffic data from a CSV file based on a user-specified date, compute specific statistics, display the results, and generate a graphical histogram of hourly traffic data from two junctions.

---

## 🧪 Features Implemented

- 📅 **Date Validation**: Ensures correct date format and logical accuracy.
- 📊 **Data Analysis**:
  - Total vehicle counts
  - Truck and electric vehicle breakdowns
  - Over-speeding incidents
  - Junction-specific counts
  - Hours with rainfall
- 💾 **Saving Results**: Stores all outputs in `results.txt`
- 📈 **Graphical Output**: Displays a histogram comparing hourly traffic at:
  - Elm Avenue / Rabbit Road
  - Hanley Highway / Westway
- 🔁 **Loop Control**: Allows continuous analysis for different dates.

---

## 🔧 How to Run

1. Ensure Python 3 is installed on your system.
2. Tkinter (usually comes pre-installed with Python)
3. Place all `.csv` files and Python scripts in the same directory.
4. Open terminal/command prompt and run:

```bash
python main.py
