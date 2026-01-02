package main  // 声明 main 包，表明当前是一个可执行程序

import (
	"fmt"
	"math"
    // "runtime"
    "time"
)

func Sqrt(x float64) float64 {
	var z float64 = 1.0
	sum := 0
	for ; math.Abs(z*z-x) > 0.0001; z -= (z*z-x)/(2*z) {
		sum += 1
	}
	fmt.Println("迭代次数", sum)
	return z
}

func main(){  // main函数，是程序执行的入口
    // 测试牛顿法计算平方根
    // fmt.Println("计算 2 的平方根:", Sqrt(2))
    // fmt.Println("计算 9 的平方根:", Sqrt(9))
    // fmt.Println("计算 0.25 的平方根:", Sqrt(0.25))
    // fmt.Println(runtime.GOOS)
    // fmt.Println(runtime.GOARCH)
    
    switch  {
       case time.Now().Hour() < 17:
            fmt.Println("下午好")
            fallthrough
       
       case time.Now().Hour() < 12:
            fmt.Println("上午好")
            fallthrough
       
       default:
            fmt.Println("晚上好")
       
    }
}