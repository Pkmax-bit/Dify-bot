import random
import string
import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime, timedelta
from flask import Blueprint, request, jsonify
import redis

# Initialize Redis client for storing verification codes
try:
    redis_client = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)
    redis_client.ping()  # Test connection
except:
    redis_client = None
    print("⚠️ Redis not available, using in-memory storage")

# In-memory storage as fallback
verification_codes = {}

admin_verification_bp = Blueprint('admin_verification', __name__)

# Test route
@admin_verification_bp.route('/console/api/admin/test', methods=['GET'])
def test_route():
    return jsonify({'message': 'Admin verification routes working!', 'status': 'ok'})

# Email configuration from environment variables
SMTP_SERVER = os.getenv("ADMIN_EMAIL_HOST", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("ADMIN_EMAIL_PORT", "587"))
SMTP_USERNAME = os.getenv("ADMIN_EMAIL_USERNAME", "your-email@gmail.com")
SMTP_PASSWORD = os.getenv("ADMIN_EMAIL_PASSWORD", "your-app-password")
SMTP_USE_TLS = os.getenv("ADMIN_EMAIL_USE_TLS", "true").lower() == "true"

def generate_verification_code():
    """Generate a 6-digit verification code"""
    return ''.join(random.choices(string.digits, k=6))

def send_email(to_email, subject, body):
    """Send email using SMTP"""
    try:
        msg = MIMEMultipart()
        msg['From'] = SMTP_USERNAME
        msg['To'] = to_email
        msg['Subject'] = subject
        
        msg.attach(MIMEText(body, 'html'))
        
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        if SMTP_USE_TLS:
            server.starttls()
        server.login(SMTP_USERNAME, SMTP_PASSWORD)
        text = msg.as_string()
        server.sendmail(SMTP_USERNAME, to_email, text)
        server.quit()
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False

def store_code(key, code, expiry=300):
    """Store verification code with expiry"""
    if redis_client:
        redis_client.setex(key, expiry, code)
    else:
        # In-memory storage with timestamp
        verification_codes[key] = {
            'code': code,
            'expires': datetime.now() + timedelta(seconds=expiry)
        }

def get_code(key):
    """Get verification code"""
    if redis_client:
        return redis_client.get(key)
    else:
        # Check in-memory storage
        if key in verification_codes:
            entry = verification_codes[key]
            if datetime.now() < entry['expires']:
                return entry['code']
            else:
                del verification_codes[key]
        return None

def delete_code(key):
    """Delete verification code"""
    if redis_client:
        redis_client.delete(key)
    else:
        verification_codes.pop(key, None)

@admin_verification_bp.route('/console/api/admin/send-verification', methods=['POST'])
def send_verification_code():
    """Send verification code to configured admin email"""
    try:
        # Use configured admin email instead of user input
        email = SMTP_USERNAME  # Send to configured admin email
        
        if not email:
            return jsonify({'error': True, 'message': 'Admin email not configured'}), 500
        
        # Generate verification code
        code = generate_verification_code()
        
        # Use session ID or generate temporary ID for storing code
        import uuid
        session_id = request.headers.get('x-session-id', str(uuid.uuid4()))
        
        # Store code with session ID
        redis_key = f"admin_verification:{session_id}"
        store_code(redis_key, code, 300)  # 5 minutes
        
        # Email template
        subject = "Mã xác minh truy cập Admin Dashboard"
        body = f"""
        <html>
        <body>
            <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
                <h2 style="color: #333;">Xác minh truy cập Admin Dashboard</h2>
                <p>Xin chào,</p>
                <p>Bạn đã yêu cầu truy cập vào Admin Dashboard. Vui lòng sử dụng mã xác minh bên dưới:</p>
                
                <div style="background-color: #f5f5f5; padding: 20px; text-align: center; margin: 20px 0;">
                    <h1 style="color: #007bff; font-size: 32px; margin: 0; letter-spacing: 5px;">{code}</h1>
                </div>
                
                <p><strong>Lưu ý:</strong></p>
                <ul>
                    <li>Mã này có hiệu lực trong 5 phút</li>
                    <li>Không chia sẻ mã này với bất kỳ ai</li>
                    <li>Nếu bạn không yêu cầu mã này, vui lòng bỏ qua email</li>
                </ul>
                
                <p>Cảm ơn,<br>Admin Team</p>
            </div>
        </body>
        </html>
        """
        
        # Send email
        if send_email(email, subject, body):
            return jsonify({
                'error': False, 
                'message': 'Verification code sent successfully',
                'expires_in': 300,
                'session_id': session_id
            })
        else:
            return jsonify({'error': True, 'message': 'Failed to send email'}), 500
            
    except Exception as e:
        return jsonify({'error': True, 'message': str(e)}), 500

@admin_verification_bp.route('/console/api/admin/verify-code', methods=['POST'])
def verify_code():
    """Verify the submitted code"""
    try:
        data = request.get_json()
        code = data.get('code')
        session_id = data.get('session_id') or request.headers.get('x-session-id')
        
        if not code:
            return jsonify({'error': True, 'message': 'Code is required'}), 400
        
        if not session_id:
            return jsonify({'error': True, 'message': 'Session ID is required'}), 400
        
        # Get stored code using session ID
        redis_key = f"admin_verification:{session_id}"
        stored_code = get_code(redis_key)
        
        if not stored_code:
            return jsonify({'error': True, 'message': 'Verification code expired or not found'}), 400
        
        if stored_code != code:
            return jsonify({'error': True, 'message': 'Invalid verification code'}), 400
        
        # Code is valid, delete it
        delete_code(redis_key)
        
        # Generate session token for admin access
        session_token = ''.join(random.choices(string.ascii_letters + string.digits, k=32))
        session_key = f"admin_session:{session_id}"
        store_code(session_key, session_token, 3600)  # 1 hour
        
        return jsonify({
            'error': False,
            'message': 'Verification successful',
            'token': session_token,
            'expires_in': 3600
        })
        
    except Exception as e:
        return jsonify({'error': True, 'message': str(e)}), 500

@admin_verification_bp.route('/console/api/admin/check-session', methods=['GET'])
def check_admin_session():
    """Check if admin session is valid"""
    try:
        session_id = request.args.get('session_id') or request.headers.get('x-session-id')
        
        if not session_id:
            return jsonify({'error': False, 'valid': False})
        
        session_key = f"admin_session:{session_id}"
        session_token = get_code(session_key)
        
        if session_token:
            return jsonify({'error': False, 'valid': True})
        else:
            return jsonify({'error': False, 'valid': False})
            
    except Exception as e:
        return jsonify({'error': True, 'message': str(e)}), 500

@admin_verification_bp.route('/console/api/admin/logout', methods=['POST'])
def admin_logout():
    """Logout admin and clear session"""
    try:
        session_id = request.json.get('session_id') if request.json else None
        session_id = session_id or request.headers.get('x-session-id')
        
        if session_id:
            # Delete admin session
            session_key = f"admin_session:{session_id}"
            delete_code(session_key)
            
            return jsonify({
                'error': False,
                'message': 'Logged out successfully'
            })
        else:
            return jsonify({
                'error': False,
                'message': 'No active session found'
            })
            
    except Exception as e:
        return jsonify({'error': True, 'message': str(e)}), 500
