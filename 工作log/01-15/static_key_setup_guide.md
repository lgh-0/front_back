# OpenVPN 静态密钥配置指南

## 为什么使用静态密钥？
静态密钥配置是最简单的方式，适合点对点连接（一台服务器对一台客户端）。无需复杂的证书管理。

## 台式机操作步骤

### 1. 运行配置脚本
以管理员身份运行：
```cmd
d:\start-9-19note\front_back\工作log\01-15\setup_static_key_openvpn.bat
```

### 2. 检查生成的文件
脚本运行后，在 `C:\Program Files\OpenVPN\config` 目录会生成：
- `static.key` - 静态密钥文件
- `server_static.ovpn` - 服务器配置
- `client_static.ovpn` - 客户端配置

### 3. 启动服务器
使用 OpenVPN GUI：
1. 打开 OpenVPN GUI（右键以管理员身份运行）
2. 点击图标，选择"导入文件"
3. 选择 `C:\Program Files\OpenVPN\config\server_static.ovpn`
4. 右键点击托盘图标，选择"连接"

## 笔记本电脑操作步骤

### 1. 创建客户端目录
在笔记本电脑上创建目录：
```cmd
mkdir C:\OpenVPN_Client
cd C:\OpenVPN_Client
```

### 2. 复制文件
从台式机复制以下文件到笔记本的 `C:\OpenVPN_Client`：
- `C:\Program Files\OpenVPN\config\static.key`
- `C:\Program Files\OpenVPN\config\client_static.ovpn`

### 3. 连接 VPN
在笔记本上：
1. 打开 OpenVPN GUI
2. 导入 `C:\OpenVPN_Client\client_static.ovpn`
3. 连接 VPN

### 4. 使用远程桌面
连接成功后：
1. 打开远程桌面客户端
2. 连接地址：`10.8.0.1`
3. 使用您的 Windows 账户登录

## 重要配置检查

### 1. 路由器端口转发
确保公司路由器配置了端口转发：
- 外部端口：1194
- 协议：UDP
- 内部IP：台式机的内网IP（如 192.168.1.100）
- 内部端口：1194

### 2. Windows 防火墙
脚本已自动配置，如需手动检查：
```cmd
# 查看防火墙规则
netsh advfirewall firewall show rule name="OpenVPN"
```

### 3. IP 转发验证
```cmd
# 检查 IP 转发是否启用
reg query HKLM\SYSTEM\CurrentControlSet\Services\Tcpip\Parameters /v IpEnableRouter
```

## 故障排除

### 1. 连接超时
- 检查路由器端口转发
- 确认台式机防火墙设置
- 验证公网 IP 是否正确

### 2. 认证失败
- 确保 static.key 文件在客户端和服务器端完全相同
- 检查文件路径是否正确

### 3. 无法访问内网
- 运行路由配置脚本：`C:\Program Files\OpenVPN\config\setup_routes.bat`
- 检查 Windows 防火墙是否阻止了连接

### 4. 查看日志
服务器日志位置：`C:\Program Files\OpenVPN\log\openvpn.log`

## 安全建议

1. 定期更换静态密钥
2. 不要通过不安全的方式传输 static.key
3. 使用强密码保护 Windows 账户
4. 考虑使用 VPN 客户端的 kill switch 功能

## 高级配置（可选）

如果需要让笔记本通过 VPN 访问整个内网，可以在服务器配置中添加：
```
push "route 192.168.1.0 255.255.255.0"
```

并在笔记本上添加路由：
```cmd
route add 192.168.1.0 mask 255.255.255.0 10.8.0.1
```
