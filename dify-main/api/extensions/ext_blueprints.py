from configs import dify_config
from dify_app import DifyApp


def init_app(app: DifyApp):
    # register blueprint routers

    from flask_cors import CORS  # type: ignore

    from controllers.console import bp as console_app_bp
    from controllers.files import bp as files_bp
    from controllers.inner_api import bp as inner_api_bp
    from controllers.mcp import bp as mcp_bp
    from controllers.service_api import bp as service_api_bp
    from controllers.web import bp as web_bp

    CORS(
        service_api_bp,
        allow_headers=["Content-Type", "Authorization", "X-App-Code"],
        methods=["GET", "PUT", "POST", "DELETE", "OPTIONS", "PATCH"],
    )
    app.register_blueprint(service_api_bp)

    CORS(
        web_bp,
        resources={r"/*": {"origins": dify_config.WEB_API_CORS_ALLOW_ORIGINS}},
        supports_credentials=True,
        allow_headers=["Content-Type", "Authorization", "X-App-Code"],
        methods=["GET", "PUT", "POST", "DELETE", "OPTIONS", "PATCH"],
        expose_headers=["X-Version", "X-Env"],
    )

    app.register_blueprint(web_bp)

    CORS(
        console_app_bp,
        resources={r"/*": {"origins": dify_config.CONSOLE_CORS_ALLOW_ORIGINS}},
        supports_credentials=True,
        allow_headers=["Content-Type", "Authorization"],
        methods=["GET", "PUT", "POST", "DELETE", "OPTIONS", "PATCH"],
        expose_headers=["X-Version", "X-Env"],
    )

    app.register_blueprint(console_app_bp)

    CORS(files_bp, allow_headers=["Content-Type"], methods=["GET", "PUT", "POST", "DELETE", "OPTIONS", "PATCH"])
    app.register_blueprint(files_bp)

    app.register_blueprint(inner_api_bp)
    app.register_blueprint(mcp_bp)
    
    # Register admin logs blueprint
    try:
        from controllers.console.admin.logs import bp as admin_logs_bp
        app.register_blueprint(admin_logs_bp)
        print("✅ Admin logs blueprint registered successfully!")
    except Exception as e:
        print(f"⚠️ Failed to register admin logs blueprint: {e}")
    
    # Register Dify logs blueprint 
    try:
        from controllers.console.admin.dify_logs import admin_logs_bp
        app.register_blueprint(admin_logs_bp)
        print("✅ Dify logs blueprint registered successfully!")
    except Exception as e:
        print(f"⚠️ Failed to register dify logs blueprint: {e}")
    
    # Register data sync blueprint
    try:
        from controllers.console.admin.data_sync import bp as data_sync_bp
        app.register_blueprint(data_sync_bp)
        print("✅ Data sync blueprint registered successfully!")
    except Exception as e:
        print(f"⚠️ Failed to register data sync blueprint: {e}")
    
    # Register error sync blueprint
    try:
        from controllers.console.admin.error_sync import bp as error_sync_bp
        app.register_blueprint(error_sync_bp)
        print("✅ Error sync blueprint registered successfully!")
    except Exception as e:
        print(f"⚠️ Failed to register error sync blueprint: {e}")
    
    # Register Supabase API blueprint for /api/admin routes
    try:
        from controllers.console.admin.api_supabase import bp as api_supabase_bp
        app.register_blueprint(api_supabase_bp)
        print("✅ API Supabase blueprint registered successfully!")
    except Exception as e:
        print(f"⚠️ Failed to register API supabase blueprint: {e}")
    
    # Register Supabase direct access blueprint
    try:
        from controllers.console.admin.supabase_direct import bp as supabase_direct_bp
        app.register_blueprint(supabase_direct_bp)
        print("✅ Supabase direct blueprint registered successfully!")
    except Exception as e:
        print(f"⚠️ Failed to register supabase direct blueprint: {e}")
    
    # Register admin verification blueprint
    try:
        from controllers.console.admin.admin_verification import admin_verification_bp
        app.register_blueprint(admin_verification_bp)
        print("✅ Admin verification blueprint registered successfully!")
    except Exception as e:
        print(f"⚠️ Failed to register admin verification blueprint: {e}")
