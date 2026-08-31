-- =============================================
-- Author:		Name
-- Create date: 
-- Description:	
-- =============================================
CREATE PROCEDURE [dbo].[GetTeacherByNationalCode] 
	-- Add the parameters for the stored procedure here
	@NationalCode VARCHAR(10)
AS
BEGIN
    SET NOCOUNT ON;  -- Prevent extra result sets from interfering with SELECT statements

    SELECT
        p.ID AS person_id,        -- Include person_id
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
		t.Startdate,
		t.InsuranceNumber,
		t.AccountNumber
    FROM Person p
    INNER JOIN Teacher t ON p.ID = t.PersonID
    WHERE p.NationalCode = @NationalCode;
END
