-- =============================================
-- Author:		Name
-- Create date: 
-- Description:	
-- =============================================
CREATE PROCEDURE [dbo].[UpdateEmployee] 
	-- Add the parameters for the stored procedure here
	@PersonID INT,
    @FirstName NVARCHAR(20),
    @LastName NVARCHAR(30),
    @Birthdate DATE,
    @NationalCode CHAR(10),
    @Gender NVARCHAR(50),
    @Address NVARCHAR(250),
    @Mobile CHAR(11),
    @Photo VARBINARY(MAX),
    @EducationID TINYINT,
	@EmployeeID INT,
	@MaritalStatus nvarchar(5),
	@JobID TINYINT,
	@DepartmentID TINYINT,
	@Hiredata date,
	@InsuranceNumber bigint,
	@AccountNumber char(16),
	@ManagerID INT
AS
BEGIN
    SET NOCOUNT ON;

    BEGIN TRY
        -- Update the Person table
        UPDATE Person
        SET
            FirstName = @FirstName,
            LastName = @LastName,
            Birthdate = @Birthdate,
            NationalCode = @NationalCode,
            Gender = @Gender,
            [Address] = @Address,
            Mobile = @Mobile,
            Photo = @Photo,
            EducationID = @EducationID
        WHERE 
            ID = @PersonID;

        -- Update the Teacher table
        UPDATE Employee
        SET 
            EmployeeID = @EmployeeID,
            MaritalStatus = @MaritalStatus,
			JobID = @JobID,
			DepartmentID = @DepartmentID,
			Hiredata = @hiredata,
			InsuranceNumber = @InsuranceNumber,
			AccountNumber = @AccountNumber,
			ManagerID =@ManagerID
        WHERE 
            PersonID = @PersonID;

        -- Optionally, you can return the number of rows affected
        SELECT @@ROWCOUNT AS RowsAffected;
    END TRY
    BEGIN CATCH
        -- Handle the error
        SELECT ERROR_NUMBER() AS ErrorNumber, ERROR_MESSAGE() AS ErrorMessage;
    END CATCH
END
