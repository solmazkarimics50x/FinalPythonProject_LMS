-- =============================================
-- Author:		Name
-- Create date: 
-- Description:	
-- =============================================
CREATE PROCEDURE [dbo].[sp_CoursesInsert] 
	-- Add the parameters for the stored procedure here
	@CourseName NVARCHAR(50),
	@EnglishCourseName VARCHAR(50),
	@Duration tinyint,
	@SyllabusFile varbinary(max),
	@PrerequisiteID smallint,
	@CourseCategoryID tinyint
AS
BEGIN

	SET NOCOUNT ON;

	-- Check if the CourseCategoryID exists
    IF NOT EXISTS (SELECT 1 FROM dbo.CourseCategory WHERE ID = @CourseCategoryID)
    BEGIN
        RAISERROR('The specified CourseCategoryID does not exist.', 16, 1);
        RETURN;
    END


    -- Insert statements for procedure here
		insert into [dbo].Courses (CourseName,EnglishCourseName,Duration,SyllabusFile,PrerequisiteID,CourseCategoryID)
	    VALUES(@CourseName,@EnglishCourseName,@Duration,@SyllabusFile,@PrerequisiteID,@CourseCategoryID)
		   	-- Get the last inserted ID
    DECLARE @NewCoursesID Smallint = SCOPE_IDENTITY();

			-- Return the new CoursesID
    SELECT @NewCoursesID AS CoursesID
END
