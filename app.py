from flask import Flask, render_template, request, send_file, flash, redirect, url_for
import os
import json
import glob
import shutil
import zipfile
import tempfile
from datetime import datetime, time
from dateutil import parser
import pandas as pd
from werkzeug.utils import secure_filename
import uuid

app = Flask(__name__)
app.secret_key = 'your-secret-key-change-this-in-production'
app.config['MAX_CONTENT_LENGTH'] = 500 * 1024 * 1024  # 500MB max file size

# Import the processing logic from the original script
from json_processor import (
    SIM_MANNEQUINS, MANNEQUIN_MAP, SIM_SCHEDULES, COURSE_DATE_RANGES, 
    COURSE_START_DATES, DAY_OFFSET_TO_SIM, get_course_for_date,
    get_sim_for_course_date, in_sim_time_window, parse_one_json,
    process_data_pipeline
)

UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'outputs'
ALLOWED_EXTENSIONS = {'json'}

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def extract_json_files(upload_folder, temp_json_folder):
    """Recursively find all JSON files and copy them to a flat structure"""
    json_count = 0
    
    for root, dirs, files in os.walk(upload_folder):
        for file in files:
            if file.lower().endswith('.json'):
                source_path = os.path.join(root, file)
                # Create unique filename to avoid conflicts
                unique_filename = f"{uuid.uuid4().hex}_{file}"
                dest_path = os.path.join(temp_json_folder, unique_filename)
                shutil.copy2(source_path, dest_path)
                json_count += 1
    
    return json_count

def create_zip_file(source_folder, zip_path):
    """Create a zip file from the source folder"""
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(source_folder):
            for file in files:
                file_path = os.path.join(root, file)
                arc_name = os.path.relpath(file_path, source_folder)
                zipf.write(file_path, arc_name)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_files():
    if 'files' not in request.files:
        flash('No files selected', 'error')
        return redirect(url_for('index'))
    
    files = request.files.getlist('files')
    
    if not files or all(f.filename == '' for f in files):
        flash('No files selected', 'error')
        return redirect(url_for('index'))
    
    try:
        # Create unique session folder
        session_id = str(uuid.uuid4())
        session_upload_folder = os.path.join(UPLOAD_FOLDER, session_id)
        session_output_folder = os.path.join(OUTPUT_FOLDER, session_id)
        temp_json_folder = os.path.join(session_upload_folder, 'extracted_json')
        
        os.makedirs(session_upload_folder, exist_ok=True)
        os.makedirs(session_output_folder, exist_ok=True)
        os.makedirs(temp_json_folder, exist_ok=True)
        
        # Save uploaded files
        uploaded_files = []
        for file in files:
            if file.filename != '':
                filename = secure_filename(file.filename)
                filepath = os.path.join(session_upload_folder, filename)
                file.save(filepath)
                uploaded_files.append(filepath)
        
        # Extract all JSON files from uploaded files/folders
        json_count = extract_json_files(session_upload_folder, temp_json_folder)
        
        if json_count == 0:
            flash('No JSON files found in the uploaded content', 'error')
            shutil.rmtree(session_upload_folder)
            return redirect(url_for('index'))
        
        # Process the JSON files using the original logic
        valid_count, unknown_count = process_data_pipeline(temp_json_folder, session_output_folder)
        
        # Create zip file for download
        zip_filename = f'sorted_vital_signs_{datetime.now().strftime("%Y%m%d_%H%M%S")}.zip'
        zip_path = os.path.join(session_output_folder, zip_filename)
        create_zip_file(session_output_folder, zip_path)
        
        # Clean up upload folder but keep output for download
        shutil.rmtree(session_upload_folder)
        
        flash(f'Processing complete! Found {json_count} JSON files. {valid_count} valid records processed, {unknown_count} unknown records.', 'success')
        
        return send_file(zip_path, as_attachment=True, download_name=zip_filename)
        
    except Exception as e:
        flash(f'Error processing files: {str(e)}', 'error')
        # Clean up on error
        if 'session_upload_folder' in locals() and os.path.exists(session_upload_folder):
            shutil.rmtree(session_upload_folder)
        if 'session_output_folder' in locals() and os.path.exists(session_output_folder):
            shutil.rmtree(session_output_folder)
        return redirect(url_for('index'))

@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port) 