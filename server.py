# ✅ PRODUCTION-READY SERVER
# 🚀 Optimized for Local + Render Deployment
# -*- coding: utf-8 -*-
import sys
import os

# Fix encoding for Windows
if sys.platform.startswith('win'):
    os.environ['PYTHONIOENCODING'] = 'utf-8'
    sys.stdout.reconfigure(encoding='utf-8')

from flask import Flask, render_template, request, jsonify, send_file
from flask_cors import CORS
import subprocess
import pandas as pd
from datetime import datetime
from pathlib import Path
import threading
import time
import logging
import io

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

# Store tracking status
tracking_status = {
    'active': False,
    'output': '',
    'progress': 0,
    'current_keyword': '',
    'total_keywords': 0
}

# ============================================================================
# 🎯 ROUTES
# ============================================================================

@app.route('/')
def index():
    """Main page"""
    try:
        return render_template('index.html')
    except Exception as e:
        logger.error(f"Error rendering index: {e}")
        return jsonify({'error': 'Could not load template'}), 500

@app.route('/api/start-tracking', methods=['POST'])
def start_tracking():
    """Start tracking in background"""
    try:
        data = request.json
        choice = data.get('choice', '1')
        
        if tracking_status['active']:
            return jsonify({'error': 'Tracking already in progress'}), 400
        
        # Reset status
        tracking_status['active'] = True
        tracking_status['output'] = ''
        tracking_status['progress'] = 0
        tracking_status['current_keyword'] = ''
        tracking_status['total_keywords'] = 0
        
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
                        logger.warning("Invalid business name provided")
                        return
                    
                    if not location or location == 'Custom Location':
                        tracking_status['output'] = "❌ ERROR: Please enter a valid location (e.g., Mumbai, Delhi, Bangalore)"
                        tracking_status['active'] = False
                        logger.warning("Invalid location provided")
                        return
                    
                    if not keywords or keywords.count('\n') == 0:
                        tracking_status['output'] = "❌ ERROR: Please enter at least one keyword"
                        tracking_status['active'] = False
                        logger.warning("No keywords provided")
                        return
                    
                    # Set environment variables with validated data
                    env['CUSTOM_BUSINESS'] = business
                    env['CUSTOM_LOCATION'] = location
                    env['CUSTOM_KEYWORDS'] = keywords
                    
                    keyword_count = len([k for k in keywords.split('\n') if k.strip()])
                    tracking_status['total_keywords'] = keyword_count
                    
                    tracking_status['output'] += f"📝 Custom Setup:\n"
                    tracking_status['output'] += f"  • Business: {business}\n"
                    tracking_status['output'] += f"  • Location: {location}\n"
                    tracking_status['output'] += f"  • Keywords: {keyword_count} keywords\n"
                    tracking_status['output'] += f"\n{'='*80}\n\n"
                    
                    logger.info(f"Starting tracking for {business} in {location} with {keyword_count} keywords")
                else:
                    logger.info(f"Starting tracking with preset choice: {choice}")
                
                # Run the scraper backend
                cmd = [sys.executable, 'gmb_tracker_backend.py']
                
                process = subprocess.Popen(
                    cmd,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    text=True,
                    encoding='utf-8',
                    errors='replace',
                    bufsize=1,
                    universal_newlines=True,
                    env=env,
                    stdin=subprocess.PIPE
                )
                
                # Send choice to stdin
                if choice != '5':
                    try:
                        process.stdin.write(f"{choice}\n")
                        process.stdin.flush()
                    except:
                        pass
                
                # Read output line by line
                line_count = 0
                for line in process.stdout:
                    try:
                        if line:
                            tracking_status['output'] += line
                            line_count += 1
                            
                            # Update progress markers
                            if 'KEYWORD' in line and '/' in line:
                                try:
                                    parts = line.split('/')
                                    if len(parts) >= 2:
                                        current = parts[0].strip().split()[-1]
                                        total = parts[1].strip().split()[0]
                                        tracking_status['progress'] = int(current)
                                        tracking_status['current_keyword'] = line.strip()
                                except:
                                    pass
                            
                            if 'TRACKING:' in line:
                                tracking_status['current_keyword'] = line.strip()
                    
                    except Exception as e:
                        logger.error(f"Error processing output line: {e}")
                        continue
                    
                    time.sleep(0.01)
                
                process.wait()
                
                if process.returncode != 0:
                    tracking_status['output'] += f"\n⚠️ Process exited with code: {process.returncode}\n"
                    logger.warning(f"Backend process exited with code: {process.returncode}")
                else:
                    logger.info("Backend process completed successfully")
                
                tracking_status['active'] = False
        
        except Exception as e:
            tracking_status['output'] += f"\n❌ Tracking Error: {str(e)}\n"
            tracking_status['active'] = False
            logger.error(f"Error in run_tracking: {e}")
        
        # Start tracking in background thread
        thread = threading.Thread(target=run_tracking, daemon=True)
        thread.start()
        
        return jsonify({'status': 'started', 'message': 'Tracking started in background'})
    
    except Exception as e:
        logger.error(f"Error in start_tracking: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/tracking-status')
def tracking_status_api():
    """Get tracking status and output"""
    try:
        return jsonify(tracking_status)
    except Exception as e:
        logger.error(f"Error in tracking_status_api: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/results')
def get_results():
    """Get latest tracking results"""
    try:
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
                
                logger.info(f"Results: {found}/{total} found ({success_rate:.1f}%)")
                
                return jsonify({
                    'found': int(found),
                    'total': int(total),
                    'success_rate': success_rate,
                    'data': data_records
                })
            
            except Exception as e:
                logger.error(f"Error reading CSV: {e}")
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
    
    except Exception as e:
        logger.error(f"Error in get_results: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/download-csv')
def download_csv():
    """Download results as CSV"""
    try:
        progress_csv = Path('gmb_ranking_progress.csv')
        
        if progress_csv.exists():
            try:
                try:
                    df = pd.read_csv(progress_csv, encoding='utf-8')
                except:
                    df = pd.read_csv(progress_csv, encoding='latin1')
                
                # Create CSV in memory
                output = io.StringIO()
                df.to_csv(output, index=False, encoding='utf-8')
                output.seek(0)
                
                filename = f'gmb_ranking_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
                
                logger.info(f"CSV downloaded: {filename}")
                
                return send_file(
                    io.BytesIO(output.getvalue().encode('utf-8')),
                    mimetype='text/csv',
                    as_attachment=True,
                    download_name=filename
                )
            
            except Exception as e:
                logger.error(f"Error downloading CSV: {e}")
                return jsonify({
                    'success': False,
                    'error': f'Error downloading CSV: {str(e)}'
                }), 500
        
        return jsonify({
            'success': False,
            'error': 'No results file found'
        }), 404
    
    except Exception as e:
        logger.error(f"Error in download_csv: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/health')
def health():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'timestamp': datetime.now().isoformat()})

# ============================================================================
# 🔧 ERROR HANDLERS
# ============================================================================

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    logger.warning(f"404 Error: {error}")
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def server_error(error):
    """Handle 500 errors"""
    logger.error(f"500 Error: {error}")
    return jsonify({'error': 'Server error'}), 500

@app.before_request
def before_request():
    """Log incoming requests"""
    if request.method != 'OPTIONS':
        logger.debug(f"{request.method} {request.path}")

# ============================================================================
# 🚀 MAIN
# ============================================================================

if __name__ == '__main__':
    print("\n" + "="*60)
    print("🚀 GMB Ranking Tracker Server Starting...")
    print("="*60)
    
    # Detect environment
    is_render = os.environ.get('RENDER', False)
    port = int(os.environ.get('PORT', 5000))
    host = '0.0.0.0' if is_render else '127.0.0.1'
    
    print(f"📊 Environment: {'Render Cloud' if is_render else 'Local'}")
    print(f"🌐 Host: {host}")
    print(f"⚙️  Port: {port}")
    
    if not is_render:
        print("📍 Open: http://localhost:5000")
    
    print("⏹️  Press Ctrl+C to stop")
    print("="*60 + "\n")
    
    try:
        # Render-compatible settings
        app.run(
            debug=False,
            port=port,
            host=host,
            threaded=True,
            use_reloader=False
        )
    except Exception as e:
        logger.error(f"❌ Error starting server: {str(e)}")
        print(f"❌ Error: {e}")
        sys.exit(1)
