-- =============================================
-- Author:		Name
-- Create date: 
-- Description:	
-- =============================================
CREATE PROCEDURE [dbo].[SP_DeleteScore]
	-- Add the parameters for the stored procedure here
    @StudentID INT,
    @CoursesID Smallint,
    @TeacherID INT,
    @TermNumber INT
AS
BEGIN
    SET NOCOUNT ON;

    -- Delete the score record from the Scores table
    DELETE FROM Student_Courses_Teacher
    WHERE StudentID = @StudentID
      AND CoursesID = @CoursesID
      AND TeacherID = @TeacherID
      AND TermNumber = @TermNumber;

    -- Optionally, you can check if the deletion was successful
    IF @@ROWCOUNT = 0
    BEGIN
        -- No rows were deleted, you can return an error or a message
        RAISERROR('No record found to delete.', 16, 1);
    END
END
