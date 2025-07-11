# Minesweeper Game Backend

基于FastAPI的扫雷游戏后端服务，提供完整的REST API接口。

## 功能特性

- 🎮 完整的扫雷游戏逻辑
- 🚀 FastAPI高性能API服务
- 🔧 可配置的游戏难度和棋盘尺寸
- 🧪 完整的单元测试覆盖
- 📚 自动生成的API文档
- 🤖 支持Agent和MCP集成
- 🔄 多游戏实例管理

## 技术栈

- **Python**: 3.10+
- **FastAPI**: 现代、快速的Web框架
- **Pydantic**: 数据验证和序列化
- **pytest**: 单元测试框架
- **uvicorn**: ASGI服务器

## 安装和运行

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 运行服务

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 3. 访问API文档

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## API端点

### 游戏管理

- `POST /game/new` - 创建新游戏
- `GET /game/{game_id}` - 获取游戏状态
- `DELETE /game/{game_id}` - 删除游戏
- `POST /game/{game_id}/restart` - 重启游戏

### 游戏操作

- `POST /game/{game_id}/reveal` - 揭开格子
- `POST /game/{game_id}/flag` - 标记地雷

### 系统信息

- `GET /` - API根信息
- `GET /info` - 详细API信息
- `GET /game/health` - 健康检查
- `GET /game/` - 列出所有游戏

## 游戏难度

### 预设难度

- **Easy**: 10x10 棋盘，10个地雷
- **Medium**: 16x16 棋盘，40个地雷
- **Hard**: 16x30 棋盘，99个地雷

### 自定义难度

可以指定任意棋盘尺寸和地雷数量（在合理范围内）。

## 数据模型

### 游戏状态

```python
class GameState:
    game_id: str
    width: int
    height: int
    mine_count: int
    revealed_count: int
    flagged_count: int
    status: GameStatus
    board: List[List[Cell]]
    created_at: datetime
    last_updated: datetime
```

### 格子状态

```python
class Cell:
    x: int
    y: int
    state: CellState  # hidden, revealed, flagged, exploded
    is_mine: bool
    neighbor_mines: int
    is_revealed: bool
```

## 运行测试

```bash
# 运行所有测试
pytest tests/

# 运行特定测试文件
pytest tests/test_game_logic.py
pytest tests/test_api.py

# 运行测试并显示覆盖率
pytest tests/ --cov=app --cov-report=html
```

## 开发指南

### 代码结构

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py          # FastAPI应用入口
│   ├── models.py        # 数据模型定义
│   ├── game_logic.py    # 游戏核心逻辑
│   └── api.py           # API路由定义
├── tests/
│   ├── __init__.py
│   ├── test_game_logic.py  # 游戏逻辑测试
│   └── test_api.py         # API端点测试
├── requirements.txt     # Python依赖
└── README.md           # 本文档
```

### 添加新功能

1. 在 `models.py` 中定义数据模型
2. 在 `game_logic.py` 中实现业务逻辑
3. 在 `api.py` 中添加API端点
4. 在 `tests/` 中编写测试用例

### 代码规范

- 遵循PEP 8代码规范
- 使用类型注解
- 编写详细的文档字符串
- 保持测试覆盖率

## 部署

### 生产环境

```bash
# 使用gunicorn部署
pip install gunicorn
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

### Docker部署

```dockerfile
FROM python:3.10-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

## 性能优化

- 使用内存存储游戏状态（适合中小规模部署）
- 支持多游戏实例并发
- 自动清理过期游戏
- 异步API处理

## 扩展功能

### 数据库集成

可以轻松集成PostgreSQL、Redis等数据库来持久化游戏状态。

### 用户认证

可以添加JWT认证来支持多用户游戏。

### WebSocket支持

可以添加实时游戏状态更新。

## 许可证

MIT License 