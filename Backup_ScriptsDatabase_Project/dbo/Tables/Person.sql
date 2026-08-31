CREATE TABLE [dbo].[Person] (
    [ID]           INT             IDENTITY (1, 1) NOT NULL,
    [FirstName]    NVARCHAR (20)   NOT NULL,
    [LastName]     NVARCHAR (30)   NOT NULL,
    [Birthdate]    DATE            NOT NULL,
    [NationalCode] CHAR (10)       NOT NULL,
    [Gender]       NVARCHAR (50)   NOT NULL,
    [Address]      NVARCHAR (250)  NULL,
    [Mobile]       CHAR (11)       NOT NULL,
    [Photo]        VARBINARY (MAX) NULL,
    [EducationID]  TINYINT         NOT NULL,
    CONSTRAINT [PK_Person] PRIMARY KEY CLUSTERED ([ID] ASC),
    CONSTRAINT [FK_Person_Education] FOREIGN KEY ([EducationID]) REFERENCES [dbo].[Education] ([ID])
);


GO
EXECUTE sp_addextendedproperty @name = N'MS_Description', @value = N'First name of the person', @level0type = N'SCHEMA', @level0name = N'dbo', @level1type = N'TABLE', @level1name = N'Person', @level2type = N'COLUMN', @level2name = N'FirstName';


GO
EXECUTE sp_addextendedproperty @name = N'MS_Description', @value = N'Last name of the person', @level0type = N'SCHEMA', @level0name = N'dbo', @level1type = N'TABLE', @level1name = N'Person', @level2type = N'COLUMN', @level2name = N'LastName';


GO
EXECUTE sp_addextendedproperty @name = N'MS_Description', @value = N'Birthdate of the person', @level0type = N'SCHEMA', @level0name = N'dbo', @level1type = N'TABLE', @level1name = N'Person', @level2type = N'COLUMN', @level2name = N'Birthdate';


GO
EXECUTE sp_addextendedproperty @name = N'MS_Description', @value = N'National key of the person', @level0type = N'SCHEMA', @level0name = N'dbo', @level1type = N'TABLE', @level1name = N'Person', @level2type = N'COLUMN', @level2name = N'NationalCode';


GO
EXECUTE sp_addextendedproperty @name = N'MS_Description', @value = N'sex of the person', @level0type = N'SCHEMA', @level0name = N'dbo', @level1type = N'TABLE', @level1name = N'Person', @level2type = N'COLUMN', @level2name = N'Gender';


GO
EXECUTE sp_addextendedproperty @name = N'MS_Description', @value = N'Address of the person', @level0type = N'SCHEMA', @level0name = N'dbo', @level1type = N'TABLE', @level1name = N'Person', @level2type = N'COLUMN', @level2name = N'Address';


GO
EXECUTE sp_addextendedproperty @name = N'MS_Description', @value = N'Mobile of the person', @level0type = N'SCHEMA', @level0name = N'dbo', @level1type = N'TABLE', @level1name = N'Person', @level2type = N'COLUMN', @level2name = N'Mobile';


GO
EXECUTE sp_addextendedproperty @name = N'MS_Description', @value = N'Photo of the person', @level0type = N'SCHEMA', @level0name = N'dbo', @level1type = N'TABLE', @level1name = N'Person', @level2type = N'COLUMN', @level2name = N'Photo';

