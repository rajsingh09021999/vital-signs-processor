# Vital Signs Data Processor - Web Application

A user-friendly web interface for processing and organizing medical simulation data from ZOLL devices. This tool automatically sorts vital signs data into structured Excel files based on simulation schedules and mannequin assignments.

## 🚀 Features

- **Easy File Upload**: Drag & drop interface for uploading folders with JSON files
- **Automatic Flattening**: Recursively extracts JSON files from nested folder structures
- **Smart Organization**: Automatically categorizes data by course, simulation, and mannequin
- **Schedule Validation**: Validates data against known simulation time windows
- **Excel Export**: Creates organized Excel files for each simulation session
- **Modern UI**: Clean, responsive interface designed for non-technical users

## 📋 What It Processes

### Supported Data Types

- ZOLL medical device JSON files
- Multiple vital sign parameters:
  - Heart Rate (HR)
  - Blood Pressure (NIBP/IBP)
  - Oxygen Saturation (SpO2)
  - Temperature readings
  - CO2 levels (FiCO2/EtCO2)
  - Respiratory Rate
  - Hemoglobin (SpHb)
  - Perfusion Index (PI)

### Simulation Configuration

- **Courses**: 2025A through 2025N
- **Simulations**: Sim1 through Sim5 (Monday-Friday)
- **Mannequins**: Dave, Chuck, Freddy, Matt, Oscar
- **Schedule**: 8:00 AM - 5:30 PM with 6 sessions per day

## 🛠️ Installation & Setup

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

### Quick Start

1. **Clone or download the application files**

   ```bash
   # Make sure you have these files:
   # - app.py
   # - json_processor.py
   # - requirements.txt
   # - templates/ (with HTML files)
   ```

2. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**

   ```bash
   python app.py
   ```

4. **Access the web interface**
   - Open your browser and go to: `http://localhost:5000`
   - The application will be running on your local machine

### Production Deployment

For production use with gunicorn:

```bash
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

## 💻 How to Use

### Step 1: Upload Your Data

1. Navigate to the web interface
2. Either drag & drop your folder or click "Select Folder"
3. Choose the folder containing your JSON files (can include subfolders)
4. The system will automatically find and list all JSON files

### Step 2: Process Data

1. Click "Process Files" to start the analysis
2. The system will:
   - Extract all JSON files from nested folders
   - Parse vital signs data
   - Classify by course, simulation, and mannequin
   - Validate against simulation schedules
   - Create organized Excel files

### Step 3: Download Results

1. Once processing is complete, a ZIP file will automatically download
2. The ZIP contains:
   - Organized folder structure: `Course/Simulation/Mannequin/Date/`
   - Excel files for each simulation session
   - CSV file with any unclassified data

## 📁 Output Structure

The processed data is organized as follows:

```
Course_Name/
├── Sim1/
│   ├── Dave/
│   │   └── 2024-10-14/
│   │       └── 2025A_Sim1_Dave_20241014.xlsx
│   └── Chuck/
│       └── 2024-10-14/
│           └── 2025A_Sim1_Chuck_20241014.xlsx
├── Sim2/
│   └── ...
└── unknown_rows.csv (if any invalid data)
```

## 🔧 Configuration

### Mannequin Mapping

The system maps device serial numbers to mannequin names:

- `AI23F013939` → Dave
- `AI23H014090` → Chuck
- `AI15F004305` → Freddy
- `AI15D003889` → Matt
- `AI20C009617` → Oscar

### Simulation Schedules

Each simulation has specific time windows throughout the day. Data is only considered valid if it falls within these windows.

### Course Dates

The system recognizes courses from 2025A through 2025N with specific date ranges for each course.

## 🔒 Privacy & Security

- All files are processed locally on the server
- Uploaded files are automatically deleted after processing
- No data is permanently stored or transmitted to external services
- Processing happens entirely within your controlled environment

## ⚠️ Troubleshooting

### Common Issues

1. **No JSON files found**

   - Ensure your folder contains .json files
   - Check that files aren't corrupted
   - Try uploading individual files to test

2. **Processing takes too long**

   - Large datasets may take several minutes
   - Don't close the browser window during processing
   - Check server logs for any errors

3. **Unknown data in results**
   - Check the `unknown_rows.csv` file for unclassified data
   - Verify device serial numbers match the mannequin mapping
   - Ensure timestamps fall within course date ranges

### File Size Limits

- Maximum upload size: 500MB
- Recommended: Process batches of files for better performance

## 🤝 Support

For issues or questions:

1. Check the "About" page in the web interface for detailed information
2. Review the console output for error messages
3. Verify your JSON files match the expected ZOLL format

## 📜 License

This tool is designed for medical simulation data processing and should be used in accordance with your institution's data handling policies.
