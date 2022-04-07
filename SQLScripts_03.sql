CREATE TABLE EntityCassification
(
	[entity_id] INT IDENTITY(1, 1) PRIMARY KEY,
	[entity_Ar] NVARCHAR(128) NOT NULL UNIQUE,
	[entity_En] NVARCHAR(128) NOT NULL UNIQUE,
	[created_at] DATETIME NOT NULL,
	[modified_at] DATETIME NULL
)


CREATE TABLE MainActors
(
	[main_actor_id] INT IDENTITY(1, 1) PRIMARY KEY,
	[entitycassification_id] INT FOREIGN KEY REFERENCES EntityCassification([entity_id]) ON DELETE CASCADE
	ON UPDATE CASCADE,
	[main_actor_Ar] NVARCHAR(128) NOT NULL UNIQUE,
	[main_actor_En] NVARCHAR(128) NOT NULL UNIQUE,
	[created_at] DATETIME NOT NULL,
	[modified_at] DATETIME NULL
)


CREATE TABLE SubActors
(
	[sub_actor_id] INT IDENTITY(1, 1) PRIMARY KEY,
	[main_actor_id] INT FOREIGN KEY REFERENCES MainActors([main_actor_id]) ON DELETE CASCADE
	ON UPDATE CASCADE,
	[sub_actor_Ar] NVARCHAR(128) NOT NULL UNIQUE,
	[sub_actor_En] NVARCHAR(128) NOT NULL UNIQUE,
	[sub_actor_key] NVARCHAR(128) NULL,
	[created_at] DATETIME NOT NULL,
	[modified_at] DATETIME NULL
)

ALTER TABLE SubActors
DROP COLUMN  [sub_actor_key]


ALTER TABLE SubActors
ADD sub_actor_parent INT NULL FOREIGN KEY REFERENCES SubActors([sub_actor_id])

ALTER TABLE UserEmploymentJobStatus
ADD [sub_actor_id] INT REFERENCES SubActors([sub_actor_id]) ON DELETE CASCADE ON UPDATE CASCADE


CREATE TABLE DeliveryMethod
(
	[delivery_method_id] INT IDENTITY(1, 1) PRIMARY KEY,
	[delivery_method_name_ar] NVARCHAR(128) NOT NULL UNIQUE,
	[delivery_method_name_en] NVARCHAR(128) NOT NULL UNIQUE,
	[created_at] DATETIME NOT NULL,
	[modified_at] DATETIME NULL
)





CREATE TABLE PriorityLevel
(
	[priority_level_id] INT IDENTITY(1, 1) PRIMARY KEY,
	[priority_level_ar] NVARCHAR(128) NOT NULL UNIQUE,
	[priority_level_en] NVARCHAR(128) NOT NULL UNIQUE,
	[created_at] DATETIME NOT NULL,
	[modified_at] DATETIME NULL
)




CREATE TABLE LetterData
(
	[letter_data_id] INT IDENTITY(1, 1) PRIMARY KEY,
	[issued_number] INT NOT NULL ,
	[letter_title] NVARCHAR(256) NOT NULL ,
	[action_user] INT NOT NULL FOREIGN KEY REFERENCES User_User([id])  ON DELETE CASCADE,
	[topic_subcategories_id] INT NOT NULL FOREIGN KEY REFERENCES TopicSubcategories([topic_subcategories_id])  ON DELETE CASCADE,
	[project_section_id] INT NOT NULL FOREIGN KEY REFERENCES ProjectSections([project_section_id])  ON DELETE CASCADE,
	[sub_actor_id] INT NOT NULL FOREIGN KEY REFERENCES [dbo].[SubActors]([sub_actor_id]),
	[delivery_user_id] INT FOREIGN KEY REFERENCES [dbo].[User_User]([id]) ON DELETE CASCADE,
	[delivery_method_id] INT NOT NULL FOREIGN KEY REFERENCES [dbo].[DeliveryMethod]([delivery_method_id]) ON DELETE CASCADE,
	[created_at] DATETIME NOT NULL,
	[modified_at] DATETIME NULL,
	CHECK ([issued_number] >= 0),
)


CREATE TABLE LetterDataLogger
(
	[log_id] INT IDENTITY(1,1) PRIMARY KEY,
	[log_message] NVARCHAR(MAX) NOT NULL,
	[letter_Id] INT NOT NULL FOREIGN KEY REFERENCES LetterData([letter_data_id]) ON DELETE CASCADE,
	[created_at] DATETIME NOT NULL DEFAULT GETDATE(),
	[modified_at] DATETIME NULL,
)


CREATE TABLE AttachmentType
(
	[attachment_type_ar] NVARCHAR(128) NOT NULL ,
	[attachment_type_en] NVARCHAR(128) NOT NULL ,
	[content_type] NVARCHAR(128) PRIMARY KEY,
	[charset] NVARCHAR(128) NULL,
	[max_size] INT NULL,
	[created_at] DATETIME NOT NULL,
	[modified_at] DATETIME NULL,
	CHECK([max_size] > 0)
)

CREATE TABLE LetterAttachemnets
(
	[letter_attachment_id] INT IDENTITY(1, 1) PRIMARY KEY,
	[letter_attach_name] NVARCHAR(256) NOT NULL ,
	[file_path_on_server] NVARCHAR(512) NOT NULL ,
	[letter_data_id] INT NOT NULL FOREIGN KEY REFERENCES [dbo].[LetterData]([letter_data_id]) ON DELETE CASCADE,
	[content_type] NVARCHAR(128) NOT NULL FOREIGN KEY REFERENCES [dbo].[AttachmentType]([content_type]) ON DELETE CASCADE,
	[created_at] DATETIME NOT NULL,
	[modified_at] DATETIME NULL,
)

CREATE TABLE MainTopic
(
	[main_topic_id] INT IDENTITY(1, 1) PRIMARY KEY,
	[main_topic_Ar] NVARCHAR(128) NOT NULL ,
	[main_topic_En] NVARCHAR(128) NOT NULL ,
	[created_at] DATETIME NOT NULL,
	[modified_at] DATETIME NULL,
)

CREATE TABLE TopicClassification
(
	[topic_classification_id] INT IDENTITY(1, 1) PRIMARY KEY,
	[topic_classification_Ar] NVARCHAR(128) NOT NULL ,
	[topic_classification_En] NVARCHAR(128) NOT NULL ,
	[main_topic] INT NOT NULL FOREIGN KEY REFERENCES [dbo].[MainTopic]([main_topic_id]) ON DELETE CASCADE,
	[created_at] DATETIME NOT NULL,
	[modified_at] DATETIME NULL,
)

CREATE TABLE TopicSubcategories
(
	[topic_subcategories_id] INT IDENTITY(1, 1) PRIMARY KEY,
	[topic_subcategories_Ar] NVARCHAR(128) NOT NULL ,
	[topic_subcategories_En] NVARCHAR(128) NOT NULL ,
	[topic_classification_id] INT NOT NULL FOREIGN KEY REFERENCES [dbo].[TopicClassification]([topic_classification_id]) ON DELETE CASCADE,
	[created_at] DATETIME NOT NULL,
	[modified_at] DATETIME NULL,
)

CREATE TABLE FinancialClaimsStatus
(
	[financial_claims_status_id] INT IDENTITY(1, 1) PRIMARY KEY,
	[financial_claims_status_Ar] NVARCHAR(128) NOT NULL ,
	[financial_claims_status_En] NVARCHAR(128) NOT NULL ,
	[created_at] DATETIME NOT NULL,
	[modified_at] DATETIME NULL,
)

CREATE TABLE FinancialClaims
(
	[financial_claims_id] INT IDENTITY(1, 1) PRIMARY KEY,
	[target] NVARCHAR(512),
	[value] DEC(18,2),
	[financial_claims_status_id] INT NOT NULL FOREIGN KEY REFERENCES [dbo].[FinancialClaimsStatus]([financial_claims_status_id]) ON DELETE CASCADE,
	[sub_actor_id] INT NOT NULL FOREIGN KEY REFERENCES [dbo].[SubActors]([sub_actor_ID]) ON DELETE CASCADE,
	[letter_data_id] INT NOT NULL FOREIGN KEY REFERENCES [dbo].[LetterData]([letter_data_id]) ON DELETE CASCADE,
	[created_at] DATETIME NOT NULL,
	[modified_at] DATETIME NULL,
)

CREATE TABLE Projects
(
	[project_id] INT IDENTITY(1, 1) PRIMARY KEY,
	[project_Ar] NVARCHAR(128) NOT NULL ,
	[project_En] NVARCHAR(128) NOT NULL ,
	[created_at] DATETIME NOT NULL,
	[modified_at] DATETIME NULL,
)

CREATE TABLE ProjectSections
(
	[project_section_id] INT IDENTITY(1, 1) PRIMARY KEY,
	[project_section_Ar] NVARCHAR(128) NOT NULL ,
	[project_section_En] NVARCHAR(128) NOT NULL ,
	[project_id] INT NOT NULL FOREIGN KEY REFERENCES [dbo].[Projects]([project_id]) ON DELETE CASCADE,
	[created_at] DATETIME NOT NULL,
	[modified_at] DATETIME NULL,
)

CREATE TABLE ProjectContracts
(
	[project_contract_id] INT IDENTITY(1, 1) PRIMARY KEY,
	[project_contract_num] NVARCHAR(128),
	[project_section_id] INT NOT NULL FOREIGN KEY REFERENCES [dbo].[ProjectSections]([project_section_id]) ON DELETE CASCADE,
	[created_at] DATETIME NOT NULL,
	[modified_at] DATETIME NULL,
)
