go官网 https://go.dev/dl/

go可以不使用gin的框架，直接使用net/http包来写web服务器

```go
// 一个简单的go例子
package main

import (
	"fmt"
	"net/http"
)

func main() {
	http.HandleFunc("/", func(w http.ResponseWriter, r *http.Request) {
		fmt.Fprintln(w, "Hello, Go server is running!")
	})

	fmt.Println("Server running at http://localhost:8080")
	err := http.ListenAndServe(":8080", nil)
	if err != nil {
		panic(err)
	}
}
```