-- =============================================
-- Author:		Name
-- Create date: 
-- Description:	
-- =============================================
CREATE PROCEDURE [dbo].[GetEducationList] 
	-- Add the parameters for the stored procedure here

AS
BEGIN
	    SELECT ID, Education FROM Education  -- Assuming ID is the primary key and Education is the description
END
