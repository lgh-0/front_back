<template>
  <div>
    {{ msg }}这是第一个vue2项目
    <el-button type="primary">按钮</el-button>
    <el-dialog title="提示" :visible.sync="dialogVisible">
      <span>这是一段信息</span>
      <span slot="footer" class="dialog-footer">
        <el-button @click="dialogVisible = false">取 消</el-button>
        <el-button type="primary" @click="dialogVisible = false">确 定</el-button>
      </span>
    </el-dialog>
    <el-button type="text" @click="dialogVisible = true">打开 Dialog</el-button>
    <hr>
    <el-form :model="form">
      <el-form-item label="姓名">
        <el-input v-model="form.name"></el-input>
      </el-form-item>
      <el-form-item label="性别">
        <el-select v-model="form.gender">
          <el-option label="男" value="male" />
          <el-option label="女" value="female" />
        </el-select>
      </el-form-item>
    </el-form>

    <el-table :data="tableData">
      <el-table-column prop="name" label="姓名" />
      <el-table-column prop="age" label="年龄" />
    </el-table>
  </div>
</template>

<script>
export default {
  name: 'HelloWorld',
  props: {
    msg: String
  },
  data() {
    return {
      dialogVisible: false,
      form: {
        name: '',
        gender: ''
      },
      tableData: [
        { name: '张三', age: 20 },
        { name: '李四', age: 25 }
      ]
    };
  },
  methods: {
    // showDialog() {
    //   this.dialogVisible = true;
    // }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
h3 {
  margin: 40px 0 0;
}

ul {
  list-style-type: none;
  padding: 0;
}

li {
  display: inline-block;
  margin: 0 10px;
}

a {
  color: #42b983;
}
</style>
