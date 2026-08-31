CREATE TABLE [dbo].[Student_Courses_Teacher] (
    [StudentID]  INT      NOT NULL,
    [CoursesID]  SMALLINT NOT NULL,
    [TeacherID]  INT      NOT NULL,
    [TermNumber] INT      NOT NULL,
    [Score]      TINYINT  NOT NULL,
    CONSTRAINT [PK_Student_Courses_Teacher_1] PRIMARY KEY CLUSTERED ([StudentID] ASC, [CoursesID] ASC, [TeacherID] ASC, [TermNumber] ASC),
    CONSTRAINT [FK_Student_Courses_Teacher_Courses] FOREIGN KEY ([CoursesID]) REFERENCES [dbo].[Courses] ([ID]),
    CONSTRAINT [FK_Student_Courses_Teacher_Student] FOREIGN KEY ([StudentID]) REFERENCES [dbo].[Student] ([PersonID]),
    CONSTRAINT [FK_Student_Courses_Teacher_Teacher] FOREIGN KEY ([TeacherID]) REFERENCES [dbo].[Teacher] ([PersonID])
);

