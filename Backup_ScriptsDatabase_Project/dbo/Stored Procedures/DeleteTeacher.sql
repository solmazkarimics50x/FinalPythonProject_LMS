-- =============================================
-- Author:		Name
-- Create date: 
-- Description:	
-- =============================================
CREATE PROCEDURE [dbo].[DeleteTeacher]  
	-- Add the parameters for the stored procedure here
	@PersonID INT
AS
BEGIN
	-- SET NOCOUNT ON added to prevent extra result sets from
	-- interfering with SELECT statements.
	SET NOCOUNT ON;

    -- Check if the Teacher_Certificate exists in the Teacher_Certificate table
    IF EXISTS (SELECT 1 FROM Teacher_Certificate WHERE TeacherID = @PersonID)
    BEGIN
        -- Delete from the Teacher_Certificate table
        DELETE FROM Teacher_Certificate WHERE TeacherID = @PersonID;
    END

    -- Check if the Teacher exists in the Teacher table
    IF EXISTS (SELECT 1 FROM Teacher WHERE PersonID = @PersonID)
    BEGIN
        -- Delete from the Teacher table
        DELETE FROM Teacher WHERE PersonID = @PersonID;
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
