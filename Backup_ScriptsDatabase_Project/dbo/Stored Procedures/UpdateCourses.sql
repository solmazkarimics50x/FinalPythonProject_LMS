-- =============================================
-- Author:		Name
-- Create date: 
-- Description:	
-- =============================================
CREATE PROCEDURE [dbo].[UpdateCourses] 
	-- Add the parameters for the stored procedure here
	@CoursesID smallint , 
	@CourseName NVARCHAR(50),
	@EnglishCourseName VARCHAR(50),
	@Duration tinyint,
	@SyllabusFile VARBINARY(MAX),
	@PrerequisiteID smallint,
	@CourseCategoryID tinyint
AS
BEGIN
	-- SET NOCOUNT ON added to prevent extra result sets from
	-- interfering with SELECT statements.
	SET NOCOUNT ON;

    -- Insert statements for procedure here
		UPDATE [dbo].Courses SET
		CourseName = @CourseName,
		EnglishCourseName = @EnglishCourseName,
		Duration =@Duration,
		SyllabusFile = @SyllabusFile,
		PrerequisiteID = @PrerequisiteID,
		CourseCategoryID = @CourseCategoryID
		
		where ID = @CoursesID
END
