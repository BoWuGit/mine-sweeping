# 扫雷游戏 (Minesweeper Game)

一个基于Web的扫雷游戏，包含前端界面和后端API服务。

## 功能特性

- 🎮 完整的扫雷游戏逻辑
- 🌐 现代化的Web界面
- 🎵 内置音效系统（点击、爆炸、胜利等）
- 🔧 可配置的游戏难度和棋盘尺寸
- 🧪 完整的单元测试
- 🚀 FastAPI后端服务
- 🤖 支持Agent和MCP集成

## 项目结构

```
mine_sweeping/
├── backend/                 # 后端FastAPI服务
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py         # FastAPI应用入口
│   │   ├── models.py       # 数据模型
│   │   ├── game_logic.py   # 游戏逻辑
│   │   └── api.py          # API路由
│   ├── tests/              # 单元测试
│   ├── requirements.txt    # Python依赖
│   └── README.md
├── frontend/               # 前端Web界面
│   ├── index.html
│   ├── styles.css
│   ├── script.js
│   ├── sounds.js          # 内置音效文件
│   ├── test_sounds.html   # 音效测试页面
│   ├── assets/            # 图标资源
│   └── README.md
└── README.md              # 项目总览
```

## 快速开始

### 一键启动（推荐）

使用项目提供的启动脚本，同时启动后端和前端服务：

```bash
python start_game.py
```

这将自动：
- 检查依赖是否安装
- 启动后端API服务 (http://localhost:8000)
- 启动前端Web服务 (http://localhost:8001)
- 显示访问链接和提示信息

### 手动启动

#### 后端服务

1. 进入后端目录：
```bash
cd backend
```

2. 安装依赖：
```bash
pip install -r requirements.txt
```

3. 运行服务：
```bash
uvicorn app.main:app --reload
```

服务将在 http://localhost:8000 启动

#### 前端界面

1. 进入前端目录：
```bash
cd frontend
```

2. 使用任何HTTP服务器启动（如Python内置服务器）：
```bash
python -m http.server 8001
```

3. 在浏览器中访问 http://localhost:8001

### 音效测试

项目包含内置的音效系统，您可以访问 http://localhost:8001/test_sounds.html 来测试各种音效：

- 🖱️ 点击音效：揭开格子时播放
- 🔔 蜂鸣音效：标记地雷时播放  
- 💥 爆炸音效：踩到地雷时播放
- 🎉 胜利音效：游戏获胜时播放

### Favicon 预览

项目包含自定义的炸弹主题favicon，您可以访问 http://localhost:8001/preview_favicon.html 来预览：

- 🎨 ICO格式：多尺寸支持，216 bytes
- 🖼️ PNG格式：32x32像素，295 bytes  
- 📐 SVG格式：矢量图形，533 bytes

### 自定义难度

在自定义难度模式下：
- 最小宽度和高度：5格
- 最大宽度和高度：50格
- 地雷数：最小1个，最大为(宽度×高度-1)

## API文档

启动后端服务后，访问 http://localhost:8000/docs 查看完整的API文档。

### 主要API端点

- `POST /game/new` - 创建新游戏
- `GET /game/{game_id}` - 获取游戏状态
- `POST /game/{game_id}/reveal` - 揭开格子
- `POST /game/{game_id}/flag` - 标记地雷

## 游戏规则

1. 点击格子揭开它
2. 数字表示周围8个格子中地雷的数量
3. 右键点击可以标记可疑的地雷位置
4. 揭开所有非地雷格子即可获胜
5. 踩到地雷游戏结束

## 技术栈

- **后端**: Python 3.10, FastAPI, Pydantic
- **前端**: HTML5, CSS3, JavaScript (ES6+)
- **测试**: pytest
- **部署**: uvicorn

## 开发

### 运行测试

```bash
cd backend
pytest tests/
```

### 代码质量

项目遵循PEP 8代码规范，包含完整的类型注解。

## 许可证

MIT License 