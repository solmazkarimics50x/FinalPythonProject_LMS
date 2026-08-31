CREATE TABLE [dbo].[Employee] (
    [PersonID]        INT          NOT NULL,
    [EmployeeID]      INT          NOT NULL,
    [MaritalStatus]   NVARCHAR (5) NOT NULL,
    [JobID]           TINYINT      NOT NULL,
    [DepartmentID]    TINYINT      NOT NULL,
    [Hiredata]        DATE         NOT NULL,
    [InsuranceNumber] BIGINT       NOT NULL,
    [AccountNumber]   CHAR (16)    NOT NULL,
    [ManagerID]       INT          NULL,
    CONSTRAINT [PK_Employee] PRIMARY KEY CLUSTERED ([PersonID] ASC),
    CONSTRAINT [FK_Employee_Department] FOREIGN KEY ([DepartmentID]) REFERENCES [dbo].[Department] ([ID]),
    CONSTRAINT [FK_Employee_Employee] FOREIGN KEY ([ManagerID]) REFERENCES [dbo].[Employee] ([PersonID]),
    CONSTRAINT [FK_Employee_Job] FOREIGN KEY ([JobID]) REFERENCES [dbo].[Job] ([ID]),
    CONSTRAINT [FK_Employee_Person] FOREIGN KEY ([PersonID]) REFERENCES [dbo].[Person] ([ID])
);

