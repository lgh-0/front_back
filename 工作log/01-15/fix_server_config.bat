@echo off
echo 修复服务器配置文件...

set CONFIG_PATH=C:\Program Files\OpenVPN\config

(
echo port 1194
echo proto udp
echo dev tun
echo.
echo ifconfig 10.8.0.1 10.8.0.2
echo secret "%CONFIG_PATH%\static.key"
echo.
echo keepalive 10 120
echo comp-lzo
echo persist-key
echo persist-tun
echo.
echo status "%CONFIG_PATH%\log\openvpn-status.log"
echo log-append "%CONFIG_PATH%\log\openvpn.log"
echo verb 3
) > "%CONFIG_PATH%\server_static.ovpn"

echo 服务器配置文件已修复
echo.
echo 现在请：
echo 1. 确保 OpenVPN GUI 以管理员身份运行
echo 2. 右键点击托盘图标，断开当前连接（如果有）
echo 3. 重新连接 server_static
echo.

pause
