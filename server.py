# -*- coding: utf-8 -*-
import sys
import os

# Fix encoding for Windows
if sys.platform.startswith('win'):
    os.environ['PYTHONIOENCODING'] = 'utf-8'
    sys.stdout.reconfigure(encoding='utf-8')

from flask import Flask, render_template, request, jsonify
import subprocess
import pandas as pd
from datetime import datetime
from pathlib import Path
import threading
import time

app = Flask(__name__)

# Store tracking status
tracking_status = {
    'active': False,
    'output': '',
    'progress': 0
}

@app.route('/')
def index():
    """Main page"""
    return render_template('index.html')

@app.route('/api/start-tracking', methods=['POST'])
def start_tracking():
    """Start tracking in background"""
    data = request.json
    choice = data.get('choice', '1')
    
    if tracking_status['active']:
        return jsonify({'error': 'Tracking already in progress'}), 400
    
    tracking_status['active'] = True
    tracking_status['output'] = ''
    tracking_status['progress'] = 0
    
    # Run in background thread
    def run_tracking():
        try:
            # Set environment variables for custom tracking
            env = os.environ.copy()
            
            if choice == '5':
                # Get custom data from request
                business = data.get('business', '').strip()
                location = data.get('location', '').strip()
                keywords = data.get('keywords', '').strip()
                
                # Validate - check for placeholder text
                if not business or business == 'Custom Business':
                    tracking_status['output'] = "❌ ERROR: Please enter a valid business name"
                    tracking_status['active'] = False
                    return
                
                if not location or location == 'Custom Location':
                    tracking_status['output'] = "❌ ERROR: Please enter a valid location (e.g., Mumbai, Delhi, Bangalore)"
                    tracking_status['active'] = False
                    return
                
                if not keywords or keywords.count('\n') == 0:
                    tracking_status['output'] = "❌ ERROR: Please enter at least one keyword"
                    tracking_status['active'] = False
                    return
                
                # Set environment variables with validated data
                env['CUSTOM_BUSINESS'] = business
                env['CUSTOM_LOCATION'] = location
                env['CUSTOM_KEYWORDS'] = keywords
                
                tracking_status['output'] += f"📝 Custom Setup:\n"
                tracking_status['output'] += f"  • Business: {business}\n"
                tracking_status['output'] += f"  • Location: {location}\n"
                tracking_status['output'] += f"  • Keywords: {len(keywords.split(chr(10)))} keywords\n\n"
            
            cmd = f'echo {choice} | python gmb_tracker_backend.py'
            
            process = subprocess.Popen(
                cmd,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                encoding='utf-8',
                errors='replace',
                bufsize=1,
                universal_newlines=True,
                env=env
            )
            
            for line in process.stdout:
                try:
                    if line:
                        tracking_status['output'] += line
                        
                        # Count keywords
                        if 'KEYWORD' in line or 'TRACKING' in line:
                            tracking_status['progress'] += 1
                except Exception as decode_error:
                    # Fallback if unicode issues
                    try:
                        tracking_status['output'] += str(line.encode('utf-8', errors='replace'))
                    except:
                        pass
                
                time.sleep(0.01)
            
            process.wait()
            tracking_status['active'] = False
        
        except Exception as e:
            tracking_status['output'] += f"\n❌ Error: {str(e)}\n"
            tracking_status['active'] = False
    
    # Start tracking in background thread
    thread = threading.Thread(target=run_tracking, daemon=True)
    thread.start()
    
    return jsonify({'status': 'started'})

@app.route('/api/tracking-status')
def tracking_status_api():
    """Get tracking status and output"""
    return jsonify(tracking_status)

@app.route('/api/results')
def get_results():
    """Get latest tracking results"""
    progress_csv = Path('gmb_ranking_progress.csv')
    
    if progress_csv.exists():
        try:
            # Try UTF-8 first
            try:
                df = pd.read_csv(progress_csv, encoding='utf-8')
            except:
                # Fallback to latin1 if UTF-8 fails
                df = pd.read_csv(progress_csv, encoding='latin1')
            
            found = len(df[df['found'] == True])
            total = len(df)
            success_rate = float((found/total*100)) if total > 0 else 0
            
            # Convert dataframe to dict safely
            data_records = []
            for _, row in df.iterrows():
                record = {}
                for col in df.columns:
                    val = row[col]
                    # Handle different data types
                    if pd.isna(val):
                        record[col] = None
                    elif isinstance(val, (int, float)):
                        record[col] = val
                    else:
                        record[col] = str(val)
                data_records.append(record)
            
            return jsonify({
                'found': int(found),
                'total': int(total),
                'success_rate': success_rate,
                'data': data_records
            })
        
        except Exception as e:
            return jsonify({
                'error': f'Error reading CSV: {str(e)}',
                'found': 0,
                'total': 0,
                'success_rate': 0,
                'data': []
            }), 200
    
    return jsonify({
        'error': 'No results file found',
        'found': 0,
        'total': 0,
        'success_rate': 0,
        'data': []
    }), 200

@app.route('/api/download-csv')
def download_csv():
    """Download results as CSV"""
    progress_csv = Path('gmb_ranking_progress.csv')
    
    if progress_csv.exists():
        try:
            try:
                df = pd.read_csv(progress_csv, encoding='utf-8')
            except:
                df = pd.read_csv(progress_csv, encoding='latin1')
            
            filename = f'gmb_ranking_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
            
            # Save new file with UTF-8 encoding
            df.to_csv(filename, index=False, encoding='utf-8')
            
            return jsonify({
                'filename': filename,
                'success': True,
                'message': 'CSV downloaded successfully'
            })
        
        except Exception as e:
            return jsonify({
                'success': False,
                'error': f'Error downloading CSV: {str(e)}'
            }), 500
    
    return jsonify({
        'success': False,
        'error': 'No results file found'
    }), 404

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def server_error(error):
    """Handle 500 errors"""
    return jsonify({'error': 'Server error'}), 500

if __name__ == '__main__':
    print("\n" + "="*60)
    print("🚀 GMB Ranking Tracker Server Starting...")
    print("="*60)
    print("📊 Open: http://localhost:5000")
    print("⏹️  Press Ctrl+C to stop")
    print("="*60 + "\n")
    
    try:
        app.run(debug=False, port=5000, host='127.0.0.1')
    except Exception as e:
        print(f"❌ Error starting server: {str(e)}")
