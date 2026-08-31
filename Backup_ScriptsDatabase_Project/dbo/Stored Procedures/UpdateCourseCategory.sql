-- =============================================
-- Author:		Name
-- Create date: 
-- Description:	
-- =============================================
CREATE PROCEDURE [dbo].[UpdateCourseCategory]
	-- Add the parameters for the stored procedure here
	@CourseCategoryID tinyint , 
	@CourseCategoryName NVARCHAR(50),
	@EnglishCourseCategoryName VARCHAR(50)
AS
BEGIN
	-- SET NOCOUNT ON added to prevent extra result sets from
	-- interfering with SELECT statements.
	SET NOCOUNT ON;

    -- Insert statements for procedure here
		UPDATE [dbo].CourseCategory SET
		CourseCategoryName = @CourseCategoryName,
		EnglishCourseCategoryName = @EnglishCourseCategoryName
		
	where ID = @CourseCategoryID
END
