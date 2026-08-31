-- =============================================
-- Author:		Name
-- Create date: 
-- Description:	
-- =============================================
CREATE PROCEDURE [dbo].[SP_DeleteStudent] 
	-- Add the parameters for the stored procedure here
	@PersonID INT
AS
BEGIN

    SET NOCOUNT ON;  -- Prevents extra result sets from interfering with SELECT statements.

    -- Check if the student exists in the Student table
    IF EXISTS (SELECT 1 FROM Student WHERE PersonID = @PersonID)
    BEGIN
        -- Delete from the Student table
        DELETE FROM Student WHERE PersonID = @PersonID;
    END

    -- Check if the person exists in the Person table
    IF EXISTS (SELECT 1 FROM Person WHERE ID = @PersonID)
    BEGIN
        -- Delete from the Person table
        DELETE FROM Person WHERE ID = @PersonID;
    END
    ELSE
    BEGIN
        -- Optionally, you could raise an error or return a message
        RAISERROR('Person not found', 16, 1);
    END
END
