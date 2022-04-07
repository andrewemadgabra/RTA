
CREATE TRIGGER [dbo].[LetterDataUpdateInstedOFTrigger]
ON LetterData
INSTEAD OF  UPDATE
AS
BEGIN

	DECLARE @Action_user INT, @letter_title NVARCHAR(256) , @Issued_number INT
	, @Message_Created NVARCHAR(MAX), @User_name Nvarchar(128), @Letter_id INT
	, @letter_title_old NVARCHAR(256) , @Issued_number_old INT

	SELECT @Letter_id = [letter_data_id], @Action_user = [action_user],
		@letter_title = [letter_title], @Issued_number = [issued_number]
	FROM inserted

	SELECT @letter_title_old = [letter_title], @Issued_number_old = [issued_number]
	FROM LetterData

	SELECT @User_name = [username]
	FROM User_User
	WHERE ID = @Action_user

	SET @Message_Created =  'Letter Updated With User ' + @User_name
	IF @letter_title_old <> @letter_title
	BEGIN
		SET @Message_Created =  @Message_Created +  ' UPDATE [letter_title]('+ @letter_title_old +') TO (' 
	 + @letter_title + ') '
	END
	IF @Issued_number_old <> @Issued_number
	BEGIN
		SET @Message_Created =  @Message_Created +  ' UPDATE [issued_number]('+ 
		CAST(@Issued_number_old AS NVARCHAR(50)) +') TO (' 
	 + CAST(@Issued_number AS NVARCHAR(50)) + ') '
	END
	INSERT INTO LetterDataLogger
		([log_message], [letter_Id])
	VALUES(@Message_Created, @Letter_id)
END