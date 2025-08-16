from sqlalchemy import Column, Integer, String, Text, DateTime, BigInteger, Numeric
from sqlalchemy.sql import func
from extensions.ext_database import db


class DifyLogs(db.Model):
    __tablename__ = 'dify_logs'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    app_id = Column(String(255), nullable=True)
    conversation_id = Column(String(255), nullable=True, index=True)
    user_id = Column(String(255), nullable=True, index=True)
    input_text = Column(Text, nullable=True)
    output_text = Column(Text, nullable=True)
    latency_ms = Column(Integer, nullable=True)
    status_code = Column(Integer, nullable=True)
    created_at = Column(DateTime(timezone=True), nullable=True, default=func.current_timestamp(), index=True)
    dialog_count = Column(Numeric, nullable=True)
    work_run_id = Column(String, nullable=True)
    status = Column(String, nullable=True)
    template = Column(Text, nullable=True)
    Bot = Column(String, nullable=True)


class ErrorLog(db.Model):
    __tablename__ = 'error'
    
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    type_error = Column(String, nullable=True, index=True)
    node = Column(String, nullable=True)
    error_message = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), nullable=False, default=func.now(), index=True)
