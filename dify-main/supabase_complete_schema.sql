-- Comprehensive Dify Database Schema for Supabase
-- This file contains all necessary tables for the Dify application

-- Enable UUID extension for Supabase
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Account related tables
CREATE TABLE accounts (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(255) NOT NULL,
    avatar VARCHAR(255),
    email VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255),
    password_salt VARCHAR(255),
    interface_language VARCHAR(255),
    interface_theme VARCHAR(255),
    timezone VARCHAR(255),
    last_login_at TIMESTAMP WITH TIME ZONE,
    last_login_ip VARCHAR(255),
    status VARCHAR(16) NOT NULL DEFAULT 'active',
    initialized_at TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL
);

-- Tenant management
CREATE TABLE tenants (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(255) NOT NULL,
    encrypt_public_key TEXT,
    plan VARCHAR(255) NOT NULL DEFAULT 'basic',
    status VARCHAR(255) NOT NULL DEFAULT 'normal',
    custom_config TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL
);

-- Tenant account memberships
CREATE TABLE tenant_account_joins (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    tenant_id UUID NOT NULL REFERENCES tenants(id),
    account_id UUID NOT NULL REFERENCES accounts(id),
    role VARCHAR(16) NOT NULL DEFAULT 'normal',
    invited_by UUID REFERENCES accounts(id),
    status VARCHAR(16) NOT NULL DEFAULT 'pending',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL,
    UNIQUE(tenant_id, account_id)
);

-- Applications
CREATE TABLE apps (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    tenant_id UUID NOT NULL REFERENCES tenants(id),
    name VARCHAR(255) NOT NULL,
    mode VARCHAR(255) NOT NULL,
    icon VARCHAR(255),
    icon_background VARCHAR(255),
    app_model_config_id UUID,
    status VARCHAR(255) NOT NULL DEFAULT 'normal',
    enable_site BOOLEAN NOT NULL DEFAULT false,
    enable_api BOOLEAN NOT NULL DEFAULT false,
    api_rpm INTEGER NOT NULL DEFAULT 0,
    api_rph INTEGER NOT NULL DEFAULT 0,
    is_demo BOOLEAN NOT NULL DEFAULT false,
    is_public BOOLEAN NOT NULL DEFAULT false,
    is_universal BOOLEAN NOT NULL DEFAULT false,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL,
    created_by UUID NOT NULL REFERENCES accounts(id),
    updated_by UUID NOT NULL REFERENCES accounts(id)
);

-- App model configurations
CREATE TABLE app_model_configs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    app_id UUID NOT NULL REFERENCES apps(id),
    provider VARCHAR(255) NOT NULL,
    model_id VARCHAR(255) NOT NULL,
    configs TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL
);

-- Conversations
CREATE TABLE conversations (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    app_id UUID NOT NULL REFERENCES apps(id),
    app_model_config_id UUID REFERENCES app_model_configs(id),
    model_provider VARCHAR(255),
    override_model_configs TEXT,
    model_id VARCHAR(255),
    mode VARCHAR(255) NOT NULL,
    name VARCHAR(255) NOT NULL,
    summary TEXT,
    inputs TEXT,
    introduction TEXT,
    system_instruction TEXT,
    system_instruction_tokens INTEGER NOT NULL DEFAULT 0,
    status VARCHAR(255) NOT NULL,
    from_source VARCHAR(255) NOT NULL,
    from_end_user_id UUID,
    from_account_id UUID REFERENCES accounts(id),
    read_at TIMESTAMP WITH TIME ZONE,
    read_account_id UUID REFERENCES accounts(id),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL,
    is_deleted BOOLEAN NOT NULL DEFAULT false,
    invoke_from VARCHAR(255),
    dialogue_count INTEGER DEFAULT 0
);

-- Messages
CREATE TABLE messages (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    app_id UUID NOT NULL REFERENCES apps(id),
    model_provider VARCHAR(255),
    model_id VARCHAR(255),
    override_model_configs TEXT,
    conversation_id UUID NOT NULL REFERENCES conversations(id),
    inputs TEXT,
    query TEXT NOT NULL,
    answer TEXT NOT NULL,
    message_tokens INTEGER NOT NULL DEFAULT 0,
    message_unit_price DECIMAL(10,7) NOT NULL,
    message_price_unit VARCHAR(255) NOT NULL DEFAULT 'tokens',
    answer_tokens INTEGER NOT NULL DEFAULT 0,
    answer_unit_price DECIMAL(10,7) NOT NULL,
    answer_price_unit VARCHAR(255) NOT NULL DEFAULT 'tokens',
    provider_response_latency REAL NOT NULL DEFAULT 0,
    total_price DECIMAL(10,7),
    currency VARCHAR(255) NOT NULL DEFAULT 'USD',
    from_source VARCHAR(255) NOT NULL,
    from_end_user_id UUID,
    from_account_id UUID REFERENCES accounts(id),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL,
    agent_based BOOLEAN NOT NULL DEFAULT false,
    workflow_run_id UUID,
    status VARCHAR(255) NOT NULL DEFAULT 'normal',
    error TEXT,
    message_metadata TEXT,
    invoke_from VARCHAR(255),
    parent_message_id UUID REFERENCES messages(id)
);

-- Message annotations
CREATE TABLE message_annotations (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    app_id UUID NOT NULL REFERENCES apps(id),
    conversation_id UUID REFERENCES conversations(id),
    message_id UUID NOT NULL REFERENCES messages(id),
    content TEXT NOT NULL,
    account_id UUID NOT NULL REFERENCES accounts(id),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL
);

-- Datasets
CREATE TABLE datasets (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    tenant_id UUID NOT NULL REFERENCES tenants(id),
    name VARCHAR(255) NOT NULL,
    description TEXT,
    provider VARCHAR(255) NOT NULL DEFAULT 'vendor',
    permission VARCHAR(255) NOT NULL DEFAULT 'only_me',
    data_source_type VARCHAR(255),
    indexing_technique VARCHAR(255),
    index_struct TEXT,
    created_by UUID NOT NULL REFERENCES accounts(id),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL,
    embedding_model VARCHAR(255),
    embedding_model_provider VARCHAR(255),
    collection_binding_id UUID
);

-- Documents
CREATE TABLE documents (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    tenant_id UUID NOT NULL REFERENCES tenants(id),
    dataset_id UUID NOT NULL REFERENCES datasets(id),
    position INTEGER NOT NULL,
    data_source_type VARCHAR(255) NOT NULL,
    data_source_info TEXT,
    dataset_process_rule_id UUID,
    batch VARCHAR(255) NOT NULL,
    name VARCHAR(255) NOT NULL,
    created_from VARCHAR(255) NOT NULL,
    created_by UUID NOT NULL REFERENCES accounts(id),
    created_api_request_id UUID,
    processing_started_at TIMESTAMP WITH TIME ZONE,
    parsing_completed_at TIMESTAMP WITH TIME ZONE,
    cleaning_completed_at TIMESTAMP WITH TIME ZONE,
    splitting_completed_at TIMESTAMP WITH TIME ZONE,
    tokens INTEGER DEFAULT 0,
    indexing_status VARCHAR(255) NOT NULL DEFAULT 'waiting',
    error TEXT,
    enabled BOOLEAN NOT NULL DEFAULT true,
    disabled_at TIMESTAMP WITH TIME ZONE,
    disabled_by UUID REFERENCES accounts(id),
    archived BOOLEAN NOT NULL DEFAULT false,
    archived_reason VARCHAR(255),
    archived_by UUID REFERENCES accounts(id),
    archived_at TIMESTAMP WITH TIME ZONE,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL,
    indexing_latency REAL DEFAULT 0,
    doc_type VARCHAR(40),
    doc_metadata TEXT,
    doc_form VARCHAR(255) NOT NULL DEFAULT 'text_model',
    doc_language VARCHAR(255)
);

-- Document segments
CREATE TABLE document_segments (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    tenant_id UUID NOT NULL REFERENCES tenants(id),
    dataset_id UUID NOT NULL REFERENCES datasets(id),
    document_id UUID NOT NULL REFERENCES documents(id),
    position INTEGER NOT NULL,
    content TEXT NOT NULL,
    word_count INTEGER NOT NULL,
    tokens INTEGER NOT NULL,
    keywords TEXT,
    index_node_id VARCHAR(255),
    index_node_hash VARCHAR(255),
    hit_count INTEGER NOT NULL DEFAULT 0,
    enabled BOOLEAN NOT NULL DEFAULT true,
    disabled_at TIMESTAMP WITH TIME ZONE,
    disabled_by UUID REFERENCES accounts(id),
    status VARCHAR(255) NOT NULL DEFAULT 'waiting',
    created_by UUID NOT NULL REFERENCES accounts(id),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL,
    indexing_at TIMESTAMP WITH TIME ZONE,
    completed_at TIMESTAMP WITH TIME ZONE,
    error TEXT,
    stopped_at TIMESTAMP WITH TIME ZONE,
    answer TEXT
);

-- Upload files
CREATE TABLE upload_files (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    tenant_id UUID NOT NULL REFERENCES tenants(id),
    storage_type VARCHAR(255) NOT NULL,
    key VARCHAR(255) NOT NULL,
    name VARCHAR(255) NOT NULL,
    size INTEGER NOT NULL,
    extension VARCHAR(255) NOT NULL,
    mime_type VARCHAR(255),
    created_by UUID NOT NULL REFERENCES accounts(id),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL,
    used BOOLEAN NOT NULL DEFAULT false,
    used_by UUID REFERENCES accounts(id),
    used_at TIMESTAMP WITH TIME ZONE,
    hash VARCHAR(255)
);

-- API tokens
CREATE TABLE api_tokens (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    app_id UUID REFERENCES apps(id),
    dataset_id UUID REFERENCES datasets(id),
    type VARCHAR(255) NOT NULL,
    token VARCHAR(255) NOT NULL,
    last_used_at TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL
);

-- Installed apps
CREATE TABLE installed_apps (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    tenant_id UUID NOT NULL REFERENCES tenants(id),
    app_id UUID NOT NULL REFERENCES apps(id),
    app_owner_tenant_id UUID NOT NULL REFERENCES tenants(id),
    position INTEGER NOT NULL,
    is_pinned BOOLEAN NOT NULL DEFAULT false,
    last_used_at TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL,
    UNIQUE(tenant_id, app_id)
);

-- Recommended apps
CREATE TABLE recommended_apps (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    app_id UUID NOT NULL REFERENCES apps(id),
    description TEXT,
    copyright VARCHAR(255),
    privacy_policy VARCHAR(255),
    category VARCHAR(255) NOT NULL,
    position INTEGER NOT NULL DEFAULT 0,
    is_listed BOOLEAN NOT NULL DEFAULT true,
    install_count INTEGER NOT NULL DEFAULT 0,
    language VARCHAR(255) NOT NULL DEFAULT 'en-US',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL
);

-- Invite codes
CREATE TABLE invite_codes (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    batch VARCHAR(255) NOT NULL,
    code VARCHAR(32) NOT NULL UNIQUE,
    status VARCHAR(16) NOT NULL DEFAULT 'unused',
    used_at TIMESTAMP WITH TIME ZONE,
    used_by_tenant_id UUID REFERENCES tenants(id),
    used_by_account_id UUID REFERENCES accounts(id),
    deprecated_at TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL
);

-- Sites
CREATE TABLE sites (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    app_id UUID NOT NULL REFERENCES apps(id) UNIQUE,
    title VARCHAR(255) NOT NULL,
    icon VARCHAR(255),
    icon_background VARCHAR(255),
    description VARCHAR(255),
    default_language VARCHAR(255) NOT NULL,
    customize_domain VARCHAR(255),
    theme VARCHAR(255),
    customize_token_strategy VARCHAR(255) NOT NULL,
    prompt_public BOOLEAN NOT NULL DEFAULT false,
    copyright VARCHAR(255),
    privacy_policy VARCHAR(255),
    custom_disclaimer VARCHAR(255),
    show_workflow_steps BOOLEAN NOT NULL DEFAULT true,
    use_icon_as_answer_icon BOOLEAN NOT NULL DEFAULT false,
    replace_webapp_logo BOOLEAN NOT NULL DEFAULT false,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL
);

-- Workflow related tables
CREATE TABLE workflows (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    tenant_id UUID NOT NULL REFERENCES tenants(id),
    app_id UUID NOT NULL REFERENCES apps(id),
    type VARCHAR(255) NOT NULL,
    version VARCHAR(255) NOT NULL,
    graph TEXT,
    features TEXT,
    created_by UUID NOT NULL REFERENCES accounts(id),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_by UUID REFERENCES accounts(id),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL,
    environment_variables TEXT,
    conversation_variables TEXT
);

CREATE TABLE workflow_runs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    tenant_id UUID NOT NULL REFERENCES tenants(id),
    app_id UUID NOT NULL REFERENCES apps(id),
    sequence_number INTEGER NOT NULL,
    workflow_id UUID NOT NULL REFERENCES workflows(id),
    type VARCHAR(255) NOT NULL,
    triggered_from VARCHAR(255) NOT NULL,
    version VARCHAR(255) NOT NULL,
    graph TEXT,
    inputs TEXT,
    status VARCHAR(255) NOT NULL,
    outputs TEXT,
    error TEXT,
    elapsed_time REAL NOT NULL DEFAULT 0,
    total_tokens INTEGER NOT NULL DEFAULT 0,
    total_steps INTEGER DEFAULT 0,
    created_by_role VARCHAR(255) NOT NULL,
    created_by UUID NOT NULL REFERENCES accounts(id),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL,
    finished_at TIMESTAMP WITH TIME ZONE
);

CREATE TABLE workflow_node_executions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    tenant_id UUID NOT NULL REFERENCES tenants(id),
    app_id UUID NOT NULL REFERENCES apps(id),
    workflow_id UUID NOT NULL REFERENCES workflows(id),
    triggered_from VARCHAR(255) NOT NULL,
    workflow_run_id UUID NOT NULL REFERENCES workflow_runs(id),
    predecessor_node_id VARCHAR(255),
    node_id VARCHAR(255) NOT NULL,
    node_type VARCHAR(255) NOT NULL,
    title VARCHAR(255) NOT NULL,
    index INTEGER NOT NULL,
    inputs TEXT,
    process_data TEXT,
    outputs TEXT,
    status VARCHAR(255) NOT NULL,
    error TEXT,
    elapsed_time REAL NOT NULL DEFAULT 0,
    execution_metadata TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL,
    created_by_role VARCHAR(255) NOT NULL,
    created_by UUID NOT NULL REFERENCES accounts(id),
    finished_at TIMESTAMP WITH TIME ZONE
);

-- Tool providers
CREATE TABLE tool_providers (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    tenant_id UUID NOT NULL REFERENCES tenants(id),
    tool_name VARCHAR(40) NOT NULL,
    encrypted_credentials TEXT,
    is_enabled BOOLEAN NOT NULL DEFAULT false,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL
);

-- Dataset permissions
CREATE TABLE dataset_permissions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    dataset_id UUID NOT NULL REFERENCES datasets(id),
    account_id UUID NOT NULL REFERENCES accounts(id),
    has_permission BOOLEAN NOT NULL DEFAULT true,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL,
    tenant_id UUID NOT NULL REFERENCES tenants(id)
);

-- Tag bindings
CREATE TABLE tag_bindings (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    tenant_id UUID REFERENCES tenants(id),
    tag_id UUID NOT NULL,
    target_id UUID NOT NULL,
    created_by UUID NOT NULL REFERENCES accounts(id),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL
);

-- Tags
CREATE TABLE tags (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    tenant_id UUID NOT NULL REFERENCES tenants(id),
    type VARCHAR(16) NOT NULL,
    name VARCHAR(255) NOT NULL,
    created_by UUID NOT NULL REFERENCES accounts(id),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL
);

-- End users
CREATE TABLE end_users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    tenant_id UUID NOT NULL REFERENCES tenants(id),
    app_id UUID REFERENCES apps(id),
    type VARCHAR(255) NOT NULL DEFAULT 'browser_anonymous_user',
    external_user_id VARCHAR(255),
    name VARCHAR(255),
    is_anonymous BOOLEAN NOT NULL,
    session_id VARCHAR(255) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL
);

-- Dify logs table (for analytics and monitoring)
CREATE TABLE dify_logs (
    id SERIAL PRIMARY KEY,
    app_id VARCHAR(255),
    conversation_id VARCHAR(255),
    user_id VARCHAR(255),
    input_text TEXT,
    output_text TEXT,
    latency_ms INTEGER,
    status_code INTEGER,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    dialog_count NUMERIC,
    work_run_id VARCHAR(255),
    status VARCHAR(255),
    template TEXT,
    bot VARCHAR(255)
);

-- Error tracking table
CREATE TABLE error (
    id BIGSERIAL PRIMARY KEY,
    type_error VARCHAR(255),
    node VARCHAR(255),
    error_message VARCHAR(255),
    user_id VARCHAR(255),
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW()
);

-- Alembic version table
CREATE TABLE alembic_version (
    version_num VARCHAR(32) NOT NULL PRIMARY KEY
);

-- Create indexes for better performance
CREATE INDEX idx_accounts_email ON accounts(email);
CREATE INDEX idx_apps_tenant_id ON apps(tenant_id);
CREATE INDEX idx_conversations_app_id ON conversations(app_id);
CREATE INDEX idx_messages_conversation_id ON messages(conversation_id);
CREATE INDEX idx_messages_app_id ON messages(app_id);
CREATE INDEX idx_documents_dataset_id ON documents(dataset_id);
CREATE INDEX idx_document_segments_document_id ON document_segments(document_id);
CREATE INDEX idx_workflow_runs_app_id ON workflow_runs(app_id);
CREATE INDEX idx_workflow_node_executions_workflow_run_id ON workflow_node_executions(workflow_run_id);

-- Dify logs indexes
CREATE INDEX idx_dify_logs_user_id ON dify_logs(user_id);
CREATE INDEX idx_dify_logs_app_id ON dify_logs(app_id);
CREATE INDEX idx_dify_logs_conversation_id ON dify_logs(conversation_id);
CREATE INDEX idx_dify_logs_created_at ON dify_logs(created_at);

-- Error logs indexes
CREATE INDEX idx_error_user_id ON error(user_id);
CREATE INDEX idx_error_created_at ON error(created_at);
CREATE INDEX idx_error_type_error ON error(type_error);

-- Insert initial Alembic version
INSERT INTO alembic_version (version_num) VALUES ('2025_08_16_0000');

-- Add some example data for testing (optional)
INSERT INTO tenants (id, name, plan, status) VALUES 
('550e8400-e29b-41d4-a716-446655440000', 'Default Tenant', 'basic', 'normal');

INSERT INTO accounts (id, name, email, status, created_at) VALUES 
('550e8400-e29b-41d4-a716-446655440001', 'Admin User', 'admin@dify.ai', 'active', CURRENT_TIMESTAMP);

INSERT INTO tenant_account_joins (tenant_id, account_id, role, status) VALUES 
('550e8400-e29b-41d4-a716-446655440000', '550e8400-e29b-41d4-a716-446655440001', 'owner', 'active');
