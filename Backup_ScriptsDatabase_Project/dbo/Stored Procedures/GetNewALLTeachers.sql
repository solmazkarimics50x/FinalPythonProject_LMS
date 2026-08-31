-- =============================================
-- Author:		Name
-- Create date: 
-- Description:	
-- =============================================
CREATE PROCEDURE [dbo].[GetNewALLTeachers] 
	-- Add the parameters for the stored procedure here

AS
BEGIN
	-- SET NOCOUNT ON added to prevent extra result sets from
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
        Teacher_Certificate tc ON t.PersonID = tc.TeacherID 


END
