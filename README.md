# front_back
前后端乱


# 							问题集合



```shell
 conda activate fastapi_project
cd C:\Users\陈美琪\Desktop\start-9-19\version1\Devolopment\fastAPI\demo1
python mains.py
// 前端
cd C:\Users\陈美琪\Desktop\start-9-19\version1\Devolopment\code-ABUS  npm run serve

```



vuerouter问题

vue2如果不用router-link标签，因为用router-link标签可以配合router-view占位符，当点击router-link标签就可以路由跳转，这很方便，也很好理解。但是对于使用router.push这种使用方式，目前我还有点迷惑，只知道是在router文件夹内定义一个route数组，写好什么路径对应什么路由组件，也知道如果使用这种方式，当在浏览器地址栏输入变化的url所对应的路由路径时，页面会渲染对应的路由组件，但是好像这种理解方式不如前面提到的router-link的方式直观，因为前者前者有一个router-link标签按钮展示在页面上，有点击效果，但是使用router-push的方式，比如首页，个人信息，about有这几个icon，使用router.push方式怎么确定点击个人信息的icon页面就显示对应的路由组件？当然router-view占位符还是需要的，是显示路由组件的地方，是不是还要在icon上与路由或者对应的组件做一些联系，生命之类的东西？

# 一、9-22

提示词

在文件夹下的C:\Users\陈美琪\Desktop\start-9-19\version1\Devolopment\code-ABUS\src\pages\ABUS_BigData\dataDictionaryQuery.vue，dataDictionaryQuery.vue是用来展示如图的数据表的所有数据的。C:\Users\陈美琪\Desktop\start-9-19\version1\Devolopment\fastAPI\demo1\Abus_BigData_Cal\dataDictionaryQuery9_22.py是后端，用来给前端的dataDictionaryQuery.vue的文件提供api的。我的内网数据库的信息如下。

 db_server: *str* = os.getenv("DB_SERVER", "192.168.10.202 ")

  db_database: *str* = os.getenv("DB_DATABASE", "Dictionary")

  db_username: *str* = os.getenv("DB_USERNAME", "sa")

  db_password: *str* = os.getenv("DB_PASSWORD", "3518j")

要求是将数据库Dictionary里的所有表里的数据展示在前端dataDictionaryQuery.vue中，基本样式就是有一个select框，这个框里面可以选择Dictionary数据库里的每一张表，然后当点击选择某一张表时，就展示这张表的所有数据。我已经将dataDictionaryQuery.vue文件的基本样式写好，请你完成前端dataDictionaryQuery.vue和后端dataDictionaryQuery9_22.py相关文件。

提示词2，

现在要在前端dataDictionaryQuery.vue中增加一个按钮，当用户点击这个按钮是将页面呈现的表格数据以excel的格式下载，我希望excle表格是在后端生成然后返回给前端，不是让前端去生成excel表格。

用户点击“导出 Excel文件”按钮时，前端请求后端的 **导出接口**

后端在这个接口里会：

- 再次去数据库查询相同的数据（或者根据前端传来的参数，查相同的一批数据）。
- 用 `pandas` 或 `openpyxl` 等库在后端生成一个 Excel 文件。
- 把这个 Excel 文件通过 **文件流** 的形式返回给前端。

前端浏览器接收到返回的数据后，会触发 **文件下载**



前端页面展示还需要再修改，将表格的展示改成如图的样式，分成一页一页的，一页内的数据条数不易太多设定为25条即可，一页内可以滚动显示数据。

然后还要给每一条数据增加一个序号，以便于阅读的人能清晰阅读

## 三、

需求分析，是更改[User Center - 万晖五金报销系统](http://reimbursement.abushardware.com/#/system/user-center)  这个网页中的更改密码的逻辑。项目路径在

```
C:\Users\陈美琪\Desktop\lyh-Reimbursement-ver1.06\Reimbursement
```

```
http://reimbursement.abushardware.com/#/system/user-center
```

MD5加密，服务器和数据库分别是 192.168.41.57 Reimbursement数据库下的user表









department2020 派工单表 预加载前1000条数据   

查找条件：  订单批号  料品名称 规格型号。   模糊查找：    确定交期，  				时间范围  日期控件

分页

派工单查询  Dispatch work order



提示词，我要在ABUS Big Data 大数据下增加一个“派工单查询”的二级菜单，也就是在前端的C:\Users\陈美琪\Desktop\start-9-19\version1\Devolopment\code-ABUS\src\pages\ABUS_BigData下新增一个.vue文件，新增文件是Dispatch_work_order.vue。与这个相关的后端.py文件放在C:\Users\陈美琪\Desktop\start-9-19\version1\Devolopment\fastAPI\demo1\Abus_BigData_Cal下，文件名是Dispatch_work_order.py。



数据库信息如下，192.168.41.57 下的department2020 数据库下的 派工单  表 这张表大小是1.6G。要求是将前1000条数据展示在web页面上，并且按照25条一页。因为这张表的数据是在是太大了，所以只是展示前1000条，那1000条后面的数据怎么查看呢？只能是在页面上摆几个输入框，根据输入查询。但是表的属性有72个，要有选择性地展示。





 select * from 派工单 where 订单批号 like '%  %'  and 料品名称 like '%  %' and 规格型号 like '%  %' and 确定交期 between '' and ''


 # 前后端跨域问题
 你这个问题涉及 前端开发环境代理 和 部署环境跨域，我帮你梳理下思路：

1. changeOrigin: true 的作用

在 Vue2 的 vue.config.js 或 Vue3 的 vite.config.js 里配置 proxy 时，
changeOrigin: true 表示 开发服务器（webpack-dev-server / Vite dev server）在转发请求时，会把请求头里的 Origin 改成目标地址的域名。

这相当于“伪装”成后端允许的请求源，从而在本地开发时解决跨域问题。

⚠️ 注意：这是 开发代理 的功能，只在本地调试时生效，生产环境（打包后）不起作用。

2. 部署到生产环境时

打包后的前端代码是静态文件，不再经过 dev server 代理，所以 proxy 配置不再生效。
这时跨域问题要看部署方式：

✅ 方案 A：前后端同域（推荐）

用 Nginx 把前端和后端统一到一个域名下，比如：

前端访问：https://example.com/ → 静态文件（Vue 打包结果）

后端访问：https://example.com/api/ → 反向代理到 127.0.0.1:8000

这样请求都在同一域下，根本没有跨域问题。

Nginx 配置类似：
```shell
server {
    listen 80;
    server_name example.com;

    location / {
        root /usr/share/nginx/html;  # Vue 打包后的 dist
        index index.html;
    }

    location /api {
        proxy_pass http://127.0.0.1:8000;
    }
}
```
✅ 方案 B：前后端不同域

如果前端是 https://www.example.com，后端是 https://api.example.com，那就是跨域。

这种情况下就不能靠前端 proxy 了，要么：

在后端开启 CORS，允许指定的前端域名访问（比如 FastAPI、Spring Boot 都有对应配置）。

或者继续用 Nginx 做反向代理，把 /api 转发到后端。

3. 结论

changeOrigin: true 只是开发环境本地解决跨域。

部署后：

如果前后端同域，不用管，Nginx 配置代理即可。

如果前后端分离不同域，需要后端允许 CORS 或 Nginx 做跨域转发。

​	























