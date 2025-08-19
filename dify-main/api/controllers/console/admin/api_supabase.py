import logging
import os
import requests
from flask import Blueprint, request, jsonify
from dotenv import load_dotenv
from datetime import datetime, timedelta
import random

# Load environment variables
load_dotenv()

logger = logging.getLogger(__name__)

bp = Blueprint('api_supabase', __name__, url_prefix='/api/admin')

@bp.route('/supabase-errors', methods=['GET'])
def get_supabase_errors():
    """Get error data from Supabase with clear error handling, without any data simulation."""
    try:
        # Get query parameters
        limit = request.args.get('limit', 50, type=int)
        
        # Get Supabase credentials
        supabase_url = os.getenv('SUPABASE_URL')
        supabase_key = os.getenv('SUPABASE_KEY')

        # Check for credentials before proceeding
        if not supabase_url or not supabase_key:
            logger.warning("Supabase credentials (SUPABASE_URL, SUPABASE_KEY) not found in .env")
            return jsonify({
                'success': False,
                'message': 'Server configuration error: Supabase credentials are not set.',
                'source': 'Configuration Error'
            }), 500

        logger.info(f"Connecting to Supabase via HTTP: {supabase_url}")
        
        # Try connecting to Supabase
        api_url = f"{supabase_url}/rest/v1/error_logs"
        headers = {
            'apikey': supabase_key,
            'Authorization': f'Bearer {supabase_key}',
            'Content-Type': 'application/json'
        }
        
        params = {
            'order': 'created_at.desc',
            'limit': limit
        }
            
        response = requests.get(api_url, headers=headers, params=params, timeout=10)
            
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
                'source': 'Supabase API Error'
            }), response.status_code
            
    except requests.exceptions.RequestException as e:
        # THAY ĐỔI: Xử lý lỗi mạng và trả về lỗi JSON thay vì dữ liệu giả
        logger.error(f"Network error connecting to Supabase: {e}")
        return jsonify({
            'success': False,
            'message': f'Network error: Could not connect to Supabase. Details: {e}',
            'source': 'Network Error'
        }), 503  # 503 Service Unavailable is appropriate here
    
    except Exception as e:
        logger.error(f"An unexpected error occurred: {str(e)}")
        return jsonify({
            'success': False,
            'message': f'An unexpected server error occurred: {str(e)}',
            'source': 'Unexpected Server Error'
        }), 500

# XÓA: Toàn bộ các hàm get_realistic_error_data() và generate_realistic_stack_trace() đã được loại bỏ.