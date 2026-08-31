-- =============================================
-- Author:		Name
-- Create date: 
-- Description:	
-- =============================================
CREATE PROCEDURE [dbo].[UpdateEducation] 
	-- Add the parameters for the stored procedure here
	@EducationID tinyint , 
	@Education NVARCHAR(50)
AS
BEGIN
	-- SET NOCOUNT ON added to prevent extra result sets from
	-- interfering with SELECT statements.
	SET NOCOUNT ON;

    -- Insert statements for procedure here
		UPDATE [dbo].Education SET
		Education = @Education
		
	where ID = @EducationID
END
