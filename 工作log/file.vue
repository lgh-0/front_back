<!-- 文件查询 -->
<template>
    <Layout :breadcrumbItems="breadcrumbItems">
      <!-- 搜索表单 -->
      <div class="el-card is-always-shadow mb-4">
        <div class="el-card__body">
          <el-form :model="searchForm" label-width="100px">
            <el-row :gutter="20">
              <el-col :span="6">
                <el-form-item label="类别">
                  <el-select v-model="searchForm.类别" placeholder="请选择类别" clearable>
                    <el-option v-for="item in categoryOptions" :key="item.id" :label="item.name" :value="item.name" />
                  </el-select>
                </el-form-item>
              </el-col>
              <el-col :span="6">
                <el-form-item label="细分项目">
                  <el-select v-model="searchForm.细分项目" placeholder="请选择细分项目" clearable>
                    <el-option v-for="item in miniproductOptions" :key="item.id" :label="item.name" :value="item.name" />
                  </el-select>
                </el-form-item>
              </el-col>
              <el-col :span="6">
                <el-form-item label="文件名称">
                  <el-input v-model="searchForm.文件名称" placeholder="请输入文件名称" />
                </el-form-item>
              </el-col>
              <el-col :span="6">
                <el-form-item label="制作日期">
                  <el-date-picker v-model="searchForm.制作日期" type="date" placeholder="选择日期" value-format="yyyy-MM-dd" />
                </el-form-item>
              </el-col>
            </el-row>
            <el-row :gutter="20">
              <el-col :span="6">
                <el-form-item label="文件类型">
                  <el-select v-model="searchForm.文件类型" placeholder="请选择文件类型" clearable>
                    <el-option v-for="type in fileTypeOptions" :key="type" :label="type" :value="type" />
                  </el-select>
                </el-form-item>
              </el-col>
            </el-row>
            <div class="form-actions">
              <el-button type="default" @click="resetForm">重置</el-button>
              <el-button type="primary" @click="searchFiles">查询</el-button>
              <el-button v-if="hasAdminPermission" type="info" @click="openMiniproductDialog">增加细分</el-button>
              <el-button v-if="hasAdminPermission" type="warning" @click="openCategoryDialog">增加类别</el-button>
              <el-button v-if="hasAdminPermission" type="success" @click="openUploadDialog">上传文件</el-button>
            </div>
          </el-form>
        </div>
      </div>

      <!-- 文件列表 -->
      <div class="el-card is-always-shadow">
        <div class="el-card__header">
          <div class="card-title">文件列表</div>
        </div>
        <div class="el-card__body">
          <el-table :data="files" stripe border style="width: 100%" v-loading="loading" :header-cell-style="{backgroundColor:'#f5f7fa'}">
            <el-table-column prop="类别" label="类别" width="120" />
            <el-table-column prop="细分项目" label="细分项目" width="140" />
            <el-table-column prop="文件名称" label="文件名称" min-width="200" />
            <el-table-column prop="制作日期" label="制作日期" width="140" />
            <el-table-column prop="负责人" label="负责人" width="100" />
            <el-table-column prop="文件类型" label="文件类型" width="100" />
            <el-table-column label="预览" width="100">
              <template v-slot="scope">
                <el-button type="text" @click="openFile(scope.row.url, scope.row)">查看</el-button>
              </template>
            </el-table-column>
            <el-table-column v-if="hasAdminPermission" label="导出" width="100">
              <template v-slot="scope">
                <el-button type="text" @click="downloadFile(scope.row.url, scope.row.文件名称, scope.row)">下载</el-button>
              </template>
            </el-table-column>
          </el-table>

          <div v-if="files.length === 0 && !loading" class="no-data">暂无数据</div>
        </div>
      </div>

      <!-- 上传文件对话框 -->
      <el-dialog title="上传文件" :visible.sync="uploadDialogVisible" width="500px" :close-on-click-modal="false">
        <el-form :model="uploadForm" label-width="90px">
          <el-form-item label="类别">
            <el-select v-model="uploadForm.类别" placeholder="请选择类别" clearable>
              <el-option v-for="item in categoryOptions" :key="item.id" :label="item.name" :value="item.name" />
            </el-select>
          </el-form-item>
          <el-form-item label="细分项目">
            <el-select v-model="uploadForm.细分项目" placeholder="请选择细分项目" clearable>
              <el-option v-for="item in miniproductOptions" :key="item.id" :label="item.name" :value="item.name" />
            </el-select>
          </el-form-item>
          <el-form-item label="文件名称">
            <el-input v-model="uploadForm.文件名称" />
          </el-form-item>
          <el-form-item label="制作日期">
            <el-date-picker v-model="uploadForm.制作日期" type="date" placeholder="选择日期" value-format="yyyy-MM-dd" />
          </el-form-item>
          <el-form-item label="文件类型">
            <el-select v-model="uploadForm.文件类型" placeholder="请选择文件类型" clearable @change="handleFileTypeChange">
              <el-option v-for="t in fileTypeOptions" :key="t" :label="t" :value="t" />
            </el-select>
          </el-form-item>
          <!-- 当文件类型为"链接"时显示输入框 -->
          <el-form-item v-if="uploadForm.文件类型 === '链接'" label="链接地址">
            <el-input 
              v-model="uploadForm.链接地址" 
              placeholder="请输入链接地址（如：https://www.baidu.com）"
              clearable
            />
          </el-form-item>
          <!-- 当文件类型不是"链接"时显示文件上传 -->
          <el-form-item v-else label="选择文件">
            <el-upload
              action="/api/file/upload"
              :auto-upload="false"
              :file-list="uploadFileList"
              :limit="1"
              :on-change="handleFileChange"
              :show-file-list="true"
              accept=".doc,.docx,.xls,.xlsx,.pdf,.ppt,.pptx,.mp4,.avi,.mov,.wmv,.flv,.mkv,.webm,.3gp,.m4v"
            >
              <el-button type="primary">选择文件</el-button>
            </el-upload>
          </el-form-item>
        </el-form>

        <template #footer>
          <span class="dialog-footer">
            <el-button @click="uploadDialogVisible = false">取消</el-button>
            <el-button type="primary" :loading="uploading" @click="submitUpload">上传</el-button>
          </span>
        </template>
      </el-dialog>

      <!-- 增加类别对话框 -->
      <el-dialog title="增加类别" :visible.sync="categoryDialogVisible" width="400px" :close-on-click-modal="false">
        <el-form :model="categoryForm" label-width="80px">
          <el-form-item label="类别名称" required>
            <el-input v-model="categoryForm.name" placeholder="请输入类别名称" maxlength="50" show-word-limit />
          </el-form-item>
        </el-form>

        <template #footer>
          <span class="dialog-footer">
            <el-button @click="categoryDialogVisible = false">取消</el-button>
            <el-button type="primary" :loading="categoryLoading" @click="createCategory">确定</el-button>
          </span>
        </template>
      </el-dialog>

      <!-- 增加细分项目对话框 -->
      <el-dialog title="增加细分项目" :visible.sync="miniproductDialogVisible" width="500px" :close-on-click-modal="false">
        <el-form :model="miniproductForm" label-width="120px">
          <el-form-item label="细分项目名称" required>
            <el-input v-model="miniproductForm.name" placeholder="请输入细分项目名称" maxlength="50" show-word-limit />
          </el-form-item>
        </el-form>

        <template #footer>
          <span class="dialog-footer">
            <el-button @click="miniproductDialogVisible = false">取消</el-button>
            <el-button type="primary" :loading="miniproductLoading" @click="createMiniproduct">确定</el-button>
          </span>
        </template>
      </el-dialog>

      <!-- 文件预览对话框 -->
      <el-dialog title="文件预览" :visible.sync="previewDialogVisible" width="80%" :destroy-on-close="true">
        <vue-office-docx v-if="isDocx" :src="previewUrl" style="height:80vh" />
        <vue-office-excel v-else-if="isXlsx" :src="previewUrl" style="height:80vh" />
        <vue-office-pdf v-else-if="isPdf" :src="previewUrl" style="height:80vh" />
        <div v-else-if="isPpt" class="ppt-preview">
          <div v-if="pptxLoading" class="ppt-loading">
            <div class="loading-spinner"></div>
            <p>正在加载PPT文件，请稍候...</p>
          </div>
          <div v-else-if="pptxError" class="ppt-error">
            <p>PPT预览失败：{{ pptxError }}</p>
            <el-button type="primary" @click="downloadCurrentFile">下载文件</el-button>
          </div>
          <div v-else ref="pptxContainer" class="pptx-container"></div>
        </div>
        <video v-else-if="isVideo" :src="previewUrl" controls style="width:100%;height:80vh;object-fit:contain;" />
        <div v-else class="other-file-preview">
          <div class="file-info">
            <h3>文件预览</h3>
            <p>文件名：{{ previewFileName }}</p>
            <p>文件类型：{{ previewExt }}</p>
            <p>此文件类型暂不支持在线预览，请下载后查看。</p>
            <el-button type="primary" @click="downloadCurrentFile">下载文件</el-button>
          </div>
        </div>
      </el-dialog>
    </Layout>
  </template>
  
  <script>
  import Layout from '../../components/Layout.vue';
  import axios from 'axios';
  import { eventBus } from '../../eventBus';
  // 文档预览组件
  import VueOfficeDocx from '@vue-office/docx'
  import VueOfficeExcel from '@vue-office/excel'
  import VueOfficePdf from '@vue-office/pdf'
  // @vue-office/pdf 当前版本无独立样式文件，若升级版本包含再取消注释
  // import '@vue-office/pdf/lib/index.css'
  import '@vue-office/docx/lib/index.css'
  import '@vue-office/excel/lib/index.css'
  
  // PPT预览组件
  import { init } from 'pptx-preview'
  
  export default {
    name: 'file',
    components: { Layout, VueOfficeDocx, VueOfficeExcel, VueOfficePdf },
    data() {
      return {
        breadcrumbItems: [],
        files: [],
        loading: false,
        searchForm: {
          类别: '',
          细分项目: '',
          文件名称: '',
          制作日期: '',
          文件类型: ''
        },
        sidebarMenus: [],
        fileTypeOptions: ['pdf', 'docx', 'xlsx', 'ppt', 'mp4', 'avi', 'mov', 'wmv', 'flv', 'mkv', 'webm', '3gp', 'm4v', '链接'],
        uploading: false, // 新增上传状态
        uploadDialogVisible: false, // 上传对话框
        previewDialogVisible: false, // 预览对话框
        previewUrl: '',
        previewExt: '',
        uploadForm: {
          file: null,
          类别: '',
          细分项目: '',
          文件名称: '',
          制作日期: '',
          文件类型: '',
          链接地址: '' // 新增链接地址字段    https://www.baidu.com
        },
        uploadFileList: [], // 新增上传文件列表
        allowedExt: ['doc','docx','xls','xlsx','pdf','ppt','pptx','mp4','avi','mov','wmv','flv','mkv','webm','3gp','m4v'],
        categoryOptions: [], // 新增类别选项
        categoryDialogVisible: false, // 类别对话框显示状态
        categoryForm: {
          name: ''
        },
        categoryLoading: false, // 类别操作加载状态
        // 细分项目相关
        miniproductOptions: [], // 细分项目选项
        miniproductDialogVisible: false, // 细分项目对话框显示状态
        miniproductForm: {
          name: ''
        },
        miniproductLoading: false, // 细分项目操作加载状态
        // 权限控制相关
        isAdmin: false,
        currentUser: null,
        // PPT预览相关
        pptxPreviewer: null,
        pptxLoading: false,
        pptxError: null
      };
    },
    computed: {
      isDocx () {
        return ['doc', 'docx'].includes(this.previewExt)
      },
      isXlsx () {
        return ['xls', 'xlsx'].includes(this.previewExt)
      },
      isPdf () {
        return this.previewExt === 'pdf'
      },
      isVideo () {
        const videoExts = ['mp4', 'avi', 'mov', 'wmv', 'flv', 'mkv', 'webm', '3gp', 'm4v'];
        return videoExts.includes(this.previewExt);
      },
      isPpt () {
        return this.previewExt === 'ppt' || this.previewExt === 'pptx';
      },
      previewFileName() {
        if (this.previewUrl) {
          const seg = this.previewUrl.split('?')[0].split('#')[0];
          return seg.substring(seg.lastIndexOf('/') + 1);
        }
        return '';
      },
      // 权限控制计算属性
      hasAdminPermission() {
        this.checkUserPermissions();
        return this.isAdmin;
      }
    },
    mounted() {
      this.initializeUserPermissions(); // 初始化用户权限
      this.searchFiles();
      this.fetchCategories(); // 在组件挂载时获取类别
      this.fetchMiniproducts(); // 在组件挂载时获取细分项目
    },
    activated() {
      // 当组件被激活时重新检查权限
      this.initializeUserPermissions();
      console.log('文件管理组件激活，重新检查权限:', { currentUser: this.currentUser, isAdmin: this.isAdmin });
    },
    created() {
      // 监听侧边栏菜单以生成面包屑
      eventBus.$on('sidebar-Menus-Updated', menus => {
        this.sidebarMenus = menus;
        this.generateBreadcrumb(this.$route.path);
      });
      // 初次进入时如果还没有菜单数据，给一个默认面包屑
      if (this.sidebarMenus.length === 0) {
        this.breadcrumbItems = ['文件查询'];
      }
    },
    watch: {
      $route(newVal) {
        this.generateBreadcrumb(newVal.path);
      },
      // 监听存储中用户信息的变化
      '$store.state.user.username': {
        handler(newVal) {
          if (newVal !== this.currentUser) {
            this.initializeUserPermissions();
          }
        },
        deep: true
      }
    },
    methods: {
      async searchFiles() {
        this.loading = true;
        try {
          const params = {};
          Object.keys(this.searchForm).forEach(k => {
            if (this.searchForm[k]) params[k] = this.searchForm[k];
          });
          const res = await axios.get('/api/file', { 
            params,
            headers: {
              'Cache-Control': 'no-cache',
              'Pragma': 'no-cache'
            }
          });
          if (res.data.status === 'success') {
            this.files = res.data.data;
          } else {
            this.$message.error('查询失败');
          }
        } catch (e) {
          console.error(e);
          this.$message.error('查询失败，请检查网络');
        } finally {
          this.loading = false;
        }
      },
      resetForm() {
        Object.keys(this.searchForm).forEach(k => (this.searchForm[k] = ''));
        this.searchFiles();
      },
      openFile(url, row) {
        // ✨ 如果是链接类型（如新闻链接），直接在新窗口打开，跳转到外部网站
        if (row && row.文件类型 === '链接' && row.备注) {
          const linkUrl = row.备注.split(' | ')[0];
          if (linkUrl) {
            // 在新标签页打开链接
            window.open(linkUrl, '_blank');
            this.$message.success('正在打开链接...');
            return;
          }
        }
        
        // 重置PPT相关状态
        this.pptxLoading = false;
        this.pptxError = null;
        if (this.pptxPreviewer) {
          this.pptxPreviewer = null;
        }
        
        // 如果有url，使用原来的逻辑
        if (url) {
          let fullUrl;
          if (url.startsWith('/static')) {
            fullUrl = window.location.origin + '/api' + url; // dev proxy
          } else {
            fullUrl = url.startsWith('http') ? url : window.location.origin + url;
          }
          this.previewUrl = fullUrl;
          const seg = fullUrl.split('?')[0].split('#')[0]
          this.previewExt = seg.substring(seg.lastIndexOf('.') + 1).toLowerCase()
          
          // 对于视频文件，检查是否在videos目录下
          if (url.startsWith('/static/videos/')) {
            this.previewExt = this.previewExt || 'mp4'; // 默认为mp4
          }
          
          this.previewDialogVisible = true;
          
          // 如果是PPT文件，在对话框打开后加载预览
          if (this.isPpt) {
            this.$nextTick(() => {
              this.loadPptxPreview(fullUrl);
            });
          }
        } else if (row && row.id) {
          // 使用新的预览API
          const viewUrl = `/api/file/view/${row.id}`;
          this.previewUrl = window.location.origin + viewUrl;
          this.previewExt = row.文件类型 ? row.文件类型.toLowerCase() : 'unknown';
          this.previewDialogVisible = true;
          
          // 如果是PPT文件，在对话框打开后加载预览
          if (this.isPpt) {
            this.$nextTick(() => {
              this.loadPptxPreview(this.previewUrl);
            });
          }
        }
      },
      generateBreadcrumb(path) {
        try {
          const find = (menusArr, t) => {
            for (const m of menusArr) {
              if (m.path === t) return m.name;
              if (m.children) {
                const c = m.children.find(ch => ch.path === t);
                if (c) return [m.name, c.name];
              }
            }
            return path.split('/').pop();
          };
          const names = find(this.sidebarMenus, path);
          this.breadcrumbItems = Array.isArray(names) ? names : [names];
        } catch (e) {
          this.breadcrumbItems = ['文件查询'];
        }
      },
      // 新增上传文件方法
      async customUpload(options) {
        this.uploading = true;
        try {
          const formData = new FormData();
          formData.append('file', options.file); // 文件对象
          formData.append('类别', this.searchForm.类别);
          formData.append('细分项目', this.searchForm.细分项目);
          formData.append('文件名称', this.searchForm.文件名称);
          formData.append('制作日期', this.searchForm.制作日期);
          formData.append('文件类型', this.searchForm.文件类型);

          const res = await axios.post('/api/file/upload', formData, {
            headers: {
              'Content-Type': 'multipart/form-data'
            },
            timeout: 300000  // 5分钟超时，适合大视频文件
          });
          if (res.data.status === 'success') {
            this.$message.success('文件上传成功');
            await this.searchFiles();
          } else {
            this.$message.error('文件上传失败: ' + res.data.message);
          }
        } catch (e) {
          console.error(e);
          this.$message.error('文件上传失败，请检查网络');
        } finally {
          this.uploading = false;
        }
      },
      openUploadDialog() {
        this.uploadDialogVisible = true;
        this.uploadForm = {
          file: null,
          类别: this.searchForm.类别,
          细分项目: this.searchForm.细分项目,
          文件名称: this.searchForm.文件名称,
          制作日期: this.searchForm.制作日期,
          文件类型: this.searchForm.文件类型,
          链接地址: ''
        };
        this.uploadFileList = []; // 清空文件列表
      },
      handleFileTypeChange(value) {
        // 当文件类型改变时，清空相关字段
        if (value === '链接') {
          this.uploadForm.file = null;
          this.uploadFileList = [];
        } else {
          this.uploadForm.链接地址 = '';
        }
      },
      handleFileChange(file) {
        const ext = file.name.split('.').pop().toLowerCase();
        const fileNameWithoutExt = file.name.substring(0, file.name.lastIndexOf('.'));
        const videoExts = ['mp4', 'avi', 'mov', 'wmv', 'flv', 'mkv', 'webm', '3gp', 'm4v'];
        const docExts = ['doc', 'docx', 'xls', 'xlsx', 'pdf', 'ppt', 'pptx'];
        const isVideo = videoExts.includes(ext);
        
        if (!videoExts.includes(ext) && !docExts.includes(ext)) {
          this.$message.error('不支持的文件类型');
          return false;
        }
        
        // 检查文件大小
        const maxSize = isVideo ? 500 * 1024 * 1024 : 50 * 1024 * 1024; // 视频500MB，文档50MB
        if (file.size > maxSize) {
          this.$message.error(`文件大小不能超过 ${isVideo ? '500MB' : '50MB'}，当前文件大小: ${(file.size / (1024 * 1024)).toFixed(1)}MB`);
          return false;
        }
        
        if (isVideo) {
          this.$message.info('已选择视频文件，上传时请耐心等待...');
        }
        
        // 自动填充文件名和文件类型
        this.uploadForm.file = file.raw;
        this.uploadForm.文件名称 = fileNameWithoutExt;
        this.uploadForm.文件类型 = ext;
        this.uploadFileList = [file];
      },
      async submitUpload() {
        // 如果是链接类型
        if (this.uploadForm.文件类型 === '链接') {
          if (!this.uploadForm.链接地址 || !this.uploadForm.链接地址.trim()) {
            this.$message.warning('请输入链接地址');
            return;
          }
          
          // 简单验证：只要包含常见的域名特征即可（支持各种新闻链接格式）
          const linkValue = this.uploadForm.链接地址.trim();
          // 检查是否包含基本的URL特征（域名、路径等）
          if (linkValue.length < 5 || (!linkValue.includes('.') && !linkValue.includes('/'))) {
            this.$message.warning('请输入有效的链接地址');
            return;
          }
          
          this.uploading = true;
          try {
            const res = await axios.post('/api/file/upload-link', {
              类别: this.uploadForm.类别,
              细分项目: this.uploadForm.细分项目,
              文件名称: this.uploadForm.文件名称,
              制作日期: this.uploadForm.制作日期,
              文件类型: '链接',
              链接地址: this.uploadForm.链接地址,
              负责人: 'admin'
            });
            
            if (res.data.status === 'success') {
              this.$message.success('链接添加成功');
              await this.searchFiles();
              this.uploadDialogVisible = false;
            } else {
              this.$message.error('链接添加失败: ' + res.data.message);
            }
          } catch (e) {
            console.error(e);
            this.$message.error('链接添加失败，请检查网络');
          } finally {
            this.uploading = false;
          }
          return;
        }
        
        // 原有的文件上传逻辑
        if (!this.uploadForm.file) {
          this.$message.warning('请选择要上传的文件');
          return;
        }
        
        // 检查是否为视频文件
        const ext = this.uploadForm.file.name.split('.').pop().toLowerCase();
        const videoExts = ['mp4', 'avi', 'mov', 'wmv', 'flv', 'mkv', 'webm', '3gp', 'm4v'];
        const isVideo = videoExts.includes(ext);
        
        this.uploading = true;
        try {
          const formData = new FormData();
          formData.append('file', this.uploadForm.file);
          formData.append('类别', this.uploadForm.类别);
          formData.append('细分项目', this.uploadForm.细分项目);
          formData.append('文件名称', this.uploadForm.文件名称);
          formData.append('制作日期', this.uploadForm.制作日期);
          formData.append('负责人', 'admin'); // 默认值
          
          let url = isVideo ? '/api/video/upload' : '/api/file/upload';
          if (!isVideo) {
            formData.append('文件类型', ext);
          }
          
          if (isVideo) {
            this.$message.info('正在上传视频文件，请耐心等待...');
          }
          
          const res = await axios.post(url, formData, {
            headers: {
              'Content-Type': 'multipart/form-data'
            },
            timeout: isVideo ? 600000 : 300000  // 视频10分钟，普通文件5分钟
          });
          
          if (res.data.status === 'success') {
            this.$message.success(isVideo ? '视频上传成功' : '文件上传成功');
            await this.searchFiles();
            this.uploadDialogVisible = false;
          } else {
            this.$message.error((isVideo ? '视频' : '文件') + '上传失败: ' + res.data.message);
          }
        } catch (e) {
          console.error(e);
          this.$message.error((isVideo ? '视频' : '文件') + '上传失败，请检查网络');
        } finally {
          this.uploading = false;
        }
      },
      handleUploadSuccess(response) {
        if (response.status === 'success') {
          this.$message.success('文件上传成功');
          this.searchFiles();
          this.uploadDialogVisible = false;
        } else {
          this.$message.error('文件上传失败: ' + response.message);
        }
      },
      handleUploadError(err) {
        console.error(err);
        this.$message.error('文件上传失败，请检查网络');
      },
      // 新增获取类别方法
      async fetchCategories() {
        try {
          console.log('正在获取类别列表...');
          const res = await axios.get('/api/category');
          console.log('类别API响应:', res.data);
          if (res.data.status === 'success') {
            this.categoryOptions = res.data.data;
            console.log('类别列表:', this.categoryOptions);
          } else {
            console.error('获取类别失败:', res.data);
            this.$message.error('获取类别失败: ' + (res.data.message || '未知错误'));
          }
        } catch (e) {
          console.error('获取类别网络错误:', e);
          if (e.response) {
            console.error('错误响应:', e.response.data);
            this.$message.error('获取类别失败: ' + (e.response.data.detail || e.message));
          } else {
            this.$message.error('获取类别失败，请检查网络连接');
          }
        }
      },
      openCategoryDialog() {
        this.categoryDialogVisible = true;
        this.categoryForm.name = ''; // 清空类别名称
      },
      async createCategory() {
        if (!this.categoryForm.name || !this.categoryForm.name.trim()) {
          this.$message.warning('类别名称不能为空');
          return;
        }
        
        console.log('正在创建类别:', this.categoryForm.name);
        this.categoryLoading = true;
        
        try {
          const res = await axios.post('/api/category', { 
            name: this.categoryForm.name.trim() 
          });
          console.log('创建类别API响应:', res.data);
          
          if (res.data.status === 'success') {
            this.$message.success('类别添加成功');
            await this.fetchCategories(); // 刷新类别列表
            this.categoryDialogVisible = false;
            this.categoryForm.name = '';
          } else {
            console.error('创建类别失败:', res.data);
            this.$message.error('类别添加失败: ' + (res.data.message || '未知错误'));
          }
        } catch (e) {
          console.error('创建类别网络错误:', e);
          if (e.response) {
            console.error('错误响应:', e.response.data);
            this.$message.error('类别添加失败: ' + (e.response.data.detail || e.message));
          } else {
            this.$message.error('类别添加失败，请检查网络连接');
          }
        } finally {
          this.categoryLoading = false;
        }
      },
      // 新增获取细分项目方法
      async fetchMiniproducts() {
        try {
          console.log('正在获取细分项目列表...');
          const res = await axios.get('/api/miniproduct');
          console.log('细分项目API响应:', res.data);
          if (res.data.status === 'success') {
            this.miniproductOptions = res.data.data;
            console.log('细分项目列表:', this.miniproductOptions);
          } else {
            console.error('获取细分项目失败:', res.data);
            this.$message.error('获取细分项目失败: ' + (res.data.message || '未知错误'));
          }
        } catch (e) {
          console.error('获取细分项目网络错误:', e);
          if (e.response) {
            console.error('错误响应:', e.response.data);
            this.$message.error('获取细分项目失败: ' + (e.response.data.detail || e.message));
          } else {
            this.$message.error('获取细分项目失败，请检查网络连接');
          }
        }
      },
      openMiniproductDialog() {
        this.miniproductDialogVisible = true;
        this.miniproductForm.name = ''; // 清空细分项目名称
      },
      async createMiniproduct() {
        if (!this.miniproductForm.name || !this.miniproductForm.name.trim()) {
          this.$message.warning('细分项目名称不能为空');
          return;
        }
        
        console.log('正在创建细分项目:', this.miniproductForm.name);
        this.miniproductLoading = true;
        
        try {
          const res = await axios.post('/api/miniproduct', { 
            name: this.miniproductForm.name.trim() 
          });
          console.log('创建细分项目API响应:', res.data);
          
          if (res.data.status === 'success') {
            this.$message.success('细分项目添加成功');
            await this.fetchMiniproducts(); // 刷新细分项目列表
            this.miniproductDialogVisible = false;
            this.miniproductForm.name = '';
          } else {
            console.error('创建细分项目失败:', res.data);
            this.$message.error('细分项目添加失败: ' + (res.data.message || '未知错误'));
          }
        } catch (e) {
          console.error('创建细分项目网络错误:', e);
          if (e.response) {
            console.error('错误响应:', e.response.data);
            this.$message.error('细分项目添加失败: ' + (e.response.data.detail || e.message));
          } else {
            this.$message.error('细分项目添加失败，请检查网络连接');
          }
        } finally {
          this.miniproductLoading = false;
        }
      },
      // 权限控制方法
      initializeUserPermissions() {
        try {
          let currentUser = localStorage.getItem('savedUsername');
          if (!currentUser && this.$store?.state?.user?.username) {
            currentUser = this.$store.state.user.username;
            localStorage.setItem('savedUsername', currentUser);
          }
          this.currentUser = currentUser;
          this.isAdmin = currentUser === 'John' || currentUser === 'admin';
          console.log('用户权限初始化:', { currentUser, isAdmin: this.isAdmin });
        } catch (error) {
          console.error('用户权限初始化失败:', error);
          this.isAdmin = false;
          this.currentUser = null;
        }
      },
      checkUserPermissions() {
        if (!this.currentUser) {
          this.initializeUserPermissions();
        }
        return this.isAdmin;
      },
      // 文件下载方法
      downloadFile(fileUrl, fileName, row) {
        // 如果有fileUrl，使用原来的逻辑
        if (fileUrl) {
          try {
            let fullUrl;
            if (fileUrl.startsWith('/static/videos/')) {
              fullUrl = window.location.origin + '/api' + fileUrl;
            } else if (fileUrl.startsWith('/static')) {
              fullUrl = window.location.origin + '/api' + fileUrl;
            } else if (fileUrl.startsWith('/api/static')) {
              fullUrl = window.location.origin + fileUrl;
            } else {
              fullUrl = fileUrl.startsWith('http') ? fileUrl : window.location.origin + fileUrl;
            }
            
            console.log('准备下载文件:', { originalUrl: fileUrl, fullUrl, fileName });
            
            // 创建隐藏的下载链接
            const link = document.createElement('a');
            link.href = fullUrl;
            link.download = fileName || 'download';
            link.target = '_blank';
            link.style.display = 'none';
            
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
            
            this.$message.success('文件下载开始');
          } catch (error) {
            console.error('下载失败:', error);
            this.$message.error('文件下载失败: ' + error.message);
          }
        } else if (row && row.id) {
          // 使用新的下载API
          try {
            const downloadUrl = `/api/file/download/${row.id}`;
            const fullUrl = window.location.origin + downloadUrl;
            
            console.log('准备下载文件:', { fileId: row.id, downloadUrl: fullUrl, fileName: row.文件名称 });
            
            // 创建隐藏的下载链接
            const link = document.createElement('a');
            link.href = fullUrl;
            link.download = row.文件名称 || fileName || 'download';
            link.target = '_blank';
            link.style.display = 'none';
            
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
            
            this.$message.success('文件下载开始');
          } catch (error) {
            console.error('下载失败:', error);
            this.$message.error('文件下载失败: ' + error.message);
          }
        } else {
          this.$message.warning('文件地址不存在');
        }
      },
      downloadCurrentFile() {
        if (this.previewUrl) {
          try {
            let fullUrl;
            if (this.previewUrl.startsWith('/static/videos/')) {
              fullUrl = window.location.origin + '/api' + this.previewUrl;
            } else if (this.previewUrl.startsWith('/static')) {
              fullUrl = window.location.origin + '/api' + this.previewUrl;
            } else if (this.previewUrl.startsWith('/api/static')) {
              fullUrl = window.location.origin + this.previewUrl;
            } else {
              fullUrl = this.previewUrl.startsWith('http') ? this.previewUrl : window.location.origin + this.previewUrl;
            }
            
            console.log('准备下载当前文件:', { originalUrl: this.previewUrl, fullUrl, fileName: this.previewFileName });
            
            // 创建隐藏的下载链接
            const link = document.createElement('a');
            link.href = fullUrl;
            link.download = this.previewFileName || 'download';
            link.target = '_blank';
            link.style.display = 'none';
            
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
            
            this.$message.success('文件下载开始');
          } catch (error) {
            console.error('下载失败:', error);
            this.$message.error('文件下载失败: ' + error.message);
          }
        } else {
          this.$message.warning('文件地址不存在');
        }
      },
      // PPT预览方法
      async loadPptxPreview(fileUrl) {
        if (!this.$refs.pptxContainer) {
          console.error('PPT容器未找到');
          return;
        }
        
        this.pptxLoading = true;
        this.pptxError = null;
        
        try {
          // 初始化PPTX预览器
          this.pptxPreviewer = init(this.$refs.pptxContainer, {
            width: 960,
            height: 540
          });
          
          // 获取文件的ArrayBuffer数据
          const response = await fetch(fileUrl);
          if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
          }
          
          const arrayBuffer = await response.arrayBuffer();
          
          // 调用预览器的preview方法
          await this.pptxPreviewer.preview(arrayBuffer);
          
          this.pptxLoading = false;
        } catch (error) {
          console.error('PPT预览失败:', error);
          this.pptxError = error.message || '预览失败，请稍后重试';
          this.pptxLoading = false;
        }
      }
    }
  };
  </script>
  
  <style scoped>
  .mb-4{margin-bottom:20px}.card-title{font-size:16px;font-weight:bold}.form-actions{display:flex;margin-top:20px;gap: 10px;}.no-data{text-align:center;padding:30px 0;color:#909399;font-size:14px}
  .ppt-preview {
    height: 80vh;
    background-color: #f5f7fa;
    border-radius: 4px;
    padding: 20px;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
  }

  .ppt-loading {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    text-align: center;
    color: #606266;
  }

  .ppt-loading p {
    margin-top: 10px;
    font-size: 14px;
  }

  .loading-spinner {
    width: 40px;
    height: 40px;
    border: 4px solid #e4e7ed;
    border-top: 4px solid #409eff;
    border-radius: 50%;
    animation: spin 1s linear infinite;
  }

  @keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
  }

  .ppt-error {
    text-align: center;
    color: #f56c6c;
  }

  .ppt-error p {
    margin-bottom: 15px;
    font-size: 14px;
  }

  .pptx-container {
    width: 80%;
    height: 80%;
    min-height: 500px;
    background-color: #fff;
    border-radius: 4px;
    border: 1px solid #dcdfe6;
    overflow: hidden;
  }

  .other-file-preview {
    display: flex;
    justify-content: center;
    align-items: center;
    height: 80vh;
    background-color: #f5f7fa;
    border-radius: 4px;
    padding: 20px;
  }

  .file-info {
    text-align: center;
    color: #606266;
  }

  .file-info h3 {
    color: #303133;
    margin-bottom: 10px;
  }

  .file-info p {
    margin-bottom: 10px;
    font-size: 14px;
  }
  </style>
  