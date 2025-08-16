from flask import Blueprint, jsonify, request
from datetime import datetime, timedelta
import random

# Create Blueprint
admin_logs_bp = Blueprint('admin_logs', __name__, url_prefix='/api/admin')

@admin_logs_bp.route('/logs', methods=['GET'])
def get_dify_logs():
    """Get Dify workflow logs"""
    try:
        # Generate mock Dify workflow logs for demonstration
        mock_logs = []
        
        # Generate some sample workflow logs
        statuses = ['completed', 'failed', 'running', 'success']
        users = ['user_001', 'user_002', 'user_003', 'user_004', 'user_005']
        
        workflows = [
            'What is machine learning?',
            'Generate a Python script for data analysis',
            'Translate this text to French',
            'Create a marketing plan',
            'Analyze customer feedback data',
            'Write a blog post about AI',
            'Summarize this document',
            'Generate code for API integration',
            'Create a product description',
            'Review and improve this content'
        ]
        
        for i in range(50):
            # Generate random time within last 24 hours
            random_minutes = random.randint(1, 1440)  # Last 24 hours
            created_time = datetime.now() - timedelta(minutes=random_minutes)
            
            status = random.choice(statuses)
            latency = random.randint(500, 5000) if status in ['completed', 'success', 'failed'] else None
            
            log = {
                'id': i + 1,
                'workflow_run_id': f'wf_{random.randint(10000000, 99999999)}-{random.randint(1000, 9999)}-{random.randint(1000, 9999)}-{random.randint(1000, 9999)}-{random.randint(100000000000, 999999999999)}',
                'conversation_id': f'conv_{random.randint(10000000, 99999999)}-{random.randint(1000, 9999)}-{random.randint(1000, 9999)}-{random.randint(1000, 9999)}-{random.randint(100000000000, 999999999999)}',
                'input_text': random.choice(workflows),
                'output_text': f'Generated output for workflow {i+1}...' if status in ['completed', 'success'] else None,
                'status': status,
                'created_at': created_time.isoformat(),
                'updated_at': created_time.isoformat(),
                'latency_ms': latency,
                'user_id': random.choice(users)
            }
            mock_logs.append(log)
        
        # Sort by created_at descending (newest first)
        mock_logs.sort(key=lambda x: x['created_at'], reverse=True)
        
        return jsonify({
            'success': True,
            'logs': mock_logs,
            'total': len(mock_logs),
            'source': 'Mock Dify Workflow Logs'
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'logs': []
        }), 500
