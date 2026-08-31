-- =============================================
-- Author:		Name
-- Create date: 
-- Description:	
-- =============================================
CREATE PROCEDURE [dbo].[sp_ScoreInsert]  
	-- Add the parameters for the stored procedure here
    @StudentID INT,          -- Input parameter for StudentID
    @CoursesID SMALLINT,     -- Input parameter for CoursesID
    @TeacherID INT,          -- Input parameter for TeacherID
    @TermNumber INT,         -- Input parameter for TermNumber
    @Score TINYINT           -- Input parameter for Score
AS
BEGIN
    -- Prevent extra result sets from interfering with SELECT statements
    SET NOCOUNT ON;

    -- Check if the combination of StudentID, CoursesID, TeacherID, and TermNumber already exists
    IF EXISTS (
        SELECT 1 
        FROM Student_Courses_Teacher 
        WHERE StudentID = @StudentID 
          AND CoursesID = @CoursesID 
          AND TeacherID = @TeacherID
          AND TermNumber = @TermNumber  -- Include TermNumber in the check
    )
    BEGIN
        -- Raise an error if the record already exists
        RAISERROR('A record with the same StudentID, CoursesID, TeacherID, and TermNumber already exists.', 16, 1);
        RETURN;
    END

    -- Insert the score into the Student_Courses_Teacher table
    INSERT INTO Student_Courses_Teacher (StudentID, CoursesID, TeacherID, TermNumber, Score)
    VALUES (@StudentID, @CoursesID, @TeacherID, @TermNumber, @Score);
    
    -- Optionally, return the newly generated TermNumber
    SELECT @TermNumber AS NewTermNumber;  -- Return the TermNumber that was inserted
END
