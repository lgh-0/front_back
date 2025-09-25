`services.msc`
get post put delete patch
```{js}
axios.get("/api/user/1")
  .then(response => {
    console.log(response.status);   // 200
    console.log(response.data);     // 后端返回的业务数据
  })
  .catch(error => {
    console.error(error.response);  // 错误时的响应
  });

```
也可以使用async/await
```{js}
async function fetchUser() {
  try {
    const res = await axios.get("/api/user/1");
    console.log(res.data); // 后端数据
  } catch (err) {
    console.error(err.response?.data);
  }
}
fetchUser();
```
1. RESTful API 返回数据

约定俗成：RESTful API 返回的数据 一般是 JSON。

前端用 axios 调用接口时，response.data 通常就是一个 JSON 对象。
Python 的 字典（dict） 可以直接作为返回值，FastAPI 会自动帮你转成 JSON。
在 Spring Boot 中：

你通常会写一个 Java 对象（POJO/Entity/DTO），方法里返回它。

Spring Boot 内置了 Jackson（JSON 序列化工具），会自动把对象转成 JSON。

是的，你说的很对——对于 Spring Boot 来说，返回一个类实例，本质上就是“类的属性名+属性值的键值对集合”，Spring Boot 会自动 JSON 化。
```java
@RestController
public class UserController {

    @GetMapping("/user")
    public User getUser() {
        return new User(1, "Alice");
    }
}

class User {
    private int id;
    private String name;

    // 构造函数 + getter/setter
}


```
FastAPI：直接返回 dict / Pydantic 模型 → 自动转 JSON

Spring Boot：直接返回对象 / 集合 → Jackson 自动转 JSON

通用 RESTful API 规范：一般约定返回结构类似：
```json
{
  "code": 0,          // 业务状态码，0 表示成功，非 0 表示失败
  "message": "ok",   // 业务消息，成功时一般是 "ok"
  "data": { ... }    // 业务数据，成功时返回具体数据，失败时通常是 null
}
```

# 数据绑定
v-bind 的本质

作用：把 JS 表达式的结果 动态绑定到某个 HTML 属性上。

语法：v-bind:属性名="JS表达式"

缩写：:属性名="JS表达式"

例子：
```html
<a v-bind:href="school.url.toUpperCase()">点我去{{school.name}}学习</a>
<a :href="school.url">点我去{{school.name}}学习</a>
```

作用：实现表单元素的 双向数据绑定（数据 <-> 视图）。

默认绑定的属性：value（针对 input、textarea、select 这些表单元素）。

完整写法：v-model:value="name"

Vue 会帮你把 value 属性和 input 事件绑定好。

所以缩写成：v-model="name"。
```html
<input v-model="username" />
<!-- 相当于 -->
<input :value="username" @input="username = $event.target.value" />
```

# 关于后端返回的json格式和前端的变量声明问题
返回 JSON 数组 → 前端 axios 会解析成一个 JS 数组对象（[]）。
返回 JSON 对象 → 前端 axios 会解析成一个 JS 普通对象（{}）。
在 setup 初始化时如果不给 ref 一个合适的默认值，Vue 的模板渲染阶段可能会遇到 undefined 的情况，比如你在数据还没请求回来之前就执行了 v-for。

为了避免报错，最好把初始值写成对应的类型：

如果最终是数组 → ref([])

如果最终是对象 → ref({})

如果是单值 → ref('') 或 ref(null)

SELECT * FROM [demo1].[dbo].[table1];

# 三、axios
## 3.1 前端发送参数

