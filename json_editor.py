import json
import tkinter as tk
from tkinter import ttk, messagebox, filedialog

JSON_FILE = "mods.json"
FIELDS = ["name", "url", "icon", "current", "mod_version", "game_version"]

class JSONEditor(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("JSON Mod Editor")
        self.geometry("1200x600")

        # Toolbar
        toolbar = tk.Frame(self)
        toolbar.pack(fill=tk.X, padx=5, pady=5)

        tk.Button(toolbar, text="Open JSON", command=self.load_json).pack(side=tk.LEFT, padx=2)
        tk.Button(toolbar, text="Save JSON", command=self.save_json).pack(side=tk.LEFT, padx=2)
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

        self.load_json()
        self.tree.bind("<Double-1>", self.edit_cell)

    def load_json(self):
        path = filedialog.askopenfilename(initialfile=JSON_FILE, filetypes=[("JSON files", "*.json")])
        if not path:
            return

        for row in self.tree.get_children():
            self.tree.delete(row)

        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to read JSON: {e}")
            return

        for mod in data:
            row = [mod.get(f, "") for f in FIELDS]
            # Normalize boolean to text
            row[FIELDS.index("current")] = str(mod.get("current", False)).lower()
            self.tree.insert("", "end", values=row)

        self.json_path = path

    def save_json(self):
        if not hasattr(self, "json_path"):
            messagebox.showerror("Error", "No file loaded.")
            return

        rows = [self.tree.item(item)["values"] for item in self.tree.get_children()]
        mods = []
        for r in rows:
            mod = {f: r[i] for i, f in enumerate(FIELDS)}
            # Convert 'current' field to boolean
            mod["current"] = str(mod["current"]).strip().lower() == "true"
            mods.append(mod)

        try:
            with open(self.json_path, "w", encoding="utf-8") as f:
                json.dump(mods, f, indent=4, ensure_ascii=False)
            messagebox.showinfo("Saved", f"Saved {len(mods)} entries to {self.json_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to write JSON: {e}")

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
    app = JSONEditor()
    app.mainloop()