CREATE TABLE [dbo].[CourseCategory] (
    [ID]                        TINYINT       IDENTITY (1, 1) NOT NULL,
    [CourseCategoryName]        NVARCHAR (50) NOT NULL,
    [EnglishCourseCategoryName] VARCHAR (50)  NOT NULL,
    CONSTRAINT [PK_CourseCategory] PRIMARY KEY CLUSTERED ([ID] ASC)
);

