-- =============================================
-- Author:		Name
-- Create date: 
-- Description:	
-- =============================================
CREATE PROCEDURE [dbo].[GetEmployeeList]  
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
		e.EmployeeID,
		e.MaritalStatus,
		e.JobID,
		e.DepartmentID,
		e.Hiredata,
		e.InsuranceNumber,
		e.AccountNumber,
		e.ManagerID

	FROM Person p
	INNER JOIN Employee e ON p.ID = e.PersonID
	WHERE p.ID = @PersonID;
END
