# Minesweeper Game Frontend

现代化的扫雷游戏前端界面，基于HTML5、CSS3和JavaScript构建。

## 功能特性

- 🎮 完整的扫雷游戏界面
- 🎨 现代化、响应式设计
- 🎵 音效支持（揭开、标记、爆炸、胜利）
- 📱 移动设备友好
- ⌨️ 键盘快捷键支持
- 🌙 深色模式支持
- ♿ 无障碍访问支持

## 技术栈

- **HTML5**: 语义化标记
- **CSS3**: 现代样式，包括Grid、Flexbox、动画
- **JavaScript (ES6+)**: 现代JavaScript特性
- **Font Awesome**: 图标库
- **Google Fonts**: Inter字体

## 快速开始

### 1. 启动后端服务

确保后端FastAPI服务正在运行：

```bash
cd backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 2. 启动前端

使用任何HTTP服务器启动前端：

```bash
cd frontend
python -m http.server 8001
```

或者使用Node.js：

```bash
cd frontend
npx http-server -p 8001
```

### 3. 访问游戏

在浏览器中访问：http://localhost:8001

## 游戏操作

### 鼠标操作

- **左键点击**: 揭开格子
- **右键点击**: 标记/取消标记地雷

### 键盘快捷键

- **N**: 开始新游戏
- **R**: 重新开始当前游戏

## 游戏难度

### 预设难度

- **简单**: 10x10 棋盘，10个地雷
- **中等**: 16x16 棋盘，40个地雷
- **困难**: 16x30 棋盘，99个地雷

### 自定义难度

可以设置任意棋盘尺寸（5-50）和地雷数量。

## 界面特性

### 响应式设计

- 桌面端：完整功能界面
- 平板端：优化的触摸体验
- 移动端：紧凑布局，适合小屏幕

### 视觉反馈

- 悬停效果
- 点击动画
- 爆炸动画
- 加载动画

### 音效系统

- 揭开格子音效
- 标记地雷音效
- 爆炸音效
- 胜利音效

### 无障碍支持

- 键盘导航
- 高对比度模式
- 减少动画模式
- 语义化HTML

## 文件结构

```
frontend/
├── index.html          # 主HTML文件
├── styles.css          # 样式文件
├── script.js           # 游戏逻辑
├── assets/             # 资源文件
│   ├── reveal.mp3      # 揭开音效
│   ├── flag.mp3        # 标记音效
│   ├── explosion.mp3   # 爆炸音效
│   └── victory.mp3     # 胜利音效
└── README.md           # 本文档
```

## 自定义配置

### 修改API地址

在 `script.js` 中修改 `apiBaseUrl`：

```javascript
this.apiBaseUrl = 'http://your-api-server:8000';
```

### 自定义样式

修改 `styles.css` 中的CSS变量：

```css
:root {
    --primary-color: #667eea;
    --secondary-color: #764ba2;
    --success-color: #38a169;
    --danger-color: #e53e3e;
}
```

### 添加新音效

1. 将音效文件放入 `assets/` 目录
2. 在 `index.html` 中添加音频元素
3. 在 `script.js` 中更新 `playSound` 方法

## 浏览器兼容性

- Chrome 60+
- Firefox 55+
- Safari 12+
- Edge 79+

## 性能优化

- 使用CSS Grid进行布局
- 事件委托减少事件监听器
- 音频预加载
- 图片和资源优化

## 开发指南

### 添加新功能

1. 在HTML中添加UI元素
2. 在CSS中添加样式
3. 在JavaScript中添加逻辑
4. 更新事件处理

### 调试

打开浏览器开发者工具，游戏实例可通过 `window.minesweeperGame` 访问。

### 测试

- 测试不同屏幕尺寸
- 测试不同浏览器
- 测试无障碍功能
- 测试网络连接问题

## 部署

### 静态文件部署

将 `frontend/` 目录内容部署到任何静态文件服务器：

- Nginx
- Apache
- CDN服务
- GitHub Pages

### 生产环境优化

1. 压缩CSS和JavaScript
2. 优化图片和音效
3. 启用Gzip压缩
4. 设置缓存头

## 故障排除

### 常见问题

1. **无法连接到后端**
   - 检查后端服务是否运行
   - 检查API地址配置
   - 检查CORS设置

2. **音效不播放**
   - 检查浏览器音频权限
   - 检查音效文件是否存在
   - 检查音频格式支持

3. **界面显示异常**
   - 检查CSS文件是否正确加载
   - 检查浏览器兼容性
   - 清除浏览器缓存

## 许可证

MIT License 