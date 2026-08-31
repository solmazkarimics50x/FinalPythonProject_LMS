-- =============================================
-- Author:		Name
-- Create date: 
-- Description:	
-- =============================================
CREATE PROCEDURE [dbo].[GetDepartmentList] 
	-- Add the parameters for the stored procedure here

AS
BEGIN
		SELECT ID, DepartmentName FROM Department  -- Assuming ID is the primary key and DepartmentName is the description
END
