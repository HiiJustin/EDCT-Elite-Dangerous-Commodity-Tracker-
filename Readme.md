Elite Dangerous Commodity Tracker

This application is a Python-based GUI tool designed to help Elite Dangerous players track and manage commodities during trade runs or market activities. The program features an autocomplete search for quickly finding commodities, an interactive checklist where you can set target amounts and update the number of items you have gathered, and a dedicated "Remaining" column that automatically calculates the difference between the target and gathered amounts. When an item’s gathered quantity meets or exceeds its target, a green checkmark is displayed in the "Complete" column.

In addition, the tracker supports multiple tabs so you can manage separate commodity lists. You have the ability to create new tabs, rename them, and close tabs (with the exception that the last remaining tab cannot be closed). Items in each list can be sorted by alphabetical order, total amount, or by amount remaining using the provided dropdown menu. The full state of the program—including the current theme, sort option, and details for all tabs—can be exported to a JSON file and later imported to restore your session exactly as you left it. For further analysis, the program offers graphical reports (a bar chart, a pie chart, and a horizontal bar chart) to visually summarize your commodity data. You can also export the current list to an Excel file.

Installation Instructions:
1. First, ensure you have Python 3 installed on your computer. You can download Python 3 from the official website (https://www.python.org/) and follow the installation instructions for your operating system.
2. Next, download or clone the repository containing the program files.
3. Open a terminal (or command prompt) and navigate to the folder where you have saved the project files.
4. The program requires two external libraries: matplotlib and pandas. Install these dependencies by running the following command:
   pip install -r requirements.txt
   (This command reads the required packages from the provided requirements.txt file and installs them automatically.)
5. Once the dependencies are installed, you are ready to run the application.

Usage Instructions:
1. In the terminal, run the program by typing:
   python commodity_tracker.py
   The application window will open with all controls visible.
2. To add a commodity, begin typing its name into the "Commodity" field. The autocomplete feature will display suggestions based on your input—select the desired commodity from the list.
3. Enter the target amount (the total number you wish to gather) in the "Target Amount" field, then click the "Add Commodity" button or press Enter. The commodity will be added to your checklist in the current tab.
4. In the checklist, you will see four columns: "Commodity", "Gathered/Needed", "Remaining", and "Complete". The "Gathered/Needed" column shows the current progress (for example, 0/100), and the "Remaining" column automatically displays the difference (in this case, 100). When the gathered amount reaches the target, a green checkmark appears in the "Complete" column.
5. To update the gathered amount for a commodity, double-click the "Gathered/Needed" cell for that item. A popup window will appear (centered over the main application). Enter the additional number of items you have gathered and click "OK" (or press Enter). The application will update the "Gathered/Needed" and "Remaining" values accordingly.
6. Use the "Sort By" dropdown to choose how to order your list (alphabetically, by total amount, or by amount remaining). The list will be automatically re-sorted each time you add or update items.
7. You can manage multiple lists using tabs. To create a new tab, use the appropriate control; to rename a tab, click the "Rename Tab" button and enter the new name; to close a tab, click the red "❌ Close Current Tab" button (the application does not allow you to close the final remaining tab).
8. To save your work, export the full state of the application by clicking the "Export to JSON" button. This file will contain all program settings (theme, sort option, active tab) and the details for each tab. Later, you can restore your session by clicking the "Import from JSON" button and selecting the saved file.
9. For visual analysis, click "View Graphs" to open a new window displaying several charts that summarize your commodity data.
10. If you wish to export the current list to Excel, click the "Export to Excel" button.

License:
This project is licensed under the MIT License.

---
