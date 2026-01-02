go官网 https://go.dev/dl/
learngo AAA2
go可以不使用gin的框架，直接使用net/http包来写web服务器

```go
// 一个简单的go例子
package main

import (
	"encoding/json"
	"net/http"
)

func main() {
	// 处理 /api/password 路由
	http.HandleFunc("/api/password", func(w http.ResponseWriter, r *http.Request) {
		// 设置 CORS 头，允许 Vue3 前端访问
		w.Header().Set("Access-Control-Allow-Origin", "http://localhost:5173")
		w.Header().Set("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
		w.Header().Set("Access-Control-Allow-Headers", "Content-Type")

		// 如果是预检请求(OPTIONS)，直接返回
		if r.Method == http.MethodOptions {
			return
		}

		// 返回 JSON
		w.Header().Set("Content-Type", "application/json")
		json.NewEncoder(w).Encode(map[string]string{
			"password": "go后端的密码123445",
		})
	})

	println("Server running at http://localhost:8083")
	http.ListenAndServe(":8083", nil)
}

✅运行go程序的几种方式
1.在目录下初始化模块 go mod init [目录]
2.再编译 go build
3.运行 .\hello.go

1.直接运行 go run hello.go

✅if和简短语句
if语句可以在条件表达式前执行一个简短语句
if shortStatement; condition{

}
二分法：速度慢但稳定
查表法：嵌入式系统常用，预先计算好值
硬件指令：现代CPU有专门的平方根指令（如 sqrtss）
C标准库：通常用优化的汇编实现

✅ switch语句
无条件的switch语句和if-else语句一样。有条件的switch语句默认break，可以使用fallthrough来实现

✅
✅

✅

✅

✅
✅

✅

✅

✅
✅

✅

✅

✅
✅

✅

✅

✅

```