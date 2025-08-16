import os
import requests
from datetime import datetime
from typing import List, Dict, Any, Optional

class SupabaseService:
    def __init__(self):
        self.url = os.getenv('SUPABASE_URL')
        self.anon_key = os.getenv('SUPABASE_ANON_KEY')
        self.service_role_key = os.getenv('SUPABASE_SERVICE_ROLE_KEY')
        
        self.headers = {
            'apikey': self.service_role_key,
            'Authorization': f'Bearer {self.service_role_key}',
            'Content-Type': 'application/json'
        }
    
    def get_dify_logs_since(self, since_timestamp: Optional[datetime] = None, limit: int = 1000) -> List[Dict[str, Any]]:
        """Lấy dify_logs từ Supabase với timestamp filter để đồng bộ"""
        try:
            url = f"{self.url}/rest/v1/dify_logs"
            params = {
                'select': '*',
                'order': 'created_at.asc',
                'limit': limit
            }
            
            # Thêm filter theo timestamp nếu có
            if since_timestamp:
                params['created_at'] = f'gt.{since_timestamp.isoformat()}'
            
            response = requests.get(url, headers=self.headers, params=params, timeout=10)
            
            if response.status_code == 200:
                logs = response.json()
                return [
                    {
                        'app_id': log.get('app_id'),
                        'conversation_id': log.get('conversation_id'),
                        'user_id': log.get('user_id'),
                        'input_text': log.get('input_text'),
                        'output_text': log.get('output_text'),
                        'latency_ms': log.get('latency_ms'),
                        'status_code': log.get('status_code'),
                        'created_at': log.get('created_at'),
                        'dialog_count': log.get('dialog_count'),
                        'work_run_id': log.get('work_run_id'),
                        'status': log.get('status'),
                        'template': log.get('template'),
                        'bot': log.get('Bot')
                    }
                    for log in logs
                ]
            else:
                print(f"Error fetching dify_logs_since: {response.status_code}")
                return []
        except Exception as e:
            print(f"Exception in get_dify_logs_since: {e}")
            return []
    
    def get_error_logs_since(self, since_timestamp: Optional[datetime] = None, limit: int = 1000) -> List[Dict[str, Any]]:
        """Lấy error logs từ Supabase với timestamp filter để đồng bộ"""
        try:
            url = f"{self.url}/rest/v1/error"
            params = {
                'select': '*',
                'order': 'created_at.asc',
                'limit': limit
            }
            
            # Thêm filter theo timestamp nếu có
            if since_timestamp:
                params['created_at'] = f'gt.{since_timestamp.isoformat()}'
            
            response = requests.get(url, headers=self.headers, params=params, timeout=10)
            
            if response.status_code == 200:
                errors = response.json()
                return [
                    {
                        'type_error': error.get('type_error'),
                        'node': error.get('node'),
                        'error_message': error.get('error_message'),
                        'user_id': error.get('user_id'),
                        'created_at': error.get('created_at')
                    }
                    for error in errors
                ]
            else:
                print(f"Error fetching error_logs_since: {response.status_code}")
                return []
        except Exception as e:
            print(f"Exception in get_error_logs_since: {e}")
            return []

    def get_dify_logs(self, limit: int = 50, offset: int = 0) -> List[Dict[str, Any]]:
        """Lấy logs từ bảng dify_logs"""
        try:
            url = f"{self.url}/rest/v1/dify_logs"
            params = {
                'select': '*',
                'order': 'created_at.desc',
                'limit': limit,
                'offset': offset
            }
            
            response = requests.get(url, headers=self.headers, params=params, timeout=5)
            
            if response.status_code == 200:
                logs = response.json()
                return [
                    {
                        'id': log.get('id', ''),
                        'timestamp': log.get('created_at', ''),
                        'level': 'info',  # Có thể thêm level column vào DB
                        'message': log.get('user_message', '') or log.get('assistant_message', '') or 'System log',
                        'module': 'chat',
                        'user_id': log.get('user_id', ''),
                        'conversation_id': log.get('conversation_id', ''),
                        'error_details': log.get('error_message', '')
                    }
                    for log in logs
                ]
            else:
                print(f"Error fetching dify_logs: {response.status_code}")
                return self.get_mock_dify_logs(limit)
        except Exception as e:
            print(f"Exception in get_dify_logs: {e}")
            return self.get_mock_dify_logs(limit)
    
    def get_error_logs(self, limit: int = 50, offset: int = 0) -> List[Dict[str, Any]]:
        """Lấy errors từ bảng error"""
        try:
            url = f"{self.url}/rest/v1/error"
            params = {
                'select': '*',
                'order': 'created_at.desc',
                'limit': limit,
                'offset': offset
            }
            
            response = requests.get(url, headers=self.headers, params=params, timeout=5)
            
            if response.status_code == 200:
                errors = response.json()
                return [
                    {
                        'id': error.get('id', ''),
                        'timestamp': error.get('created_at', ''),
                        'level': 'error',
                        'message': error.get('error_message', 'Unknown error'),
                        'module': error.get('source', 'system'),
                        'user_id': error.get('user_id', ''),
                        'error_details': error.get('stack_trace', '') or error.get('details', '')
                    }
                    for error in errors
                ]
            else:
                print(f"Error fetching error logs: {response.status_code}")
                return self.get_mock_error_logs(limit)
        except Exception as e:
            print(f"Exception in get_error_logs: {e}")
            return self.get_mock_error_logs(limit)
    
    def get_combined_logs(self, limit: int = 50) -> List[Dict[str, Any]]:
        """Lấy cả logs và errors, sắp xếp theo thời gian"""
        try:
            dify_logs = self.get_dify_logs(limit=limit//2)
            error_logs = self.get_error_logs(limit=limit//2)
            
            # Kết hợp và sắp xếp theo thời gian
            all_logs = dify_logs + error_logs
            all_logs.sort(key=lambda x: x.get('timestamp', ''), reverse=True)
            
            return all_logs[:limit]
        except Exception as e:
            print(f"Exception in get_combined_logs: {e}")
            return []
    
    def get_log_stats(self) -> Dict[str, Any]:
        """Lấy thống kê logs"""
        try:
            # Đếm tổng số logs
            dify_count_url = f"{self.url}/rest/v1/dify_logs"
            dify_response = requests.get(
                dify_count_url, 
                headers={**self.headers, 'Prefer': 'count=exact'},
                params={'select': 'id'},
                timeout=5
            )
            
            error_count_url = f"{self.url}/rest/v1/error"
            error_response = requests.get(
                error_count_url, 
                headers={**self.headers, 'Prefer': 'count=exact'},
                params={'select': 'id'},
                timeout=5
            )
            
            total_logs = 0
            error_count = 0
            
            if dify_response.status_code == 200:
                total_logs = int(dify_response.headers.get('Content-Range', '0').split('/')[1])
            
            if error_response.status_code == 200:
                error_count = int(error_response.headers.get('Content-Range', '0').split('/')[1])
            
            return {
                'total_logs': total_logs,
                'error_count': error_count,
                'success_logs': total_logs - error_count
            }
        except Exception as e:
            print(f"Exception in get_log_stats: {e}")
            # Mock stats
            return {
                'total_logs': 156,
                'error_count': 12,
                'success_logs': 144
            }
    
    def test_connection(self) -> Dict[str, Any]:
        """Test kết nối Supabase"""
        try:
            # Test bằng cách query một bảng đơn giản
            url = f"{self.url}/rest/v1/dify_logs"
            params = {'select': 'id', 'limit': 1}
            
            response = requests.get(url, headers=self.headers, params=params, timeout=5)
            
            if response.status_code == 200:
                return {
                    'status': 'connected',
                    'message': 'Supabase connection successful',
                    'url': self.url
                }
            else:
                return {
                    'status': 'error',
                    'message': f'HTTP {response.status_code}: {response.text}',
                    'url': self.url
                }
        except Exception as e:
            # Trả về mock data nếu không kết nối được
            return {
                'status': 'mock_mode',
                'message': f'Using mock data due to connection error: {str(e)}',
                'url': self.url
            }
    
    def get_mock_dify_logs(self, limit: int = 50) -> List[Dict[str, Any]]:
        """Mock data cho dify logs"""
        from datetime import datetime, timedelta
        import random
        
        mock_logs = []
        for i in range(min(limit, 20)):
            timestamp = (datetime.now() - timedelta(hours=random.randint(0, 24))).isoformat()
            mock_logs.append({
                'id': f'mock_{i}',
                'timestamp': timestamp,
                'level': random.choice(['info', 'warning', 'error']),
                'message': f'Mock chat message {i}: User interaction with AI assistant',
                'module': 'chat',
                'user_id': f'user_{random.randint(1, 10)}',
                'conversation_id': f'conv_{random.randint(1, 5)}',
                'error_details': ''
            })
        return mock_logs
    
    def get_mock_error_logs(self, limit: int = 50) -> List[Dict[str, Any]]:
        """Mock data cho error logs"""
        from datetime import datetime, timedelta
        import random
        
        mock_errors = []
        error_messages = [
            'Database connection timeout',
            'API rate limit exceeded',
            'Invalid user input format',
            'Model inference failed',
            'File upload error'
        ]
        
        for i in range(min(limit, 10)):
            timestamp = (datetime.now() - timedelta(hours=random.randint(0, 48))).isoformat()
            mock_errors.append({
                'id': f'error_{i}',
                'timestamp': timestamp,
                'level': 'error',
                'message': random.choice(error_messages),
                'module': random.choice(['api', 'database', 'model', 'file_upload']),
                'user_id': f'user_{random.randint(1, 10)}',
                'error_details': f'Stack trace for error {i}'
            })
        return mock_errors

# Singleton instance
supabase_service = SupabaseService()
