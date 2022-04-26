CREATE TRIGGER DBO.SubActors_INSTEAD_OF_INSERT_sub_actor_parent
ON [dbo].[SubActors]
INSTEAD OF INSERT 
AS
BEGIN

    DECLARE @Sub_Actor_Parent INT;

    SET @Sub_Actor_Parent = (SELECT [sub_actor_parent]
    FROM INSERTED)

    IF @Sub_Actor_Parent IS NULL 
	BEGIN
        INSERT INTO [dbo].[SubActors]
            ([main_actor_id],[sub_actor_Ar],[sub_actor_En],[created_at],[modified_at],[sub_actor_parent])
        SELECT INSERTED.[main_actor_id]
      , INSERTED.[sub_actor_Ar]
      , INSERTED.[sub_actor_En]
      , INSERTED.[created_at]
      , INSERTED.[modified_at]
      , INSERTED.[sub_actor_parent]
        FROM INSERTED

    END
ELSE 
	BEGIN
        DECLARE @main_actor_id INT;
        SET @main_actor_id = (SELECT main_actor_id
        FROM [dbo].[SubActors]
        WHERE [sub_actor_id] = @Sub_Actor_Parent)

        INSERT INTO [dbo].[SubActors]
            ([main_actor_id],[sub_actor_Ar],[sub_actor_En],[created_at],[modified_at],[sub_actor_parent])
        SELECT @main_actor_id, INSERTED.[sub_actor_Ar] , INSERTED.[sub_actor_En] , INSERTED.[created_at] , INSERTED.[modified_at], INSERTED.[sub_actor_parent]
        FROM INSERTED

    END
END