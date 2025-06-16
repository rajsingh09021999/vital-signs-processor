# Vital Signs Data Processor

## Powerful and Private Medical Data Processing

Transform your ZOLL medical simulation data with this revolutionary **100% browser-based** application. No servers, no uploads, no limits—just pure power and privacy.

---

## **Key Features**

### **Complete Privacy & Security**

- **Zero Data Uploads**: All processing happens locally in your browser
- **No Server Dependencies**: Works completely offline after initial load
- **HIPAA-Friendly**: Data never leaves your computer
- **End-to-End Encryption**: Your data stays secure on your device

### **Unlimited Performance**

- **Process Thousands of Files**: No file size limits
- **Lightning-Fast Processing**: Optimized JavaScript engine
- **Real-Time Progress**: Live updates and visual feedback
- **Memory Efficient**: Smart processing for large datasets

### **Beautiful & Modern UI**

- **Stunning Design**: Professional, medical-grade interface
- **Dark/Light Themes**: Easy on the eyes during long sessions
- **Responsive Design**: Works perfectly on all devices
- **Smooth Animations**: Delightful user experience

---

## **Quick Start**

### **Option 1: Run Locally (Recommended)**

```bash
# Download the files
# index.html, styles.css, script.js

# Open index.html in your browser
# That's it! No installation required.
```

### **Option 2: Deploy to GitHub Pages**

1. Push files to a GitHub repository
2. Enable GitHub Pages in repository settings
3. Access at: `https://username.github.io/repo-name`

---

## **How to Use**

### **Step 1: Upload Your Data**

- **Drag & Drop**: Simply drag your ZOLL data folder into the upload zone
- **Browse**: Or click "Select Folder" to choose your data directory
- **Multiple Formats**: Handles nested folders and complex structures

### **Step 2: Analyze & Preview**

- View comprehensive file statistics
- See folder structure and organization
- Preview data before processing

### **Step 3: Configure Processing**

- **Include Unknown Data**: Export unclassified records to CSV
- **Validate Schedules**: Check against simulation time windows
- **Generate Summary**: Create processing summary report

### **Step 4: Process & Download**

1. Click "Process Data" to start
2. Watch real-time progress with detailed updates
3. Download your organized ZIP file

---

## **Data Organization**

The processor automatically organizes your data into:

```
ProcessedData.zip
├── 2025A/
│   ├── Sim1/
│   │   ├── Dave/
│   │   │   └── 2025A_Sim1_Dave_20241014.xlsx
│   │   └── Chuck/
│   │       └── 2025A_Sim1_Chuck_20241014.xlsx
│   └── Sim2/
│       └── ...
├── 2025B/
│   └── ...
└── unknown_rows.csv (if enabled)
```

---

## **Technical Specifications**

### **Supported Data**

- **File Types**: JSON files from ZOLL devices
- **Data Size**: Unlimited (browser memory dependent)
- **File Count**: Thousands of files supported
- **Mannequins**: Dave, Chuck, Freddy, Matt, Oscar
- **Simulations**: Sim1 through Sim5
- **Courses**: 2025A through 2025N

### **Vital Signs Processed**

- Heart Rate (HR)
- Blood Pressure (NIBP/IBP: SYS, DIA, MAP)
- Oxygen Saturation (SpO2, SpMet, SpCo)
- Temperature (multiple sensors)
- Respiratory Rate
- End-tidal CO2 (EtCO2)
- Fractional CO2 (FiCO2)
- Perfusion Index (PI, PVI)

### **Browser Requirements**

- **Modern Browser**: Chrome 80+, Firefox 75+, Safari 13+, Edge 80+
- **JavaScript**: Must be enabled
- **Memory**: 4GB+ RAM recommended for large datasets

---

## **Comparison: Client-Side vs Server-Based**

| Feature                | Client-Side (This App) | Server-Based       |
| ---------------------- | ---------------------- | ------------------ |
| **Privacy**            | 100% Private           | Data uploaded      |
| **File Size Limits**   | Unlimited              | Server limits      |
| **Processing Speed**   | Lightning fast         | Network dependent  |
| **Hosting Costs**      | Free forever           | Ongoing costs      |
| **Offline Capability** | Works offline          | Requires internet  |
| **Setup Complexity**   | Just open file         | Server setup       |
| **Scalability**        | Scales with device     | Server bottlenecks |

---

## **Deployment Options**

### **1. Local Development**

Perfect for testing and development:

```bash
# Simply open index.html in your browser
# No build process required
```

### **2. GitHub Pages**

Free hosting with automatic deployment:

```bash
# Push to GitHub
git push origin main

# Enable GitHub Pages in repository settings
# Access at: https://username.github.io/repo-name
```

### **3. Static Site Hosts**

Deploy to any static hosting service:

- **Vercel**: Drag & drop deployment
- **Netlify**: Instant deployment
- **Firebase Hosting**: `firebase deploy`
- **AWS S3**: Static website hosting

---

## **Security & Privacy**

### **Data Protection**

- **No Network Requests**: Files never leave your device
- **Local Storage Only**: Temporary browser storage
- **Memory Cleanup**: Secure data disposal
- **No Logging**: Zero data collection

### **Compliance**

- **HIPAA Compatible**: Local processing meets requirements
- **GDPR Friendly**: No data transmission or storage
- **SOC 2 Ready**: Enterprise security standards

---

## **Future Enhancements**

### **Planned Features**

- **Web Workers**: Background processing for larger datasets
- **Data Visualization**: Charts and graphs for vital signs
- **Advanced Search**: Filter and search within processed data
- **PWA Support**: Install as native app
- **API Integration**: Connect with hospital systems

---

## **Support & Documentation**

### **Getting Help**

- **GitHub Issues**: Bug reports and feature requests
- **Discussions**: Community support and ideas
- **Documentation**: Comprehensive usage guides

---

## **License**

This project is licensed under the MIT License.

### **Open Source**

- Free to use, modify, and distribute
- Commercial use permitted
- No attribution required (but appreciated)

---

## **Why Choose This Processor?**

### **For Individuals**

- **Complete Privacy**: Your data stays on your device
- **No Costs**: Free forever, no subscriptions
- **Unlimited Use**: Process as much data as you need
- **Professional Results**: Hospital-grade organization

### **For Organizations**

- **HIPAA Compliance**: Local processing meets requirements
- **Zero Infrastructure**: No servers to maintain
- **Instant Deployment**: Share a single HTML file
- **Unlimited Scaling**: Each user has full capacity

---

## **Get Started Today**

Transform your medical data processing workflow with the most powerful, beautiful, and private solution available.

**Simply download the files and open `index.html` in your browser!**

---

_Professional medical data processing for simulation training programs._
