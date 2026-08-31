-- =============================================
-- Author:		Name
-- Create date: 
-- Description:	
-- =============================================
CREATE PROCEDURE [dbo].[GetJobList] 
	-- Add the parameters for the stored procedure here

AS
BEGIN
			SELECT ID, JobTitle FROM Job  -- Assuming ID is the primary key and JobTitle is the description
END
