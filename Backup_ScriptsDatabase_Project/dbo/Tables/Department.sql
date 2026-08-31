CREATE TABLE [dbo].[Department] (
    [ID]             TINYINT       IDENTITY (1, 1) NOT NULL,
    [DepartmentName] NVARCHAR (50) NOT NULL,
    CONSTRAINT [PK_Department] PRIMARY KEY CLUSTERED ([ID] ASC)
);

