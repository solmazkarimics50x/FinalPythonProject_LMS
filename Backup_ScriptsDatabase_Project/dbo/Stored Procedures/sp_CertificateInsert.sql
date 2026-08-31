-- =============================================
-- Author:		Name
-- Create date: 
-- Description:	
-- =============================================
CREATE PROCEDURE [dbo].[sp_CertificateInsert] 
	-- Add the parameters for the stored procedure here
	@CertificateTitle VARCHAR(100),
	@Vendor VARCHAR(50)
AS
BEGIN
	-- SET NOCOUNT ON added to prevent extra result sets from
	-- interfering with SELECT statements.
	SET NOCOUNT ON;

	    -- Insert statements for procedure here
		insert into [dbo].[Certificate](CertificateTitle,Vendor)
	    VALUES(@CertificateTitle,@Vendor)
		   	-- Get the last inserted ID
    DECLARE @NewCertificateID INT = SCOPE_IDENTITY();

			-- Return the new CertificateID
    SELECT @NewCertificateID AS CertificateID
END
