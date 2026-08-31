-- =============================================
-- Author:		Name
-- Create date: 
-- Description:	
-- =============================================
CREATE PROCEDURE [dbo].[GetNewTeacherList] 
	-- Add the parameters for the stored procedure here
	@PersonID INT

AS
BEGIN
    SET NOCOUNT ON;

    SELECT 
        p.ID AS PersonID,
        p.FirstName,
        p.LastName,
        p.Birthdate,
        p.NationalCode,
        p.Gender,
        p.[Address],
        p.Mobile,
        p.Photo,
        p.EducationID,
        t.TeacherCode,
        t.MaritalStatus,
        t.StartDate,
        t.InsuranceNumber,
        t.AccountNumber,
        tc.CertificateID,
        tc.ExpirationDate,
        tc.ResID
    FROM 
        Person p
    INNER JOIN 
        Teacher t ON p.ID = t.PersonID
    LEFT JOIN 
        Teacher_Certificate tc ON t.PersonID = tc.TeacherID  -- Assuming TeacherCode is the correct foreign key
    WHERE 
        p.ID = @PersonID  -- Filter by the provided PersonID
END

