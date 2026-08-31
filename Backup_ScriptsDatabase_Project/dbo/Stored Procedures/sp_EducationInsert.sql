-- =============================================
-- Author:		Name
-- Create date: 
-- Description:	
-- =============================================
CREATE PROCEDURE [dbo].[sp_EducationInsert] 
	-- Add the parameters for the stored procedure here
	@Education NVARCHAR(50)
AS
BEGIN
	-- SET NOCOUNT ON added to prevent extra result sets from
	-- interfering with SELECT statements.
	SET NOCOUNT ON;

    -- Insert statements for procedure here
		insert into [dbo].Education(Education)
	    VALUES(@Education)
		   	-- Get the last inserted ID
    DECLARE @NewEducationID INT = SCOPE_IDENTITY();

			-- Return the new EducationID
    SELECT @NewEducationID AS EducationID
END
