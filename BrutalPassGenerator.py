import itertools
import string
import random
import os
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from tqdm import tqdm


# ============================================================
# CORE PASSWORD GENERATION FUNCTIONS
# ============================================================

def build_charset(upper, lower, digits, symbols):
    chars = ""
    if upper: chars += string.ascii_uppercase
    if lower: chars += string.ascii_lowercase
    if digits: chars += string.digits
    if symbols: chars += "!@#$%^&*()-_=+[]{};:,.<>/?"
    return chars


def warn_large_output(chars, max_len):
    return sum(len(chars) ** i for i in range(1, max_len + 1))


def generate_all_combos(seed, chars, max_len, filename):
    total = warn_large_output(chars, max_len)

    with open(filename, "w") as f:
        for length in range(1, max_len + 1):
            for combo in tqdm(itertools.product(chars, repeat=length),
                              total=len(chars)**length,
                              desc=f"Length {length}"):
                f.write(seed + "".join(combo) + "\n")

    print(f"\n✔ Saved to {filename}")


def generate_random(seed, chars, count, length_min, length_max, filename):
    with open(filename, "w") as f:
        for _ in tqdm(range(count), desc="Generating random passwords"):
            length = random.randint(length_min, length_max)
            password = seed + "".join(random.choice(chars) for _ in range(length))
            f.write(password + "\n")

    print(f"\n✔ Saved to {filename}")


# ============================================================
# GUI MODE (Tkinter)
# ============================================================

def gui_generate():
    seed = seed_entry.get()
    upper = upper_var.get()
    lower = lower_var.get()
    digits = digits_var.get()
    symbols = symbols_var.get()
    chars = build_charset(upper, lower, digits, symbols)

    if not chars:
        messagebox.showerror("Error", "Select at least one character set.")
        return

    filename = filedialog.asksaveasfilename(defaultextension=".txt")

    if not filename:
        return

    if mode_var.get() == 1:
        max_len = int(max_len_entry.get())
        total = warn_large_output(chars, max_len)

        if total > 5_000_000:
            messagebox.showwarning(
                "Warning",
                "Output too large. Automatically limiting to ~5 million passwords."
            )
            max_len = 3

        generate_all_combos(seed, chars, max_len, filename)

    else:
        count = int(random_count_entry.get())
        length_min = int(random_min_entry.get())
        length_max = int(random_max_entry.get())

        generate_random(seed, chars, count, length_min, length_max, filename)

    messagebox.showinfo("Done", "Passwords generated!")


def gui_mode():
    global seed_entry, upper_var, lower_var, digits_var, symbols_var
    global mode_var, max_len_entry, random_count_entry, random_min_entry, random_max_entry

    window = tk.Tk()
    window.title("Password Generator Tool")
    window.geometry("380x500")

    ttk.Label(window, text="Base Word / Seed").pack()
    seed_entry = ttk.Entry(window)
    seed_entry.pack()

    ttk.Label(window, text="\nCharacter Sets").pack()
    upper_var = tk.BooleanVar(value=True)
    lower_var = tk.BooleanVar(value=True)
    digits_var = tk.BooleanVar(value=True)
    symbols_var = tk.BooleanVar(value=True)

    ttk.Checkbutton(window, text="Uppercase", variable=upper_var).pack()
    ttk.Checkbutton(window, text="Lowercase", variable=lower_var).pack()
    ttk.Checkbutton(window, text="Digits", variable=digits_var).pack()
    ttk.Checkbutton(window, text="Symbols", variable=symbols_var).pack()

    ttk.Label(window, text="\nMode").pack()
    mode_var = tk.IntVar(value=1)
    ttk.Radiobutton(window, text="All combinations", variable=mode_var, value=1).pack()
    ttk.Radiobutton(window, text="Random passwords", variable=mode_var, value=2).pack()

    ttk.Label(window, text="Max appended length").pack()
    max_len_entry = ttk.Entry(window)
    max_len_entry.insert(0, "2")
    max_len_entry.pack()

    ttk.Label(window, text="Random count").pack()
    random_count_entry = ttk.Entry(window)
    random_count_entry.insert(0, "1000")
    random_count_entry.pack()

    ttk.Label(window, text="Random min length").pack()
    random_min_entry = ttk.Entry(window)
    random_min_entry.insert(0, "4")
    random_min_entry.pack()

    ttk.Label(window, text="Random max length").pack()
    random_max_entry = ttk.Entry(window)
    random_max_entry.insert(0, "12")
    random_max_entry.pack()

    ttk.Button(window, text="Generate", command=gui_generate).pack()

    window.mainloop()


# ============================================================
# ENTRY POINT
# ============================================================

if __name__ == "__main__":
    # GUI mode is now the default
    gui_mode()

