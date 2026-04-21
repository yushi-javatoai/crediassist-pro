# 🤖 智能客服多Agent系统 (Python实现)

基于 LangGraph 构建的多Agent智能客服系统，采用 Supervisor 编排架构，集成 RAG 知识库、工单系统和合规审查，为金融/电商场景提供专业的智能客服解决方案。

## 📋 项目概览

- **多Agent协作**：Supervisor + 意图路由 + 知识检索 + 工单处理 + 合规审查
- **完整记忆系统**：工作记忆 + 短期记忆(Redis) + 长期记忆(FAISS向量库)
- **端到端RAG流程**：Query改写 → 向量检索 → 重排序 → 上下文注入 → 生成回答
- **金融级合规**：两阶段审查(规则引擎 + LLM深度审查)
- **REST API接口**：支持流式响应和工具调用
- **可观测性**：集成OpenTelemetry监控和追踪

## 🏗️ 系统架构

### 核心组件

```
┌─────────────────────────────────────────────────────────┐
│                    智能客服多Agent系统                     │
├─────────────────┬─────────────────┬────────────────────┤
│     API层      │    协调层      │      功能层        │
├─────────────────┼─────────────────┼────────────────────┤
│  FastAPI接口    │ Supervisor     │ IntentRouter      │
│  RESTful API    │ 中央协调者     │ 意图识别与分类     │
│  流式响应       │ 路由决策       │                    │
│  工具调用       │ 结果汇总       │ KnowledgeRAG      │
│                 │                │ 知识库检索与回答   │
└─────────────────┘                │                    │
                                   │ TicketHandler     │
                                   │ 工单创建与查询     │
                                   │                    │
                                   │ ComplianceChecker │
                                   │ 合规审查与敏感词检测 │
                                   └────────────────────┘
```

### 记忆系统

- **工作记忆**：进程内存储，维护当前对话的中间推理状态
- **短期记忆**：基于Redis，存储最近N轮对话上下文，自动过期
- **长期记忆**：基于FAISS向量库，存储知识库文档，支持语义检索

### 数据流

1. 用户发送消息 → API层接收请求
2. Supervisor分析意图 → 路由到对应子Agent
3. 子Agent处理请求（RAG/工单/合规）
4. 所有回复经过合规审查
5. Supervisor汇总结果 → 返回最终回答
6. 对话历史存储到短期记忆

## 🚀 核心功能

### 1. 意图识别与分类
- 一级意图：咨询、投诉、交易办理、账户、合规
- 二级意图：具体业务子类型
- 实体提取：订单号、产品名、金额等关键信息
- 智能路由：根据意图自动选择合适的Agent

### 2. 知识检索（RAG）
- Query改写：将口语化问题转为检索友好的查询
- 向量检索：从知识库中找到相关文档
- 文档重排序：提升检索结果的相关性
- 上下文注入：基于检索文档生成准确回答
- 引用标注：自动标注信息来源

### 3. 工单系统
- 工单创建：支持退款、理赔、开户等业务
- 工单查询：根据工单号查询状态
- 优先级管理：自动评估工单优先级
- 状态跟踪：完整的工单生命周期管理

### 4. 合规审查
- 敏感词检测：识别违规金融用语
- PII信息保护：自动脱敏处理个人信息
- 越权承诺检测：防止不当承诺
- 两阶段审查：规则引擎快速检查 + LLM深度审查

### 5. 可观测性
- OpenTelemetry集成：追踪Agent调用链路
- 系统指标：响应时间、成功率、合规率
- 工具调用日志：记录外部工具调用情况

## 📦 安装部署

### 环境要求
- Python 3.8+
- Redis (可选，用于短期记忆)
- FAISS (可选，用于长期记忆)

### 安装步骤

1. **克隆项目**
   ```bash
   git clone https://github.com/your-repo/crediassist-pro.git
   cd crediassist-pro
   ```

2. **安装依赖**
   ```bash
   pip install -r requirements.txt
   ```

3. **配置环境变量**
   ```bash
   cp .env.example .env
   # 编辑 .env 文件，设置OpenAI API Key等配置
   ```

4. **启动服务**
   ```bash
   python api/main.py
   ```

5. **访问接口**
   - API文档：http://localhost:8000/docs
   - 健康检查：http://localhost:8000/health

## 📡 API接口

### 1. 聊天接口
- **Endpoint**: `POST /api/chat`
- **请求体**:
  ```json
  {
    "message": "我想了解理财产品A的收益率",
    "user_id": "user123",
    "session_id": "session456"
  }
  ```
- **响应**:
  ```json
  {
    "response": "理财产品A的年化收益率为3.5%-5.2%...",
    "session_id": "session456",
    "intent": "knowledge_rag",
    "compliance_passed": true
  }
  ```

### 2. 历史查询
- **Endpoint**: `GET /api/history/{session_id}`
- **响应**:
  ```json
  {
    "session_id": "session456",
    "messages": [
      {"role": "user", "content": "...", "timestamp": "..."},
      {"role": "assistant", "content": "...", "timestamp": "..."}
    ]
  }
  ```

### 3. 工具调用
- **Endpoint**: `POST /api/tools/call`
- **请求体**:
  ```json
  {
    "name": "ticket_query",
    "arguments": {"ticket_id": "TK-20240101-ABC123"}
  }
  ```

### 4. 系统指标
- **Endpoint**: `GET /api/metrics`
- **响应**:
  ```json
  {
    "agent_metrics": {...},
    "tool_call_log": [...]
  }
  ```

## 🎯 使用场景

### 金融客服
- 产品咨询：理财产品、利率、政策了解
- 业务办理：开户、退款、理赔申请
- 账户服务：账户查询、密码重置、异常处理
- 合规审查：防止违规承诺和信息泄露

### 电商客服
- 商品咨询：产品信息、库存、价格
- 订单处理：下单、退款、物流查询
- 售后支持：退换货、维修、投诉处理
- 个性化推荐：基于历史对话推荐相关产品

## 🔧 配置与扩展

### 1. 知识库配置
- **添加文档**：在 `api/main.py` 中使用 `long_term_memory.add_document()` 添加知识库文档
- **批量导入**：使用 `long_term_memory.load_knowledge_base(kb_dir)` 从目录批量导入
- **向量模型**：生产环境建议替换为OpenAI Embedding API或本地模型

### 2. 工单系统扩展
- **存储后端**：将 `TicketStore` 替换为数据库存储
- **状态流转**：扩展工单状态和处理流程
- **通知机制**：添加邮件/短信通知功能

### 3. 合规规则配置
- **敏感词列表**：在 `compliance_checker.py` 中更新 `FORBIDDEN_TERMS`
- **PII模式**：更新 `SENSITIVE_PATTERNS` 添加新的敏感信息模式
- **审查规则**：修改 `COMPLIANCE_SYSTEM_PROMPT` 调整审查标准

### 4. 性能优化
- **缓存策略**：优化Redis缓存配置
- **检索性能**：使用FAISS IVF索引提升检索速度
- **并发处理**：调整Worker数量和超时设置

## 📊 监控与维护

### 1. 日志管理
- **Agent调用日志**：记录每个Agent的调用情况
- **工具调用日志**：记录外部工具的调用结果
- **错误日志**：捕获和分析系统异常

### 2. 指标监控
- **响应时间**：各Agent的处理时间
- **成功率**：API调用和Agent执行的成功率
- **合规率**：合规审查的通过率
- **知识库覆盖率**：查询命中知识库的比例

### 3. 故障排查
- **调用链路**：通过OpenTelemetry追踪Agent调用链路
- **内存状态**：监控工作记忆和短期记忆的使用情况
- **知识库健康**：检查向量库的完整性和性能

## 🤝 贡献指南

1. **Fork 项目**
2. **创建分支**：`git checkout -b feature/your-feature`
3. **提交更改**：`git commit -m 'Add your feature'`
4. **推送分支**：`git push origin feature/your-feature`
5. **创建Pull Request**

## 📄 许可证

本项目采用 MIT 许可证，详情请查看 [LICENSE](LICENSE) 文件。

## 📞 联系方式

- **项目维护者**：Your Name
- **邮箱**：your.email@example.com
- **GitHub**：[your-username/crediassist-pro](https://github.com/your-username/crediassist-pro)

---

**🚀 开始使用**：部署系统后，访问 http://localhost:8000/docs 查看完整的API文档和交互式测试界面。

**💡 提示**：生产环境部署时，建议配置HTTPS、设置合理的API密钥、并定期更新知识库和合规规则。