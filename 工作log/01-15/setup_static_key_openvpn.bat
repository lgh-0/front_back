@echo off
chcp 65001 >nul
echo === OpenVPN 静态密钥配置脚本 ===
echo.

:: 检查管理员权限
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo 错误: 请以管理员身份运行此脚本!
    pause
    exit /b 1
)

set OPENVPN_PATH=C:\Program Files\OpenVPN
set CONFIG_PATH=%OPENVPN_PATH%\config

echo 1. 生成静态密钥...
cd /d "%CONFIG_PATH%"
"%OPENVPN_PATH%\bin\openvpn.exe" --genkey secret static.key
echo    静态密钥已生成: %CONFIG_PATH%\static.key

echo.
echo 2. 创建服务器配置文件...
(
echo port 1194
echo proto udp
echo dev tun
echo.
echo ifconfig 10.8.0.1 10.8.0.2
echo secret static.key
echo.
echo keepalive 10 120
echo comp-lzo
echo persist-key
echo persist-tun
echo.
echo status openvpn-status.log
echo log-append openvpn.log
echo verb 3
) > "%CONFIG_PATH%\server_static.ovpn"
echo    server_static.ovpn 已创建

echo.
echo 3. 创建客户端配置文件...
(
echo remote 120.234.11.54 1194
echo proto udp
echo dev tun
echo.
echo ifconfig 10.8.0.2 10.8.0.1
echo secret static.key
echo.
echo resolv-retry infinite
echo nobind
echo persist-key
echo persist-tun
echo.
echo comp-lzo
echo verb 3
) > "%CONFIG_PATH%\client_static.ovpn"
echo    client_static.ovpn 已创建

echo.
echo 4. 配置防火墙...
netsh advfirewall firewall add rule name="OpenVPN" dir=in action=allow protocol=UDP localport=1194
echo    防火墙规则已添加

echo.
echo 5. 启用 IP 转发...
reg add HKLM\SYSTEM\CurrentControlSet\Services\Tcpip\Parameters /v IpEnableRouter /t REG_DWORD /d 1 /f
echo    IP 转发已启用

echo.
echo 6. 配置路由和 NAT...
:: 创建路由脚本
(
echo @echo off
echo route add 10.8.0.0 mask 255.255.255.0 10.8.0.2
echo netsh interface ipv4 set global forwarding=enabled
) > "%CONFIG_PATH%\setup_routes.bat"
echo    路由配置脚本已创建

echo.
echo 7. 启用远程桌面...
reg add "HKLM\SYSTEM\CurrentControlSet\Control\Terminal Server" /v fDenyTSConnections /t REG_DWORD /d 0 /f
netsh advfirewall firewall set rule group="Remote Desktop" new enable=Yes
echo    远程桌面已启用

echo.
echo === 配置完成! ===
echo.
echo 需要复制到笔记本电脑的文件:
echo    - %CONFIG_PATH%\static.key
echo    - %CONFIG_PATH%\client_static.ovpn
echo.
echo 注意事项:
echo 1. 确保公司路由器已配置端口转发: 1194 UDP -> 台式机IP
echo 2. 在笔记本上将 client_static.ovpn 和 static.key 放在同一目录
echo 3. 连接后使用远程桌面连接: 10.8.0.1
echo.

set /p choice=是否立即启动 OpenVPN 服务器? (y/n): 
if /i "%choice%"=="y" (
    echo 启动 OpenVPN 服务器...
    start "OpenVPN Server" /D "%OPENVPN_PATH%\bin" openvpn.exe --config "%CONFIG_PATH%\server_static.ovpn"
    echo OpenVPN 服务器已启动
    echo 提示: 保持此窗口开启
)

pause
