-- =============================================
-- Author:		Name
-- Create date: 
-- Description:	
-- =============================================
CREATE PROCEDURE [dbo].[sp_CourseCategoryInsert] 
	-- Add the parameters for the stored procedure here
	@CourseCategoryName NVARCHAR(50),
	@EnglishCourseCategoryName VARCHAR(50)
AS
BEGIN
	-- SET NOCOUNT ON added to prevent extra result sets from
	-- interfering with SELECT statements.
	SET NOCOUNT ON;

    -- Insert statements for procedure here
		insert into [dbo].CourseCategory (CourseCategoryName,EnglishCourseCategoryName)
	    VALUES(@CourseCategoryName,@EnglishCourseCategoryName)
		   	-- Get the last inserted ID
    DECLARE @NewCourseCategoryID INT = SCOPE_IDENTITY();

			-- Return the new CourseCategoryID
    SELECT @NewCourseCategoryID AS CourseCategoryID
END
