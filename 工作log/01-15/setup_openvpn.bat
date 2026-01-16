@echo off
chcp 65001 >nul
echo === OpenVPN 服务器配置脚本 ===
echo.

:: 检查管理员权限
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo 错误: 请以管理员身份运行此脚本!
    pause
    exit /b 1
)

set OPENVPN_PATH=C:\Program Files\OpenVPN
set EASYRSA_PATH=%OPENVPN_PATH%\easy-rsa-work

echo 1. 初始化 easy-rsa...
if not exist "%EASYRSA_PATH%" (
    xcopy /E /I "%OPENVPN_PATH%\easy-rsa" "%EASYRSA_PATH%"
    echo    easy-rsa 已复制到工作目录
) else (
    echo    easy-rsa 工作目录已存在
)

echo.
echo 2. 创建配置变量...
(
echo @echo off
echo set HOME=%%~dp0
echo set KEY_COUNTRY=CN
echo set KEY_PROVINCE=Beijing
echo set KEY_CITY=Beijing
echo set KEY_ORG=Company
echo set KEY_EMAIL=admin@company.com
echo set KEY_CN=openvpn-server
echo set KEY_NAME=openvpn-server
echo set KEY_OU=IT
) > "%EASYRSA_PATH%\vars.bat"
echo    vars.bat 已创建

echo.
echo 3. 初始化 PKI...
cd /d "%EASYRSA_PATH%"
call vars.bat
call clean-all.bat

echo.
echo 4. 生成 CA 证书...
call build-ca.bat --batch

echo.
echo 5. 生成服务器证书...
call build-key-server.bat server --batch

echo.
echo 6. 生成 DH 参数...
call build-dh.bat

echo.
echo 7. 生成客户端证书...
call build-key.bat client --batch

echo.
echo 8. 创建服务器配置文件...
if not exist "%OPENVPN_PATH%\config" mkdir "%OPENVPN_PATH%\config"

(
echo port 1194
echo proto udp
echo dev tun
echo.
echo ca "%EASYRSA_PATH%\keys\ca.crt"
echo cert "%EASYRSA_PATH%\keys\server.crt"
echo key "%EASYRSA_PATH%\keys\server.key"
echo dh "%EASYRSA_PATH%\keys\dh2048.pem"
echo.
echo server 10.8.0.0 255.255.255.0
echo push "redirect-gateway def1 bypass-dns"
echo push "dhcp-option DNS 8.8.8.8"
echo push "dhcp-option DNS 8.8.4.4"
echo.
echo keepalive 10 120
echo cipher AES-256-CBC
echo auth SHA256
echo comp-lzo
echo persist-key
echo persist-tun
echo.
echo status openvpn-status.log
echo log-append openvpn.log
echo verb 3
echo.
echo client-to-client
echo duplicate-cn
) > "%OPENVPN_PATH%\config\server.ovpn"
echo    server.ovpn 已创建

echo.
echo 9. 配置防火墙...
netsh advfirewall firewall add rule name="OpenVPN" dir=in action=allow protocol=UDP localport=1194
echo    防火墙规则已添加

echo.
echo 10. 启用 IP 转发...
reg add HKLM\SYSTEM\CurrentControlSet\Services\Tcpip\Parameters /v IpEnableRouter /t REG_DWORD /d 1 /f
echo    IP 转发已启用

echo.
echo 11. 创建客户端配置文件模板...
(
echo client
echo dev tun
echo proto udp
echo remote 120.234.11.54 1194
echo.
echo resolv-retry infinite
echo nobind
echo persist-key
echo persist-tun
echo.
echo ca ca.crt
echo cert client.crt
echo key client.key
echo.
echo cipher AES-256-CBC
echo auth SHA256
echo comp-lzo
echo verb 3
) > "%EASYRSA_PATH%\client.ovpn"
echo    client.ovpn 模板已创建

echo.
echo 12. 启用远程桌面...
reg add "HKLM\SYSTEM\CurrentControlSet\Control\Terminal Server" /v fDenyTSConnections /t REG_DWORD /d 0 /f
netsh advfirewall firewall set rule group="Remote Desktop" new enable=Yes
echo    远程桌面已启用

echo.
echo === 配置完成! ===
echo.
echo 下一步操作:
echo 1. 将以下文件复制到笔记本电脑:
echo    - %EASYRSA_PATH%\keys\ca.crt
echo    - %EASYRSA_PATH%\keys\client.crt
echo    - %EASYRSA_PATH%\keys\client.key
echo    - %EASYRSA_PATH%\client.ovpn
echo.
echo 2. 在台式机上启动 OpenVPN 服务:
echo    使用 OpenVPN GUI 导入 server.ovpn 并连接
echo.
echo 3. 在笔记本上连接 VPN 后，使用远程桌面连接: 10.8.0.1
echo.

set /p choice=是否立即启动 OpenVPN 服务器? (y/n): 
if /i "%choice%"=="y" (
    echo 启动 OpenVPN 服务器...
    start "" /D "%OPENVPN_PATH%\bin" openvpn.exe --config "%OPENVPN_PATH%\config\server.ovpn"
    echo OpenVPN 服务器已启动
)

pause
