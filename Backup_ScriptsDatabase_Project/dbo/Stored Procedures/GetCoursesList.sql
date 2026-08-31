-- =============================================
-- Author:		Name
-- Create date: 
-- Description:	
-- =============================================
CREATE PROCEDURE [dbo].[GetCoursesList] 
	-- Add the parameters for the stored procedure here

AS
BEGIN

    -- Insert statements for procedure here
	SELECT ID,CourseName,EnglishCourseName,Duration,SyllabusFile,PrerequisiteID,CourseCategoryID From Courses
END
