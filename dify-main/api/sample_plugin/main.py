
# Sample Plugin Implementation
import json

def hello_endpoint(request_data):
    """
    Simple hello endpoint
    """
    message = request_data.get('message', 'Hello from Plugin!')
    
    return {
        'status': 'success',
        'response': f"Plugin says: {message}",
        'timestamp': '2025-08-14T13:00:00Z'
    }

# Plugin entry point
def handle_request(endpoint, method, data):
    if endpoint == '/hello' and method == 'POST':
        return hello_endpoint(data)
    else:
        return {'error': 'Endpoint not found'}
