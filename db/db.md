无密码window登录验证`sqlcmd -S localhost -d demo1 -E`

SELECT * FROM dbo.table1;
GO
真正有用
`sqlcmd -S localhost -U sa -P 1432 -d demo1`

下面的目录输出会好看些
`sqlcmd -S localhost -d demo1 -E -W -s"," `
`SELECT * FROM dbo.table1;`
`GO`

下面的命令是设置登录密码
```{shell}
$RegPath = "HKLM:\SOFTWARE\Microsoft\Microsoft SQL Server\MSSQL15.MSSQLSERVER\MSSQLServer"
Set-ItemProperty -Path $RegPath -Name "LoginMode" -Value 2

ALTER LOGIN sa WITH PASSWORD = '1432';
ALTER LOGIN sa ENABLE;
GO
EXIT
```