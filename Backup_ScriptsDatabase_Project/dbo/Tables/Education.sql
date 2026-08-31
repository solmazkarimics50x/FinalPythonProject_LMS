CREATE TABLE [dbo].[Education] (
    [ID]        TINYINT       IDENTITY (1, 1) NOT NULL,
    [Education] NVARCHAR (50) NOT NULL,
    CONSTRAINT [PK_Education] PRIMARY KEY CLUSTERED ([ID] ASC)
);


GO
EXECUTE sp_addextendedproperty @name = N'MS_Description', @value = N'Education level of the person', @level0type = N'SCHEMA', @level0name = N'dbo', @level1type = N'TABLE', @level1name = N'Education', @level2type = N'COLUMN', @level2name = N'Education';

