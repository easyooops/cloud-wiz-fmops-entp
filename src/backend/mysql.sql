

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

INSERT INTO providers (  
    provider_id, name, company, pvd_key, description, logo, type, sort_order, is_deleted, creator_id, updater_id  
) VALUES  
    (REPLACE(UUID(), '-', ''), 'Azure OpenAI', 'Microsoft Azure', 'azure', 'Microsoft Azure의 Azure OpenAI는 텍스트 생성, 번역, 요약 및 질문 응답 등 다양한 응용 프로그램에서 인간과 유사한 텍스트를 생성하는 데 사용됩니다.', 'openai.png', 'M', 1, FALSE, '2e9279bc33104a7ba53d342dafba7841', '2e9279bc33104a7ba53d342dafba7841'),  
    (REPLACE(UUID(), '-', ''), 'Bedrock', 'Amazon Web Services', 'aws', 'Amazon Web Services의 Bedrock은 다양한 언어 모델을 지원하며, AI21 Labs, Titan, Anthropic, Cohere, Meta, Mistral AI, Stability AI 등의 모델을 통합하여 사용할 수 있습니다.', 'bedrock.png', 'M', 2, FALSE, '2e9279bc33104a7ba53d342dafba7841', '2e9279bc33104a7ba53d342dafba7841'),  
    (REPLACE(UUID(), '-', ''), 'VertexAI', 'Google Cloud Platform', 'gcp', 'Google Cloud Platform의 VertexAI는 AI 모델을 쉽고 빠르게 개발, 배포 및 유지 관리할 수 있는 통합 플랫폼입니다.', 'gemini.png', 'M', 3, FALSE, '2e9279bc33104a7ba53d342dafba7841', '2e9279bc33104a7ba53d342dafba7841'),  
    (REPLACE(UUID(), '-', ''), 'Azure Storage Accounts', 'Microsoft Azure', 'azure', 'Microsoft Azure의 Azure Storage Accounts는 다양한 파일 형식과 크기를 지원하며, 데이터를 안전하게 저장하고 웹 기반으로 쉽게 업로드 및 다운로드할 수 있는 서비스를 제공합니다.', 'azure.png', 'S', 1, FALSE, '2e9279bc33104a7ba53d342dafba7841', '2e9279bc33104a7ba53d342dafba7841'),  
    (REPLACE(UUID(), '-', ''), 'Amazon S3', 'Amazon Web Services', 'aws', 'Amazon Web Services의 Amazon S3는 다양한 파일 형식과 크기를 지원하며, 대규모 데이터를 안전하게 저장하고 웹 기반으로 쉽게 업로드 및 다운로드할 수 있는 서비스를 제공합니다.', 'aws.png', 'S', 2, FALSE, '2e9279bc33104a7ba53d342dafba7841', '2e9279bc33104a7ba53d342dafba7841'),  
    (REPLACE(UUID(), '-', ''), 'Google Cloud Storage', 'Google Cloud Platform', 'gcp', 'Google Cloud Platform의 Google Cloud Storage는 Google Workspace의 일부로, 모든 기기에서 파일을 백업하고 접근할 수 있는 안전한 클라우드 저장소를 제공합니다.', 'google-drive.png', 'S', 3, FALSE, '2e9279bc33104a7ba53d342dafba7841', '2e9279bc33104a7ba53d342dafba7841'),  
    (REPLACE(UUID(), '-', ''), 'Azure AI Search', 'Microsoft Azure', 'azure', 'Microsoft Azure의 Azure AI Search는 다양한 파일 형식과 크기를 지원하며, 웹 기반으로 데이터를 쉽게 업로드하고 다운로드할 수 있는 고성능 검색 서비스를 제공합니다.', 'azure.png', 'V', 1, FALSE, '2e9279bc33104a7ba53d342dafba7841', '2e9279bc33104a7ba53d342dafba7841'),  
    (REPLACE(UUID(), '-', ''), 'Amazon OpenSearch', 'Amazon Web Services', 'aws', 'Amazon Web Services의 Amazon OpenSearch는 다양한 파일 형식과 크기를 지원하며, 데이터를 빠르게 검색하고 분석할 수 있는 오픈 소스 검색 엔진 서비스를 제공합니다.', 'aws.png', 'V', 2, FALSE, '2e9279bc33104a7ba53d342dafba7841', '2e9279bc33104a7ba53d342dafba7841'),  
    (REPLACE(UUID(), '-', ''), 'Vertex AI Search', 'Google Cloud Platform', 'gcp', 'Google Cloud Platform의 Vertex AI Search는 Google Workspace의 일부로, 모든 기기에서 파일을 백업하고 접근할 수 있는 안전한 클라우드 저장소와 고성능 검색 기능을 제공합니다.', 'google-drive.png', 'V', 3, FALSE, '2e9279bc33104a7ba53d342dafba7841', '2e9279bc33104a7ba53d342dafba7841'),  
    (REPLACE(UUID(), '-', ''), 'ChromaDB', 'ChromaWay', 'chroma', 'ChromaWay의 ChromaDB는 블록체인 기반 데이터베이스로, 스마트 계약 및 분산 애플리케이션을 위한 데이터 저장 및 관리 기능을 제공합니다.', 'chromadb.png', 'V', 4, FALSE, '2e9279bc33104a7ba53d342dafba7841', '2e9279bc33104a7ba53d342dafba7841');  

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
	fm_provider_id CHAR(36) NOT NULL,
	fm_temperature FLOAT NOT NULL, 
	fm_top_p FLOAT NOT NULL, 
	embedding_enabled BOOLEAN NOT NULL DEFAULT 0,
	storage_provider_id CHAR(36), 
	storage_object_id CHAR(36), 
	vector_db_provider_id CHAR(36), 
	processing_enabled BOOLEAN NOT NULL DEFAULT 0, 
	pre_processing_id CHAR(36), 
	post_processing_id CHAR(36),
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
CREATE INDEX ix_agents_user_id ON agents (user_id);
CREATE INDEX ix_agents_fm_provider_id ON agents (fm_provider_id);
CREATE INDEX ix_agents_agent_id ON agents (agent_id);
CREATE INDEX ix_credentials_user_id ON credentials (user_id);
CREATE INDEX ix_credentials_credential_id ON credentials (credential_id);
CREATE INDEX ix_credentials_provider_id ON credentials (provider_id);
CREATE INDEX ix_store_store_id ON store (store_id);
CREATE INDEX ix_store_user_id ON store (user_id);
CREATE INDEX ix_processing_user_id ON processing (user_id);
CREATE INDEX ix_processing_processing_id ON processing (processing_id);