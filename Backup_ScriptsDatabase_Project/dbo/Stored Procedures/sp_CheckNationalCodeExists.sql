-- =============================================
-- Author:		Name
-- Create date: 
-- Description:	
-- =============================================
CREATE PROCEDURE [dbo].[sp_CheckNationalCodeExists] 
	-- Add the parameters for the stored procedure here
	 @NationalCode VARCHAR(10)
AS
BEGIN
	DECLARE @Exists BIT = 0
    
    IF EXISTS (SELECT 1 FROM Person WHERE NationalCode = @NationalCode)
        SET @Exists = 1
    
    SELECT @Exists AS NationalCodeExists
END
