-- =============================================
-- Author:		Name
-- Create date: 
-- Description:	
-- =============================================
CREATE PROCEDURE [dbo].[sp_InsertStudent] 
	-- Add the parameters for the stored procedure here
	@FirstName nvarchar(20) , 
	@LastName nvarchar(30),
	@Birthdate date,
	@NationalCode char(10),
	@Gender nvarchar(50),
	@Address nvarchar(250),
	@Mobile char(11),
	@Photo varbinary(max),
	@EducationID tinyint,
	@StudentCode INT,
	@Job nvarchar(20)
AS
BEGIN

	SET NOCOUNT ON;  -- Prevent extra result sets from interfering with SELECT statements

		-- Insert the new student record into the Person table
	INSERT INTO Person (FirstName, LastName, Birthdate, NationalCode, Gender, [Address], Mobile,Photo, EducationID)
    VALUES (@FirstName, @LastName, @Birthdate, @NationalCode, @Gender, @Address, @Mobile,@Photo, @EducationID);
   	-- Get the last inserted ID
    DECLARE @NewPersonID INT = SCOPE_IDENTITY();
   
       -- Insert into the Student table using the new PersonID
	INSERT INTO Student (PersonID, StudentCode, Job)
	VALUES (@NewPersonID, @StudentCode, @Job);

		-- Return the new PersonID
    SELECT @NewPersonID AS PersonID;
END
