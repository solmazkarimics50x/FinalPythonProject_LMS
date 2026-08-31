-- =============================================
-- Author:		Name
-- Create date: 
-- Description:	
-- =============================================
CREATE PROCEDURE [dbo].[GetStudentScoreList] 
	-- Add the parameters for the stored procedure here

AS
BEGIN


    -- Insert statements for procedure here
	SELECT PersonID,StudentCode,Job From Student
END
