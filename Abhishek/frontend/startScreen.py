import sys

sys.path.append("./")
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

import plots as plot  # your plots.py file
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

df = None
canvas = None


def load_csv_file():
    global df
    file_path = filedialog.askopenfilename(
        title="Select a CSV file", filetypes=[("CSV files", "*.csv")]
    )

    if file_path:
        try:
            df = plot.load_dataset(file_path)
            print("✅ File loaded successfully")
            messagebox.showinfo("Success", "CSV file loaded successfully!")

            # Populate column dropdowns
            x_menu["values"] = df.columns.tolist()
            y_menu["values"] = df.columns.tolist()
        except Exception as e:
            print(f"Error loading CSV: {e}")
            messagebox.showerror("Error", f"Failed to load CSV: {e}")
    else:
        print("⚠️ No file selected")


def show_plot(fig):
    global canvas
    if canvas:
        canvas.get_tk_widget().destroy()

    canvas = FigureCanvasTkAgg(fig, master=plot_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(fill="both", expand=True)


def generate_plot():
    global df
    if df is None:
        messagebox.showwarning("Warning", "Please load a CSV first!")
        return

    plot_type = plot_choice.get()

    if plot_type == "Scatterplot":
        x = x_menu.get()
        y = y_menu.get()
        if not x or not y:
            messagebox.showwarning("Warning", "Select both X and Y columns!")
            return
        fig = plot.scatterplot(x, y)
        show_plot(fig)

    elif plot_type == "Histogram":
        fig = plot.histogram()
        show_plot(fig)

    elif plot_type == "Correlation Heatmap":
        fig = plot.corr_heatmap()
        show_plot(fig)

    elif plot_type == "Pair Plot":
        fig = plot.pair_plots()
        show_plot(fig)
    else:
        messagebox.showerror("Error", "Invalid plot type selected.")


root = tk.Tk()
root.title("Data Visualization Tool")
root.configure(bg="black")

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
root.geometry(f"{screen_width}x{screen_height - 50}")

top_frame = tk.Frame(root, bg="black")
top_frame.pack(pady=10, fill="x")

load_btn = ttk.Button(top_frame, text="📂 Load CSV File", command=load_csv_file)
load_btn.pack(side="left", padx=20, pady=10)

options_frame = tk.LabelFrame(
    root, text="Plot Options", bg="black", fg="white", padx=10, pady=10
)
options_frame.pack(fill="x", padx=20, pady=10)

plot_choice = ttk.Combobox(
    options_frame,
    values=["Scatterplot", "Histogram", "Correlation Heatmap", "Pair Plot"],
    state="readonly",
)
plot_choice.current(0)
plot_choice.grid(row=0, column=1, padx=10, pady=5)
tk.Label(options_frame, text="Plot Type:", bg="black", fg="white").grid(row=0, column=0)

tk.Label(options_frame, text="X-axis:", bg="black", fg="white").grid(row=1, column=0)
x_menu = ttk.Combobox(options_frame, state="readonly")
x_menu.grid(row=1, column=1, padx=10, pady=5)

tk.Label(options_frame, text="Y-axis:", bg="black", fg="white").grid(row=2, column=0)
y_menu = ttk.Combobox(options_frame, state="readonly")
y_menu.grid(row=2, column=1, padx=10, pady=5)

generate_btn = ttk.Button(options_frame, text="🎨 Generate Plot", command=generate_plot)
generate_btn.grid(row=3, column=1, pady=10)

plot_frame = tk.Frame(root, bg="white")
plot_frame.pack(fill="both", expand=True, padx=20, pady=10)

root.mainloop()
