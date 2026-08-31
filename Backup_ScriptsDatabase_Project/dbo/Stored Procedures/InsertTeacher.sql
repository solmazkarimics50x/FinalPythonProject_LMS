-- =============================================
-- Author:		Name
-- Create date: 
-- Description:	
-- =============================================
CREATE PROCEDURE [dbo].[InsertTeacher] 
	-- Add the parameters for the stored procedure here
    @FirstName NVARCHAR(20),
    @LastName NVARCHAR(30),
    @Birthdate DATE,
    @NationalCode CHAR(10),
    @Gender NVARCHAR(50),
    @Address NVARCHAR(250),
    @Mobile CHAR(11),
    @Photo VARBINARY(MAX),
    @EducationID TINYINT,
    @TeacherCode INT,
    @MaritalStatus NVARCHAR(5),
    @StartDate DATE,
    @InsuranceNumber BIGINT,
    @AccountNumber CHAR(16),
    @CertificateID SMALLINT,
    @ExpirationDate DATE,
    @ResID VARCHAR(50)
AS
BEGIN
    SET NOCOUNT ON;

    BEGIN TRY
        BEGIN TRANSACTION;

        -- Insert into Person table
        INSERT INTO Person (FirstName, LastName, Birthdate, NationalCode, Gender, [Address], Mobile, Photo, EducationID)
        VALUES (@FirstName, @LastName, @Birthdate, @NationalCode, @Gender, @Address, @Mobile, @Photo, @EducationID);

        -- Get the last inserted PersonID, which is also the TeacherID
        DECLARE @NewPersonID INT = SCOPE_IDENTITY();

        -- Insert into Teacher table using the same PersonID as TeacherID
        INSERT INTO Teacher (PersonID, TeacherCode, MaritalStatus, StartDate, InsuranceNumber, AccountNumber)
        VALUES (@NewPersonID, @TeacherCode, @MaritalStatus, @StartDate, @InsuranceNumber, @AccountNumber);

        -- Insert into Teacher_Certificate table using the same PersonID as TeacherID
        INSERT INTO Teacher_Certificate (TeacherID, CertificateID, ExpirationDate, ResID)
        VALUES (@NewPersonID, @CertificateID, @ExpirationDate, @ResID);

        -- Commit the transaction
        COMMIT TRANSACTION;

        -- Return the new PersonID
        SELECT @NewPersonID AS PersonID;
    END TRY
    BEGIN CATCH
        -- Rollback the transaction in case of error
        ROLLBACK TRANSACTION;

        -- Return error information
        DECLARE @ErrorMessage NVARCHAR(4000);
        DECLARE @ErrorSeverity INT;
        DECLARE @ErrorState INT;

        SELECT 
            @ErrorMessage = ERROR_MESSAGE(),
            @ErrorSeverity = ERROR_SEVERITY(),
            @ErrorState = ERROR_STATE();

        RAISERROR(@ErrorMessage, @ErrorSeverity, @ErrorState);
    END CATCH
END
