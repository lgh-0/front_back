# OpenVPN 服务器配置指南

## 环境信息
- 公司台式机公网IP: 120.234.11.54
- OpenVPN安装路径: C:\Program Files\OpenVPN
- 目标：通过笔记本电脑远程控制公司台式机

## 第一步：生成证书和密钥

### 1. 初始化 easy-rsa
```powershell
# 以管理员身份运行 PowerShell
cd "C:\Program Files\OpenVPN\bin"

# 复制 easy-rsa 到 OpenVPN 目录
xcopy /E /I "C:\Program Files\OpenVPN\easy-rsa" "C:\Program Files\OpenVPN\easy-rsa-work"

cd "C:\Program Files\OpenVPN\easy-rsa-work"
```

### 2. 配置变量
```powershell
# 创建 vars.bat 文件
vim vars.bat
```

在 vars.bat 中添加：
```batch
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
```

### 3. 初始化 PKI
```powershell
# 清理之前的证书（如果存在）
vars.bat
clean-all.bat

# 生成 CA 证书
build-ca.bat

# 生成服务器证书
build-key-server.bat server

# 生成 Diffie Hellman 参数
build-dh.bat

# 生成客户端证书
build-key.bat client
```

## 第二步：创建服务器配置文件

```powershell
cd "C:\Program Files\OpenVPN\config"
vim server.ovpn
```

在 server.ovpn 中添加：
```
port 1194
proto udp
dev tun

ca "C:\\Program Files\\OpenVPN\\easy-rsa-work\\keys\\ca.crt"
cert "C:\\Program Files\\OpenVPN\\easy-rsa-work\\keys\\server.crt"
key "C:\\Program Files\\OpenVPN\\easy-rsa-work\\keys\\server.key"
dh "C:\\Program Files\\OpenVPN\\easy-rsa-work\\keys\\dh2048.pem"

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

# 允许客户端之间通信
client-to-client

# 允许同一证书多个客户端登录
duplicate-cn
```

## 第三步：配置 Windows 防火墙

```powershell
# 以管理员身份运行 PowerShell
# 开放 OpenVPN 端口
New-NetFirewallRule -DisplayName "OpenVPN" -Direction Inbound -Protocol UDP -LocalPort 1194 -Action Allow

# 启用 IP 转发（需要修改注册表）
reg add HKLM\SYSTEM\CurrentControlSet\Services\Tcpip\Parameters /v IpEnableRouter /t REG_DWORD /d 1 /f

# 配置 NAT 共享
netsh routing ip nat install
netsh routing ip nat add interface "内部" private
netsh routing ip nat add interface name="内部" mode=private
netsh routing ip nat add interface name="外部" mode=public
```

## 第四步：启动 OpenVPN 服务器

```powershell
# 使用 OpenVPN GUI 或命令行启动
cd "C:\Program Files\OpenVPN\bin"
.\openvpn.exe --config "C:\Program Files\OpenVPN\config\server.ovpn"
```

## 第五步：创建客户端配置文件

在笔记本上创建 client.ovpn：
```
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
```

## 第六步：传输客户端文件

将以下文件从台式机复制到笔记本：
- C:\Program Files\OpenVPN\easy-rsa-work\keys\ca.crt
- C:\Program Files\OpenVPN\easy-rsa-work\keys\client.crt
- C:\Program Files\OpenVPN\easy-rsa-work\keys\client.key
- client.ovpn

## 第七步：启用远程桌面

在台式机上：
```powershell
# 启用远程桌面
Set-ItemProperty -Path 'HKLM:\System\CurrentControlSet\Control\Terminal Server' -name "fDenyTSConnections" -value 0

# 配置防火墙允许远程桌面
Enable-NetFirewallRule -DisplayGroup "Remote Desktop"
```

## 连接测试

1. 在笔记本上安装 OpenVPN 客户端
2. 导入 client.ovpn 配置文件
3. 连接 VPN
4. 连接成功后，使用远程桌面连接：10.8.0.1

## 故障排除

### 检查日志
```powershell
# 查看服务器日志
type "C:\Program Files\OpenVPN\log\openvpn.log"

# 查看连接状态
type "C:\Program Files\OpenVPN\log\openvpn-status.log"
```

### 常见问题
1. 连接失败：检查防火墙设置和端口 1194 是否开放
2. 认证失败：确认证书文件路径正确
3. 无法访问内网：检查 IP 转发和 NAT 配置

## 安全建议

1. 定期更新 OpenVPN
2. 使用强密码保护证书
3. 限制客户端证书的有效期
4. 监控连接日志
