# SafeSkill 项目计划

> **For Hermes:** Use subagent-driven-development skill to implement this plan task-by-task.

**Goal:** 构建一个面向 Agent Skill 的安全分析平台，融合静态审计、动态利用验证、LLM 语义分析与 benchmark 数据集能力，重点用于对新的 skill 或多个 skill 进行扫描、评估与潜在威胁行为检测，输出结构化、可解释、可扩展的安全评级报告。

**Architecture:** SafeSkill 采用“输入适配层 → 解析归一化层 → 多引擎分析层 → 结果归并与评分层 → 报告与批量扫描层”的分层架构。系统统一管理来自本地目录、GitHub、平台安装目录与已归档 benchmark 样本的 Skill 数据，将规则命中、语义判断、动态验证结果归一化为统一 finding 模型，再进行去重、验证、评分与报告生成。

**Tech Stack:** Python、Typer、Pydantic、Jinja2、pytest、httpx、可插拔 LLM provider 接口、可选 Docker/runtime adapter、结构化 JSON/Markdown/HTML 报告。

---

## 一、项目定位

SafeSkill 是一个针对 AI Agent Skills 的安全分析系统，重点用于对新的 skill 或多个 skill 进行自动化安全扫描、风险评估与潜在威胁行为检测，并输出结构化报告。benchmark 数据集用于评估扫描能力、校准规则质量和验证检测效果，而不是产品主运行形态。

### 目标用户
- Skill 开发者
- 安全研究人员
- 企业内部 agent / automation 平台团队
- 最终安装或审核 skill 的使用者
- 需要批量审核 skill 的平台运营方

### 核心价值
- 在 skill 安装、接入、发布前发现潜在威胁行为
- 提供可解释、可复核的风险报告
- 支持单个 skill 与多个 skill 的批量扫描
- 用 benchmark 数据集验证检测质量与误报控制效果
- 建立可扩展的 skill 安全评级标准

### 非目标
当前阶段不追求：
- 覆盖所有 agent 平台的完整运行时兼容
- 完全自动化、零误报的风险判定
- 立即建设成公网多租户 SaaS 产品

---

## 二、总体架构

SafeSkill 建议采用五层架构，避免抓取、分析、评分、报告之间强耦合。

### 2.1 分层视图

1. **输入适配层**
   - 本地目录
   - GitHub 仓库
   - 平台安装目录
   - 批量输入清单
   - 已归档 benchmark 样本

2. **解析归一化层**
   - Skill 文件解析
   - 代码块提取
   - 依赖提取
   - URL / 权限 / capability 提取
   - benchmark 元数据归一化

3. **多引擎分析层**
   - 规则/静态审计引擎
   - LLM 语义分析引擎
   - 动态利用验证引擎

4. **结果归并与评分层**
   - finding 去重
   - 证据聚合
   - 置信度管理
   - 强制降级规则
   - 综合评分与评级

5. **报告与批量扫描层**
   - JSON / Markdown / HTML / SARIF 报告
   - CLI
   - 单目标扫描
   - 批量扫描
   - benchmark 回归评测

### 2.2 核心设计原则
- **采集与分析解耦**：市场抓取失败不应阻塞本地扫描主链路
- **分析引擎解耦**：静态、语义、动态三类分析可独立开关
- **统一数据模型**：所有输入先归一化，再进入分析引擎
- **证据优先**：所有结论必须附证据、上下文或执行痕迹
- **可插拔扩展**：provider、marketplace、runtime 都走 adapter 接口
- **先 MVP 后增强**：先做静态 + 语义，再引入动态利用验证

---

## 三、端到端数据流

### 3.1 单个 Skill 的分析流程
1. 接收输入目标（本地目录 / GitHub / benchmark 记录 / 安装目录）
2. 下载或定位 skill 内容
3. 解析 Skill 文档、代码块、脚本、依赖、元数据
4. 生成统一 `SkillManifest`
5. 依次运行：
   - 静态分析
   - 语义分析
   - 可选动态验证
6. 归并 findings 与证据
7. 执行评分、强制降级与风险解释
8. 输出报告与结构化结果

### 3.2 benchmark 数据流
1. 从各 Skill 市场同步目录页与详情页
2. 归档原始页面和解析结果
3. 去重、合并、补全 repo / skill 文件来源
4. 形成标准化 `MarketplaceSkillRecord`
5. 存入 benchmark 数据集
6. 用于规则回归测试、语义评估、批量基准扫描与检测效果验证

---

## 四、三类分析引擎

### 4.1 规则 / 静态审计引擎
负责快速识别高确定性的风险信号。

**职责：**
- SKILL.md / scripts / references / dependencies 解析结果审计
- danger function / command / secret / dependency / URL / reputation 检测
- 规则命中、证据提取、上下文切片、基础扣分
- 低成本、可批量、适合 benchmark 基准初筛与大规模预筛

**适合发现：**
- 危险命令/危险函数
- 硬编码 secrets
- 动态下载与远程执行模式
- 外联 API / 域名风险
- 依赖漏洞与可疑依赖
- context / memory / config 篡改痕迹

### 4.2 LLM 语义分析引擎
负责识别规则难以稳定覆盖的语义级风险。

**职责：**
- 理解 skill 文档、代码片段、工具说明、权限声明、任务目标之间的关系
- 判断“声明功能”与“实际行为”是否偏离
- 对静态 findings 做二次语义裁定，收缩误报
- 为动态验证生成更高质量的风险摘要与 exploit hypothesis

**适合发现：**
- 隐蔽意图与策略语言
- 权限声明与任务目标不匹配
- 对用户、系统提示、memory、workspace、tool calling 的操控意图
- 多段文本合并后才成立的风险语义

### 4.3 动态利用验证引擎
负责验证“风险是否真的可被利用”。

**职责：**
- 生成 attack surface 与 exploit hypothesis
- 在隔离 runtime 中执行 skill
- 观察文件、网络、进程、输出与状态变化
- 判断 exploit 成功与否，并保留 trace

**适合发现：**
- 真实可触发的危险行为
- 静态规则未命中但运行中暴露的问题
- exploitability 等级

### 4.4 三引擎协作关系
- **静态引擎**负责广覆盖初筛
- **语义引擎**负责意图理解与误报收缩
- **动态引擎**负责高价值、高成本验证

建议默认执行顺序：
1. 静态分析
2. 语义分析
3. 仅对高风险目标或指定模式启用动态验证

---

## 五、分析方式设计

### 5.1 规则 / 静态分析
用于识别高确定性的风险信号：
- 危险命令 / 危险函数
- Prompt 注入 / 指令劫持模式
- Secrets / Token / Key 泄露
- 外联 URL / API 分类
- 动态下载与远程执行模式
- Context / memory / config 篡改风险

### 5.2 动态验证分析
用于验证“是否真的能被利用”：
- 针对 attack surface 生成攻击 prompt
- 在隔离运行时执行 skill
- 观察文件、网络、进程、输出、状态变化
- 判断 exploit 成功与否
- 保留 attack trace

### 5.3 LLM 语义分析
用于识别规则难以捕获的语义级风险。

**典型任务：**
1. 功能-行为一致性分析
2. 意图与措辞分析
3. 权限合理性分析
4. 上下文操控分析
5. 规则命中二次裁定
6. 动态验证辅助

---

## 六、LLM 语义分析接口设计

为避免后续重构，建议从一开始就定义统一的语义分析接口。

### 6.1 抽象接口
```python
class SemanticAnalyzer(Protocol):
    def analyze(self, request: SemanticAnalysisRequest) -> SemanticAnalysisResult:
        ...
```

### 6.2 输入模型
```python
class SemanticAnalysisRequest(BaseModel):
    target_id: str
    skill_manifest: SkillManifest
    static_findings: list[Finding] = []
    attack_surfaces: list[AttackSurface] = []
    analysis_mode: str  # overview / triage / deep_review / exploit_assist
    focus_areas: list[str] = []
    llm_provider: str | None = None
    llm_model: str | None = None
```

### 6.3 输出模型
```python
class SemanticAnalysisResult(BaseModel):
    summary: str
    findings: list[Finding]
    semantic_risks: list[SemanticRisk]
    false_positive_overrides: list[str]
    exploit_hypotheses: list[str]
    confidence: float
    provider_metadata: dict = {}
```

### 6.4 Provider 适配层
```python
class LLMProvider(Protocol):
    def complete(self, prompt: str, system_prompt: str | None = None) -> str:
        ...
```

初期至少支持：
- OpenAI-compatible provider
- Anthropic-compatible provider
- 本地模型 provider（可选）

### 6.5 在 pipeline 中的挂载点
1. `manifest_ready`：做整体风险概览
2. `static_finished`：做 findings triage
3. `dynamic_prepare`：生成 exploit hypothesis
4. `reporting_prepare`：补充自然语言解释与修复建议

---

## 七、系统模块规划

### 7.1 Input Adapters
支持输入：
- 本地目录
- GitHub repo URL
- 单个 `SKILL.md`
- benchmark 记录 URL / ID
- 平台安装目录
- 批量输入清单

输出统一对象：
```json
{
  "source_type": "local|github|benchmark|installed|batch",
  "source": "...",
  "resolved_path": "...",
  "metadata": {
    "name": "...",
    "author": "...",
    "platform": "...",
    "version": "..."
  }
}
```

### 7.2 Benchmark Dataset Pipeline
用于持续拉取和维护主流 skill 市场的数据集，但其主要定位是 SafeSkill 的 benchmark 与评测基础设施，而不是产品主输入入口。

**目标市场：**
- `https://skillsmp.com/`
- `https://skills.sh/`
- `https://skillsllm.com/`
- `https://clawhub.ai/`
- `https://agentskill.sh/`
- `https://smithery.ai/skills`

**核心职责：**
1. 拉取 skill 列表、详情页、作者信息、标签、更新时间、安装方式、源码链接
2. 归档 `SKILL.md`、GitHub 仓库、脚本、依赖、截图、描述文本等内容
3. 将多来源异构数据归一化为统一的 `MarketplaceSkillRecord`
4. 维护可增量更新的数据快照
5. 为静态分析、语义分析、动态验证提供 benchmark 样本与回归测试数据

**建议子模块：**
- `marketplaces/discovery/`
- `marketplaces/fetchers/`
- `marketplaces/normalizers/`
- `marketplaces/storage/`
- `marketplaces/dedup/`
- `marketplaces/schedulers/`

**输出数据模型：**
```json
{
  "marketplace": "skillsmp|skills.sh|skillsllm|clawhub|agentskill|smithery",
  "skill_id": "...",
  "name": "...",
  "author": "...",
  "summary": "...",
  "tags": [],
  "detail_url": "...",
  "source_repo_url": "...",
  "skill_file_url": "...",
  "last_seen_at": "...",
  "updated_at": "...",
  "raw_snapshot_path": "...",
  "normalized_manifest_path": "..."
}
```

**抓取策略要求：**
- 优先使用公开 API / feed / sitemap；无 API 时再使用 HTML 抓取
- 每个市场实现独立 adapter，避免 selector 污染核心逻辑
- 保存原始响应与解析后结果，支持重放与 parser 修复
- 支持全量初始化抓取与按更新时间增量同步
- 支持失败重试、限速、降级与断点恢复

### 7.3 Skill Parser
解析：
- `SKILL.md`
- markdown code blocks
- `scripts/`
- `references/`
- `assets/`
- `package.json`, `requirements.txt`, `pyproject.toml`

输出统一 manifest：
```json
{
  "files": [],
  "code_blocks": [],
  "dependencies": [],
  "urls": [],
  "declared_capabilities": [],
  "requested_permissions": []
}
```

### 7.4 Static Analyzers
首批分析器：
1. Dangerous Execution Analyzer
2. Secret Leakage Analyzer
3. Prompt / Instruction Attack Analyzer
4. Network / API Analyzer
5. Dependency Analyzer
6. Reputation Analyzer

### 7.5 Semantic Analyzers
建议拆成多个可组合子模块：
1. Manifest Intent Analyzer
2. Capability-Permission Consistency Analyzer
3. Context Manipulation Analyzer
4. Static Finding Triage Analyzer
5. Exploit Hypothesis Generator
6. Report Explanation Generator

### 7.6 Dynamic Validation Engine
建议抽象为：
- surface extraction
- attacker
- runtime adapter
- simulator
- judge
- feedback refiner

### 7.7 Result Merge & Scoring Engine
评分输入不再只来自 static findings，还应支持：
- static findings
- semantic findings
- dynamic exploit verdicts
- source reputation
- benchmark 元数据与历史记录

建议评分维度：
- Code Execution Risk
- Data Exfiltration Risk
- Prompt Manipulation Risk
- Dependency Risk
- External Network Risk
- Source Trustworthiness
- Semantic Intent Risk
- Verified Exploitability

并保留：
- `forced_downgrade_reason`
- `hard_fail_flags`
- `confidence_score`

### 7.8 Reporting
至少输出：
- `report.json`
- `report.md`

增强版输出：
- `report.html`
- `report.sarif`
- `summary.csv`

报告中建议包含字段：
```json
{
  "summary": {},
  "rating": {},
  "findings": [],
  "semantic_analysis": {
    "summary": "...",
    "risks": [],
    "provider": "...",
    "model": "...",
    "confidence": 0.0
  },
  "dynamic_validation": {
    "executed": true,
    "verdict": "...",
    "traces": []
  }
}
```

### 7.9 Service Surface
建议在 CLI 层预留以下命令：
- `safeskill scan <target>`
- `safeskill batch-scan <input>`
- `safeskill benchmark sync`
- `safeskill benchmark run`
- `safeskill benchmark export`
- `safeskill report <run_id>`

---

## 八、架构演进原则

### 8.1 静态审计层
重点建设：
- 可复用规则扫描器
- threat / secret / entropy / url / dependency / reputation 能力
- 分类与策略选择机制
- 结构化报告字段设计

### 8.2 动态验证层
重点建设：
- 动态红队方法论
- staged pipeline 思路
- judge / feedback 机制
- lane workflow 与并行思路
- benchmark / dataset 组织方式

### 8.3 LLM 语义层
关键增量能力：
- 不只做规则扫描
- 不只做 exploit 红队
- 还要做语义级安全理解

### 8.4 benchmark 数据层
关键基础设施：
- 真实世界 skill benchmark 样本池
- 多来源去重与增量同步
- 回归测试与检测效果验证
- benchmark 与研究数据沉淀

---

## 九、阶段规划

### Phase 1：MVP（优先）
**目标：** 静态分析 + LLM 语义概览 + 报告输出

**交付：**
1. Python 项目骨架
2. `safeskill scan <target>` CLI
3. 本地目录输入
4. SKILL.md 解析
5. 规则命中输出 JSON
6. 语义分析接口定义
7. 一个基础 LLM provider adapter
8. Markdown / JSON 报告

### Phase 2：增强版
**目标：** 完善规则覆盖与结果质量

**交付：**
1. static findings triage 的语义二次裁定
2. dependency analyzer
3. reputation analyzer
4. GitHub adapter
5. skill 分类策略
6. HTML 报告
7. 配置文件支持

### Phase 3：动态验证
**目标：** 对高风险 skill 做利用性验证

**交付：**
1. attack surface schema
2. exploit hypothesis 生成
3. runtime adapter 抽象
4. sandbox 执行
5. exploit judge
6. attack trace 报告

### Phase 4：benchmark 与批量能力
**目标：** 建立 benchmark 数据管线与多 skill 批量扫描能力

**交付：**
1. SARIF / API 输出
2. 批量扫描
3. benchmark 数据集
4. 误报收敛流程
5. benchmark 数据同步管线
6. benchmark 回归评测
7. 扫描结果导出与汇总能力

---

## 十、建议目录结构

```text
safeskill/
├── README.md
├── todo.md
├── docs/
│   ├── architecture.md
│   ├── threat-model.md
│   ├── rating-model.md
│   └── plans/
│       └── 2026-04-29-safeskill-plan.md
├── safeskill/
│   ├── cli/
│   ├── core/
│   ├── adapters/
│   │   ├── inputs/
│   │   ├── marketplaces/
│   │   └── runtimes/
│   ├── parsers/
│   ├── analyzers/
│   │   ├── static/
│   │   ├── semantic/
│   │   └── dynamic/
│   ├── llm/
│   │   ├── providers/
│   │   └── prompts/
│   ├── scoring/
│   ├── reporting/
│   ├── datasets/
│   ├── models/
│   └── pipelines/
├── tests/
│   ├── fixtures/
│   ├── unit/
│   ├── integration/
│   └── e2e/
└── data/
    ├── rules/
    ├── samples/
    ├── benchmarks/
    └── marketplaces/
        ├── raw/
        ├── normalized/
        ├── snapshots/
        └── indexes/
```

---

## 十一、近期优先事项

### 第 1 周
1. 建立 Python 项目骨架
2. 定义 manifest / finding / report schema
3. 定义 SemanticAnalysisRequest / Result 接口
4. 建立最小 LLM provider adapter
5. 准备 3~5 个样本 skill

### 第 2 周
1. Markdown / skill parser
2. threat pattern matcher
3. secret detector
4. url extractor
5. semantic overview analyzer
6. markdown / json 报告

### 第 3 周
1. static findings triage analyzer
2. 评分模型
3. GitHub 来源检查
4. 强制降级规则
5. CLI 参数与配置模型统一

### 第 4 周
1. benchmark 扩充
2. 误报收敛
3. HTML 报告
4. 配置化规则
5. 动态验证接口草案
6. benchmark 数据抓取 adapter 草案

---

## 十二、关键设计原则

1. **规则、语义、动态三类分析解耦**
2. **采集层、分析层、报告层必须分层**
3. **统一 finding schema，避免不同引擎输出割裂**
4. **LLM 能力必须是可插拔接口，不写死具体 provider**
5. **LLM 语义分析用于增强，不应阻塞基础静态链路**
6. **市场同步是数据基础设施，不应侵入核心扫描器**
7. **保留 evidence-first 报告原则，语义结论必须附解释和证据来源**
8. **先做静态 + 语义 MVP，再按风险价值引入动态验证和市场批扫**

---

## 十三、一句话策略

先把 SafeSkill 做成“可对本地/GitHub/批量输入的 skill 进行静态分析并结合大模型做语义安全评估，输出可解释报告”的 Python 工具，再逐步补齐动态验证能力、benchmark 数据同步能力与统一评分报告体系，演进为完整的 skill 安全分析平台。
