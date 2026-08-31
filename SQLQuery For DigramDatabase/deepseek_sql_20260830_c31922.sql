DECLARE @values nvarchar(max);
SET @values = (
    SELECT ' (''' + REPLACE(name, '''', '''''') + ''', ' 
           + CAST(principal_id AS VARCHAR(100)) +', ' 
           + CAST(version AS VARCHAR(100)) + ', ' 
           + sys.fn_varbintohexstr(definition) + '),'
    FROM sysdiagrams
    FOR XML PATH(''), TYPE
).value('.', 'nvarchar(max)');

IF LEN(@values) > 0
BEGIN
    SET @values = LEFT(@values, LEN(@values) - 1);
    SELECT 'IF OBJECT_ID(N''dbo.sysdiagrams'') IS NULL
             CREATE TABLE dbo.sysdiagrams
             (
                 name sysname NOT NULL,
                 principal_id int NOT NULL,
                 diagram_id int PRIMARY KEY IDENTITY,
                 version int,
                 definition varbinary(max)
                 CONSTRAINT UK_principal_name UNIQUE ( principal_id, name )
             );
             
             MERGE sysdiagrams AS Target
             USING ( VALUES' + @values + ' ) 
             AS Source (name, principal_id, version, definition)
             ON Target.name = Source.name AND Target.principal_id = Source.principal_id
             WHEN MATCHED THEN
                 UPDATE SET version = Source.version, definition = Source.definition
             WHEN NOT MATCHED BY Target THEN
                 INSERT (name, principal_id, version, definition)
                 VALUES (name, principal_id, version, definition);';
END