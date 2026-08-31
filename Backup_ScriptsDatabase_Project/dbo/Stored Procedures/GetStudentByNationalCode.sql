-- =============================================
-- Author:		Name
-- Create date: 
-- Description:	
-- =============================================
CREATE PROCEDURE [dbo].[GetStudentByNationalCode] 
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
        s.StudentCode,
        s.Job AS StudentJob
    FROM Person p
    INNER JOIN Student s ON p.ID = s.PersonID
    WHERE p.NationalCode = @NationalCode;
END
