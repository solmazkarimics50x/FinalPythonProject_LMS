-- =============================================
-- Author:		Name
-- Create date: 
-- Description:	
-- =============================================
CREATE PROCEDURE [dbo].[UpdateCertificate]  
	-- Add the parameters for the stored procedure here
	@CertificateID smallint , 
	@CertificateTitle VARCHAR(100),
	@Vendor VARCHAR(50)
AS
BEGIN
	-- SET NOCOUNT ON added to prevent extra result sets from
	-- interfering with SELECT statements.
	SET NOCOUNT ON;

    -- Insert statements for procedure here
		UPDATE [dbo].[Certificate] SET
		CertificateTitle = @CertificateTitle,
		Vendor = @Vendor
		
	where ID = @CertificateID
END
