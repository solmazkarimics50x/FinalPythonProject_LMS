CREATE TABLE [dbo].[Teacher_Certificate] (
    [TeacherID]      INT          NOT NULL,
    [CertificateID]  SMALLINT     NOT NULL,
    [ExpirationDate] DATE         NOT NULL,
    [ResID]          VARCHAR (50) NOT NULL,
    CONSTRAINT [PK_Teacher_Certificate] PRIMARY KEY CLUSTERED ([TeacherID] ASC, [CertificateID] ASC),
    CONSTRAINT [FK_Teacher_Certificate_Certificate] FOREIGN KEY ([CertificateID]) REFERENCES [dbo].[Certificate] ([ID]),
    CONSTRAINT [FK_Teacher_Certificate_Teacher] FOREIGN KEY ([TeacherID]) REFERENCES [dbo].[Teacher] ([PersonID])
);

