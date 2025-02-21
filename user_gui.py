import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from datetime import datetime
from tkcalendar import Calendar




def calculate_days_from_2017(date_str):
    """Calculate days passed from 01/01/2017."""
    start_date = datetime(2017, 1, 1)
    selected_date = datetime.strptime(date_str, "%Y-%m-%d")
    return (selected_date - start_date).days

def submit():
    """Handle form submission."""
    try:
        global usd_min, usd_max, rating_min, rating_max, start_days, end_days
        # Get range inputs for 100g_USD (as float)
        usd_min = usd_min_var.get()  # This will be a float
        usd_max = usd_max_var.get()  # This will be a float
        if not (0 <= usd_min <= usd_max <= 140):
            raise ValueError("100g_USD range must be between 0 and 20.")
        
        # Get range inputs for rating (as int)
        rating_min = rating_min_var.get()  # This will be an int
        rating_max = rating_max_var.get()  # This will be an int
        if not (0 <= rating_min <= rating_max <= 100):
            raise ValueError("Rating range must be between 0 and 100.")
        
        # Get date range and convert to days (as int)
        start_date = start_date_var.get()  # This will be a string in "YYYY-MM-DD" format
        end_date = end_date_var.get()  # This will be a string in "YYYY-MM-DD" format
        start_days = calculate_days_from_2017(start_date)  # Convert to days as integer
        end_days = calculate_days_from_2017(end_date)  # Convert to days as integer
        if start_days > end_days:
            raise ValueError("Start date must be earlier than end date.")
        
        # Get maximum capacity (as int)
        max_capacity = capacity_var.get()  # This will be an int
        if not (0 <= max_capacity <= 20):
            raise ValueError("Maximum capacity must be between 0 and 20.")
        
        # Display results or save them for further processing
        messagebox.showinfo("Submission Successful", 
                            f"Inputs received:\n"
                            f"100g_USD: {usd_min} to {usd_max}\n"
                            f"Date Range (Days from 01/01/2017): {start_days} to {end_days}\n"
                            f"Rating: {rating_min} to {rating_max}\n"
                            f"Max Capacity: {max_capacity}")
        
        # Print to console or further processing
        print(f"Inputs received: 100g_USD=[{usd_min}, {usd_max}], "
              f"Days=[{start_days}, {end_days}], "
              f"Rating=[{rating_min}, {rating_max}], Max Capacity={max_capacity}")
        
    except Exception as e:
        messagebox.showerror("Error", str(e))

def pick_start_date():
    """Open a calendar to select the start date."""
    def set_date():
        start_date_var.set(cal.selection_get().strftime("%Y-%m-%d"))
        cal_window.destroy()
    
    cal_window = tk.Toplevel(root)
    cal = Calendar(cal_window, date_pattern="yyyy-mm-dd", mindate=datetime(2017, 1, 1))
    cal.pack(pady=20)
    ttk.Button(cal_window, text="Select", command=set_date).pack()

def pick_end_date():
    """Open a calendar to select the end date."""
    def set_date():
        end_date_var.set(cal.selection_get().strftime("%Y-%m-%d"))
        cal_window.destroy()
    
    cal_window = tk.Toplevel(root)
    cal = Calendar(cal_window, date_pattern="yyyy-mm-dd", mindate=datetime(2017, 1, 1))
    cal.pack(pady=20)
    ttk.Button(cal_window, text="Select", command=set_date).pack()

# Create the main window
root = tk.Tk()
root.title("Octree Range Input Form")
root.geometry("400x450")

# Variables to hold the inputs with proper types
usd_min_var = tk.DoubleVar()
usd_max_var = tk.DoubleVar()
start_date_var = tk.StringVar()
end_date_var = tk.StringVar()
rating_min_var = tk.IntVar()
rating_max_var = tk.IntVar()
capacity_var = tk.IntVar()

# Create input fields
ttk.Label(root, text="100g_USD Range (0-20):").pack(pady=5)
frame_usd = ttk.Frame(root)
frame_usd.pack(pady=5)
ttk.Entry(frame_usd, textvariable=usd_min_var, width=10).pack(side="left", padx=5)
ttk.Label(frame_usd, text="to").pack(side="left")
ttk.Entry(frame_usd, textvariable=usd_max_var, width=10).pack(side="left", padx=5)

ttk.Label(root, text="Review Date Range:").pack(pady=5)
frame_date = ttk.Frame(root)
frame_date.pack(pady=5)
ttk.Entry(frame_date, textvariable=start_date_var, width=15).pack(side="left", padx=5)
ttk.Button(frame_date, text="Pick Start Date", command=pick_start_date).pack(side="left", padx=5)
ttk.Entry(frame_date, textvariable=end_date_var, width=15).pack(side="left", padx=5)
ttk.Button(frame_date, text="Pick End Date", command=pick_end_date).pack(side="left", padx=5)

ttk.Label(root, text="Rating Range (0-100):").pack(pady=5)
frame_rating = ttk.Frame(root)
frame_rating.pack(pady=5)
ttk.Entry(frame_rating, textvariable=rating_min_var, width=10).pack(side="left", padx=5)
ttk.Label(frame_rating, text="to").pack(side="left")
ttk.Entry(frame_rating, textvariable=rating_max_var, width=10).pack(side="left", padx=5)

ttk.Label(root, text="Maximum Capacity (0-20):").pack(pady=5)
ttk.Entry(root, textvariable=capacity_var).pack(pady=5)

# Submit button
ttk.Button(root, text="Submit", command=submit).pack(pady=20)

# Run the application
root.mainloop()
