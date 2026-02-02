# 🏛️ Claude Common (Intelligence Base)

这个仓库旨在将 Claude Code 的配置、规则、技能和知识库工程化、版本化。

## 📂 目录结构

*   **`rules/`**: 全局交互法则 (`CLAUDE.md`)。
*   **`skills/`**: 自定义技能定义与逻辑。
*   **`knowledge/`**: 长期知识沉淀与技术规范。
*   **`configs/`**: 环境配置备份 (`settings.json`)。
*   **`templates/`**: 项目级 `.claude.md` 模板。
*   **`scripts/`**: 自动化部署与同步脚本。

## 🚀 快速开始

### 1. 同步到本地
在仓库根目录下运行：
```bash
chmod +x scripts/setup.sh
./scripts/setup.sh
```

### 2. 工作流
1. 修改仓库中的 `rules/` 或 `skills/`。
2. 提交代码并推送到 GitHub。
3. 本地 Claude 会由于软链接实时生效。

## 🛡️ 安全提示
*   请勿在 `configs/settings.json` 中提交包含 API Key 或敏感信息的配置。
*   建议使用 `.template` 文件进行管理。
