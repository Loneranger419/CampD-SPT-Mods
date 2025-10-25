import csv
import tkinter as tk
from tkinter import ttk, messagebox, filedialog

CSV_FILE = "mods.csv"
FIELDS = ["name", "url", "icon", "current", "mod_version", "game_version"]

class CSVEditor(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("CSV Mod Editor")
        self.geometry("1200x600")

        # Toolbar
        toolbar = tk.Frame(self)
        toolbar.pack(fill=tk.X, padx=5, pady=5)

        tk.Button(toolbar, text="Open CSV", command=self.load_csv).pack(side=tk.LEFT, padx=2)
        tk.Button(toolbar, text="Save CSV", command=self.save_csv).pack(side=tk.LEFT, padx=2)
        tk.Button(toolbar, text="Add Row", command=self.add_row).pack(side=tk.LEFT, padx=2)
        tk.Button(toolbar, text="Delete Selected", command=self.delete_row).pack(side=tk.LEFT, padx=2)

        # Table
        self.tree = ttk.Treeview(self, columns=FIELDS, show="headings")
        for field in FIELDS:
            self.tree.heading(field, text=field)
            self.tree.column(field, width=180, anchor="w")

        vsb = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        hsb = ttk.Scrollbar(self, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscroll=vsb.set, xscroll=hsb.set)

        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        vsb.pack(side=tk.RIGHT, fill=tk.Y)
        hsb.pack(side=tk.BOTTOM, fill=tk.X)

        self.load_csv()
        self.tree.bind("<Double-1>", self.edit_cell)

    def load_csv(self):
        path = CSV_FILE


        # Clear existing rows
        for row in self.tree.get_children():
            self.tree.delete(row)

        # Load CSV safely
        with open(path, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            # Normalize headers: remove BOM, lowercase, trim
            field_map = {h.strip().replace('\ufeff', '').lower(): h for h in reader.fieldnames}
            for row in reader:
                clean = {}
                for field in FIELDS:
                    source = field_map.get(field)
                    clean[field] = row.get(source, "") if source else ""
                self.tree.insert("", "end", values=[clean[f] for f in FIELDS])

        self.csv_path = path

    def save_csv(self):
        if not hasattr(self, "csv_path"):
            messagebox.showerror("Error", "No file loaded.")
            return

        rows = [self.tree.item(item)["values"] for item in self.tree.get_children()]

        with open(self.csv_path, "w", newline='', encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(FIELDS)
            writer.writerows(rows)

        messagebox.showinfo("Saved", f"Saved {len(rows)} rows to {self.csv_path}")

    def add_row(self):
        self.tree.insert("", "end", values=[""] * len(FIELDS))

    def delete_row(self):
        for sel in self.tree.selection():
            self.tree.delete(sel)

    def edit_cell(self, event):
        item = self.tree.identify_row(event.y)
        column = self.tree.identify_column(event.x)
        if not item or not column:
            return

        col_index = int(column[1:]) - 1
        x, y, width, height = self.tree.bbox(item, column)
        value = self.tree.set(item, FIELDS[col_index])

        entry = tk.Entry(self.tree)
        entry.place(x=x, y=y, width=width, height=height)
        entry.insert(0, value)
        entry.focus()

        def save_edit(event):
            self.tree.set(item, FIELDS[col_index], entry.get())
            entry.destroy()

        entry.bind("<Return>", save_edit)
        entry.bind("<FocusOut>", lambda e: entry.destroy())

if __name__ == "__main__":
    app = CSVEditor()
    app.mainloop()