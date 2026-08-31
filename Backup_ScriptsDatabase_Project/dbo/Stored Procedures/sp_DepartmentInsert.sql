-- =============================================
-- Author:		Name
-- Create date: 
-- Description:	
-- =============================================
CREATE PROCEDURE [dbo].[sp_DepartmentInsert] 
	-- Add the parameters for the stored procedure here
	@DepartmentName NVARCHAR(50)
AS
BEGIN
	-- SET NOCOUNT ON added to prevent extra result sets from
	-- interfering with SELECT statements.
	SET NOCOUNT ON;

    -- Insert statements for procedure here
		insert into [dbo].Department(DepartmentName)
	    VALUES(@DepartmentName)
		   	-- Get the last inserted ID
    DECLARE @NewDepartmentID INT = SCOPE_IDENTITY();

			-- Return the new DepartmentID
    SELECT @NewDepartmentID AS DepartmentID
END
