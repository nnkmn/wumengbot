# 舞萌Bot

一个基于maimai.py开发的舞萌数据查询工具，包含完整的后端服务和前端界面，用于个人及朋友使用。

## 功能特性

### 1. 玩家查询
- 查询舞萌玩家的基本信息，包括昵称、ID、Rating等
- 支持水鱼和落雪查分器
- 提供玩家信息的详细展示

### 2. 成绩查询
- 查看玩家的成绩列表
- 支持按难度、等级等条件筛选
- 展示玩家的Rating和b15成绩
- 提供成绩的详细数据分析

### 3. 歌曲查询
- 搜索和查看舞萌歌曲的详细信息
- 支持按歌曲名称、艺术家、难度等条件搜索
- 展示歌曲的谱面信息、BPM、时长等
- 提供歌曲的封面图片展示

### 4. 牌子进度
- 查看玩家的舞将、舞霸等牌子完成进度
- 展示各个牌子的获取条件和当前进度
- 提供牌子进度的可视化展示

### 5. Segamaid绑定
- 绑定Segamaid账号，获取更多舞萌数据
- 支持Segamaid Token的验证和绑定
- 提供绑定状态的查询和管理

### 6. 数据存储
- 使用SQLite数据库存储玩家数据和成绩信息
- 支持数据的持久化存储
- 提供数据的查询和管理功能

### 7. 自动爬虫
- 定期爬取舞萌相关数据并更新到数据库
- 支持多种数据源的爬取
- 提供爬虫任务的管理和监控

## 技术栈

### 后端
| 技术 | 版本 | 用途 |
| --- | --- | --- |
| Python | 3.10+ | 后端开发语言 |
| FastAPI | 0.100+ | API框架 |
| maimai.py | 最新版 | 舞萌数据处理库 |
| SQLAlchemy | 2.0+ | ORM框架，用于数据库操作 |
| SQLite | 3.0+ | 轻量级数据库，用于数据存储 |
| Celery | 5.0+ | 任务队列，用于异步任务处理（当前临时禁用） |
| Redis | 7.0+ | 消息代理，用于Celery任务队列（当前临时禁用） |
| Pydantic | 2.0+ | 数据验证和序列化 |
| python-dotenv | 1.0+ | 环境变量管理 |

### 前端
| 技术 | 版本 | 用途 |
| --- | --- | --- |
| Vue | 3.3+ | 前端框架 |
| Vite | 5.0+ | 构建工具 |
| Element Plus | 2.3+ | UI组件库 |
| Axios | 1.5+ | HTTP客户端，用于API请求 |
| Vue Router | 4.2+ | 路由管理 |

## 项目结构

```
wumengbot/
├── backend/              # 后端服务
│   ├── app/              # 应用代码
│   │   ├── api/          # API路由
│   │   │   ├── __init__.py     # API路由初始化
│   │   │   ├── players.py      # 玩家相关API
│   │   │   ├── scores.py       # 成绩相关API
│   │   │   ├── songs.py        # 歌曲相关API
│   │   │   ├── plates.py       # 牌子相关API
│   │   │   ├── segamaid.py     # Segamaid绑定API
│   │   │   ├── spiders.py      # 爬虫管理API
│   │   │   └── search.py       # 数据查询API
│   │   ├── core/         # 核心配置
│   │   │   ├── __init__.py     # 核心配置初始化
│   │   │   ├── config.py       # 配置管理
│   │   │   ├── database.py     # 数据库连接
│   │   │   ├── db_utils.py     # 数据库工具函数
│   │   │   └── celery.py       # Celery配置
│   │   ├── models/       # 数据库模型
│   │   │   ├── __init__.py     # 模型初始化
│   │   │   ├── user_segamaid.py    # 用户-Segamaid绑定模型
│   │   │   └── crawled_data.py     # 爬取数据模型
│   │   ├── services/     # 业务逻辑
│   │   │   ├── __init__.py     # 服务初始化
│   │   │   ├── player_service.py   # 玩家服务
│   │   │   ├── score_service.py    # 成绩服务
│   │   │   └── segamaid_service.py # Segamaid服务
│   │   ├── spiders/      # 爬虫代码
│   │   │   ├── __init__.py     # 爬虫初始化
│   │   │   ├── base_spider.py      # 基础爬虫类
│   │   │   ├── spider_manager.py   # 爬虫管理器
│   │   │   ├── wi_spider.py        # 舞萌Web爬虫
│   │   │   └── processors/         # 数据处理器
│   │   │       ├── __init__.py     # 处理器初始化
│   │   │       └── data_processor.py # 数据处理逻辑
│   │   └── main.py       # 应用入口
│   ├── requirements.txt  # 依赖列表
│   └── .env.example      # 环境变量示例
├── frontend/             # 前端界面
│   ├── public/           # 静态资源
│   │   ├── favicon.ico   # 网站图标
│   │   └── robots.txt    # 爬虫协议
│   ├── src/              # 源代码
│   │   ├── api/          # API请求
│   │   │   └── index.js  # API接口定义
│   │   ├── components/   # 组件
│   │   │   └── MaimaiIcon.vue  # 舞萌图标组件
│   │   ├── views/        # 页面
│   │   │   ├── HomeView.vue      # 首页
│   │   │   ├── PlayerView.vue    # 玩家查询页
│   │   │   ├── ScoresView.vue    # 成绩查询页
│   │   │   ├── SongsView.vue     # 歌曲查询页
│   │   │   ├── PlatesView.vue    # 牌子进度页
│   │   │   └── SegamaidView.vue  # Segamaid绑定页
│   │   ├── router/       # 路由
│   │   │   └── index.js  # 路由配置
│   │   ├── App.vue       # 应用入口组件
│   │   └── main.js       # 应用初始化
│   ├── package.json      # 依赖配置
│   ├── vite.config.js    # Vite配置
│   └── index.html        # HTML模板
└── README.md             # 项目说明
```

## 快速开始

### 后端部署

#### 1. 环境准备
- 安装Python 3.10+：https://www.python.org/downloads/
- 安装pip：Python包管理工具

#### 2. 安装依赖
```bash
# 进入后端目录
cd backend

# 安装依赖
pip install -r requirements.txt
```

#### 3. 配置环境变量
```bash
# 复制环境变量示例文件
cp .env.example .env

# 编辑.env文件，填写必要的配置信息
# 可以使用文本编辑器打开.env文件进行编辑
```

#### 4. 启动后端服务
```bash
# 开发模式启动（带热重载）
uvicorn app.main:app --reload

# 生产模式启动
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

后端服务将运行在 http://localhost:8000

### 前端部署

#### 1. 环境准备
- 安装Node.js 16+：https://nodejs.org/en/download/
- 安装npm：Node.js包管理工具

#### 2. 安装依赖
```bash
# 进入前端目录
cd frontend

# 安装依赖
npm install
```

#### 3. 启动前端开发服务器
```bash
# 启动开发服务器
npm run dev
```

前端服务将运行在 http://localhost:5174（端口可能会根据系统情况自动调整）

#### 4. 构建生产版本
```bash
# 构建生产版本
npm run build

# 预览生产版本
npm run preview
```

## API文档

后端服务启动后，可以通过以下地址访问API文档：

### Swagger UI
- 地址：http://localhost:8000/docs
- 特点：交互式API文档，支持在线测试API
- 用途：开发和测试API

### ReDoc
- 地址：http://localhost:8000/redoc
- 特点：结构化API文档，更适合阅读
- 用途：查看和理解API结构

## 数据库设计

### 1. 用户-Segamaid绑定表（user_segamaid）
| 字段名 | 类型 | 约束 | 描述 |
| --- | --- | --- | --- |
| id | Integer | PRIMARY KEY, AUTOINCREMENT | 主键ID |
| player_id | String | NOT NULL, UNIQUE | 玩家ID |
| segamaid_id | String | NOT NULL | Segamaid ID |
| segamaid_token | String | NOT NULL | Segamaid Token |
| created_at | DateTime | NOT NULL, DEFAULT CURRENT_TIMESTAMP | 创建时间 |
| updated_at | DateTime | NOT NULL, DEFAULT CURRENT_TIMESTAMP | 更新时间 |

### 2. 爬取数据表（crawled_data）
| 字段名 | 类型 | 约束 | 描述 |
| --- | --- | --- | --- |
| id | Integer | PRIMARY KEY, AUTOINCREMENT | 主键ID |
| data_type | String | NOT NULL | 数据类型（player, song, score等） |
| data_id | String | NOT NULL | 数据ID |
| data_content | JSON | NOT NULL | 数据内容（JSON格式） |
| source | String | NOT NULL | 数据源 |
| crawled_at | DateTime | NOT NULL, DEFAULT CURRENT_TIMESTAMP | 爬取时间 |
| updated_at | DateTime | NOT NULL, DEFAULT CURRENT_TIMESTAMP | 更新时间 |

## 环境变量配置

### 后端环境变量
| 变量名 | 类型 | 默认值 | 描述 |
| --- | --- | --- | --- |
| API_V1_STR | String | /api | API前缀 |
| PROJECT_NAME | String | 舞萌Bot | 项目名称 |
| BACKEND_CORS_ORIGINS | List | ["*"] | 允许的跨域来源 |
| DATABASE_URL | String | sqlite:///./app/db/wumengbot.db | 数据库连接URL |
| SECRET_KEY | String | 随机生成 | JWT密钥 |
| ACCESS_TOKEN_EXPIRE_MINUTES | Integer | 30 | 访问令牌过期时间（分钟） |
| SPIDER_ENABLED | Boolean | True | 是否启用爬虫 |
| SPIDER_INTERVAL | Integer | 3600 | 爬虫运行间隔（秒） |
| SEGAMAID_API_URL | String | https://api.segamaid.com | Segamaid API地址 |

### 前端环境变量
| 变量名 | 类型 | 默认值 | 描述 |
| --- | --- | --- | --- |
| VITE_API_BASE_URL | String | /api | API基础URL |
| VITE_APP_TITLE | String | 舞萌Bot | 应用标题 |

## 注意事项

1. **maimai.py使用规范**：
   - 严格遵循maimai.py的使用规范，特别是全局单例MaimaiClient的创建
   - 避免频繁创建MaimaiClient实例，以提高性能

2. **API令牌配置**：
   - 确保在.env文件中正确配置了水鱼和落雪的API令牌
   - 这些令牌是访问第三方API的必要凭证

3. **前端代理配置**：
   - 前端开发服务器已配置代理，将/api请求转发到后端服务
   - 生产环境中需要配置Nginx或其他反向代理服务器

4. **异步编程**：
   - 项目使用了异步编程，确保所有异步方法都使用了await关键字
   - 避免在异步方法中使用同步阻塞操作

5. **错误处理**：
   - 所有API端点都已添加了错误处理，返回友好的错误信息
   - 开发过程中注意捕获和处理异常

6. **Segamaid绑定**：
   - Segamaid绑定功能需要正确配置Segamaid API相关参数
   - 确保Segamaid Token的安全性，避免泄露

7. **数据库管理**：
   - 数据库使用SQLite，默认存储在backend/app/db目录下
   - 定期备份数据库文件，以防止数据丢失

8. **爬虫系统**：
   - 爬虫系统当前直接运行，后续将支持Celery任务队列
   - 避免频繁运行爬虫，以减轻第三方服务器的负担

9. **首次运行**：
   - 首次运行时会自动创建数据库表结构
   - 无需手动创建数据库表

10. **性能优化**：
    - 对于大量数据的查询，考虑添加索引以提高查询性能
    - 避免在循环中执行数据库查询操作

## 开发指南

### 代码规范

#### 后端
- 遵循PEP 8代码规范
- 使用Black进行代码格式化
- 使用Flake8进行代码检查
- 使用mypy进行类型检查

#### 前端
- 遵循Vue 3代码规范
- 使用ESLint进行代码检查
- 使用Prettier进行代码格式化

### 测试

#### 后端
```bash
# 运行单元测试
pytest

# 运行覆盖率测试
pytest --cov=app
```

#### 前端
```bash
# 运行单元测试
npm run test

# 运行E2E测试
npm run test:e2e
```

### 部署

#### 后端部署
```bash
# 构建Docker镜像
docker build -t wumengbot-backend .

# 运行Docker容器
docker run -d -p 8000:8000 --name wumengbot-backend wumengbot-backend
```

#### 前端部署
```bash
# 构建生产版本
npm run build

# 部署到Nginx
cp -r dist/* /usr/share/nginx/html/
```

## 许可证

MIT License

Copyright (c) 2024 舞萌Bot

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

## 贡献

欢迎提交Issue和Pull Request！

### 提交Pull Request的流程
1. Fork本仓库
2. 创建你的特性分支：`git checkout -b feature/AmazingFeature`
3. 提交你的修改：`git commit -m 'Add some AmazingFeature'`
4. 推送到分支：`git push origin feature/AmazingFeature`
5. 打开一个Pull Request

### 提交Issue的流程
1. 确保你使用的是最新版本
2. 检查是否已经存在类似的Issue
3. 提供详细的问题描述和复现步骤
4. 提供相关的错误信息和日志
5. 提供你的环境信息（操作系统、Python版本等）

## 联系方式

- 项目地址：https://github.com/nnkmn/wumengbot
- 作者：nnkmn
- 邮箱：your-email@example.com

## 更新日志

### v1.0.0 (2024-01-01)
- 初始版本发布
- 实现了玩家查询、成绩查询、歌曲查询、牌子进度等功能
- 实现了Segamaid绑定功能
- 实现了数据存储和自动爬虫系统
- 完成了前端界面的开发

## 致谢

- [maimai.py](https://github.com/Diving-Fish/maimai.py)：舞萌数据处理库
- [FastAPI](https://fastapi.tiangolo.com/)：现代化的API框架
- [Vue 3](https://vuejs.org/)：渐进式JavaScript框架
- [Element Plus](https://element-plus.org/)：基于Vue 3的UI组件库
- 所有为舞萌社区做出贡献的开发者和玩家
