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
	[attachment_type_id] INT IDENTITY(1, 1) PRIMARY KEY,
	[attachment_type_ar] NVARCHAR(128) NOT NULL UNIQUE,
	[attachment_type_en] NVARCHAR(128) NOT NULL UNIQUE,
	[created_at] DATETIME NOT NULL,
	[modified_at] DATETIME NULL
)

