package main

import (
	"fmt"
	"time"
)

func main() {
	// 1. fallthrough - 穿透到下一个 case
	fmt.Println("=== fallthrough 示例 ===")
	hour := time.Now().Hour()
	
	switch {
	case hour < 12:
		fmt.Println("上午好")
		fallthrough // 继续执行下一个 case，不判断条件
	case hour < 18:
		fmt.Println("下午好") // 这行会被执行
	case hour < 22:
		fmt.Println("晚上好")
	default:
		fmt.Println("夜深了")
	}
	
	// 2. break - 跳出 switch（默认行为，通常不需要写）
	fmt.Println("\n=== break 示例 ===")
	for i := 0; i < 5; i++ {
		switch i {
		case 2:
			fmt.Println("遇到2，跳出")
			break // break 是可选的，switch 默认就会跳出
		case 3:
			fmt.Println("遇到3")
		default:
			fmt.Printf("数字: %d\n", i)
		}
	}
	
	// 3. 带标签的 break - 跳出外层循环
	fmt.Println("\n=== 带标签的 break ===")
OuterLoop:
	for i := 0; i < 3; i++ {
		for j := 0; j < 3; j++ {
			if i == 1 && j == 1 {
				fmt.Printf("跳出外层循环 i=%d, j=%d\n", i, j)
				break OuterLoop // 跳出 OuterLoop 标记的循环
			}
			fmt.Printf("i=%d, j=%d\n", i, j)
		}
	}
	
	// 4. continue - 跳过当前迭代，继续下一次
	fmt.Println("\n=== continue 示例 ===")
	for i := 0; i < 5; i++ {
		if i == 2 {
			continue // 跳过 i=2 的情况
		}
		fmt.Printf("数字: %d\n", i)
	}
	
	// 5. goto - 跳转到标签（不推荐使用）
	fmt.Println("\n=== goto 示例 ===")
	i := 0
Here:
	fmt.Printf("i = %d\n", i)
	i++
	if i < 3 {
		goto Here // 跳转到 Here 标签
	}
	
	// 6. switch 中的 continue（在循环中）
	fmt.Println("\n=== switch 中的 continue ===")
	for i := 0; i < 5; i++ {
		switch i {
		case 1, 3:
			continue // 跳过奇数
		default:
			fmt.Printf("偶数: %d\n", i)
		}
	}
	
	// 7. 修复你的时间判断逻辑
	fmt.Println("\n=== 正确的时间判断 ===")
	switch {
	case hour < 12:
		fmt.Println("上午好")
	case hour < 18:
		fmt.Println("下午好")
	case hour < 22:
		fmt.Println("晚上好")
	default:
		fmt.Println("夜深了")
	}
}
