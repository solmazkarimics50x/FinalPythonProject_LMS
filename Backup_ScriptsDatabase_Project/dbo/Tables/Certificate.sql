CREATE TABLE [dbo].[Certificate] (
    [ID]               SMALLINT      IDENTITY (1, 1) NOT NULL,
    [CertificateTitle] VARCHAR (100) NOT NULL,
    [Vendor]           VARCHAR (50)  NOT NULL,
    CONSTRAINT [PK_Certificate] PRIMARY KEY CLUSTERED ([ID] ASC)
);

