-- =============================================
-- Author:		Name
-- Create date: 
-- Description:	
-- =============================================
CREATE PROCEDURE [dbo].[UpdateJob] 
	-- Add the parameters for the stored procedure here
	@JobID tinyint , 
	@JobTitle NVARCHAR(50)
AS
BEGIN
	-- SET NOCOUNT ON added to prevent extra result sets from
	-- interfering with SELECT statements.
	SET NOCOUNT ON;

    -- Insert statements for procedure here
		UPDATE [dbo].Job SET
		JobTitle = @JobTitle
		
	where ID = @JobID
END
