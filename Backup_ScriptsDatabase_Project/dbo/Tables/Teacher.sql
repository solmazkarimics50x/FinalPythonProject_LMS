CREATE TABLE [dbo].[Teacher] (
    [PersonID]        INT          NOT NULL,
    [TeacherCode]     INT          NOT NULL,
    [MaritalStatus]   NVARCHAR (5) NOT NULL,
    [StartDate]       DATE         NOT NULL,
    [InsuranceNumber] BIGINT       NOT NULL,
    [AccountNumber]   CHAR (16)    NOT NULL,
    CONSTRAINT [PK_Teacher] PRIMARY KEY CLUSTERED ([PersonID] ASC),
    CONSTRAINT [FK_Teacher_Person] FOREIGN KEY ([PersonID]) REFERENCES [dbo].[Person] ([ID])
);

