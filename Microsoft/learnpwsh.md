在linux中一切管理操作的配置都是文本文件，因此所有的管理类软件其实就是处理文本文件的程序，而win是基于API的操作系统，所有的API
返回的都是结构化的数据，因此那些Unix软件没有什么帮助。
powershell的测试框架Pester powershell有两个指代，一个是命令行shell,另一个是脚本语言。
查看powershell的配置文件位置 `$PROFILE`
查看powershell的版本 `$PSVersionTable`
notepad $PROFILE
使用get-command命令查看powershell支持的所有的命令

大小写敏感问题
🔹 PowerShell：命令、参数、变量 → 不区分大小写
🔹 字符串比较、正则、外部命令、Linux 文件系统 → 可能区分大小写
🔹 写成 Get-Command 是规范，不是要求

```powershell
get-command -verb get -noun content

get-command -name echo 


update-help 命令不能保证能更新所有的

set-strictmode -version latest 严格模式


| 项目   | Strict Mode      | ExecutionPolicy       |
| ---- | ---------------- | --------------------- |
| 作用   | **脚本运行行为**       | **脚本允不允许运行**          |
| 解决什么 | 逻辑错误 / 隐式 Bug    | 安全策略                  |
| 常用命令 | `Set-StrictMode` | `Set-ExecutionPolicy` |

# Strict Mode 不是全局一次性开关，而是跟作用域走的：
Set-StrictMode -Version Latest

function Test {
    # 这里仍然是严格模式
}

Set-StrictMode -Off


| 后缀          | 用途 | 本质    |
| ----------- | -- | ----- |
| **`.ps1`**  | 脚本 | 可直接运行 |
| **`.psm1`** | 模块 | 被导入使用 |

✅变量
PowerShell 没有“声明 + 赋值分离”
第一次赋值 = 声明
$foo = 123
这一步同时做了三件事：
创建变量 foo
给它赋值 123
类型自动推断为 Int32
显示指定类型 [int]$foo = 123
PowerShell 不是“命令行版 C”，而是“基于对象的脚本语言 + REPL
PowerShell 管道 ≠ 文本流，而是对象流

✅偏好设置变量用于设置控制各种输出流的行为
PS C:\Users\ShiXiSheng001> get-variable   -name *preference

Name                           Value
----                           -----
ConfirmPreference              High
DebugPreference                SilentlyContinue
ErrorActionPreference          Continue
InformationPreference          SilentlyContinue
ProgressPreference             Continue
PSNativeCommandUseErrorAction… False
VerbosePreference              SilentlyContinue
WarningPreference              Continue
WhatIfPreference               False

PS C:\Users\ShiXiSheng001>

✅psm1 是干嘛的？
用来写 模块
不能像脚本那样直接运行
通过 Import-Module 加载

✅$color = @('red','green','blue')
$color = [System.Collections.ArrayList]@()
$color.Add('red')
$color.Remove('red')
$color.Insert(1,'green')
$color.Gettype()


✅Hashtable
$user = @{
    name = 'John'
    age = 30
    city = 'New York'
}
$user.keys
$user.values
$user.Add('name','John')
$user.Remove('name')
pwsh组合命令的两种方式：管道和脚本

✅执行脚本的方式
PS D:\kong> D:\kong\service.ps1
PS D:\kong> .\service
PS D:\kong> pwsh -file .\service.ps1
PS D:\kong> powershell -file .\service.ps1
PS D:\kong> powershell -ExecutionPolicy Bypass -File .\service.ps1

✅更改Path
查看系统Path [Environment]::GetEnvironmentVariable("Path", "Machine") -split ';'
查看用户Path [Environment]::GetEnvironmentVariable("Path", "User") -split ';'
修改系统Path 
$old = [Environment]::GetEnvironmentVariable("Path", "Machine")
$new = $old + ";C:\Some\System\Tool"
[Environment]::SetEnvironmentVariable("Path", $new, "Machine")

修改系统path
$add = "C:\Program Files\Vim\vim91"
$old = [Environment]::GetEnvironmentVariable("Path", "Machine") -split ';'
if ($old -notcontains $add) {
    $new = ($old + $add) -join ';'
    [Environment]::SetEnvironmentVariable("Path", $new, "Machine")
    Write-Host "已添加到系统 Path：" $add
} else {
    Write-Host "系统 Path 中已存在：" $add
}

修改用户Path
$newDir = "C:\MyTools\bin"
$old = [Environment]::GetEnvironmentVariable("Path", "User")
if ($old -notmatch [regex]::Escape($newDir)) {
    $new = $old + ";" + $newDir
    [Environment]::SetEnvironmentVariable("Path", $new, "User")
}

删除某个用户Path
$remove = "C:\Users\LGH\miniconda3\Scripts"
$old = [Environment]::GetEnvironmentVariable("Path", "User") -split ';'
$new = $old | Where-Object { $_ -and $_ -ne $remove }
[Environment]::SetEnvironmentVariable("Path", ($new -join ';'), "User")

删除某个系统Path
# 要删除的路径
$remove = "C:\Program Files\Vim\vim91"
# 读取系统 Path
$old = [Environment]::GetEnvironmentVariable("Path", "Machine") -split ';'
# 过滤掉要删除的路径
$new = $old | Where-Object {
    $_ -and $_.TrimEnd('\') -ne $remove.TrimEnd('\')
}
# 写回系统 Path
[Environment]::SetEnvironmentVariable("Path", ($new -join ';'), "Machine")
Write-Host "已从系统 Path 删除：" $remove


删除系统的多个Path
$removeList = @(
    "C:\Program Files\Vim\vim91",
    "C:\OldTool\bin"
)
$old = [Environment]::GetEnvironmentVariable("Path", "Machine") -split ';'
$new = $old | Where-Object {
    $_ -and ($removeList | ForEach-Object { $_.TrimEnd('\') }) -notcontains $_.TrimEnd('\')
}
[Environment]::SetEnvironmentVariable("Path", ($new -join ';'), "Machine")

✅conda的shell问题
S C:\Users\LGH> conda env list

# conda environments:
#
# * -> active
# + -> frozen
base                     D:\Anaconda

PS C:\Users\LGH> conda activate base

CondaError: Run 'conda init' before 'conda activate'

PS C:\Users\LGH> conda init powershell
no change     D:\Anaconda\Scripts\conda.exe
no change     D:\Anaconda\Scripts\conda-env.exe
no change     D:\Anaconda\Scripts\conda-script.py
no change     D:\Anaconda\Scripts\conda-env-script.py
no change     D:\Anaconda\condabin\conda.bat
no change     D:\Anaconda\Library\bin\conda.bat
no change     D:\Anaconda\condabin\_conda_activate.bat
no change     D:\Anaconda\condabin\rename_tmp.bat
no change     D:\Anaconda\condabin\conda_auto_activate.bat
no change     D:\Anaconda\condabin\conda_hook.bat
no change     D:\Anaconda\Scripts\activate.bat
no change     D:\Anaconda\condabin\activate.bat
no change     D:\Anaconda\condabin\deactivate.bat
modified      D:\Anaconda\Scripts\activate
modified      D:\Anaconda\Scripts\deactivate
modified      D:\Anaconda\etc\profile.d\conda.sh
modified      D:\Anaconda\etc\fish\conf.d\conda.fish
no change     D:\Anaconda\shell\condabin\Conda.psm1
modified      D:\Anaconda\shell\condabin\conda-hook.ps1
no change     D:\Anaconda\Lib\site-packages\xontrib\conda.xsh
modified      D:\Anaconda\etc\profile.d\conda.csh
modified      C:\Users\LGH\Documents\PowerShell\profile.ps1
modified      C:\Users\LGH\Documents\WindowsPowerShell\profile.ps1

==> For changes to take effect, close and re-open your current shell. <==

PS C:\Users\LGH>
































```