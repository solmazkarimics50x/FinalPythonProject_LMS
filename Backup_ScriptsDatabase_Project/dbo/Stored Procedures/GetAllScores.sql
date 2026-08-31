-- =============================================
-- Author:		Name
-- Create date: 
-- Description:	
-- =============================================
CREATE PROCEDURE [dbo].[GetAllScores] 
	-- Add the parameters for the stored procedure here

AS
BEGIN


    -- Insert statements for procedure here
	SELECT StudentID,CoursesID,TeacherID,TermNumber,Score from Student_Courses_Teacher
END
