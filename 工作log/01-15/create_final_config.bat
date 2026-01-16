@echo off
echo 创建最终的 OpenVPN 配置文件...

set CONFIG_PATH=C:\Program Files\OpenVPN\config

cd /d "%CONFIG_PATH%"

(
echo port 1194
echo proto udp
echo dev tun
echo.
echo ifconfig 10.8.0.1 10.8.0.2
echo secret "%CONFIG_PATH%\static.key"
echo.
echo keepalive 10 120
echo comp-lzo allow-compression yes
echo persist-key
echo persist-tun
echo.
echo verb 4
) > server_static_final.ovpn

echo.
echo 配置文件已创建: server_static_final.ovpn
echo.
echo 现在运行以下命令启动服务器:
echo cd "C:\Program Files\OpenVPN\bin"
echo openvpn.exe --config "%CONFIG_PATH%\server_static_final.ovpn"
echo.

pause
