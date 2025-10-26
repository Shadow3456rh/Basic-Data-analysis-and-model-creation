import tkinter as tk

frame1 = tk.Frame(bg="lightblue")

label = tk.Label(frame1, text="Screen 1", font=("Arial", 18))
label.pack(pady=50)


# The function to raise frame2
def go_to_screen2():
    from startScreen import root

    root.tkraise()


button = tk.Button(frame1, text="Go to Screen 2", command=go_to_screen2)
button.pack()
