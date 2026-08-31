CREATE TABLE [dbo].[Student] (
    [PersonID]    INT           NOT NULL,
    [StudentCode] INT           NOT NULL,
    [Job]         NVARCHAR (20) NOT NULL,
    CONSTRAINT [PK_Student_1] PRIMARY KEY CLUSTERED ([PersonID] ASC),
    CONSTRAINT [FK_Student_Person] FOREIGN KEY ([PersonID]) REFERENCES [dbo].[Person] ([ID])
);

