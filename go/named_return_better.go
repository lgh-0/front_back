package main

import (
	"fmt"
	"time"
)

// 带名字的返回值示例
// 使用场景：函数返回多个相关值时，命名让代码更清晰

// 示例1: 短函数 - 适合使用裸返回
func splitName(fullName string) (first, last string) {
	// 找到空格位置
	spaceIndex := 0
	for i, char := range fullName {
		if char == ' ' {
			spaceIndex = i
			break
		}
	}
	
	// 分割名字
	first = fullName[:spaceIndex]
	last = fullName[spaceIndex+1:]
	
	// 裸返回 - 适合短函数
	return
}

// 示例2: 带有错误处理的函数
func processAge(age int) (isValid bool, message string) {
	if age < 0 {
		isValid = false
		message = "年龄不能为负数"
		return // 裸返回
	}
	
	if age > 150 {
		isValid = false
		message = "年龄超出合理范围"
		return
	}
	
	isValid = true
	message = "年龄有效"
	return
}

// 示例3: 长函数 - 不推荐裸返回（这里为了演示对比）
func longFunction(input int) (result int, err error) {
	// 在长函数中，明确返回更清晰
	fmt.Println("开始处理...")
	
	if input < 0 {
		err = fmt.Errorf("输入不能为负数")
		return 0, err // 明确返回，避免混淆
	}
	
	// 模拟复杂处理
	time.Sleep(100 * time.Millisecond)
	result = input * 10
	
	// 即使可以裸返回，也明确写出
	return result, nil
}

// 示例4: 带名字返回值的零值
func getUser(id int) (name string, age int, active bool) {
	// 命名的返回值自动初始化为零值
	// name = "", age = 0, active = false
	
	if id == 1 {
		name = "张三"
		age = 25
		active = true
	} else if id == 2 {
		name = "李四"
		age = 30
		active = true
	}
	// 其他情况返回零值
	
	return // 裸返回零值或设置的值
}

func main() {
	// 测试分割名字
	first, last := splitName("John Doe")
	fmt.Printf("名: %s, 姓: %s\n", first, last)
	
	// 测试年龄验证
	valid, msg := processAge(25)
	fmt.Printf("验证结果: %v, 消息: %s\n", valid, msg)
	
	valid, msg = processAge(-5)
	fmt.Printf("验证结果: %v, 消息: %s\n", valid, msg)
	
	// 测试长函数
	res, err := longFunction(5)
	fmt.Printf("结果: %d, 错误: %v\n", res, err)
	
	// 测试用户查询（返回零值的情况）
	name, age, active := getUser(3)
	fmt.Printf("用户3: 姓名='%s', 年龄=%d, 活跃=%v\n", name, age, active)
}
