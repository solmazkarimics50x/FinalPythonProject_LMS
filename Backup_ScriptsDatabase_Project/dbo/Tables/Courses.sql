CREATE TABLE [dbo].[Courses] (
    [ID]                SMALLINT        IDENTITY (1, 1) NOT NULL,
    [CourseName]        NVARCHAR (50)   NOT NULL,
    [EnglishCourseName] VARCHAR (50)    NOT NULL,
    [Duration]          TINYINT         NOT NULL,
    [SyllabusFile]      VARBINARY (MAX) NULL,
    [PrerequisiteID]    SMALLINT        NULL,
    [CourseCategoryID]  TINYINT         NOT NULL,
    CONSTRAINT [PK_Courses] PRIMARY KEY CLUSTERED ([ID] ASC),
    CONSTRAINT [FK_Courses_CourseCategory] FOREIGN KEY ([CourseCategoryID]) REFERENCES [dbo].[CourseCategory] ([ID]),
    CONSTRAINT [FK_Courses_Courses] FOREIGN KEY ([PrerequisiteID]) REFERENCES [dbo].[Courses] ([ID])
);


GO
EXECUTE sp_addextendedproperty @name = N'MS_Description', @value = N'نام دوره', @level0type = N'SCHEMA', @level0name = N'dbo', @level1type = N'TABLE', @level1name = N'Courses', @level2type = N'COLUMN', @level2name = N'CourseName';


GO
EXECUTE sp_addextendedproperty @name = N'MS_Description', @value = N'نام دوره به انگلیسی', @level0type = N'SCHEMA', @level0name = N'dbo', @level1type = N'TABLE', @level1name = N'Courses', @level2type = N'COLUMN', @level2name = N'EnglishCourseName';


GO
EXECUTE sp_addextendedproperty @name = N'MS_Description', @value = N'مدت زمان دوره به ساعت', @level0type = N'SCHEMA', @level0name = N'dbo', @level1type = N'TABLE', @level1name = N'Courses', @level2type = N'COLUMN', @level2name = N'Duration';


GO
EXECUTE sp_addextendedproperty @name = N'MS_Description', @value = N' PDF فایل سرفصل دوره در قالب ', @level0type = N'SCHEMA', @level0name = N'dbo', @level1type = N'TABLE', @level1name = N'Courses', @level2type = N'COLUMN', @level2name = N'SyllabusFile';


GO
EXECUTE sp_addextendedproperty @name = N'MS_Description', @value = N'پیش نیاز دوره', @level0type = N'SCHEMA', @level0name = N'dbo', @level1type = N'TABLE', @level1name = N'Courses', @level2type = N'COLUMN', @level2name = N'PrerequisiteID';


GO
EXECUTE sp_addextendedproperty @name = N'MS_Description', @value = N'کد دسته بندی دوره', @level0type = N'SCHEMA', @level0name = N'dbo', @level1type = N'TABLE', @level1name = N'Courses', @level2type = N'COLUMN', @level2name = N'CourseCategoryID';

