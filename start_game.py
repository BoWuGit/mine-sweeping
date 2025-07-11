#!/usr/bin/env python3
"""
扫雷游戏启动脚本
同时启动后端API服务和前端Web服务器
"""

import subprocess
import sys
import time
from pathlib import Path

def check_dependencies():
    """检查必要的依赖是否安装"""
    try:
        import uvicorn
        print("✓ uvicorn 已安装")
    except ImportError:
        print("❌ uvicorn 未安装，请运行: pip install uvicorn")
        return False
    
    try:
        import fastapi
        print("✓ fastapi 已安装")
    except ImportError:
        print("❌ fastapi 未安装，请运行: pip install fastapi")
        return False
    
    return True

def start_backend():
    """启动后端服务"""
    print("🚀 启动后端API服务...")
    backend_dir = Path("backend")
    if not backend_dir.exists():
        print("❌ 后端目录不存在")
        return None
    
    try:
        # 切换到后端目录并启动服务
        process = subprocess.Popen(
            [sys.executable, "-m", "uvicorn", "app.main:app", "--reload", "--host", "0.0.0.0", "--port", "8000"],
            cwd=backend_dir,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        print("✓ 后端服务已启动在 http://localhost:8000")
        return process
    except Exception as e:
        print(f"❌ 启动后端服务失败: {e}")
        return None

def start_frontend():
    """启动前端服务"""
    print("🌐 启动前端Web服务...")
    frontend_dir = Path("frontend")
    if not frontend_dir.exists():
        print("❌ 前端目录不存在")
        return None
    
    try:
        # 启动Python内置HTTP服务器
        process = subprocess.Popen(
            [sys.executable, "-m", "http.server", "8001"],
            cwd=frontend_dir,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        print("✓ 前端服务已启动在 http://localhost:8001")
        return process
    except Exception as e:
        print(f"❌ 启动前端服务失败: {e}")
        return None

def wait_for_backend():
    """等待后端服务启动"""
    import requests
    max_attempts = 30
    for i in range(max_attempts):
        try:
            response = requests.get("http://localhost:8000/game/health", timeout=1)
            if response.status_code == 200:
                print("✓ 后端服务已就绪")
                return True
        except:
            pass
        time.sleep(1)
        if i % 5 == 0:
            print(f"⏳ 等待后端服务启动... ({i+1}/{max_attempts})")
    
    print("❌ 后端服务启动超时")
    return False

def main():
    """主函数"""
    print("🎮 扫雷游戏启动器")
    print("=" * 50)
    
    # 检查依赖
    if not check_dependencies():
        print("\n请先安装必要的依赖:")
        print("pip install fastapi uvicorn requests")
        return
    
    print("\n📋 启动检查:")
    print("✓ 后端API服务: http://localhost:8000")
    print("✓ 前端Web界面: http://localhost:8001")
    print("✓ 音效测试页面: http://localhost:8001/test_sounds.html")
    print("✓ API文档: http://localhost:8000/docs")
    
    # 启动服务
    backend_process = start_backend()
    if not backend_process:
        return
    
    # 等待后端启动
    if not wait_for_backend():
        backend_process.terminate()
        return
    
    frontend_process = start_frontend()
    if not frontend_process:
        backend_process.terminate()
        return
    
    print("\n🎉 所有服务已启动!")
    print("\n📱 在浏览器中访问:")
    print("   🎮 游戏界面: http://localhost:8001")
    print("   🎵 音效测试: http://localhost:8001/test_sounds.html")
    print("   📚 API文档: http://localhost:8000/docs")
    print("\n💡 提示:")
    print("   - 按 Ctrl+C 停止所有服务")
    print("   - 游戏支持键盘快捷键: R(重启), N(新游戏)")
    print("   - 右键点击可以标记地雷")
    
    try:
        # 等待用户中断
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n\n🛑 正在停止服务...")
        
        # 停止服务
        if backend_process:
            backend_process.terminate()
            print("✓ 后端服务已停止")
        
        if frontend_process:
            frontend_process.terminate()
            print("✓ 前端服务已停止")
        
        print("👋 再见!")

if __name__ == "__main__":
    main() 