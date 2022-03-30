CREATE TRIGGER [dbo].[LetterDataInsertAfterTrigger]
ON LetterData
AFTER INSERT
AS
BEGIN
	DECLARE @Action_user INT, @letter_title NVARCHAR(256) , @Issued_number INT
	, @Message_Created NVARCHAR(MAX), @User_name Nvarchar(128), @Letter_id INT
	SELECT @Letter_id = [letter_data_id] , @Action_user = [action_user],
		@letter_title = [letter_title], @Issued_number = [issued_number]
	FROM inserted
	SELECT @User_name = [username]
	FROM User_User
	WHERE ID = @Action_user

	SET @Message_Created =  'Letter Created With User ' + @User_name +  'With letter_Title(' + @letter_title +  ') and issued_number(' +  CAST(@Issued_number AS nvarchar(50)) +') '

	INSERT INTO LetterDataLogger
		([log_message], [letter_Id])
	VALUES(@Message_Created, @Letter_id)
END

