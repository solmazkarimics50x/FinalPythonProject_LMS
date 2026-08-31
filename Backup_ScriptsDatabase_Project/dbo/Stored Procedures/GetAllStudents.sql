-- =============================================
-- Author:		Name
-- Create date: 
-- Description:	
-- =============================================
CREATE PROCEDURE [dbo].[GetAllStudents] 
	-- Add the parameters for the stored procedure here

AS
BEGIN
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
END
