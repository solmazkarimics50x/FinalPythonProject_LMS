-- =============================================
-- Author:		Name
-- Create date: 
-- Description:	
-- =============================================
CREATE PROCEDURE [dbo].[RegisterUsers] 
    -- Parameters (removed @isActive since it's hardcoded and not passed from Python)
    @UserName NVARCHAR(50),    -- Adjust length to match your table (e.g., NVARCHAR(100) if needed)
    @Password NVARCHAR(50),
    @FirstName NVARCHAR(50),
    @LastName NVARCHAR(50),
    @isAdmin BIT 
AS
BEGIN
    -- Optional: Add validation to prevent duplicates
    IF EXISTS (SELECT 1 FROM Users WHERE UserName = @UserName)
    BEGIN
        RAISERROR('UserName already exists.', 16, 1);
        RETURN;
    END
    
    -- Insert the new user
    INSERT INTO Users (UserName, Password, FirstName, LastName, isActive, isAdmin)
    VALUES (@UserName, @Password, @FirstName, @LastName, 1, @isAdmin);  -- isActive hardcoded to 1
END
