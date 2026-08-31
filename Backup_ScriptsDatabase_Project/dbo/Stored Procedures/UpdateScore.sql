-- =============================================
-- Author:		Name
-- Create date: 
-- Description:	
-- =============================================
CREATE PROCEDURE [dbo].[UpdateScore] 
	-- Add the parameters for the stored procedure here
    
    @StudentID INT,
    @CoursesID SMALLINT,
    @TeacherID INT,
	@TermNumber INT,
    @Score TINYINT
AS
BEGIN
    SET NOCOUNT ON;
    
    -- Update ONLY the score for the exact composite key match
    UPDATE Student_Courses_Teacher
    SET Score = @Score
    WHERE TermNumber = @TermNumber
      AND StudentID = @StudentID
      AND CoursesID = @CoursesID
      AND TeacherID = @TeacherID;
	  

END
