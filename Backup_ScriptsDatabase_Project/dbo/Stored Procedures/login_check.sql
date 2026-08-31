-- =============================================
-- Author:		Name
-- Create date: 
-- Description:	
-- =============================================
CREATE PROCEDURE login_check 
	-- Add the parameters for the stored procedure here
	@user_name varchar(50), 
	@password varchar(50)
AS
BEGIN
	-- SET NOCOUNT ON added to prevent extra result sets from
	-- interfering with SELECT statements.
	SET NOCOUNT ON;

    -- Insert statements for procedure here
	SELECT UserName,[Password],FirstName,LastName,isAdmin FROM Users
                                  WHERE UserName = @user_name and [Password] = @password and isActive = 1 
END
