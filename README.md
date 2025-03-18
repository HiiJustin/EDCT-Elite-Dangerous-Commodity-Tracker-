Elite Dangerous Commodity Tracker
===================================

Overview:
---------
This is a Python-based GUI application for tracking commodity progress in Elite Dangerous.
The script provides a graphical interface to add commodities, update gathered amounts,
set prices, and export/import tracking data in JSON format.
It also features a live search dropdown for commodities and a theme toggle (light/dark).

Requirements:
-------------
- Python 3.6 or higher (with the tkinter module, which is included by default)
- No additional third-party libraries are required

Installation:
-------------
1. Make sure you have Python 3.6 or higher installed.
2. Download the Python script (e.g., commodity_tracker.py) and place it in your desired directory.
3. (Optional) Create and activate a virtual environment:
   - On Windows: python -m venv venv && venv\Scripts\activate
   - On macOS/Linux: python3 -m venv venv && source venv/bin/activate
4. Since no external packages are needed, you can run the script directly.

Usage:
------
1. Open a terminal or command prompt in the directory containing the script.
2. Run the script with:
   python commodity_tracker.py
3. The application window will open. You can:
   - **Add a Commodity**: Type in the commodity name (a live-updating dropdown helps with selection)
     and a target amount, then click "Add Commodity".
   - **Update Data**: Enter gathered amounts and unit prices in the respective fields.
   - **View Progress**: Check the "Remaining" and "Cost" columns, with a checkmark indicating completion.
   - **Save/Export/Import Data**: Use the "File" menu to export your list to a JSON file,
     import an existing file, or save changes.
   - **Toggle Theme**: Click the "Toggle Theme" button to switch between light and dark themes.

Notes:
------
- Data is stored in JSON format, allowing you to easily back up or share your tracking list.
- The application window can be closed normally; unsaved changes will not be automatically saved.
- For best performance, ensure you run the script using the standard Python interpreter.
