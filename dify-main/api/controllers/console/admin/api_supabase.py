import logging
import os
import requests
from flask import Blueprint, request, jsonify
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

logger = logging.getLogger(__name__)

bp = Blueprint('api_supabase', __name__, url_prefix='/api/admin')

@bp.route('/supabase-error_logs', methods=['GET'])
def get_supabase_error_logs():
    """Get error data from Supabase with clear error handling, using the correct service role key."""
    try:
        # Get query parameters
        limit = request.args.get('limit', 50, type=int)
        
        # Get Supabase credentials from environment variables
        supabase_url = os.getenv('SUPABASE_URL', "https://nuadflxsgwazllqiswfo.supabase.co")
        supabase_key = os.getenv('SUPABASE_SERVICE_ROLE_KEY')  # Load từ .env file
        
        # Check for credentials before proceeding
        if not supabase_url or not supabase_key:
            logger.warning("Supabase credentials (SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY) not found in .env")
            return jsonify({
                'success': False,
                'message': 'Server configuration error: Supabase service role key is not set.',
                'source': 'Configuration Error'
            }), 500

        logger.info(f"Connecting to Supabase via HTTP: {supabase_url}")
        
        # Try connecting to Supabase
        api_url = f"{supabase_url}/rest/v1/error_logs"
        headers = {
            'apikey': supabase_key,
            'Authorization': f'Bearer {supabase_key}',  # SỬA: Dùng biến thay vì hardcode
            'Content-Type': 'application/json'
        }
        
        params = {
            'order': 'created_at.desc',
            'limit': limit,
            'select': '*'  # Đảm bảo lấy tất cả các cột
        }
        
        # Log để debug
        logger.info(f"Making request to: {api_url}")
        logger.info(f"Headers: {dict(headers)}")  # Không log key để bảo mật
        logger.info(f"Params: {params}")
            
        response = requests.get(api_url, headers=headers, params=params, timeout=10)
        
        # Log response để debug
        logger.info(f"Response status: {response.status_code}")
        logger.info(f"Response headers: {dict(response.headers)}")
            
        if response.status_code == 200:
            data = response.json()
            if data:  # If we have real data
                logger.info(f"Successfully fetched {len(data)} real error records")
                return jsonify({
                    'success': True,
                    'errors': data,
                    'count': len(data),
                    'total': len(data),
                    'source': 'Supabase Database'
                })
            else:
                # The table is empty, return an empty list
                logger.info("Error table is empty, returning empty list.")
                return jsonify({
                    'success': True,
                    'errors': [],
                    'count': 0,
                    'total': 0,
                    'source': 'Supabase Database (empty)'
                })
        else:
            # Return the actual error from Supabase
            error_message = f"Failed to fetch from Supabase. Status: {response.status_code}"
            try:
                error_details = response.json().get('message', response.text)
                error_message += f" - Details: {error_details}"
            except Exception:
                error_message += f" - Response: {response.text}"

            logger.warning(error_message)
            return jsonify({
                'success': False,
                'message': error_message,
                'source': 'Supabase API Error',
                'status_code': response.status_code,
                'response_text': response.text[:500]  # Giới hạn độ dài response
            }), response.status_code
            
    except requests.exceptions.RequestException as e:
        logger.error(f"Network error connecting to Supabase: {e}")
        return jsonify({
            'success': False,
            'message': f'Network error: Could not connect to Supabase. Details: {str(e)}',
            'source': 'Network Error'
        }), 503
    
    except Exception as e:
        logger.error(f"An unexpected error occurred: {str(e)}")
        return jsonify({
            'success': False,
            'message': f'An unexpected server error occurred: {str(e)}',
            'source': 'Unexpected Server Error'
        }), 500