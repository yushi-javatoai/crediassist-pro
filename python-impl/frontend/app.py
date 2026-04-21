"""
智能客服多Agent系统 - Streamlit前端界面
适合面试展示，突出技术架构和Agent协作流程
"""

import streamlit as st
import requests
import json
import uuid
from datetime import datetime

API_BASE_URL = "http://localhost:8001"

st.set_page_config(
    page_title="智能客服多Agent系统",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
.main-header {
    font-size: 2.5rem;
    font-weight: bold;
    color: #1f77b4;
    text-align: center;
    margin-bottom: 0.5rem;
}
.sub-header {
    font-size: 1rem;
    color: #666;
    text-align: center;
    margin-bottom: 2rem;
}
.agent-card {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    padding: 1rem;
    border-radius: 10px;
    color: white;
    margin: 0.5rem 0;
}
.chat-message {
    padding: 1rem;
    border-radius: 10px;
    margin: 0.5rem 0;
}
.user-message {
    background-color: #e3f2fd;
    border-left: 4px solid #2196f3;
}
.assistant-message {
    background-color: #f3e5f5;
    border-left: 4px solid #9c27b0;
}
.intent-badge {
    display: inline-block;
    padding: 2px 8px;
    border-radius: 12px;
    font-size: 0.75rem;
    font-weight: bold;
}
.intent-knowledge { background-color: #4caf50; color: white; }
.intent-ticket { background-color: #ff9800; color: white; }
.intent-compliance { background-color: #f44336; color: white; }
.intent-unknown { background-color: #9e9e9e; color: white; }
.architecture-box {
    background-color: #f5f5f5;
    border: 2px solid #ddd;
    border-radius: 8px;
    padding: 1rem;
    margin: 0.5rem 0;
}
</style>
""", unsafe_allow_html=True)

if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())
if "messages" not in st.session_state:
    st.session_state.messages = []
if "show_architecture" not in st.session_state:
    st.session_state.show_architecture = True

def get_intent_badge(intent):
    intent_map = {
        "knowledge_rag": ("知识检索", "intent-knowledge"),
        "ticket_handler": ("工单处理", "intent-ticket"),
        "compliance_checker": ("合规审查", "intent-compliance"),
    }
    label, css_class = intent_map.get(intent, (intent or "未知", "intent-unknown"))
    return f'<span class="intent-badge {css_class}">{label}</span>'

def check_health():
    try:
        response = requests.get(f"{API_BASE_URL}/health", timeout=5)
        return response.status_code == 200
    except:
        return False

def send_message(message):
    try:
        response = requests.post(
            f"{API_BASE_URL}/api/chat",
            json={
                "message": message,
                "user_id": "interview_demo",
                "session_id": st.session_state.session_id
            },
            timeout=30
        )
        return response.json()
    except Exception as e:
        return {"response": f"请求失败: {str(e)}", "intent": "error", "compliance_passed": False}

def get_metrics():
    try:
        response = requests.get(f"{API_BASE_URL}/api/metrics", timeout=5)
        return response.json()
    except:
        return None

st.markdown('<div class="main-header">🤖 智能客服多Agent系统</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">基于 LangGraph 的 Supervisor 编排架构 | 金融级合规审查 | 端到端RAG</div>', unsafe_allow_html=True)

with st.sidebar:
    st.header("📊 系统架构")
    
    with st.expander("🏗️ 架构说明", expanded=True):
        st.markdown("""
        **核心组件:**
        - **Supervisor**: 中央协调者，负责意图识别和路由决策
        - **IntentRouter**: 意图识别与分类
        - **KnowledgeRAG**: 知识库检索与回答生成
        - **TicketHandler**: 工单创建与查询
        - **ComplianceChecker**: 合规审查与敏感词检测
        
        **记忆系统:**
        - 工作记忆: 进程内存储中间状态
        - 短期记忆: Redis存储对话上下文
        - 长期记忆: FAISS向量库存储知识库
        """)
    
    st.header("🔧 系统状态")
    
    if check_health():
        st.success("✅ 后端服务运行正常")
    else:
        st.error("❌ 后端服务未启动")
        st.info("请确保后端服务已启动: `python api/main.py`")
    
    metrics = get_metrics()
    if metrics:
        st.metric("Agent调用次数", len(metrics.get("tool_call_log", [])))
    
    st.header("📋 面试亮点")
    with st.expander("点击查看技术亮点"):
        st.markdown("""
        **技术栈:**
        - LangGraph + LangChain 构建Agent工作流
        - FastAPI 提供REST API
        - OpenTelemetry 全链路追踪
        - FAISS 向量检索
        
        **核心能力:**
        - 多Agent协作与编排
        - 两阶段合规审查
        - 端到端RAG流程
        - 三级记忆系统
        """)
    
    if st.button("🔄 重置会话"):
        st.session_state.session_id = str(uuid.uuid4())
        st.session_state.messages = []
        st.rerun()

col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("💬 智能对话")
    
    chat_container = st.container()
    with chat_container:
        for msg in st.session_state.messages:
            if msg["role"] == "user":
                st.markdown(f'''
                <div class="chat-message user-message">
                    <strong>👤 用户</strong> <span style="color:#999;font-size:0.8rem">{msg.get("time", "")}</span><br/>
                    {msg["content"]}
                </div>
                ''', unsafe_allow_html=True)
            else:
                intent_badge = get_intent_badge(msg.get("intent", ""))
                compliance = "✅ 合规通过" if msg.get("compliance_passed") else "❌ 合规未通过"
                st.markdown(f'''
                <div class="chat-message assistant-message">
                    <strong>🤖 智能客服</strong> 
                    {intent_badge}
                    <span style="color:#999;font-size:0.8rem;float:right">{compliance}</span><br/>
                    {msg["content"]}
                </div>
                ''', unsafe_allow_html=True)
    
    with st.form("chat_form", clear_on_submit=True):
        user_input = st.text_input("输入消息", placeholder="例如: 理财产品A的收益率是多少？")
        cols = st.columns([1, 1, 4])
        with cols[0]:
            submitted = st.form_submit_button("🚀 发送", use_container_width=True)
        with cols[1]:
            show_flow = st.form_submit_button("📊 查看流程", use_container_width=True)
    
    if submitted and user_input:
        current_time = datetime.now().strftime("%H:%M:%S")
        
        st.session_state.messages.append({
            "role": "user",
            "content": user_input,
            "time": current_time
        })
        
        with st.spinner("Agent协作处理中..."):
            result = send_message(user_input)
        
        st.session_state.messages.append({
            "role": "assistant",
            "content": result.get("response", "处理异常"),
            "intent": result.get("intent", "unknown"),
            "compliance_passed": result.get("compliance_passed", True),
            "time": datetime.now().strftime("%H:%M:%S")
        })
        
        st.rerun()

with col2:
    st.subheader("🎯 Agent决策流程")
    
    if st.session_state.messages:
        last_msg = st.session_state.messages[-1]
        if last_msg["role"] == "assistant":
            intent = last_msg.get("intent", "unknown")
            
            st.markdown("**1️⃣ 意图识别**")
            st.info(f"识别意图: `{intent}`")
            
            st.markdown("**2️⃣ Agent路由**")
            if intent == "knowledge_rag":
                st.success("→ KnowledgeRAG Agent")
                st.markdown("- Query改写\n- 向量检索\n- 文档重排序\n- 生成回答")
            elif intent == "ticket_handler":
                st.warning("→ TicketHandler Agent")
                st.markdown("- 工单创建\n- 优先级评估\n- 状态跟踪")
            elif intent == "compliance_checker":
                st.error("→ ComplianceChecker Agent")
                st.markdown("- 敏感词检测\n- PII脱敏\n- 越权承诺检测")
            
            st.markdown("**3️⃣ 合规审查**")
            if last_msg.get("compliance_passed"):
                st.success("✅ 两阶段审查通过")
            else:
                st.error("❌ 合规审查未通过")
            
            st.markdown("**4️⃣ 结果返回**")
            st.info("Supervisor汇总结果")
    else:
        st.info("开始对话后查看Agent协作流程")
    
    st.divider()
    
    st.subheader("📚 示例问题")
    examples = [
        "理财产品A的收益率是多少？",
        "我想申请退款",
        "如何开户？",
        "查询工单 TK-20240101-ABC123",
    ]
    for ex in examples:
        if st.button(f"💡 {ex}", use_container_width=True, key=f"ex_{ex}"):
            current_time = datetime.now().strftime("%H:%M:%S")
            st.session_state.messages.append({
                "role": "user",
                "content": ex,
                "time": current_time
            })
            
            with st.spinner("Agent协作处理中..."):
                result = send_message(ex)
            
            st.session_state.messages.append({
                "role": "assistant",
                "content": result.get("response", "处理异常"),
                "intent": result.get("intent", "unknown"),
                "compliance_passed": result.get("compliance_passed", True),
                "time": datetime.now().strftime("%H:%M:%S")
            })
            
            st.rerun()

st.divider()
with st.expander("📖 系统架构图"):
    st.markdown("""
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
                                       │ 合规审查与敏感词检测│
                                       └────────────────────┘
    
    记忆系统:
    ┌──────────────┬──────────────┬──────────────┐
    │  工作记忆     │  短期记忆     │  长期记忆     │
    │  (进程内)     │  (Redis)     │  (FAISS)     │
    │ 中间推理状态  │ 对话上下文    │ 知识库文档    │
    └──────────────┴──────────────┴──────────────┘
    ```
    """)
