-- Exemplo de script SQL

DECLARE @nome NVARCHAR(50);
DECLARE @bairro NVARCHAR(50);

UPDATE EMPRESA SET RAZAOSOCIAL = @nome, BAIRRO = @bairro;
