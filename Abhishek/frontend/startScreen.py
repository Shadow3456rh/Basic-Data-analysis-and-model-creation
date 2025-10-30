import sys

sys.path.append("./")

import tkinter as tk
from tkinter import filedialog, messagebox, ttk

import pandas as pd
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

import modeltraining as train
import plots as plot

# Global variables
df = None
canvas = None

# ------------------- MAIN WINDOW -------------------

root = tk.Tk()
root.title("📊 Data Visualization & Model Trainer")
root.configure(bg="black")

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
root.geometry(f"{screen_width}x{screen_height - 50}")

# --- Plot Display Frame ---
plot_frame = tk.Frame(root, bg="white")
plot_frame.pack(fill="both", expand=True, padx=20, pady=10)


# ------------------- FUNCTIONS -------------------


def load_csv_file():
    """Load a CSV file and populate dropdowns"""
    global df
    file_path = filedialog.askopenfilename(
        title="Select a CSV file", filetypes=[("CSV files", "*.csv")]
    )

    if file_path:
        try:
            df = plot.load_dataset(file_path)
            messagebox.showinfo("Success", "✅ CSV file loaded successfully!")

            numeric_cols = df.select_dtypes(include="number").columns.tolist()
            all_cols = df.columns.tolist()

            # Update dropdowns
            x_menu["values"] = numeric_cols
            y_menu["values"] = numeric_cols
            target_menu["values"] = all_cols

            x_menu.set("")
            y_menu.set("")
            target_menu.set("")

        except Exception as e:
            messagebox.showerror("Error", f"❌ Failed to load CSV:\n{e}")
    else:
        print("⚠️ No file selected")


def show_plot(fig):
    """Display matplotlib figure inside Tkinter frame"""
    global canvas
    if canvas:
        canvas.get_tk_widget().destroy()
    canvas = FigureCanvasTkAgg(fig, master=plot_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(fill="both", expand=True)


def generate_plot():
    """Generate and display selected plot"""
    global df
    if df is None:
        messagebox.showwarning("Warning", "Please load a CSV first!")
        return

    plot_type = plot_choice.get()

    try:
        if plot_type == "Scatterplot":
            x, y = x_menu.get(), y_menu.get()
            if not x or not y:
                messagebox.showwarning("Warning", "Select both X and Y columns!")
                return
            fig = plot.scatterplot(x, y)
        elif plot_type == "Histogram":
            fig = plot.histogram()
        elif plot_type == "Correlation Heatmap":
            fig = plot.corr_heatmap()
        elif plot_type == "Pair Plot":
            fig = plot.pair_plots()
        else:
            messagebox.showerror("Error", "Invalid plot type selected.")
            return

        if fig:
            show_plot(fig)

    except Exception as e:
        messagebox.showerror("Error", f"❌ Plot generation failed:\n{e}")


def clear_plot():
    """Clear current plot"""
    global canvas
    if canvas:
        canvas.get_tk_widget().destroy()
        canvas = None
        messagebox.showinfo("Cleared", "Plot cleared.")


def train_model():
    """Train models and show results"""
    global df
    if df is None:
        messagebox.showwarning("Warning", "Please load a dataset first!")
        return

    target = target_menu.get()
    if not target:
        messagebox.showwarning("Warning", "Please select a target column!")
        return

    model_type = model_choice.get()

    try:
        x_train, x_test, y_train, y_test, scaler = train.data_preprocessing(df, target)

        if model_type == "Classification":
            results = train.classification_algorithm(x_train, x_test, y_train, y_test)
            show_results(results, ["Model", "Accuracy", "Precision", "Recall"])
        else:
            results = train.regression_algorithm(x_train, x_test, y_train, y_test)
            show_results(results, ["Model", "MSE", "R²"])

    except Exception as e:
        messagebox.showerror("Error", f"❌ Training failed:\n{e}")


def show_results(results, columns):
    """Display training results in a table"""
    result_window = tk.Toplevel(root)
    result_window.title("📈 Model Results")
    result_window.geometry("600x400")

    tree = ttk.Treeview(result_window, columns=columns, show="headings")
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=150, anchor="center")
    tree.pack(fill="both", expand=True)

    for res in results:
        if "accuracy" in res:
            tree.insert(
                "",
                "end",
                values=(
                    res["model_name"],
                    f"{res['accuracy']:.2f}",
                    f"{res['precision']:.2f}",
                    f"{res['recall']:.2f}",
                ),
            )
        else:
            tree.insert(
                "",
                "end",
                values=(
                    res["model_name"],
                    f"{res['MSE']:.4f}",
                    f"{res['R2']:.4f}",
                ),
            )


# ------------------- UI COMPONENTS -------------------

# Top Frame
top_frame = tk.Frame(root, bg="black")
top_frame.pack(pady=10, fill="x")

load_btn = ttk.Button(top_frame, text="📂 Load CSV File", command=load_csv_file)
load_btn.pack(side="left", padx=20, pady=10)

clear_btn = ttk.Button(top_frame, text="🧹 Clear Plot", command=clear_plot)
clear_btn.pack(side="left", padx=10, pady=10)

# Plot Options
options_frame = tk.LabelFrame(
    root, text="📊 Plot Options", bg="black", fg="white", padx=10, pady=10
)
options_frame.pack(fill="x", padx=20, pady=10)

tk.Label(options_frame, text="Plot Type:", bg="black", fg="white").grid(row=0, column=0)
plot_choice = ttk.Combobox(
    options_frame,
    values=["Scatterplot", "Histogram", "Correlation Heatmap", "Pair Plot"],
    state="readonly",
)
plot_choice.current(0)
plot_choice.grid(row=0, column=1, padx=10, pady=5)

tk.Label(options_frame, text="X-axis:", bg="black", fg="white").grid(row=1, column=0)
x_menu = ttk.Combobox(options_frame, state="readonly")
x_menu.grid(row=1, column=1, padx=10, pady=5)

tk.Label(options_frame, text="Y-axis:", bg="black", fg="white").grid(row=2, column=0)
y_menu = ttk.Combobox(options_frame, state="readonly")
y_menu.grid(row=2, column=1, padx=10, pady=5)

generate_btn = ttk.Button(options_frame, text="🎨 Generate Plot", command=generate_plot)
generate_btn.grid(row=3, column=1, pady=10)

# Training Section
train_frame = tk.LabelFrame(
    root, text="🤖 Model Training", bg="black", fg="white", padx=10, pady=10
)
train_frame.pack(fill="x", padx=20, pady=10)

tk.Label(train_frame, text="Target Column:", bg="black", fg="white").grid(
    row=0, column=0
)
target_menu = ttk.Combobox(train_frame, state="readonly")
target_menu.grid(row=0, column=1, padx=10, pady=5)

tk.Label(train_frame, text="Model Type:", bg="black", fg="white").grid(row=1, column=0)
model_choice = ttk.Combobox(
    train_frame, values=["Classification", "Regression"], state="readonly"
)
model_choice.current(0)
model_choice.grid(row=1, column=1, padx=10, pady=5)

train_btn = ttk.Button(train_frame, text="🚀 Train Model", command=train_model)
train_btn.grid(row=2, column=1, pady=10)

root.mainloop()
