# Automobile Statistics Dashboard

## Overview

The **Dashboard.py** script is a Python application designed to create an interactive dashboard using the Dash library. This dashboard provides insights into automobile sales data, offering users the ability to explore yearly statistics and recession period statistics through interactive visualizations.

## Features

- **Data Loading**: Automatically loads automobile sales data from an online CSV file.
- **Interactive Dashboard**: Utilizes Dash components to create dropdown menus for selecting different statistics types and years.
- **Dynamic Visualization**: Implements callbacks to update charts based on user selections, providing a responsive user experience.
- **Data Visualization**: Uses Plotly Express to generate various charts, including line graphs, bar charts, and pie charts.

## Technical Details

- **Libraries Used**:
  - Dash
  - Pandas
  - Plotly Express

- **App Structure**:
  - The layout is defined using HTML components provided by Dash.
  - Interactivity is managed through callback functions that react to user inputs.

- **Execution**:
  - The script runs a local server to host the dashboard, accessible via a web browser.

## Usage

1. Ensure you have Python installed along with the necessary libraries (`dash`, `pandas`, `plotly`).
2. Run the script using the command:
   ```bash
   
   python Dashboard.py

3. Access the dashboard by opening a web browser and navigating to http://127.0.0.1:8050.
