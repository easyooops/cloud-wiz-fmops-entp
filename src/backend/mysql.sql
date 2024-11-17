

DROP TABLE IF EXISTS providers;
CREATE TABLE providers (
	provider_id CHAR(36) NOT NULL, 
	name VARCHAR(255) NOT NULL, 
	company VARCHAR(255) NOT NULL, 
	pvd_key VARCHAR(10) NOT NULL, 
	description VARCHAR(512), 
	logo VARCHAR(255), 
	type VARCHAR(1) NOT NULL, 
	sort_order INTEGER NOT NULL, 
	is_deleted BOOLEAN NOT NULL DEFAULT 0, 
	creator_id CHAR(36) NOT NULL, 
	created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP, 
	updater_id CHAR(36),
	updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP, 
	PRIMARY KEY (provider_id)
);

DROP TABLE IF EXISTS inquiry;
CREATE TABLE inquiry (
	inquiry_id INTEGER NOT NULL AUTO_INCREMENT, 
	inquiry_type VARCHAR(10) NOT NULL, 
	title VARCHAR(255) NOT NULL, 
	content TEXT NOT NULL, 
	response_content TEXT, 
	processing_type VARCHAR(255) NOT NULL, 
	is_deleted BOOLEAN NOT NULL DEFAULT 0, 
	creator_id CHAR(36) NOT NULL, 
	created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP, 
	updater_id CHAR(36),
	updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP, 
	PRIMARY KEY (inquiry_id)
);

DROP TABLE IF EXISTS user;
CREATE TABLE user (
	user_id CHAR(36) NOT NULL, 
	username VARCHAR(128) NOT NULL, 
	email VARCHAR(128) NOT NULL,
	google_token TEXT NULL,
	last_login DATETIME NOT NULL, 
	is_deleted BOOLEAN NOT NULL DEFAULT 0, 
	creator_id CHAR(36) NOT NULL, 
	created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP, 
	updater_id CHAR(36),
	updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP, 
	PRIMARY KEY (user_id)
);

DROP TABLE IF EXISTS agents;
CREATE TABLE agents (
	agent_id CHAR(36) NOT NULL, 
	user_id CHAR(36) NOT NULL, 
	agent_name VARCHAR(128) NOT NULL, 
	agent_description VARCHAR(255), 
	fm_provider_type VARCHAR(10) NOT NULL, 
	fm_provider_id CHAR(36) NOT NULL, 
	fm_model_id CHAR(36) NOT NULL, 
	fm_temperature FLOAT NOT NULL, 
	fm_top_p FLOAT NOT NULL, 
	fm_request_token_limit INTEGER NOT NULL, 
	fm_response_token_limit INTEGER NOT NULL, 
	embedding_enabled BOOLEAN NOT NULL DEFAULT 0, 
	embedding_provider_id CHAR(36), 
	embedding_model_id CHAR(36), 
	storage_provider_id CHAR(36), 
	storage_object_id CHAR(36), 
	vector_db_provider_id CHAR(36), 
	processing_enabled BOOLEAN NOT NULL DEFAULT 0, 
	pre_processing_id CHAR(36), 
	post_processing_id CHAR(36),
    template_enabled BOOLEAN NOT NULL DEFAULT 0, 
    template TEXT,
	expected_request_count INTEGER NOT NULL, 
	expected_token_count INTEGER NOT NULL, 
	expected_cost FLOAT NOT NULL, 
	is_deleted BOOLEAN NOT NULL DEFAULT 0, 
	creator_id CHAR(36) NOT NULL, 
	created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP, 
	updater_id CHAR(36),
	updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP, 
	PRIMARY KEY (agent_id)
);

DROP TABLE IF EXISTS models;
CREATE TABLE models (
	model_id CHAR(36) NOT NULL, 
	model_name VARCHAR(255) NOT NULL, 
	provider_id CHAR(36) NOT NULL, 
	model_type VARCHAR(10) NOT NULL, 
	sort_order INTEGER NOT NULL, 
	is_deleted BOOLEAN NOT NULL DEFAULT 0, 
	creator_id CHAR(36) NOT NULL, 
	created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP, 
	updater_id CHAR(36),
	updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP, 
	PRIMARY KEY (model_id)
);

DROP TABLE IF EXISTS chain;
CREATE TABLE chain (
	chain_id CHAR(36) NOT NULL, 
	agent_id CHAR(36) NOT NULL, 
	provider_id CHAR(36) NOT NULL, 
	connection_order INTEGER NOT NULL, 
	is_deleted BOOLEAN NOT NULL DEFAULT 0, 
	creator_id CHAR(36) NOT NULL, 
	created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP, 
	updater_id CHAR(36),
	updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
	PRIMARY KEY (chain_id)
);

DROP TABLE IF EXISTS credentials;
CREATE TABLE credentials (
	credential_id CHAR(36) NOT NULL, 
	user_id CHAR(36) NOT NULL, 
	provider_id CHAR(36) NOT NULL, 
	credential_name VARCHAR(255) NOT NULL, 
	access_key VARCHAR(125), 
	secret_key VARCHAR(125), 
	session_key VARCHAR(125), 
	access_token VARCHAR(125), 
	api_key VARCHAR(125), 
	api_endpoint VARCHAR(255),
    git_clone_url VARCHAR(512),
    git_branch VARCHAR(125),
    git_repo_path VARCHAR(512),
    git_file_filter VARCHAR(125),
    db_user VARCHAR(125),
    db_password VARCHAR(125),
    db_account VARCHAR(125),
    db_role VARCHAR(125),
    db_database VARCHAR(125),
    db_schema VARCHAR(125),
    db_warehouse VARCHAR(125),
    db_query TEXT,
	refresh_token TEXT,
    inner_used BOOLEAN NOT NULL DEFAULT 0,
    limit_cnt FLOAT NOT NULL,
	is_deleted BOOLEAN NOT NULL DEFAULT 0, 
	creator_id CHAR(36) NOT NULL, 
	created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP, 
	updater_id CHAR(36),
	updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
	PRIMARY KEY (credential_id)
);

DROP TABLE IF EXISTS store;
CREATE TABLE store (
	store_id CHAR(36) NOT NULL, 
	user_id CHAR(36) NOT NULL, 
	credential_id CHAR(36) NOT NULL, 
	store_name VARCHAR(255) NOT NULL, 
	description VARCHAR(255), 
	is_deleted BOOLEAN NOT NULL DEFAULT 0,
	creator_id CHAR(36) NOT NULL, 
	created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP, 
	updater_id CHAR(36),
	updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
	PRIMARY KEY (store_id)
);

DROP TABLE IF EXISTS processing;
CREATE TABLE processing (
	processing_id CHAR(36) NOT NULL, 
	user_id CHAR(36) NOT NULL, 
	processing_type VARCHAR(10) NOT NULL, 
	processing_name VARCHAR(255) NOT NULL, 
	processing_desc VARCHAR(255), 
	template TEXT, 
	pii_masking VARCHAR(512), 
	normalization VARCHAR(512), 
	stopword_removal TEXT, 
	is_deleted BOOLEAN NOT NULL DEFAULT 0, 
	creator_id CHAR(36) NOT NULL, 
	created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP, 
	updater_id CHAR(36),
	updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
	PRIMARY KEY (processing_id)
);

DROP TABLE IF EXISTS opinions;

CREATE TABLE opinions (
    opinion_id INTEGER NOT NULL AUTO_INCREMENT,
    title VARCHAR(255) NULL,
    content TEXT NULL,
    answer TEXT,
    is_deleted BOOLEAN NOT NULL DEFAULT 0,
    creator_id CHAR(36) NOT NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updater_id CHAR(36),
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (opinion_id)
);

DROP TABLE IF EXISTS contactus;

CREATE TABLE contactus (
    contactus_id INTEGER NOT NULL AUTO_INCREMENT,
    customer_name VARCHAR(255),
    customer_email VARCHAR(255),
    title VARCHAR(255),
    content TEXT,
    answer TEXT,
    is_deleted BOOLEAN NOT NULL DEFAULT 0,
    creator_id VARCHAR(255) DEFAULT 'system',
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updater_id VARCHAR(255) DEFAULT 'system',
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (contactus_id)
);



CREATE INDEX ix_providers_provider_id ON providers (provider_id);
CREATE INDEX ix_providers_company ON providers (company);
CREATE INDEX ix_providers_name ON providers (name);
CREATE INDEX ix_providers_description ON providers (description);
CREATE INDEX ix_inquiry_title ON inquiry (title);
CREATE INDEX ix_inquiry_id ON inquiry (inquiry_id);
CREATE INDEX ix_inquiry_inquiry_type ON inquiry (inquiry_type);
CREATE INDEX ix_user_user_id ON user (user_id);
CREATE INDEX ix_user_email ON user (email);
CREATE INDEX ix_user_username ON user (username);
CREATE INDEX ix_agents_fm_model_id ON agents (fm_model_id);
CREATE INDEX ix_agents_user_id ON agents (user_id);
CREATE INDEX ix_agents_fm_provider_id ON agents (fm_provider_id);
CREATE INDEX ix_agents_agent_id ON agents (agent_id);
CREATE INDEX ix_models_provider_id ON models (provider_id);
CREATE INDEX ix_models_model_type ON models (model_type);
CREATE INDEX ix_models_model_name ON models (model_name);
CREATE INDEX ix_models_model_id ON models (model_id);
CREATE INDEX ix_chain_chain_id ON chain (chain_id);
CREATE INDEX ix_credentials_user_id ON credentials (user_id);
CREATE INDEX ix_credentials_credential_id ON credentials (credential_id);
CREATE INDEX ix_credentials_provider_id ON credentials (provider_id);
CREATE INDEX ix_store_store_id ON store (store_id);
CREATE INDEX ix_store_user_id ON store (user_id);
CREATE INDEX ix_processing_user_id ON processing (user_id);
CREATE INDEX ix_processing_processing_id ON processing (processing_id);