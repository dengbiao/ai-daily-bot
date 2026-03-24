# 每日AI日报

🤖 一个自动聚合每日AI领域最新进展的网站，基于 Chirpy Jekyll 主题构建，自动部署到 GitHub Pages。

## 功能特性

- 📄 **每日最新AI论文** - 从 HuggingFace Daily Papers 获取热门论文
- ⭐ **GitHub热门AI仓库** - 获取当日新增热门AI相关开源项目
- 📰 **AI行业新闻** - 聚合多个优质AI媒体RSS源新闻
- 🔄 **自动更新** - 每日自动运行，生成新的日报文件并自动部署
- 📱 **响应式设计** - 使用 Chirpy 主题，完美适配桌面和移动设备

## 项目结构

```
├── .github/
│   └── workflows/
│       └── daily-build.yml    # GitHub Actions 自动构建配置
├── _posts/                    # 生成的每日日报存放目录
├── scripts/
│   ├── __init__.py
│   ├── config.py             # 配置文件（数据源、数量等）
│   ├── huggingface.py        # HuggingFace 论文抓取
│   ├── github_trending.py    # GitHub Trending 抓取
│   ├── rss_parser.py         # RSS 新闻解析
│   └── generate_daily.py     # 主程序，生成日报markdown
├── assets/                   # 静态资源
├── _config.yml              # Jekyll 配置
├── Gemfile                  # Ruby 依赖
├── requirements.txt         # Python 依赖
└── README.md
```

## 快速开始

### 1. Fork 这个仓库

点击 GitHub 页面右上角的 **Fork** 按钮，把这个项目复制到你的账户下。

### 2. 配置 GitHub Pages

1. 进入你的仓库 → **Settings** → **Pages**
2. **Build and deployment** → **Source** 选择 **GitHub Actions**
3. 保存设置

### 3. 修改配置（可选）

编辑 `scripts/config.py` 可以自定义：

- 修改 RSS 新闻源
- 调整每种内容的显示数量
- 修改日期格式等

编辑 `_config.yml` 修改网站信息：

- 修改 `title`、`tagline`、`description` 网站信息
- 修改 `author` 信息
- 修改 `url` 为你的 GitHub Pages 地址

### 4. 启用 GitHub Actions

1. 在你的仓库点击 **Actions** 标签
2. 点击 **I understand my workflows, go ahead and enable them**
3. 每日自动运行会自动开启，你也可以手动触发运行

### 5. 手动运行生成（可选）

如果你想手动生成今天的日报：

```bash
# 克隆项目
git clone https://github.com/你的用户名/你的用户名.github.io.git
cd 你的用户名.github.io

# 创建虚拟环境
python3 -m venv venv
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt

# 生成今日日报
python -m scripts.generate_daily

# 推送提交
git add _posts/
git commit -m "Add daily report"
git push
```

## 工作流程

1. **每天 UTC 时间 0 点**（北京时间 8 点）GitHub Action 自动触发
2. 运行 Python 脚本抓取各个数据源
3. 生成当天的日报 markdown 文件保存到 `_posts/` 目录
4. 自动提交新文件到你的仓库
5. Jekyll 自动构建并部署到 GitHub Pages

## 数据源

当前配置的数据源：

- [MIT Technology Review AI](https://www.technologyreview.com/topic/artificial-intelligence/feed) - AI领域新闻
- Google AI Blog - Google AI研究博客
- OpenAI Blog - OpenAI官方博客
- NVIDIA AI Blog - NVIDIA AI博客
- Amazon Science Blog - Amazon AI科学博客

## 自定义修改

### 添加更多 RSS 源

编辑 `scripts/config.py`，在 `RSS_FEEDS` 中添加：

```python
{
    "name": "源名称",
    "url": "RSS地址",
    "category": "分类"
}
```

### 修改抓取数量

修改 `scripts/config.py` 中的：

- `MAX_PAPERS` - 最大论文数量
- `MAX_TRENDING_REPOS` - 最大仓库数量

## 本地预览

如果你想本地预览网站：

```bash
# 安装 Ruby 和 Bundler
gem install bundler

# 安装依赖
bundle install

# 本地启动
bundle exec jekyll serve

# 打开浏览器访问 http://localhost:4000
```

## 许可证

MIT License

## 致谢

- [Chirpy Jekyll Theme](https://github.com/cotes2020/jekyll-theme-chirpy) - 使用的主题
- [HuggingFace](https://huggingface.co/) - 论文数据源
- [GitHub](https://github.com/) - Trending 数据源
