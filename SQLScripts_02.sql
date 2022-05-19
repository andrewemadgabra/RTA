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
	[sub_actor_parent] INT NULL FOREIGN KEY REFERENCES SubActors([sub_actor_id]),
	[created_at] DATETIME NOT NULL,
	[modified_at] DATETIME NULL
)


CREATE TABLE UserEmploymentJobStatus
(
	[created_at] DATETIME NOT NULL ,
	[modified_at] DATETIME NULL ,
	[user_employment_id] INT PRIMARY KEY IDENTITY(1,1),
	[user_id] INT NOT NULL FOREIGN KEY REFERENCES User_User([id])  
    ON DELETE CASCADE ON UPDATE CASCADE,
	[employment_id] INT NOT NULL FOREIGN KEY REFERENCES EmploymentStatus([employment_id])
    ON DELETE CASCADE ON UPDATE CASCADE,
	[job_id] INT NOT NULL FOREIGN KEY REFERENCES Jobs([job_id])  
    ON DELETE CASCADE ON UPDATE CASCADE,
	[action_user] INT NOT NULL FOREIGN KEY REFERENCES User_User([id]),
	[sub_actor_id] INT REFERENCES SubActors([sub_actor_id]) 
    ON DELETE CASCADE ON UPDATE CASCADE,
	CONSTRAINT UC_User_EmploymentStatus UNIQUE ([employment_id],[user_id])
)


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
	[topic_classification_id] INT NOT NULL FOREIGN KEY REFERENCES 
	[dbo].[TopicClassification]([topic_classification_id]) ON DELETE CASCADE,
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

CREATE TABLE LetterStatus
(
	letter_status_id INT PRIMARY KEY IDENTITY(1, 1),
	letter_status_group INT NOT NULL,
	letter_status_description_ar NVARCHAR(1024) NOT NULL,
	letter_status_description_en NVARCHAR(1024) NOT NULL,
	created_at DATETIME NOT NULL,
	modified_at DATETIME NULL
)
DELETE FROM LetterStatus
DBCC CHECKIDENT ('LetterStatus', RESEED, 1);
INSERT INTO LetterStatus
	(letter_status_group, letter_status_description_ar, letter_status_description_en, created_at)
VALUES(1, N'وارد خارجى', N'External Incoming Letter', GETDATE())
INSERT INTO LetterStatus
	(letter_status_group, letter_status_description_ar, letter_status_description_en, created_at)
VALUES(1, N'وارد داخى', N'Internal Incoming Letter', GETDATE())



CREATE TABLE LetterData
(
	[letter_data_id] INT IDENTITY(1, 1) PRIMARY KEY,
	[issued_number] INT NOT NULL ,
	[letter_title] NVARCHAR(256) NOT NULL ,
	[action_user] INT NOT NULL FOREIGN KEY REFERENCES User_User([id])  ON DELETE CASCADE,
	[topic_subcategories_id] INT NULL FOREIGN KEY REFERENCES TopicSubcategories([topic_subcategories_id])  ON DELETE CASCADE,
	[project_section_id] INT NOT NULL FOREIGN KEY REFERENCES ProjectSections([project_section_id])  ON DELETE CASCADE,
	[sub_actor_sender_id] INT NOT NULL FOREIGN KEY REFERENCES [dbo].[SubActors]([sub_actor_id]),
	[delivery_user_id] INT FOREIGN KEY REFERENCES [dbo].[User_User]([id]),
	[delivery_method_id] INT NOT NULL FOREIGN KEY REFERENCES [dbo].[DeliveryMethod]([delivery_method_id]) ON DELETE CASCADE,
	[project_section_id] INT NULL FOREIGN KEY REFERENCES [dbo].[ProjectSections]([project_section_id]),
	[created_at] DATETIME NOT NULL,
	[modified_at] DATETIME NULL,
	CHECK ([issued_number] >= 0),
)

ALTER TABLE LetterData ADD [subject_text] NVARCHAR(1000) NOT NULL
ALTER TABLE LetterData ADD [sub_actor_receiver_id] INT NOT NULL FOREIGN KEY REFERENCES [dbo].[SubActors]([sub_actor_id])
ALTER TABLE LetterData ADD issued_date DATE
ALTER TABLE LetterData ADD financial_target NVARCHAR(512) NULL
ALTER TABLE LetterData ADD financial_value DECIMAL(18,2) NULL
ALTER TABLE LetterData ADD financial_claims_status_id INT NULL FOREIGN KEY REFERENCES [dbo].[FinancialClaimsStatus]([financial_claims_status_id])
ALTER TABLE LetterData ADD letter_status_id INT NOT NULL FOREIGN KEY REFERENCES LetterStatus(letter_status_id)

CREATE TABLE LetterDataLogger
(
	[log_id] INT IDENTITY(1,1) PRIMARY KEY,
	[log_message] NVARCHAR(MAX) NOT NULL,
	[letter_Id] INT NOT NULL FOREIGN KEY REFERENCES LetterData([letter_data_id]) ON DELETE CASCADE,
	[created_at] DATETIME NOT NULL DEFAULT GETDATE(),
	[modified_at] DATETIME NULL,
	[user_id] INT NOT NULL FOREIGN KEY REFERENCES User_User(ID),
	[From_status] INT FOREIGN KEY REFERENCES LetterStatus(letter_status_id),
	[To_status] INT FOREIGN KEY REFERENCES LetterStatus(letter_status_id)
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
	[created_at] DATETIME NOT NULL,
	[modified_at] DATETIME NULL,
)