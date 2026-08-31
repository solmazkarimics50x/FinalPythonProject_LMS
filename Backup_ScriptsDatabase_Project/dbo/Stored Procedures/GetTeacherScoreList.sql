-- =============================================
-- Author:		Name
-- Create date: 
-- Description:	
-- =============================================
CREATE PROCEDURE [dbo].[GetTeacherScoreList] 
	-- Add the parameters for the stored procedure here

AS
BEGIN


    -- Insert statements for procedure here
	SELECT PersonID,TeacherCode,MaritalStatus,Startdate,InsuranceNumber,AccountNumber From Teacher
END
