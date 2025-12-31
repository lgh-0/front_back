package main

import (
	"fmt"
	"math"
)

// 示例1: 带名字的返回值 - 矩形的长和宽
func rectangle(length, width float64) (area, perimeter float64) {
	// area 和 perimeter 已经在函数顶部定义，可以直接使用
	area = length * width
	perimeter = 2 * (length + width)
	// 裸返回 - 直接返回已命名的返回值
	return
}

// 示例2: 带名字的返回值作为文档 - 计算圆的属性
func circle(radius float64) (area, circumference float64) {
	// 命名的返回值让函数意图更清晰
	area = math.Pi * radius * radius
	circumference = 2 * math.Pi * radius
	// 裸返回
	return
}

// 示例3: 不推荐在长函数中使用裸返回
func complexCalculation(x int) (result int, err error) {
	// 在长函数中，明确返回值更清晰
	if x < 0 {
		err = fmt.Errorf("negative number not allowed")
		return 0, err // 明确返回，避免裸返回
	}
	
	// 复杂的计算...
	result = x * 2
	// 明确返回
	return result, err
}

// 示例4: 混合使用 - 有时需要覆盖命名的返回值
func divide(a, b float64) (quotient float64, err error) {
	if b == 0 {
		err = fmt.Errorf("division by zero")
		return 0, err // 覆盖默认的 quotient 值
	}
	
	quotient = a / b
	// 可以裸返回，因为 err 是零值(nil)
	return
}

func main() {
	// 测试矩形函数
	a, p := rectangle(5.0, 3.0)
	fmt.Printf("矩形: 面积=%.2f, 周长=%.2f\n", a, p)
	
	// 测试圆函数
	area, circ := circle(2.5)
	fmt.Printf("圆: 面积=%.2f, 周长=%.2f\n", area, circ)
	
	// 测试除法函数
	q, e := divide(10, 2)
	if e != nil {
		fmt.Println("错误:", e)
	} else {
		fmt.Printf("除法: 商=%.2f\n", q)
	}
	
	// 测试错误情况
	_, e2 := divide(10, 0)
	if e2 != nil {
		fmt.Println("错误:", e2)
	}
}
