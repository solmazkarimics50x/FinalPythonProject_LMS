CREATE TABLE [dbo].[Users] (
    [ID]        INT          IDENTITY (1, 1) NOT NULL,
    [UserName]  VARCHAR (50) NULL,
    [Password]  VARCHAR (50) NULL,
    [FirstName] VARCHAR (50) NULL,
    [LastName]  VARCHAR (50) NULL,
    [isActive]  BIT          CONSTRAINT [DF_Users_isActive] DEFAULT ((1)) NULL,
    [isAdmin]   BIT          CONSTRAINT [DF_Users_isAdmin] DEFAULT ((1)) NULL,
    CONSTRAINT [PK_Users] PRIMARY KEY CLUSTERED ([ID] ASC)
);

