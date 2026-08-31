-- =============================================
-- Author:		Name
-- Create date: 
-- Description:	
-- =============================================
CREATE PROCEDURE [dbo].[UpdateDepartment] 
	-- Add the parameters for the stored procedure here
	@DepartmentID tinyint , 
	@DepartmentName NVARCHAR(50)
AS
BEGIN
	-- SET NOCOUNT ON added to prevent extra result sets from
	-- interfering with SELECT statements.
	SET NOCOUNT ON;

    -- Insert statements for procedure here
		UPDATE [dbo].Department SET
		DepartmentName = @DepartmentName
		
	    where ID = @DepartmentID
END
