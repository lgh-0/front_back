# OpenVPN 服务器自动配置脚本
# 以管理员身份运行

Write-Host "=== OpenVPN 服务器配置脚本 ===" -ForegroundColor Green

# 设置工作目录
$openvpnPath = "C:\Program Files\OpenVPN"
$easyRsaPath = "$openvpnPath\easy-rsa-work"

# 1. 初始化 easy-rsa
Write-Host "1. 初始化 easy-rsa..." -ForegroundColor Yellow
if (!(Test-Path $easyRsaPath)) {
    Copy-Item -Path "$openvpnPath\easy-rsa" -Destination $easyRsaPath -Recurse -Force
    Write-Host "   easy-rsa 已复制到工作目录" -ForegroundColor Green
} else {
    Write-Host "   easy-rsa 工作目录已存在" -ForegroundColor Yellow
}

# 2. 创建 vars.bat
Write-Host "2. 创建配置变量..." -ForegroundColor Yellow
$varsContent = @"
@echo off
set HOME=%~dp0
set KEY_COUNTRY=CN
set KEY_PROVINCE=Beijing
set KEY_CITY=Beijing
set KEY_ORG=Company
set KEY_EMAIL=admin@company.com
set KEY_CN=openvpn-server
set KEY_NAME=openvpn-server
set KEY_OU=IT
"@
Set-Content -Path "$easyRsaPath\vars.bat" -Value $varsContent -Encoding ASCII
Write-Host "   vars.bat 已创建" -ForegroundColor Green

# 3. 切换到 easy-rsa 目录
Set-Location $easyRsaPath

# 4. 初始化 PKI
Write-Host "3. 初始化 PKI..." -ForegroundColor Yellow
& "$easyRsaPath\vars.bat"
& "$easyRsaPath\clean-all.bat"

# 5. 生成证书
Write-Host "4. 生成 CA 证书..." -ForegroundColor Yellow
& "$easyRsaPath\build-ca.bat" --batch

Write-Host "5. 生成服务器证书..." -ForegroundColor Yellow
& "$easyRsaPath\build-key-server.bat" server --batch

Write-Host "6. 生成 DH 参数..." -ForegroundColor Yellow
& "$easyRsaPath\build-dh.bat"

Write-Host "7. 生成客户端证书..." -ForegroundColor Yellow
& "$easyRsaPath\build-key.bat" client --batch

# 6. 创建服务器配置文件
Write-Host "8. 创建服务器配置文件..." -ForegroundColor Yellow
$configPath = "$openvpnPath\config"
if (!(Test-Path $configPath)) {
    New-Item -Path $configPath -ItemType Directory -Force
}

$serverConfig = @"
port 1194
proto udp
dev tun

ca "$($easyRsaPath -replace '\\', '\\')\\keys\\ca.crt"
cert "$($easyRsaPath -replace '\\', '\\')\\keys\\server.crt"
key "$($easyRsaPath -replace '\\', '\\')\\keys\\server.key"
dh "$($easyRsaPath -replace '\\', '\\')\\keys\\dh2048.pem"

server 10.8.0.0 255.255.255.0
push "redirect-gateway def1 bypass-dns"
push "dhcp-option DNS 8.8.8.8"
push "dhcp-option DNS 8.8.4.4"

keepalive 10 120
cipher AES-256-CBC
auth SHA256
comp-lzo
persist-key
persist-tun

status openvpn-status.log
log-append openvpn.log
verb 3

client-to-client
duplicate-cn
"@
Set-Content -Path "$configPath\server.ovpn" -Value $serverConfig -Encoding UTF8
Write-Host "   server.ovpn 已创建" -ForegroundColor Green

# 7. 配置防火墙
Write-Host "9. 配置防火墙..." -ForegroundColor Yellow
New-NetFirewallRule -DisplayName "OpenVPN" -Direction Inbound -Protocol UDP -LocalPort 1194 -Action Allow -ErrorAction SilentlyContinue
Write-Host "   防火墙规则已添加" -ForegroundColor Green

# 8. 启用 IP 转发
Write-Host "10. 启用 IP 转发..." -ForegroundColor Yellow
Set-ItemProperty -Path "HKLM:\SYSTEM\CurrentControlSet\Services\Tcpip\Parameters" -Name "IpEnableRouter" -Value 1 -Type DWord
Write-Host "   IP 转发已启用" -ForegroundColor Green

# 9. 创建客户端配置文件模板
Write-Host "11. 创建客户端配置文件模板..." -ForegroundColor Yellow
$clientConfig = @"
client
dev tun
proto udp
remote 120.234.11.54 1194

resolv-retry infinite
nobind
persist-key
persist-tun

ca ca.crt
cert client.crt
key client.key

cipher AES-256-CBC
auth SHA256
comp-lzo
verb 3
"@
Set-Content -Path "$easyRsaPath\client.ovpn" -Value $clientConfig -Encoding UTF8
Write-Host "   client.ovpn 模板已创建" -ForegroundColor Green

# 10. 启用远程桌面
Write-Host "12. 启用远程桌面..." -ForegroundColor Yellow
Set-ItemProperty -Path 'HKLM:\System\CurrentControlSet\Control\Terminal Server' -name "fDenyTSConnections" -value 0
Enable-NetFirewallRule -DisplayGroup "Remote Desktop" -ErrorAction SilentlyContinue
Write-Host "   远程桌面已启用" -ForegroundColor Green

Write-Host "`n=== 配置完成! ===" -ForegroundColor Green
Write-Host "下一步操作:" -ForegroundColor Cyan
Write-Host "1. 将以下文件复制到笔记本电脑:" -ForegroundColor White
Write-Host "   - $easyRsaPath\keys\ca.crt" -ForegroundColor Gray
Write-Host "   - $easyRsaPath\keys\client.crt" -ForegroundColor Gray
Write-Host "   - $easyRsaPath\keys\client.key" -ForegroundColor Gray
Write-Host "   - $easyRsaPath\client.ovpn" -ForegroundColor Gray
Write-Host "`n2. 在台式机上启动 OpenVPN 服务:" -ForegroundColor White
Write-Host "   使用 OpenVPN GUI 导入 server.ovpn 并连接" -ForegroundColor Gray
Write-Host "`n3. 在笔记本上连接 VPN 后，使用远程桌面连接: 10.8.0.1" -ForegroundColor White

# 询问是否立即启动 OpenVPN
$choice = Read-Host "`n是否立即启动 OpenVPN 服务器? (y/n)"
if ($choice -eq 'y') {
    Write-Host "启动 OpenVPN 服务器..." -ForegroundColor Yellow
    Start-Process -FilePath "$openvpnPath\bin\openvpn.exe" -ArgumentList "--config `"$configPath\server.ovpn`"" -NoNewWindow
    Write-Host "OpenVPN 服务器已启动" -ForegroundColor Green
}
