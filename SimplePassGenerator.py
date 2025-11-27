import tkinter as tk
from tkinter import ttk, filedialog, messagebox

def generate_variants(seed):
    seed_lower = seed.lower()
    seed_upper = seed.upper()
    seed_title = seed.capitalize()

    symbols = ["!", "@", "#", "$", "_", "-", "."]
    numbers = ["1", "12", "123", "01", "001", "2024", "2025"]

    # Leetspeak replacements
    leet_map = {
        "a": "4",
        "e": "3",
        "i": "1",
        "o": "0",
        "s": "5",
    }

    def leetspeak(word):
        return "".join(leet_map.get(c, c) for c in word)

    variants = set()

    base_forms = [seed_lower, seed_upper, seed_title, leetspeak(seed_lower)]

    for base in base_forms:
        # Basic forms
        variants.add(base)

        # Base + numbers
        for num in numbers:
            variants.add(base + num)

        # Base + symbol
        for sym in symbols:
            variants.add(base + sym)

        # Base + symbol + number
        for sym in symbols:
            for num in numbers:
                variants.add(base + sym + num)

        # Symbol + base + number
        for sym in symbols:
            for num in numbers:
                variants.add(sym + base + num)

    return sorted(variants)


def gui_generate():
    seed = seed_entry.get().strip()

    if not seed:
        messagebox.showerror("Error", "Please enter a seed word.")
        return

    variants = generate_variants(seed)

    filename = filedialog.asksaveasfilename(defaultextension=".txt")
    if not filename:
        return

    with open(filename, "w") as f:
        f.write("\n".join(variants))

    messagebox.showinfo("Done", f"Generated {len(variants)} password variants!")


# GUI
window = tk.Tk()
window.title("Simple Password Variant Generator")
window.geometry("350x200")

ttk.Label(window, text="Enter base word / seed:").pack(pady=5)
seed_entry = ttk.Entry(window, width=30)
seed_entry.pack()

ttk.Button(window, text="Generate Variants", command=gui_generate).pack(pady=20)

window.mainloop()
