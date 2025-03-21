import os
import tkinter as tk
from tkinter import ttk, messagebox, filedialog, simpledialog
import json
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd

# --------------------------
# Commodity Data Definitions
# --------------------------
COMMODITY_CATEGORIES = {
    "Chemicals": ["Agronomic Treatment","Explosives","Hydrogen Fuel","Hydrogen Peroxide","Liquid Oxygen","Mineral Oil","Nerve Agents","Pesticides","Rockforth Fertiliser","Surface Stabilisers","Synthetic Reagents","Tritium","Water"],
    "Consumer Items": ["Clothing","Consumer Technology","Domestic Appliances","Evacuation Shelter","Survival Equipment"],
    "Foods": ["Algae","Animal Meat","Coffee","Fish","Food Cartridges","Fruit and Vegetables","Grain","Synthetic Meat","Tea"],
    "Industrial Materials": ["Ceramic Composites","CMM Composite","Insulating Membrane","Meta-Alloys","Micro-Weave Cooling Hoses","Neofabric Insulation","Polymers","Semiconductors","Superconductors"],
    "Legal Drugs": ["Beer","Bootleg Liquor","Liquor","Narcotics","Onionhead Gamma Strain","Tobacco","Wine"],
    "Machinery": ["Articulation Motors","Atmospheric Processors","Building Fabricators","Crop Harvesters","Emergency Power Cells","Energy Grid Assembly","Exhaust Manifold","Geological Equipment","Heatsink Interlink","HN Shock Mount","Magnetic Emitter Coil","Marine Equipment","Microbial Furnaces","Mineral Extractors","Modular Terminals","Power Converter","Power Generators","Power Transfer Bus","Radiation Baffle","Reinforced Mounting Plate","Skimmer Components","Thermal Cooling Units","Water Purifiers"],
    "Medicines": ["Advanced Medicines","Agri-Medicines","Basic Medicines","Combat Stabilisers","Performance Enhancers","Progenitor Cells"],
    "Metals": ["Aluminium","Beryllium","Bismuth","Cobalt","Copper","Gallium","Gold","Hafnium 178","Indium","Lanthanum","Lithium","Osmium","Palladium","Platinum","Platinum Alloy","Praseodymium","Samarium","Silver","Steel","Tantalum","Thallium","Thorium","Titanium","Uranium"],
    "Minerals": ["Alexandrite","Bauxite","Benitoite","Bertrandite","Bromellite","Coltan","Cryolite","Gallite","Goslarite","Grandidierite","Indite","Jadeite","Lepidolite","Lithium Hydroxide","Low Temperature Diamonds","Methane Clathrate","Methanol Monohydrate Crystals","Moissanite","Monazite","Musgravite","Painite","Pyrophyllite","Rhodplumsite","Rutile","Serendibite","Taaffeite","Uraninite","Void Opals"],
    "Salvage": ["AI Relics","Ancient Artefact","Ancient Key","Anomaly Particles","Antimatter Containment Unit","Antique Jewellery","Antiquities","Assault Plans","Black Box","Commercial Samples","Damaged Escape Pod","Data Core","Diplomatic Bag","Earth Relics","Encrypted Correspondence","Encrypted Data Storage","Experimental Chemicals","Fossil Remnants","Gene Bank","Geological Samples","Guardian Casket","Guardian Orb","Guardian Relic","Guardian Tablet","Guardian Totem","Guardian Urn","Hostage","Large Survey Data Cache","Military Intelligence","Military Plans","Mollusc Brain Tissue","Mollusc Fluid","Mollusc Membrane","Mollusc Mycelium","Mollusc Soft Tissue","Mollusc Spores","Mysterious Idol","Occupied Escape Pod","Personal Effects","Pod Core Tissue","Pod Dead Tissue","Pod Mesoglea","Pod Outer Tissue","Pod Shell Tissue","Pod Surface Tissue","Pod Tissue","Political Prisoner","Precious Gems","Prohibited Research Materials","Prototype Tech","Rare Artwork","Rebel Transmissions","SAP 8 Core Container","Scientific Research","Scientific Samples","Small Survey Data Cache","Space Pioneer Relics","Tactical Data","Technical Blueprints","Thargoid Basilisk Tissue Sample","Thargoid Biological Matter","Thargoid Bio-Storage Capsule","Thargoid Cyclops Tissue Sample","Thargoid Glaive Tissue Sample","Thargoid Heart","Thargoid Hydra Tissue Sample","Thargoid Link","Thargoid Orthrus Tissue Sample","Thargoid Probe","Thargoid Resin","Thargoid Sensor","Thargoid Medusa Tissue Sample","Thargoid Scout Tissue Sample","Thargoid Technology Samples","Time Capsule","Titan Deep Tissue Sample","Titan Maw Deep Tissue Sample","Titan Maw Partial Tissue Sample","Titan Maw Tissue Sample","Titan Partial Tissue Sample","Titan Tissue Sample","Trade Data","Trinkets of Hidden Fortune","Unclassified Relic","Unoccupied Escape Pod","Unstable Data Core","Wreckage Components"],
    "Slavery": ["Imperial Slaves","Slaves"],
    "Technology": ["Advanced Catalysers","Animal Monitors","Aquaponic Systems","Auto Fabricators","Bioreducing Lichen","Computer Components","H.E. Suits","Hardware Diagnostic Sensor","Ion Distributor","Land Enrichment Systems","Medical Diagnostic Equipment","Micro Controllers","Muon Imager","Nanobreakers","Resonating Separators","Robotics","Structural Regulators","Telemetry Suite"],
    "Textiles": ["Conductive Fabrics","Leather","Military Grade Fabrics","Natural Fabrics","Synthetic Fabrics"],
    "Waste": ["Biowaste","Chemical Waste","Scrap","Toxic Waste"],
    "Weapons": ["Battle Weapons","Landmines","Non Lethal Weapons","Personal Weapons","Reactive Armour"]
}

COMMODITY_LIST = sorted([item for sublist in COMMODITY_CATEGORIES.values() for item in sublist])
COMMODITY_TO_CATEGORY = {commodity: category for category, commodities in COMMODITY_CATEGORIES.items() for commodity in commodities}

# --------------------------
# Themes Definition
# --------------------------
THEMES = {
    "Light": {"bg": "white", "fg": "black", "text_bg": "white"},
    "Dark": {"bg": "#2e2e2e", "fg": "white", "text_bg": "#3e3e3e"},
    "Contrast": {"bg": "black", "fg": "yellow", "text_bg": "black"},
    "Blue": {"bg": "#cce6ff", "fg": "#003366", "text_bg": "white"}
}

# Create profiles folder if not exists.
PROFILES_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "profiles")
if not os.path.exists(PROFILES_DIR):
    os.makedirs(PROFILES_DIR)

# --------------------------
# Main Application Class
# --------------------------
class CommodityTracker(tk.Tk):
    def __init__(self):
        super().__init__()
        # Increase initial width so that controls are fully visible.
        self.title("Elite Dangerous Commodity Tracker")
        self.geometry("950x750")
        # Each tab stores {"tracked": list of dicts, "tree": treeview widget, "name": tab name}
        self.tab_data = {}
        self.current_theme = "Light"
        self.sort_option = tk.StringVar(value="Alphabetical")
        self.listbox_window = None  # For autocomplete Toplevel
        self.create_widgets()
        self.apply_theme()

    def create_widgets(self):
        # --- Top Controls ---
        top_frame = tk.Frame(self)
        top_frame.pack(pady=10, padx=10, fill=tk.X)

        tk.Label(top_frame, text="Commodity:").grid(row=0, column=0, sticky="w")
        self.commodity_entry = tk.Entry(top_frame)
        self.commodity_entry.grid(row=0, column=1, sticky="ew", padx=5)
        self.commodity_entry.bind("<KeyRelease>", self.on_keyrelease)
        self.commodity_entry.bind("<Down>", self.focus_listbox)

        tk.Label(top_frame, text="Target Amount:").grid(row=1, column=0, sticky="w", pady=(10,0))
        self.amount_entry = tk.Entry(top_frame)
        self.amount_entry.grid(row=1, column=1, sticky="ew", padx=5, pady=(10,0))
        self.amount_entry.bind("<Return>", self.add_commodity)

        self.add_button = tk.Button(top_frame, text="Add Commodity", command=self.add_commodity)
        self.add_button.grid(row=0, column=2, rowspan=2, padx=10)

        self.total_remaining_var = tk.StringVar(value="Total Remaining: 0")
        total_label = tk.Label(top_frame, textvariable=self.total_remaining_var, font=("Arial", 16, "bold"))
        total_label.grid(row=0, column=3, rowspan=2, padx=10, sticky="nsew")

        tk.Label(top_frame, text="Theme:").grid(row=0, column=4, padx=(10,0))
        self.theme_var = tk.StringVar(value=self.current_theme)
        theme_options = ttk.Combobox(top_frame, textvariable=self.theme_var, values=list(THEMES.keys()), state="readonly", width=10)
        theme_options.grid(row=0, column=5, padx=(5,10))
        theme_options.bind("<<ComboboxSelected>>", self.change_theme)

        tk.Label(top_frame, text="Sort By:").grid(row=0, column=6, padx=(10,0))
        sort_options = ttk.Combobox(top_frame, textvariable=self.sort_option,
                                    values=["Alphabetical", "Total Amount", "Amount Remaining"],
                                    state="readonly", width=15)
        sort_options.grid(row=0, column=7, padx=(5,10))
        sort_options.bind("<<ComboboxSelected>>", lambda e: self.sort_current_tab())

        self.close_tab_button = tk.Button(top_frame, text="❌ Close Current Tab", fg="red", command=self.close_current_tab)
        self.close_tab_button.grid(row=1, column=6, padx=5, pady=(10,0))
        self.rename_tab_button = tk.Button(top_frame, text="Rename Tab", command=self.rename_current_tab)
        self.rename_tab_button.grid(row=1, column=7, padx=5, pady=(10,0))

        top_frame.columnconfigure(1, weight=1)

        # --- Notebook for Tabs ---
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        self.notebook.bind("<<NotebookTabChanged>>", lambda e: self.update_total_remaining())
        self.create_new_tab(default=True)

        # --- Bottom Controls ---
        bottom_frame = tk.Frame(self)
        bottom_frame.pack(pady=10, padx=10)
        self.export_json_button = tk.Button(bottom_frame, text="Export to JSON", command=self.export_state)
        self.export_json_button.pack(side=tk.LEFT, padx=5)
        self.import_json_button = tk.Button(bottom_frame, text="Import from JSON", command=self.import_state)
        self.import_json_button.pack(side=tk.LEFT, padx=5)
        self.export_excel_button = tk.Button(bottom_frame, text="Export to Excel", command=self.export_to_excel)
        self.export_excel_button.pack(side=tk.LEFT, padx=5)
        self.view_graphs_button = tk.Button(bottom_frame, text="View Graphs", command=self.view_graphs)
        self.view_graphs_button.pack(side=tk.LEFT, padx=5)

    # --------------------------
    # Autocomplete Functions using Toplevel
    # --------------------------
    def on_keyrelease(self, event):
        typed = self.commodity_entry.get().lower()
        if typed == "":
            self.hide_listbox()
            return
        suggestions = [c for c in COMMODITY_LIST if typed in c.lower()]
        if suggestions:
            if self.listbox_window is None or not self.listbox_window.winfo_exists():
                self.listbox_window = tk.Toplevel(self)
                self.listbox_window.overrideredirect(True)
                self.listbox = tk.Listbox(self.listbox_window, height=7)
                self.listbox.pack()
                self.listbox.bind("<<ListboxSelect>>", self.on_listbox_select)
                self.listbox.bind("<Return>", self.on_listbox_select)
                self.listbox.bind("<Escape>", lambda e: self.hide_listbox())
            self.listbox.delete(0, tk.END)
            for s in suggestions:
                self.listbox.insert(tk.END, s)
            x = self.commodity_entry.winfo_rootx()
            y = self.commodity_entry.winfo_rooty() + self.commodity_entry.winfo_height()
            self.listbox_window.geometry(f"+{x}+{y}")
            self.listbox_window.deiconify()
            self.listbox.lift()
        else:
            self.hide_listbox()

    def hide_listbox(self):
        if self.listbox_window and self.listbox_window.winfo_exists():
            self.listbox_window.withdraw()

    def focus_listbox(self, event):
        if self.listbox_window and self.listbox_window.winfo_exists():
            self.listbox.focus_set()
            self.listbox.selection_set(0)

    def on_listbox_select(self, event):
        if self.listbox.curselection():
            index = self.listbox.curselection()[0]
            selected = self.listbox.get(index)
            self.commodity_entry.delete(0, tk.END)
            self.commodity_entry.insert(0, selected)
            self.hide_listbox()
            self.amount_entry.focus_set()

    # --------------------------
    # Tab Management Functions
    # --------------------------
    def create_new_tab(self, default=False):
        tab_frame = tk.Frame(self.notebook)
        tab_index = len(self.notebook.tabs()) + 1
        tab_name = f"List {tab_index}"
        self.notebook.add(tab_frame, text=tab_name)
        # Use a Treeview for the checklist with four columns.
        tree = ttk.Treeview(tab_frame, columns=("Commodity", "Status", "Remaining", "Complete"), show="headings", selectmode="browse")
        tree.heading("Commodity", text="Commodity")
        tree.heading("Status", text="Gathered/Needed")
        tree.heading("Remaining", text="Remaining")
        tree.heading("Complete", text="Complete")
        tree.column("Commodity", width=250)
        tree.column("Status", width=120, anchor="center")
        tree.column("Remaining", width=100, anchor="center")
        tree.column("Complete", width=80, anchor="center")
        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        tree.bind("<Double-1>", self.on_treeview_double_click)
        scrollbar = tk.Scrollbar(tab_frame, command=tree.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        tree.configure(yscrollcommand=scrollbar.set)
        self.tab_data[tab_frame] = {"tracked": [], "tree": tree, "name": tab_name}
        if default:
            self.notebook.select(tab_frame)
        self.update_total_remaining()

    def clear_current_tab(self):
        current_tab = self.get_current_tab()
        if messagebox.askyesno("Clear List", "Are you sure you want to clear this list?"):
            self.tab_data[current_tab]["tracked"] = []
            self.update_tracked_display(current_tab)
            self.update_total_remaining()

    def close_current_tab(self):
        current_tab = self.get_current_tab()
        if len(self.notebook.tabs()) == 1:
            messagebox.showwarning("Close Tab", "Cannot close the only remaining tab.")
            return
        self.notebook.forget(current_tab)
        if current_tab in self.tab_data:
            del self.tab_data[current_tab]
        self.update_total_remaining()

    def rename_current_tab(self):
        current_tab = self.get_current_tab()
        current_name = self.tab_data[current_tab]["name"]
        new_name = simpledialog.askstring("Rename Tab", "Enter new tab name:", initialvalue=current_name)
        if new_name:
            self.tab_data[current_tab]["name"] = new_name
            self.notebook.tab(current_tab, text=new_name)
            profile_data = {
                "tab_name": new_name,
                "theme": self.current_theme
            }
            profile_path = os.path.join(PROFILES_DIR, f"{new_name}.json")
            try:
                with open(profile_path, "w") as pf:
                    json.dump(profile_data, pf, indent=4)
            except Exception as e:
                messagebox.showerror("Profile Save Error", f"Failed to save profile: {e}")

    def get_current_tab(self):
        return self.notebook.nametowidget(self.notebook.select())

    # --------------------------
    # Commodity List Functions (Treeview Checklist)
    # --------------------------
    def add_commodity(self, event=None):
        commodity = self.commodity_entry.get().strip()
        amount_str = self.amount_entry.get().strip()
        if not commodity:
            messagebox.showwarning("Input Error", "Please enter a commodity name.")
            return
        if commodity not in COMMODITY_LIST:
            messagebox.showwarning("Input Error", "Commodity not recognized. Please select a valid commodity from the list.")
            return
        try:
            needed = float(amount_str)
        except ValueError:
            messagebox.showwarning("Input Error", "Please enter a valid numeric target amount.")
            return

        current_tab = self.get_current_tab()
        record = {"commodity": commodity, "needed": needed, "gathered": 0}
        self.tab_data[current_tab]["tracked"].append(record)
        self.sort_current_tab()
        self.update_tracked_display(current_tab)
        self.update_total_remaining()
        self.commodity_entry.delete(0, tk.END)
        self.amount_entry.delete(0, tk.END)
        self.commodity_entry.focus_set()

    def sort_current_tab(self):
        current_tab = self.get_current_tab()
        sort_by = self.sort_option.get()
        tracked = self.tab_data[current_tab]["tracked"]
        if sort_by == "Alphabetical":
            tracked.sort(key=lambda x: x["commodity"].lower())
        elif sort_by == "Total Amount":
            tracked.sort(key=lambda x: x["needed"], reverse=True)
        elif sort_by == "Amount Remaining":
            tracked.sort(key=lambda x: (x["needed"] - x["gathered"]), reverse=True)
        self.update_tracked_display(current_tab)

    def update_tracked_display(self, tab):
        tree = self.tab_data[tab]["tree"]
        tree.delete(*tree.get_children())
        for idx, item in enumerate(self.tab_data[tab]["tracked"], start=1):
            status = f"{item['gathered']}/{item['needed']}"
            remaining = item["needed"] - item["gathered"]
            complete = "✔" if item["gathered"] >= item["needed"] else ""
            tree.insert("", tk.END, iid=str(idx), values=(item["commodity"], status, remaining, complete))

    def update_total_remaining(self):
        current_tab = self.get_current_tab()
        total_remaining = sum(item["needed"] - item["gathered"] for item in self.tab_data[current_tab]["tracked"])
        self.total_remaining_var.set(f"Total Remaining: {total_remaining}")

    # --------------------------
    # Popup Editing for Gathered Value
    # --------------------------
    def on_treeview_double_click(self, event):
        current_tab = self.get_current_tab()
        tree = self.tab_data[current_tab]["tree"]
        region = tree.identify("region", event.x, event.y)
        if region != "cell":
            return
        column = tree.identify_column(event.x)
        if column != "#2":  # Allow editing only on the "Status" column.
            return
        row_id = tree.identify_row(event.y)
        if not row_id:
            return
        index = int(row_id) - 1
        record = self.tab_data[current_tab]["tracked"][index]
        self.open_edit_popup(record, index, current_tab)

    def open_edit_popup(self, record, index, current_tab):
        popup = tk.Toplevel(self)
        popup.title(f"Update {record['commodity']}")
        popup.geometry("250x100")
        # Center popup over main window.
        self.update_idletasks()
        x = self.winfo_rootx() + (self.winfo_width() - popup.winfo_reqwidth()) // 2
        y = self.winfo_rooty() + (self.winfo_height() - popup.winfo_reqheight()) // 2
        popup.geometry(f"+{x}+{y}")
        tk.Label(popup, text=f"Additional gathered for\n{record['commodity']}:").pack(pady=5)
        entry = tk.Entry(popup)
        entry.pack(pady=5)
        entry.focus_set()

        def on_ok():
            try:
                additional = float(entry.get())
            except ValueError:
                messagebox.showwarning("Input Error", "Please enter a valid numeric value.")
                return
            record["gathered"] += additional
            if record["gathered"] > record["needed"]:
                record["gathered"] = record["needed"]
            self.update_tracked_display(current_tab)
            self.update_total_remaining()
            popup.destroy()

        ok_button = tk.Button(popup, text="OK", command=on_ok)
        ok_button.pack(pady=5)
        popup.bind("<Return>", lambda e: on_ok())
        popup.transient(self)
        popup.grab_set()
        self.wait_window(popup)

    # --------------------------
    # Export / Import Functions (Full State)
    # --------------------------
    def export_state(self):
        state = {
            "global": {
                "current_theme": self.current_theme,
                "sort_option": self.sort_option.get(),
                "active_tab": self.notebook.index(self.notebook.select())
            },
            "tabs": []
        }
        for tab_id in self.notebook.tabs():
            tab_frame = self.notebook.nametowidget(tab_id)
            tab_info = self.tab_data.get(tab_frame, {})
            state["tabs"].append({
                "name": tab_info.get("name", "Unnamed"),
                "tracked": tab_info.get("tracked", [])
            })
        file_path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON Files", "*.json")])
        if file_path:
            try:
                with open(file_path, "w") as outfile:
                    json.dump(state, outfile, indent=4)
                messagebox.showinfo("Export", "State successfully exported!")
            except Exception as e:
                messagebox.showerror("Export Error", f"Failed to export state: {e}")

    def import_state(self):
        file_path = filedialog.askopenfilename(defaultextension=".json", filetypes=[("JSON Files", "*.json")])
        if file_path:
            try:
                with open(file_path, "r") as infile:
                    state = json.load(infile)
                # Clear existing tabs
                for tab in list(self.tab_data.keys()):
                    self.notebook.forget(tab)
                    del self.tab_data[tab]
                # Restore global settings
                self.current_theme = state.get("global", {}).get("current_theme", "Light")
                self.theme_var.set(self.current_theme)
                sort_val = state.get("global", {}).get("sort_option", "Alphabetical")
                self.sort_option.set(sort_val)
                # Restore tabs
                for tab_state in state.get("tabs", []):
                    self.create_new_tab()
                    current_tab = self.get_current_tab()
                    self.tab_data[current_tab]["name"] = tab_state.get("name", "Unnamed")
                    self.notebook.tab(current_tab, text=self.tab_data[current_tab]["name"])
                    self.tab_data[current_tab]["tracked"] = tab_state.get("tracked", [])
                    self.sort_current_tab()
                # Set active tab
                active_index = state.get("global", {}).get("active_tab", 0)
                self.notebook.select(active_index)
                self.update_tracked_display(self.get_current_tab())
                self.update_total_remaining()
                self.apply_theme()
                messagebox.showinfo("Import", "State successfully imported!")
            except Exception as e:
                messagebox.showerror("Import Error", f"Failed to import state: {e}")

    def export_to_excel(self):
        current_tab = self.get_current_tab()
        data = self.tab_data[current_tab]["tracked"]
        if not data:
            messagebox.showinfo("Export", "No commodities to export.")
            return
        file_path = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel Files", "*.xlsx")])
        if file_path:
            try:
                df = pd.DataFrame(data)
                df.to_excel(file_path, index=False)
                messagebox.showinfo("Export", "Data successfully exported to Excel!")
            except Exception as e:
                messagebox.showerror("Export Error", f"Failed to export data: {e}")

    # --------------------------
    # Graphs Functions
    # --------------------------
    def view_graphs(self):
        current_tab = self.get_current_tab()
        data = self.tab_data[current_tab]["tracked"]
        if not data:
            messagebox.showinfo("Graphs", "No data available to display graphs.")
            return

        graph_window = tk.Toplevel(self)
        graph_window.title("Commodity Graphs")
        graph_window.geometry("800x600")
        notebook = ttk.Notebook(graph_window)
        notebook.pack(fill=tk.BOTH, expand=True)

        frame1 = ttk.Frame(notebook)
        notebook.add(frame1, text="Bar Chart")
        fig1, ax1 = plt.subplots(figsize=(7, 4))
        commodities = [item["commodity"] for item in data]
        needed = [item["needed"] for item in data]
        gathered = [item["gathered"] for item in data]
        ax1.bar(commodities, needed, label="Needed", color='lightgrey')
        ax1.bar(commodities, gathered, label="Gathered", color='skyblue')
        ax1.set_title("Needed vs Gathered")
        ax1.set_ylabel("Amount")
        ax1.tick_params(axis='x', rotation=45)
        ax1.legend()
        canvas1 = FigureCanvasTkAgg(fig1, master=frame1)
        canvas1.draw()
        canvas1.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        frame2 = ttk.Frame(notebook)
        notebook.add(frame2, text="Pie Chart")
        category_remaining = {}
        for item in data:
            cat = COMMODITY_TO_CATEGORY.get(item["commodity"], "Unknown")
            remaining = item["needed"] - item["gathered"]
            category_remaining[cat] = category_remaining.get(cat, 0) + remaining
        labels = list(category_remaining.keys())
        sizes = list(category_remaining.values())
        fig2, ax2 = plt.subplots(figsize=(7, 4))
        ax2.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140)
        ax2.axis('equal')
        ax2.set_title("Remaining by Category")
        canvas2 = FigureCanvasTkAgg(fig2, master=frame2)
        canvas2.draw()
        canvas2.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        frame3 = ttk.Frame(notebook)
        notebook.add(frame3, text="Horizontal Bar")
        sorted_data = sorted(data, key=lambda x: (x["needed"] - x["gathered"]), reverse=True)
        sorted_commodities = [item["commodity"] for item in sorted_data]
        remaining_vals = [item["needed"] - item["gathered"] for item in sorted_data]
        fig3, ax3 = plt.subplots(figsize=(7, 4))
        ax3.barh(sorted_commodities, remaining_vals, color='salmon')
        ax3.set_title("Remaining Amount (Sorted)")
        ax3.set_xlabel("Remaining")
        canvas3 = FigureCanvasTkAgg(fig3, master=frame3)
        canvas3.draw()
        canvas3.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    # --------------------------
    # Theme Functions (Using ttk.Style for Treeview)
    # --------------------------
    def change_theme(self, event):
        self.current_theme = self.theme_var.get()
        self.apply_theme()

    def apply_theme(self):
        theme = THEMES.get(self.current_theme, THEMES["Light"])
        self.configure(bg=theme["bg"])
        for widget in self.winfo_children():
            if isinstance(widget, tk.Frame):
                widget.configure(bg=theme["bg"])
                for child in widget.winfo_children():
                    try:
                        child.configure(bg=theme["bg"], fg=theme["fg"])
                    except tk.TclError:
                        pass
        style = ttk.Style(self)
        style.configure("Treeview", 
                        background=theme["text_bg"], 
                        foreground=theme["fg"], 
                        fieldbackground=theme["text_bg"])
        style.configure("Treeview.Heading", background=theme["bg"], foreground=theme["fg"])

if __name__ == "__main__":
    app = CommodityTracker()
    app.mainloop()
