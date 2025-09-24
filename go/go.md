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

```