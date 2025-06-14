// ===== VITAL SIGNS PROCESSOR =====
// Client-side JavaScript implementation

class VitalSignsProcessor {
    constructor() {
        this.files = [];
        this.processedData = null;
        this.currentTheme = localStorage.getItem('theme') || 'light';
        
        // Configuration (converted from Python)
        this.SIM_MANNEQUINS = {
            "Sim1": ["Dave", "Chuck"],
            "Sim2": ["Freddy", "Oscar"],
            "Sim3": ["Dave", "Chuck"],
            "Sim4": ["Dave", "Chuck"],
            "Sim5": ["Freddy", "Oscar", "Matt"]
        };

        this.MANNEQUIN_MAP = {
            "AI23F013939": "Dave",
            "AI23H014090": "Chuck",
            "AI15F004305": "Freddy",
            "AI15D003889": "Matt",
            "AI20C009617": "Oscar"
        };

        this.COURSE_DATE_RANGES = [
            { start: "10/14", end: "10/18", name: "2025A" },
            { start: "10/28", end: "11/01", name: "2025B" },
            { start: "11/18", end: "11/22", name: "2025C" },
            { start: "12/09", end: "12/13", name: "2025D" },
            { start: "01/13", end: "01/17", name: "2025E" },
            { start: "01/27", end: "01/31", name: "2025F" },
            { start: "02/17", end: "02/21", name: "2025G/H" },
            { start: "02/24", end: "02/28", name: "2025H" },
            { start: "03/24", end: "03/28", name: "2025I" },
            { start: "04/14", end: "04/18", name: "2025J" },
            { start: "05/05", end: "05/09", name: "2025K/L" },
            { start: "05/12", end: "05/16", name: "2025L" },
            { start: "06/09", end: "06/13", name: "2025M" },
            { start: "06/23", end: "06/27", name: "2025N" }
        ];

        this.COURSE_START_DATES = {
            "2025A": "2024-10-14",
            "2025B": "2024-10-28",
            "2025C": "2024-11-18",
            "2025D": "2024-12-09",
            "2025E": "2025-01-13",
            "2025F": "2025-01-27",
            "2025G/H": "2025-02-17",
            "2025H": "2025-02-24",
            "2025I": "2025-03-24",
            "2025J": "2025-04-14",
            "2025K/L": "2025-05-05",
            "2025L": "2025-05-12",
            "2025M": "2025-06-09",
            "2025N": "2025-06-23"
        };

        this.DAY_OFFSET_TO_SIM = {
            0: "Sim1", 1: "Sim2", 2: "Sim3", 3: "Sim4", 4: "Sim5"
        };

        this.init();
    }

    init() {
        this.setupTheme();
        this.setupEventListeners();
    }

    setupTheme() {
        document.documentElement.setAttribute('data-theme', this.currentTheme);
        const themeIcon = document.querySelector('#themeToggle i');
        if (themeIcon) {
            themeIcon.className = this.currentTheme === 'light' ? 'fas fa-moon' : 'fas fa-sun';
        }
    }

    setupEventListeners() {
        // Theme toggle
        const themeToggle = document.getElementById('themeToggle');
        if (themeToggle) {
            themeToggle.addEventListener('click', () => this.toggleTheme());
        }

        // Info modal
        const infoBtn = document.getElementById('infoBtn');
        const modalClose = document.getElementById('modalClose');
        const infoModal = document.getElementById('infoModal');
        
        if (infoBtn) {
            infoBtn.addEventListener('click', () => {
                infoModal.classList.add('active');
            });
        }
        
        if (modalClose) {
            modalClose.addEventListener('click', () => {
                infoModal.classList.remove('active');
            });
        }

        // File handling
        const fileInput = document.getElementById('fileInput');
        const uploadZone = document.getElementById('uploadZone');

        if (fileInput) {
            fileInput.addEventListener('change', (e) => this.handleFiles(e.target.files));
        }

        if (uploadZone) {
            uploadZone.addEventListener('dragover', (e) => {
                e.preventDefault();
                uploadZone.classList.add('dragover');
            });

            uploadZone.addEventListener('dragleave', () => {
                uploadZone.classList.remove('dragover');
            });

            uploadZone.addEventListener('drop', (e) => {
                e.preventDefault();
                uploadZone.classList.remove('dragover');
                this.handleFiles(e.dataTransfer.files);
            });
        }

        // Process button
        const processBtn = document.getElementById('processBtn');
        if (processBtn) {
            processBtn.addEventListener('click', () => this.processData());
        }
    }

    toggleTheme() {
        this.currentTheme = this.currentTheme === 'light' ? 'dark' : 'light';
        localStorage.setItem('theme', this.currentTheme);
        this.setupTheme();
    }

    async handleFiles(fileList) {
        const files = Array.from(fileList);
        const jsonFiles = files.filter(file => file.name.toLowerCase().endsWith('.json'));
        
        if (jsonFiles.length === 0) {
            this.showNotification('No JSON files found. Please select a folder containing JSON files.', 'error');
            return;
        }

        this.files = jsonFiles;
        this.analyzeFiles();
        this.showAnalysisPanel();
    }

    analyzeFiles() {
        const totalSize = this.files.reduce((sum, file) => sum + file.size, 0);
        const folders = new Set();
        
        this.files.forEach(file => {
            const path = file.webkitRelativePath || file.name;
            if (path.includes('/')) {
                folders.add(path.split('/')[0]);
            }
        });

        // Update UI
        const totalFilesEl = document.getElementById('totalFiles');
        const totalFoldersEl = document.getElementById('totalFolders');
        const totalSizeEl = document.getElementById('totalSize');
        
        if (totalFilesEl) totalFilesEl.textContent = this.files.length;
        if (totalFoldersEl) totalFoldersEl.textContent = folders.size || 1;
        if (totalSizeEl) totalSizeEl.textContent = this.formatFileSize(totalSize);

        this.buildFileTree();
    }

    buildFileTree() {
        const fileTree = document.getElementById('fileTree');
        if (!fileTree) return;
        
        const folders = {};
        
        this.files.forEach(file => {
            const path = file.webkitRelativePath || file.name;
            const folder = path.includes('/') ? path.split('/')[0] : 'Root';
            if (!folders[folder]) folders[folder] = [];
            folders[folder].push(file.name);
        });

        let html = '<div class="file-tree-content">';
        Object.entries(folders).forEach(([folder, files]) => {
            html += `
                <div class="folder-item">
                    <div class="folder-header">
                        <i class="fas fa-folder" style="color: #f59e0b;"></i>
                        <span class="folder-name">${folder}</span>
                        <span class="file-count">${files.length} files</span>
                    </div>
                </div>
            `;
        });
        html += '</div>';
        
        fileTree.innerHTML = html;
    }

    showAnalysisPanel() {
        this.showSection('analysisPanel');
        this.showSection('processControls');
    }

    showSection(elementId) {
        const element = document.getElementById(elementId);
        if (element) element.style.display = 'block';
    }

    hideSection(elementId) {
        const element = document.getElementById(elementId);
        if (element) element.style.display = 'none';
    }

    async processData() {
        this.showSection('progressSection');
        this.hideSection('processControls');
        
        try {
            const options = {
                includeUnknown: document.getElementById('includeUnknown')?.checked || false,
                validateSchedules: document.getElementById('validateSchedules')?.checked || false,
                generateSummary: document.getElementById('generateSummary')?.checked || false
            };

            const result = await this.processFiles(options);
            this.processedData = result;
            this.showResults(result);
            
        } catch (error) {
            console.error('Processing error:', error);
            this.showNotification('Error processing files: ' + error.message, 'error');
        }
    }

    async processFiles(options) {
        const updateProgress = (text, percent) => {
            const progressText = document.getElementById('progressText');
            const progressPercent = document.getElementById('progressPercent');
            const progressFill = document.getElementById('progressFill');
            
            if (progressText) progressText.textContent = text;
            if (progressPercent) progressPercent.textContent = `${percent}%`;
            if (progressFill) progressFill.style.width = `${percent}%`;
        };

        updateProgress('Reading files...', 10);
        
        // Read all JSON files
        const jsonData = [];
        for (let i = 0; i < this.files.length; i++) {
            const file = this.files[i];
            try {
                const content = await this.readFileContent(file);
                const data = JSON.parse(content);
                const rows = this.parseJsonFile(data, file.name);
                jsonData.push(...rows);
                
                const percent = 10 + (i / this.files.length) * 30;
                updateProgress(`Processing ${file.name}...`, Math.round(percent));
            } catch (error) {
                console.warn(`Error reading ${file.name}:`, error);
            }
        }

        updateProgress('Analyzing data...', 50);

        // Process data
        const processedRows = this.processJsonData(jsonData, options);
        
        updateProgress('Generating Excel files...', 80);
        
        // Create ZIP file
        const zipFile = await this.createZipFile(processedRows, options);
        
        updateProgress('Complete!', 100);
        
        return {
            totalRows: jsonData.length,
            validRows: processedRows.valid.length,
            unknownRows: processedRows.unknown.length,
            zipFile: zipFile
        };
    }

    readFileContent(file) {
        return new Promise((resolve, reject) => {
            const reader = new FileReader();
            reader.onload = () => resolve(reader.result);
            reader.onerror = () => reject(reader.error);
            reader.readAsText(file);
        });
    }

    parseJsonFile(data, filename) {
        const rows = [];
        
        try {
            const records = data.ZOLL?.FullDisclosure?.[0]?.FullDisclosureRecord;
            if (!records) return rows;
            
            // Find device serial
            let deviceSerial = null;
            for (const record of records) {
                if (record.DeviceConfiguration) {
                    deviceSerial = record.DeviceConfiguration.DeviceSerialNumber;
                    break;
                }
            }

            // Process TrendRpt records
            for (const record of records) {
                if (record.TrendRpt) {
                    const trendRows = this.parseTrendReport(record.TrendRpt, deviceSerial, filename);
                    rows.push(...trendRows);
                }
            }
        } catch (error) {
            console.warn(`Error parsing ${filename}:`, error);
        }

        return rows;
    }

    parseTrendReport(trendRpt, deviceSerial, sourceFile) {
        const dateTimeStr = trendRpt.StdHdr?.DevDateTime;
        let dateTime = null;
        
        if (dateTimeStr) {
            try {
                dateTime = new Date(dateTimeStr);
            } catch (error) {
                console.warn('Error parsing datetime:', dateTimeStr);
            }
        }

        const trend = trendRpt.Trend || {};
        const row = {
            TimeObj: dateTime,
            TimeStr: dateTimeStr,
            DevSerial: deviceSerial,
            SourceFile: sourceFile,
            // Vital signs
            Hr: this.getTrendValue(trend.Hr?.TrendData),
            FiCO2: this.getTrendValue(trend.Fico2?.TrendData),
            SpO2: this.getTrendValue(trend.Spo2?.TrendData),
            EtCO2: this.getTrendValue(trend.Etco2?.TrendData),
            RespRate: this.getTrendValue(trend.Resp?.TrendData)
        };

        // Add more vital signs as needed
        if (trend.Spo2) {
            row.SpMet = this.getTrendValue(trend.Spo2.SpMet?.TrendData);
            row.SpCo = this.getTrendValue(trend.Spo2.SpCo?.TrendData);
            row.PVI = this.getTrendValue(trend.Spo2.PVI?.TrendData);
            row.PI = this.getTrendValue(trend.Spo2.PI?.TrendData);
        }

        if (trend.Nibp) {
            row.NIBP_SYS = this.getTrendValue(trend.Nibp.Sys?.TrendData);
            row.NIBP_DIA = this.getTrendValue(trend.Nibp.Dia?.TrendData);
            row.NIBP_MAP = this.getTrendValue(trend.Nibp.Map?.TrendData);
        }
        
        return [row];
    }

    getTrendValue(trendData) {
        if (!trendData) return null;
        
        const dataState = trendData.DataState;
        const dataStatus = trendData.DataStatus;
        
        if (dataState === "unmonitored" || dataState === "invalid") return null;
        if (dataStatus === 1) return null;
        
        return trendData.Val?.['#text'] || null;
    }

    processJsonData(rows, options) {
        // Filter valid timestamps
        const validTimeRows = rows.filter(row => row.TimeObj && !isNaN(row.TimeObj.getTime()));
        
        // Sort by time
        validTimeRows.sort((a, b) => a.TimeObj - b.TimeObj);

        // Add processing fields
        validTimeRows.forEach(row => {
            row.rawMannequin = this.MANNEQUIN_MAP[row.DevSerial] || null;
            row.Course = this.getCourseForDate(row.TimeObj);
            row.Sim = this.getSimForCourseDate(row.Course, row.TimeObj);
            row.overrideMannequin = row.rawMannequin;
            row.DateStr = row.TimeObj.toISOString().split('T')[0];
        });

        // Separate valid and unknown
        const valid = validTimeRows.filter(row => this.isValidRow(row, options));
        const unknown = validTimeRows.filter(row => !this.isValidRow(row, options));

        return { valid, unknown };
    }

    getCourseForDate(dateObj) {
        const month = dateObj.getMonth() + 1;
        const day = dateObj.getDate();
        
        for (const range of this.COURSE_DATE_RANGES) {
            const [startMonth, startDay] = range.start.split('/').map(Number);
            const [endMonth, endDay] = range.end.split('/').map(Number);
            
            const okStart = (month > startMonth) || (month === startMonth && day >= startDay);
            const okEnd = (month < endMonth) || (month === endMonth && day <= endDay);
            
            if (okStart && okEnd) {
                return range.name;
            }
        }
        
        return null;
    }

    getSimForCourseDate(course, dateObj) {
        if (!course || !this.COURSE_START_DATES[course]) return null;
        
        try {
            const courseStart = new Date(this.COURSE_START_DATES[course]);
            const diffTime = dateObj.getTime() - courseStart.getTime();
            const diffDays = Math.floor(diffTime / (1000 * 60 * 60 * 24));
            
            return this.DAY_OFFSET_TO_SIM[diffDays] || null;
        } catch (error) {
            return null;
        }
    }

    isValidRow(row, options) {
        if (!row.Course) return false;
        if (!row.Sim) return false;
        if (!row.overrideMannequin) return false;
        
        const validMannequins = this.SIM_MANNEQUINS[row.Sim] || [];
        return validMannequins.includes(row.overrideMannequin);
    }

    async createZipFile(data, options) {
        const zip = new JSZip();
        
        // Group valid data
        const groups = this.groupValidData(data.valid);
        
        // Create Excel files
        for (const [key, rows] of Object.entries(groups)) {
            const [course, sim, mannequin, dateStr] = key.split('_');
            const folder = `${course}/${sim}/${mannequin}/${dateStr}`;
            const filename = `${course}_${sim}_${mannequin}_${dateStr.replace(/-/g, '')}.xlsx`;
            
            const workbook = this.createExcelWorkbook(rows);
            const excelBuffer = XLSX.write(workbook, { bookType: 'xlsx', type: 'array' });
            
            const folderPath = folder.split('/').slice(0, -1).join('/');
            zip.folder(folderPath).file(filename, excelBuffer);
        }
        
        // Add unknown data CSV if requested
        if (options.includeUnknown && data.unknown.length > 0) {
            const csvContent = this.createCSV(data.unknown);
            zip.file('unknown_rows.csv', csvContent);
        }
        
        return await zip.generateAsync({ type: 'blob' });
    }

    groupValidData(validRows) {
        const groups = {};
        
        validRows.forEach(row => {
            const key = `${row.Course}_${row.Sim}_${row.overrideMannequin}_${row.DateStr}`;
            if (!groups[key]) groups[key] = [];
            groups[key].push(row);
        });
        
        return groups;
    }

    createExcelWorkbook(rows) {
        const workbook = XLSX.utils.book_new();
        
        const wsData = rows.map(row => {
            const cleanRow = { ...row };
            delete cleanRow.TimeObj;
            return cleanRow;
        });
        
        const worksheet = XLSX.utils.json_to_sheet(wsData);
        XLSX.utils.book_append_sheet(workbook, worksheet, 'VitalSigns');
        
        return workbook;
    }

    createCSV(rows) {
        if (rows.length === 0) return '';
        
        const headers = Object.keys(rows[0]).filter(key => key !== 'TimeObj');
        const csvRows = [headers.join(',')];
        
        rows.forEach(row => {
            const values = headers.map(header => {
                const value = row[header];
                if (value === null || value === undefined) return '';
                if (typeof value === 'string' && value.includes(',')) return `"${value}"`;
                return value;
            });
            csvRows.push(values.join(','));
        });
        
        return csvRows.join('\n');
    }

    showResults(result) {
        this.hideSection('progressSection');
        this.showSection('resultsSection');
        
        // Update summary
        const summary = document.getElementById('resultsSummary');
        if (summary) {
            summary.innerHTML = `
                <div class="summary-grid">
                    <div class="summary-item">
                        <span class="summary-number">${result.validRows}</span>
                        <span class="summary-label">Valid Records</span>
                    </div>
                    <div class="summary-item">
                        <span class="summary-number">${result.unknownRows}</span>
                        <span class="summary-label">Unknown Records</span>
                    </div>
                    <div class="summary-item">
                        <span class="summary-number">${this.files.length}</span>
                        <span class="summary-label">Files Processed</span>
                    </div>
                </div>
            `;
        }
        
        // Setup download
        const downloadBtn = document.getElementById('downloadBtn');
        if (downloadBtn) {
            downloadBtn.onclick = () => {
                const url = URL.createObjectURL(result.zipFile);
                const a = document.createElement('a');
                a.href = url;
                a.download = `vital_signs_processed_${new Date().toISOString().split('T')[0]}.zip`;
                document.body.appendChild(a);
                a.click();
                document.body.removeChild(a);
                URL.revokeObjectURL(url);
            };
        }
    }

    showNotification(message, type = 'info') {
        console.log(`${type.toUpperCase()}: ${message}`);
        // Simple alert for now
        alert(message);
    }

    formatFileSize(bytes) {
        if (bytes === 0) return '0 Bytes';
        const k = 1024;
        const sizes = ['Bytes', 'KB', 'MB', 'GB'];
        const i = Math.floor(Math.log(bytes) / Math.log(k));
        return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
    }
}

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.vitalProcessor = new VitalSignsProcessor();
});

// Add styles for summary grid
const additionalStyles = `
    .summary-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
        gap: 1.5rem;
        margin: 1.5rem 0;
    }
    
    .summary-item {
        text-align: center;
        padding: 1rem;
        background: var(--bg-secondary);
        border-radius: 12px;
        border: 1px solid var(--border-color);
    }
    
    .summary-number {
        display: block;
        font-size: 2rem;
        font-weight: 700;
        color: var(--primary-color);
        margin-bottom: 0.5rem;
    }
    
    .summary-label {
        color: var(--text-secondary);
        font-size: 0.875rem;
        font-weight: 500;
    }
    
    .file-tree-content {
        max-height: 200px;
        overflow-y: auto;
    }
    
    .folder-item {
        padding: 0.75rem;
        border: 1px solid var(--border-color);
        border-radius: 8px;
        margin-bottom: 0.5rem;
    }
    
    .folder-header {
        display: flex;
        align-items: center;
        gap: 0.75rem;
    }
    
    .folder-name {
        font-weight: 600;
        color: var(--text-primary);
        flex: 1;
    }
    
    .file-count {
        background: var(--bg-tertiary);
        color: var(--text-secondary);
        padding: 0.25rem 0.5rem;
        border-radius: 12px;
        font-size: 0.75rem;
        font-weight: 500;
    }
`;

// Inject additional styles
const styleSheet = document.createElement('style');
styleSheet.textContent = additionalStyles;
document.head.appendChild(styleSheet); 