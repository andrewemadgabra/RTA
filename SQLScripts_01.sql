CREATE TABLE Django_Content_Type
(
    [id] INT PRIMARY KEY IDENTITY(1,1),
    [app_label] NVARCHAR(100) NOT NULL,
    [model] NVARCHAR(100) NOT NULL
)


CREATE TABLE Auth_Permission
(
    [id] INT PRIMARY KEY IDENTITY(1,1),
    [content_type_id] INT NOT NULL FOREIGN KEY REFERENCES Django_Content_Type([id]) ON DELETE CASCADE
ON UPDATE CASCADE,
    [codename] NVARCHAR(100) NOT NULL,
    [name] NVARCHAR(255) NOT NULL UNIQUE
)


CREATE TABLE Django_Migrations
(
    [id] INT PRIMARY KEY IDENTITY(1,1),
    [app] NVARCHAR(255) NOT NULL ,
    [name] NVARCHAR(255) NOT NULL,
    [applied] DATETIME NOT NULL
)


CREATE TABLE Auth_Group
(
    [id] INT PRIMARY KEY IDENTITY(1,1),
    [name] NVARCHAR(255) NOT NULL UNIQUE,
)



CREATE TABLE Auth_Group_Permissions
(
    [id] INT PRIMARY KEY IDENTITY(1,1),
    [group_id] INT NOT NULL FOREIGN KEY REFERENCES Auth_Group([id])  ON DELETE CASCADE
ON UPDATE CASCADE,
    [permission_id] INT NOT NULL FOREIGN KEY REFERENCES Auth_Permission([id])  ON DELETE CASCADE
ON UPDATE CASCADE,
    CONSTRAINT UC_Auth_Group_Permissions UNIQUE ([group_id],[permission_id])
)



CREATE TABLE User_User
(
    [id] INT PRIMARY KEY IDENTITY(1,1),
    [created_at] DATETIME NOT NULL ,
    [modified_at] DATETIME NULL ,
    [password] NVARCHAR(255) NOT NULL ,
    [last_login] DATETIME NULL ,
    [is_superuser] BIT NOT NULL,
    [is_active] BIT NOT NULL,
    [is_staff] BIT NOT NULL,
    [is_admin] BIT NOT NULL,
    [username] NVARCHAR(30) NOT NULL UNIQUE,
    [email] NVARCHAR(128) NOT NULL UNIQUE,
    [first_name] NVARCHAR(30) NOT NULL ,
    [last_name] NVARCHAR(30) NOT NULL ,
    [middle_name] NVARCHAR(30) NOT NULL ,
    [gender] NVARCHAR(1) NOT NULL ,
    [number_of_identification] NVARCHAR(14) NOT NULL UNIQUE,
    [home_address] NVARCHAR(30) NULL ,
    [mobile] NVARCHAR(14) NOT NULL UNIQUE,
)



CREATE TABLE User_User_Groups
(
    [id] INT PRIMARY KEY IDENTITY(1,1),
    [user_id] INT NOT NULL FOREIGN KEY REFERENCES User_User([id])  ON DELETE CASCADE
ON UPDATE CASCADE,
    [group_id] INT NOT NULL FOREIGN KEY REFERENCES Auth_Group([id])  ON DELETE CASCADE
ON UPDATE CASCADE,
    CONSTRAINT UC_Auth_User_Groups UNIQUE ([group_id],[user_id])
)


CREATE TABLE User_User_User_Permissions
(
    [id] INT PRIMARY KEY IDENTITY(1,1),
    [user_id] INT NOT NULL FOREIGN KEY REFERENCES User_User([id])  ON DELETE CASCADE
ON UPDATE CASCADE,
    [permission_id] INT NOT NULL FOREIGN KEY REFERENCES Auth_Permission([id])  ON DELETE CASCADE
ON UPDATE CASCADE,
    CONSTRAINT UC_Auth_User_Permissions UNIQUE ([permission_id],[user_id])
)


CREATE TABLE Django_Admin_Log
(
    [id] INT PRIMARY KEY IDENTITY(1,1),
    [action_time] DATETIME NOT NULL ,
    [object_id] TEXT NULL ,
    [object_repr] NVARCHAR(200) NOT NULL ,
    [change_message] TEXT NOT NULL ,
    [content_type_id] INT NULL FOREIGN KEY REFERENCES Django_Content_Type([id]) ON DELETE CASCADE
ON UPDATE CASCADE,
    [user_id] INT NOT NULL FOREIGN KEY REFERENCES User_User([id])  ON DELETE CASCADE
ON UPDATE CASCADE,
    [action_flag] SMALLINT NOT NULL
)


CREATE TABLE Django_Session
(
    [session_key] NVARCHAR(40) PRIMARY KEY ,
    [session_data] TEXT NOT NULL,
    [expire_date] DATETIME NOT NULL
    ,
)


CREATE TABLE Django_Rest_Passwordreset_Resetpasswordtoken
(
    [created_at] DATETIME NOT NULL ,
    [key] NVARCHAR(64) NOT NULL,
    [user_agent] NVARCHAR(256) NOT NULL,
    [user_id] INT NOT NULL FOREIGN KEY REFERENCES User_User([id])  ON DELETE CASCADE
ON UPDATE CASCADE,
    [id] INT PRIMARY KEY IDENTITY(1,1),
    [ip_address] CHAR(39) NULL,
)

CREATE TABLE Knox_Authtoken
(
    [digest] NVARCHAR(128) PRIMARY KEY ,
    [created] DATETIME NOT NULL ,
    [user_id] INT NOT NULL FOREIGN KEY REFERENCES User_User([id])  ON DELETE CASCADE
ON UPDATE CASCADE,
    [token_key] NVARCHAR(8) NOT NULL,
    [expiry] DATETIME NULL,

)


CREATE TABLE Jobs
(
    [created_at] DATETIME NOT NULL ,
    [modified_at] DATETIME NULL ,
    [job_id] INT PRIMARY KEY IDENTITY(1,1),
    [job_title_Ar] NVARCHAR(128) NOT NULL UNIQUE,
    [job_title_En] NVARCHAR(128) NOT NULL UNIQUE,
)


CREATE TABLE EmploymentStatus
(
    [created_at] DATETIME NOT NULL ,
    [modified_at] DATETIME NULL ,
    [employment_id] INT PRIMARY KEY IDENTITY(1,1),
    [employment_title_Ar] NVARCHAR(128) NOT NULL UNIQUE,
    [employment_title_En] NVARCHAR(128) NOT NULL UNIQUE,
)


CREATE TABLE System_Table(
[system_id] INT PRIMARY KEY IDENTITY(1,1),
[system_ar] NVARCHAR(128) NOT NULL UNIQUE, 
[system_en] NVARCHAR(128) NOT NULL UNIQUE, 
[created_at] DATETIME NOT NULL, 
[modified_at] DATETIME NULL
)


CREATE TABLE SystemGroup(
[system_group_id] INT PRIMARY KEY IDENTITY(1,1),
[group_id] INT NOT NULL FOREIGN KEY REFERENCES [dbo].[Auth_Group](id) ON DELETE CASCADE UNIQUE, 
[system_id] INT NOT NULL FOREIGN KEY REFERENCES System_Table([system_id]) ON DELETE CASCADE , 
[created_at] DATETIME NOT NULL, 
[modified_at] DATETIME NULL
)