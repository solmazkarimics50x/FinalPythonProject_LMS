-- =============================================
-- Author:		Name
-- Create date: 
-- Description:	
-- =============================================
CREATE PROCEDURE [dbo].[sp_JobInsert] 
	-- Add the parameters for the stored procedure here
	@JobTitle NVARCHAR(50)
AS
BEGIN
	-- SET NOCOUNT ON added to prevent extra result sets from
	-- interfering with SELECT statements.
	SET NOCOUNT ON;

    -- Insert statements for procedure here
		insert into [dbo].Job(JobTitle)
	    VALUES(@JobTitle)
		   	-- Get the last inserted ID
    DECLARE @NewJobID INT = SCOPE_IDENTITY();

			-- Return the new JobID
    SELECT @NewJobID AS JobID
END
