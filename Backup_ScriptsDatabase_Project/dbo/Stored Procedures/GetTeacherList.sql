-- =============================================
-- Author:		Name
-- Create date: 
-- Description:	
-- =============================================
CREATE PROCEDURE [dbo].[GetTeacherList] 
	-- Add the parameters for the stored procedure here
	@PersonID INT
AS
BEGIN
	SET NOCOUNT ON;

	SELECT
		p.ID AS person_id,-- Include person_id
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
	WHERE p.ID = @PersonID;
END
