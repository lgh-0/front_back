
```js
// node-server.js 不依赖于express
const http = require("http");

const port = 3001;

const server = http.createServer((req, res) => {
  if (req.method === "GET" && req.url === "/nodeapi/password") {
    const result = { password: "123445nodejs返回的密码" };

    res.writeHead(200, { "Content-Type": "application/json" });
    res.end(JSON.stringify(result));
  } else {
    res.writeHead(404, { "Content-Type": "application/json" });
    res.end(JSON.stringify({ error: "Not Found" }));
  }
});

server.listen(port, () => {
  console.log(`✅ Node.js API 运行在 http://127.0.0.1:${port}`);
});

```

