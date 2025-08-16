import logging
import time
import threading
from datetime import datetime, timedelta
from typing import Optional, List, Dict, Any
from sqlalchemy import text, and_, or_
from sqlalchemy.exc import SQLAlchemyError
from extensions.ext_database import db
from models.custom_logs import DifyLogs, ErrorLog
from services.supabase_service import SupabaseService
import schedule

logger = logging.getLogger(__name__)

class DataSyncService:
    """Service để đồng bộ dữ liệu từ Supabase về local database"""
    
    def __init__(self):
        self.supabase_service = SupabaseService()
        self.is_running = False
        self.sync_thread = None
        self.last_sync_time = None
        self.sync_interval_minutes = 5  # Sync mỗi 5 phút
        
    def start_continuous_sync(self):
        """Bắt đầu đồng bộ liên tục"""
        if self.is_running:
            logger.warning("Sync service đã đang chạy")
            return
            
        self.is_running = True
        logger.info("Bắt đầu service đồng bộ dữ liệu liên tục")
        
        # Schedule sync job
        schedule.every(self.sync_interval_minutes).minutes.do(self._sync_job)
        
        # Chạy sync ngay lập tức
        self._sync_job()
        
        # Tạo thread để chạy scheduler
        self.sync_thread = threading.Thread(target=self._run_scheduler, daemon=True)
        self.sync_thread.start()
        
    def stop_continuous_sync(self):
        """Dừng đồng bộ liên tục"""
        self.is_running = False
        schedule.clear()
        logger.info("Đã dừng service đồng bộ dữ liệu")
        
    def _run_scheduler(self):
        """Chạy scheduler trong thread riêng"""
        while self.is_running:
            schedule.run_pending()
            time.sleep(1)
            
    def _sync_job(self):
        """Job đồng bộ dữ liệu"""
        try:
            logger.info("Bắt đầu đồng bộ dữ liệu từ Supabase")
            
            # Sync DifyLogs
            dify_synced = self.sync_dify_logs()
            logger.info(f"Đã đồng bộ {dify_synced} DifyLogs records")
            
            # Sync ErrorLogs
            error_synced = self.sync_error_logs()
            logger.info(f"Đã đồng bộ {error_synced} ErrorLog records")
            
            self.last_sync_time = datetime.now()
            logger.info(f"Hoàn thành đồng bộ lúc {self.last_sync_time}")
            
        except Exception as e:
            logger.error(f"Lỗi trong quá trình đồng bộ: {str(e)}")
            
    def sync_dify_logs(self, limit: int = 1000) -> int:
        """Đồng bộ DifyLogs từ Supabase về local"""
        try:
            # Lấy timestamp của record mới nhất trong local DB
            latest_local = db.session.query(DifyLogs.created_at).order_by(
                DifyLogs.created_at.desc()
            ).first()
            
            # Lấy dữ liệu từ Supabase (chỉ những record mới hơn)
            supabase_logs = self.supabase_service.get_dify_logs_since(
                since_timestamp=latest_local[0] if latest_local else None,
                limit=limit
            )
            
            if not supabase_logs:
                return 0
                
            synced_count = 0
            
            for log_data in supabase_logs:
                try:
                    # Kiểm tra xem record đã tồn tại chưa (dựa vào session_id và created_at)
                    existing = db.session.query(DifyLogs).filter(
                        and_(
                            DifyLogs.session_id == log_data.get('session_id'),
                            DifyLogs.created_at == log_data.get('created_at')
                        )
                    ).first()
                    
                    if existing:
                        continue
                        
                    # Tạo record mới
                    new_log = DifyLogs(
                        user_id=log_data.get('user_id'),
                        message=log_data.get('message'),
                        response=log_data.get('response'),
                        created_at=log_data.get('created_at'),
                        session_id=log_data.get('session_id'),
                        message_id=log_data.get('message_id'),
                        metadata=log_data.get('metadata')
                    )
                    
                    db.session.add(new_log)
                    synced_count += 1
                    
                except Exception as e:
                    logger.error(f"Lỗi khi sync DifyLog record: {str(e)}")
                    continue
                    
            db.session.commit()
            return synced_count
            
        except Exception as e:
            db.session.rollback()
            logger.error(f"Lỗi khi sync DifyLogs: {str(e)}")
            raise
            
    def sync_error_logs(self, limit: int = 1000) -> int:
        """Đồng bộ ErrorLogs từ Supabase về local"""
        try:
            # Lấy timestamp của record mới nhất trong local DB
            latest_local = db.session.query(ErrorLog.created_at).order_by(
                ErrorLog.created_at.desc()
            ).first()
            
            # Lấy dữ liệu từ Supabase (chỉ những record mới hơn)
            supabase_errors = self.supabase_service.get_error_logs_since(
                since_timestamp=latest_local[0] if latest_local else None,
                limit=limit
            )
            
            if not supabase_errors:
                return 0
                
            synced_count = 0
            
            for error_data in supabase_errors:
                try:
                    # Kiểm tra xem record đã tồn tại chưa
                    existing = db.session.query(ErrorLog).filter(
                        and_(
                            ErrorLog.user_id == error_data.get('user_id'),
                            ErrorLog.created_at == error_data.get('created_at'),
                            ErrorLog.error_message == error_data.get('error_message')
                        )
                    ).first()
                    
                    if existing:
                        continue
                        
                    # Tạo record mới
                    new_error = ErrorLog(
                        type_error=error_data.get('type_error'),
                        node=error_data.get('node'),
                        error_message=error_data.get('error_message'),
                        user_id=error_data.get('user_id'),
                        created_at=error_data.get('created_at')
                    )
                    
                    db.session.add(new_error)
                    synced_count += 1
                    
                except Exception as e:
                    logger.error(f"Lỗi khi sync ErrorLog record: {str(e)}")
                    continue
                    
            db.session.commit()
            return synced_count
            
        except Exception as e:
            db.session.rollback()
            logger.error(f"Lỗi khi sync ErrorLogs: {str(e)}")
            raise
            
    def manual_sync(self) -> Dict[str, Any]:
        """Đồng bộ thủ công và trả về kết quả"""
        try:
            start_time = datetime.now()
            
            dify_synced = self.sync_dify_logs()
            error_synced = self.sync_error_logs()
            
            end_time = datetime.now()
            duration = (end_time - start_time).total_seconds()
            
            result = {
                'success': True,
                'dify_logs_synced': dify_synced,
                'error_logs_synced': error_synced,
                'total_synced': dify_synced + error_synced,
                'duration_seconds': duration,
                'sync_time': end_time.isoformat()
            }
            
            self.last_sync_time = end_time
            return result
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'sync_time': datetime.now().isoformat()
            }
            
    def get_sync_status(self) -> Dict[str, Any]:
        """Lấy trạng thái sync hiện tại"""
        try:
            # Đếm records trong local DB
            dify_count = db.session.query(DifyLogs).count()
            error_count = db.session.query(ErrorLog).count()
            
            # Kiểm tra Supabase connection
            supabase_status = self.supabase_service.test_connection()
            
            return {
                'is_running': self.is_running,
                'last_sync_time': self.last_sync_time.isoformat() if self.last_sync_time else None,
                'sync_interval_minutes': self.sync_interval_minutes,
                'local_db_counts': {
                    'dify_logs': dify_count,
                    'error_logs': error_count
                },
                'supabase_status': supabase_status['status'],
                'next_sync': self._get_next_sync_time()
            }
            
        except Exception as e:
            return {
                'error': str(e),
                'is_running': self.is_running
            }
            
    def _get_next_sync_time(self) -> Optional[str]:
        """Lấy thời gian sync tiếp theo"""
        if not self.is_running or not self.last_sync_time:
            return None
            
        next_sync = self.last_sync_time + timedelta(minutes=self.sync_interval_minutes)
        return next_sync.isoformat()

# Global instance
data_sync_service = DataSyncService()
