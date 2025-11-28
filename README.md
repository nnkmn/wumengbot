# 舞萌Bot

一个基于maimai.py开发的舞萌数据查询工具，包含完整的后端服务和前端界面，用于个人及朋友使用。

## 功能特性

- **玩家查询**：查询舞萌玩家的基本信息，支持水鱼和落雪查分器
- **成绩查询**：查看玩家的成绩列表、Rating和b15成绩
- **歌曲查询**：搜索和查看舞萌歌曲的详细信息
- **牌子进度**：查看玩家的舞将、舞霸等牌子完成进度

## 技术栈

### 后端
- Python 3.10+
- FastAPI
- maimai.py

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
│   ├── requirements.txt  # 依赖列表
│   └── .env.example      # 环境变量示例
├── frontend/             # 前端界面
│   ├── public/           # 静态资源
│   ├── src/              # 源代码
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

## 许可证

MIT
