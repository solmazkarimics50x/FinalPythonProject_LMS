-- =============================================
-- Author:		Name
-- Create date: 
-- Description:	
-- =============================================
CREATE PROCEDURE [dbo].[GetStudentList] 
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
		s.StudentCode,
		s.Job AS StudentJob
	FROM Person p
	INNER JOIN Student s ON p.ID = s.PersonID
	WHERE p.ID = @PersonID;
END
