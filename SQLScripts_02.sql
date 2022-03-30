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