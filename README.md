
![Comm Tracker Pic](https://github.com/user-attachments/assets/720f3b67-4e4e-442e-ae11-721969deea08)
![Comm Tracker Pic 2](https://github.com/user-attachments/assets/37c8591a-e64d-40e4-8751-7705f2f181dd)


# Commodity Tracker with Centralized Sync

This is a Python-based Commodity Tracker application for Elite Dangerous that now includes a real-time, centralized sync system. With this new release, users can share and update their commodity lists in real time via a dedicated server–client model.

## Features

- **Commodity Tracking:** Add, update, and manage a list of tracked commodities.
- **Real-Time Sync:** A centralized sync system allows one user to run as the server (using their public or private IP) and others connect as clients.
- **Automatic Updates:** When one user makes changes (adds or updates items), the update is broadcast to all connected clients (with notifications on the receiving end).
- **Notifications:** Non-intrusive notifications appear on the client side whenever an update is received from another user.
- **Import/Export:** Supports importing and exporting state as JSON and Excel files.
- **Graphical Visualization:** View graphs (bar charts and pie charts) of your data using Matplotlib.
- **UPnP Support:** Automatically sets up UPnP port mapping if available.

## Requirements

- Python 3.8 or higher
- [matplotlib](https://matplotlib.org/)
- [pandas](https://pandas.pydata.org/)
- [miniupnpc](https://pypi.org/project/miniupnpc/)

See the [requirements.txt](requirements.txt) file for version details.

## Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/yourusername/CommodityTracker.git
   cd CommodityTracker
   ```

2. **Create a virtual environment (optional but recommended):**

   ```bash
   python -m venv venv
   source venv/bin/activate    # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. **Run the Application:**

   ```bash
   python CommodityTrackerV2.6.py
   ```

2. **Sync Setup:**

   - Click **"Sync with Buddy"**.
   - Enter your user ID.
   - When prompted, choose whether this instance should act as the server.
     - If **server**: enter your server IP (either your private IP for LAN or your public IP if you have port forwarding set up).
     - If **client**: enter the server’s IP.
   - Enter the port (default is 5000; if you change it, update the port in the code and your port forwarding settings accordingly).

3. **Testing:**

   - You can test on a single computer by running two instances: one in server mode and one in client mode using `120.0.0.1` (or your LAN IP).
   - Once synced, any updates (adding/updating items, importing state, etc.) will be broadcast to all connected clients (except the one that initiated the change, which won’t receive a duplicate update).

## Port Forwarding

To allow external connections:
- Use your **public IP** (e.g., `70.09.009.007`) and ensure port forwarding is configured on your router.
- If testing on a LAN, use your **private IP** (e.g., `10.0.0.003`).

## UPnP

If your network supports UPnP, the app will attempt to automatically set up a port mapping on the default port (5000).

## Release Instructions

1. **Update Version Information:**  
   - Update the version in your repository (e.g., tag this release as `v2.6`).

2. **Commit Changes:**  
   - Ensure your latest changes (code, README.md, requirements.txt, etc.) are committed.

3. **Tag the Release:**  
   - Create a Git tag:
     ```bash
     git tag -a v2.6 -m "Release version 2.6 with centralized sync and UPnP support"
     git push origin v2.6
     ```

4. **Publish on GitHub:**  
   - Go to your GitHub repository’s "Releases" section.
   - Draft a new release using the tag, add release notes (highlight new features, instructions, etc.), and publish.

5. **Share the Link:**  
   - Once published, share the GitHub release link with your users.

---

Feel free to modify the README content as needed for your project. Enjoy your new release!
