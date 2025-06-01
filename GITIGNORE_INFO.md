# .gitignore 说明文档

## 📋 概览

这个 `.gitignore` 文件为 Norma ORM 项目提供了全面的文件忽略规则，确保不必要的文件不会被 Git 版本控制系统跟踪。

## 🗂️ 被忽略的文件类型

### Python 相关
- 📁 `__pycache__/` - Python 字节码缓存目录
- 📄 `*.pyc`, `*.pyo`, `*.pyd` - 编译的 Python 文件
- 📄 `*$py.class` - Python 类文件

### 构建和分发
- 📁 `build/`, `dist/` - 构建和分发目录
- 📁 `*.egg-info/` - Python 包信息
- 📄 `*.egg` - Python egg 文件
- 📄 `MANIFEST` - 构建清单文件

### 虚拟环境
- 📁 `venv/`, `env/`, `.venv/` - 虚拟环境目录
- 📁 `ENV/`, `env.bak/`, `venv.bak/` - 虚拟环境备份

### 测试和覆盖率
- 📁 `.pytest_cache/`, `.coverage.*` - 测试缓存
- 📄 `coverage.xml`, `nosetests.xml` - 测试报告
- 📁 `htmlcov/` - HTML 覆盖率报告

### 开发工具
- 📁 `.idea/` - PyCharm 配置
- 📁 `.vscode/` - VS Code 配置
- 📄 `*.sublime-*` - Sublime Text 配置
- 📄 `*.swp`, `*.swo` - Vim 临时文件

### 操作系统
- 📄 `.DS_Store` - macOS 文件系统元数据
- 📄 `Thumbs.db` - Windows 缩略图缓存
- 📄 `Desktop.ini` - Windows 文件夹配置

### 数据库
- 📄 `*.db`, `*.sqlite`, `*.sqlite3` - 数据库文件
- 📄 `*.db-journal` - SQLite 日志文件

### 配置和敏感信息
- 📄 `.env*` - 环境变量文件
- 📄 `secrets.json` - 敏感配置
- 📄 `config/local.py` - 本地配置

### 日志和临时文件
- 📄 `*.log` - 日志文件
- 📁 `logs/`, `tmp/`, `temp/` - 日志和临时目录
- 📄 `*.backup`, `*.bak` - 备份文件

### 项目特定
- 📁 `test_env/` - 测试环境
- 📁 `generated_schemas/` - 生成的模式文件
- 📁 `benchmarks/` - 基准测试结果
- 📁 `*_data/`, `*_logs/` - 数据库特定文件

## 🔧 使用说明

### 检查状态
```bash
# 查看当前 git 状态
git status

# 查看所有文件（包括被忽略的）
git status --ignored
```

### 测试 .gitignore
```bash
# 构建项目来测试是否正确忽略构建文件
python -m build

# 运行代码来测试是否忽略 __pycache__
python -c "import norma"

# 检查 git 状态，应该没有新的未跟踪文件
git status
```

### 强制添加被忽略的文件（不推荐）
```bash
# 如果确实需要添加被忽略的文件
git add -f path/to/ignored/file
```

## 📝 自定义配置

如果需要添加项目特定的忽略规则，可以在 `.gitignore` 文件末尾添加：

```gitignore
# 项目特定忽略规则
my_custom_directory/
*.my_extension
```

## ⚠️ 注意事项

1. **已跟踪文件**: `.gitignore` 只对未跟踪的文件生效。如果文件已经被 Git 跟踪，需要先移除：
   ```bash
   git rm --cached filename
   ```

2. **全局 .gitignore**: 可以配置全局 .gitignore 文件：
   ```bash
   git config --global core.excludesfile ~/.gitignore_global
   ```

3. **检查忽略**: 查看文件是否被忽略：
   ```bash
   git check-ignore -v filename
   ```

## 🛠️ 维护

这个 `.gitignore` 文件覆盖了常见的开发场景。如果项目需求变化，可能需要：

- 添加新的数据库类型忽略规则
- 添加新的开发工具配置
- 调整项目特定的忽略模式

定期审查和更新 `.gitignore` 文件，确保它符合项目的当前需求。 