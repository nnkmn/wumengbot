# 舞萌Bot

一个基于maimai.py开发的舞萌数据查询工具，包含完整的后端服务和前端界面，用于个人及朋友使用。

## 功能特性

- **玩家查询**：查询舞萌玩家的基本信息，支持水鱼和落雪查分器
- **成绩查询**：查看玩家的成绩列表、Rating和b15成绩
- **歌曲查询**：搜索和查看舞萌歌曲的详细信息
- **牌子进度**：查看玩家的舞将、舞霸等牌子完成进度
- **Segamaid绑定**：绑定Segamaid账号，获取更多舞萌数据
- **数据存储**：使用SQLite数据库存储玩家数据和成绩信息
- **自动爬虫**：定期爬取舞萌相关数据并更新到数据库

## 技术栈

### 后端
- Python 3.10+
- FastAPI
- maimai.py
- SQLAlchemy (ORM框架)
- SQLite (数据库)
- Celery (任务队列，当前临时禁用)
- Redis (消息代理，当前临时禁用)

### 前端
- Vue 3
- Vite
- Element Plus
- Axios

## 项目结构

```
wumengbot/
├── backend/              # 后端服务
│   ├── app/              # 应用代码
│   │   ├── api/          # API路由
│   │   ├── core/         # 核心配置
│   │   ├── models/       # 数据库模型
│   │   ├── services/     # 业务逻辑
│   │   ├── spiders/      # 爬虫代码
│   │   └── main.py       # 应用入口
│   ├── requirements.txt  # 依赖列表
│   └── .env.example      # 环境变量示例
├── frontend/             # 前端界面
│   ├── public/           # 静态资源
│   ├── src/              # 源代码
│   │   ├── api/          # API请求
│   │   ├── components/   # 组件
│   │   ├── views/        # 页面
│   │   ├── router/       # 路由
│   │   └── App.vue       # 应用入口
│   ├── package.json      # 依赖配置
│   └── vite.config.js    # Vite配置
└── README.md             # 项目说明
```

## 快速开始

### 后端部署

1. 进入后端目录
   ```bash
   cd backend
   ```

2. 安装依赖
   ```bash
   pip install -r requirements.txt
   ```

3. 配置环境变量
   ```bash
   cp .env.example .env
   # 编辑.env文件，填写必要的配置信息
   ```

4. 启动后端服务
   ```bash
   uvicorn app.main:app --reload
   ```

   后端服务将运行在 http://localhost:8000

### 前端部署

1. 进入前端目录
   ```bash
   cd frontend
   ```

2. 安装依赖
   ```bash
   npm install
   ```

3. 启动前端开发服务器
   ```bash
   npm run dev
   ```

   前端服务将运行在 http://localhost:5174（端口可能会根据系统情况自动调整）

## API文档

后端服务启动后，可以通过以下地址访问API文档：
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 注意事项

1. 严格遵循maimai.py的使用规范，特别是全局单例MaimaiClient的创建
2. 确保在.env文件中正确配置了水鱼和落雪的API令牌
3. 前端开发服务器已配置代理，将/api请求转发到后端服务
4. 项目使用了异步编程，确保所有异步方法都使用了await关键字
5. 所有API端点都已添加了错误处理，返回友好的错误信息
6. Segamaid绑定功能需要正确配置Segamaid API相关参数
7. 数据库使用SQLite，默认存储在backend/app/db目录下
8. 爬虫系统当前直接运行，后续将支持Celery任务队列
9. 首次运行时会自动创建数据库表结构

## 许可证

MIT
