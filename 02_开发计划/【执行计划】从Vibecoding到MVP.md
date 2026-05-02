# 执行计划：从零开始，一步步搭建汽车CRM AI系统

> **核心策略**：用最小的知识起步，每一步都能跑通，每一步都学到东西
> **原则**：先抄→再改→后懂，跑通 > 理解，能演示 > 完美
> **目标**：8周完成MVP，面试能演示5个核心功能

---

## 全局路线图

```
阶段0  环境搭建（1天）
  ↓
阶段1  第一个对话：调用大模型API（2天）
  ↓
阶段2  第一个RAG：售后故障诊断（3天）
  ↓
阶段3  结构化输出：对话信息抽取（2天）
  ↓
阶段4  Tool Calling：语音创建工单（3天）
  ↓
阶段5  Text-to-SQL：智能问数（2天）
  ↓
阶段6  Streamlit界面：5合1 MVP（3天）
  ↓
阶段7  LangGraph多Agent协作（4天）
  ↓
阶段8  知识图谱：联系人关系（3天）
  ↓
阶段9  打磨包装：准备面试（持续）

总计：约8周（含课程学习同步推进）
```

---

## 附录A：业务资产来源（真实方案文档）

> 本项目所有业务痛点、功能设计均来自**前公司（瑞能股份）实际使用的CRM解决方案文档**。

### 来源文件（共9份）

| # | 文件 | 来源 | 核心价值 |
|---|------|------|---------|
| 1 | 瑞能×纷享销客CRM解决方案0428.pdf (55页) | 瑞能×纷享销客(2023.04) | 6步建设路线、LTC全链路、PaaS四流合一 |
| 2 | 瑞能CRM项目解决方案0322.pdf (55页) | 瑞能×纷享销客(2023.03) | 完整痛点分析(16条)、项目蓝图、BI架构 |
| 3 | 泛微九氚汇CRM整体解决方案.pptx | 泛微×九氚汇 | 竞品：数字名片、营销效果验证 |
| 4 | ⭐**纷享销客AI销售Agent白皮书**(67页) | 纷享销客官方 | **15种Agent类型、ShareAI平台架构、嵌入式vs对话式AI** |
| 5 | ⭐**瑞能CRM A3文档**(9页) | 瑞能内部 | **78功能模块(P1-P4)、12月周期、22个ERP/OA接口** |
| 6 | ⭐**售前LTC AI场景清单**(53场景) | 瑞能内部 | **53个AI场景完整清单+LTC全链路映射** |
| 7 | ⭐**售前业务全流程**(1页) | 瑞能内部 | **线索打分(A/B/C)、公海池规则、联系人图谱(6种)** |
| 8 | CRM功能差异对比.xlsx (113行) | 瑞能内部 | 16个一级功能详细二级清单+实现状态 |

> 详细内容（ShareAI架构/15种Agent/78模块/53场景/业务规则）见【5个月完整落地.md】

### 业务架构：OKR + MTL + LTC + ITR

```
OKR(目标管理) → MTL(市场到线索) → LTC(线索到现金) → ITR(问题到解决)
  目标/预测        活动→线索→转化     客户→商机→合同→回款   受理→派单→维修→结算
```

> 详细框架和痛点分层见【5个月完整落地.md】

---

## 阶段0：环境搭建（1天）

### 你需要知道的（最小知识）

```
1. Python基础：变量、函数、if/else、import、pip install
2. 终端/命令行：cd、mkdir、python xxx.py
3. VS Code基本操作：打开文件夹、运行代码
```

### 知识速查：Python必会清单

```python
# 变量
name = "张三"
age = 25

# 字典（后面到处用）
customer = {"name": "张三", "car": "秦Plus", "fault": "电池故障"}

# 列表
faults = ["启动困难", "异响", "漏油"]

# 函数
def greet(name):
    return f"你好，{name}"

# f-string（格式化字符串，后面到处用）
msg = f"客户{name}的{customer['car']}存在{customer['fault']}问题"

# try-except（后面调用API到处用）
try:
    result = call_api()
except Exception as e:
    print(f"出错了：{e}")

# with open（读写文件）
with open("data.txt", "r", encoding="utf-8") as f:
    content = f.read()
```

### 步骤

```bash
# 1. 创建项目目录结构
mkdir CRM-AI-Project
cd CRM-AI-Project
mkdir src
mkdir src\agents
mkdir src\tools
mkdir src\prompts
mkdir data
mkdir data\knowledge_base
mkdir data\mock_db
mkdir tests
mkdir pages

# 2. 创建虚拟环境（隔离依赖，不污染全局）
python -m venv venv
venv\Scripts\activate

# 3. 安装最小依赖（先装这些，后续按需追加）
pip install openai python-dotenv streamlit chromadb langchain langchain-community langchain-openai langgraph pyvis networkx

# 4. 创建配置文件
```

```bash
# 在项目根目录创建 .env 文件
# ===== .env =====
OPENAI_API_KEY=sk-你的key
OPENAI_BASE_URL=https://你的api地址/v1   # 如果用国产模型填这个
MODEL_NAME=gpt-4o-mini                      # 或 qwen-plus / deepseek-chat
```

```python
# 创建 src/config.py 统一读取配置
from dotenv import load_dotenv
import os

load_dotenv()  # 加载.env文件

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_BASE_URL = os.getenv("OPENAI_BASE_URL")
MODEL_NAME = os.getenv("MODEL_NAME", "gpt-4o-mini")
```

### 验证

```python
# 创建 test_env.py 运行测试
from src.config import OPENAI_API_KEY, MODEL_NAME
print(f"API Key: {OPENAI_API_KEY[:10]}...")
print(f"Model: {MODEL_NAME}")
print("环境OK!")
```

### ✅ 阶段0交付：环境跑通，config能读取

---

## 阶段1：第一个对话——调用大模型API（2天）

### 你需要知道的（最小知识）

```
1. 什么是API：你发请求，服务器返回结果
2. 什么是大模型API：发一段文字，返回AI回复
3. OpenAI SDK：Python调用大模型的工具包
```

### 知识速查：大模型调用核心概念

```python
# 大模型调用的本质就是：发消息 → 收回复
# 消息有3种角色：
#   system    → 系统指令，告诉AI"你是谁"
#   user      → 用户说的话
#   assistant → AI的回复

# 调用参数：
#   temperature → 0=确定性强，1=创意性强，诊断场景用0.1
#   max_tokens  → 回复最大长度
```

### 步骤

```python
# 创建 src/llm.py —— 大模型调用的统一封装
from openai import OpenAI
from src.config import OPENAI_API_KEY, OPENAI_BASE_URL, MODEL_NAME

client = OpenAI(
    api_key=OPENAI_API_KEY,
    base_url=OPENAI_BASE_URL
)

def chat(messages: list, temperature: float = 0.1) -> str:
    """调用大模型，返回AI回复文本"""
    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=messages,
        temperature=temperature
    )
    return response.choices[0].message.content

def simple_chat(user_input: str, system_prompt: str = "你是一个有用的AI助手。") -> str:
    """最简单的对话：一句话进，一句话出"""
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_input}
    ]
    return chat(messages)
```

```python
# 创建 test_chat.py 测试
from src.llm import simple_chat

# 测试1：基础对话
result = simple_chat("你好，请介绍一下你自己")
print(result)

# 测试2：带角色设定
result = simple_chat(
    "我的比亚迪秦Plus启动困难，可能是什么原因？",
    system_prompt="你是一个专业的汽车售后诊断助手，请给出可能的原因和建议。"
)
print(result)
```

### 知识点复习

```
Q: system消息和user消息有什么区别？
A: system是"人设"，告诉AI该怎么回答；user是"问题"，用户实际说的内容。
   比如system说"你是汽车诊断专家"，AI就会用专业口吻回答。

Q: 为什么temperature设0.1？
A: 诊断场景需要确定性答案，不想AI发挥创意。聊天/创意场景可以调高。

Q: OpenAI和通义千问/DeepSeek的API有什么区别？
A: 接口几乎一样！改base_url和model_name就行，这就是用OpenAI SDK的好处。
```

### ✅ 阶段1交付：能调通API，能拿到AI回复

---

## 阶段2：第一个RAG——售后故障诊断（3天）

### 你需要知道的（最小知识）

```
1. RAG = Retrieval Augmented Generation（检索增强生成）
2. 通俗理解：先从知识库找到相关内容，再让AI基于这些内容回答
3. 为什么需要RAG：大模型不知道你公司的内部知识，RAG帮它"查资料"
4. 向量数据库：把文字变成数字，用数字的"距离"找相似内容
```

### 知识速查：RAG流程图

```
用户提问："秦Plus启动困难怎么办？"
       ↓
① 文本向量化：把问题变成数字向量 [0.12, -0.34, 0.56, ...]
       ↓
② 向量检索：在知识库中找最相似的文档片段（Top-K）
       ↓
  找到："秦Plus电池亏电会导致启动困难，建议检查电池电压..."
       ↓
③ 拼接Prompt：把"找到的内容" + "用户问题"一起发给大模型
       ↓
④ 大模型回答：基于检索到的内容，生成有依据的回答
```

### 步骤

#### 2.1 准备知识库文档

```
在 data/knowledge_base/ 下创建以下txt文件：
```

**比亚迪保修政策摘要.txt**
```
比亚迪汽车保修政策：
1. 整车保修期：6年或15万公里（以先到者为准）
2. 三电系统保修期：8年或15万公里（电池、电机、电控）
3. 保修期内非人为损坏免费维修
4. 以下情况不在保修范围内：
   - 未在授权4S店保养
   - 私自改装车辆
   - 事故造成的损坏
   - 正常磨损件（刹车片、雨刮、灯泡等）
5. 索赔流程：客户报修 → 4S店检测 → 系统提交索赔 → 厂家审批 → 维修/更换
```

**故障诊断案例库.txt**
```
案例1：秦Plus启动困难
症状：车辆无法启动或启动缓慢，仪表盘显示正常
可能原因：
- 12V辅助电池亏电（最常见）
- 启动继电器故障
- 高压电池SOC过低
- BCM（车身控制器）故障
诊断步骤：
1. 检查12V电池电压，低于11.5V需充电或更换
2. 检查高压电池SOC，低于10%需充电
3. 检查启动继电器是否正常吸合
4. 用诊断仪读取BCM故障码
维修建议：先充12V电池测试，如仍无法启动则检查继电器和BCM

案例2：唐DM异响
症状：行驶中底盘异响，过减速带时明显
可能原因：
- 下摆臂衬套老化
- 减震器漏油失效
- 稳定杆球头松旷
- 制动片磨损到极限
诊断步骤：
1. 举升车辆检查底盘各连接件
2. 检查减震器是否有油迹
3. 检查制动片厚度
4. 路试确认异响位置和频率

案例3：宋Plus EV续航骤降
症状：满电续航从502km降至350km左右
可能原因：
- 电池健康度下降（SOH低于80%）
- 驾驶习惯变化（频繁急加速）
- 环境温度过低（冬季）
- 轮胎气压不足
诊断步骤：
1. 用诊断仪读取电池SOH值
2. 检查轮胎气压是否在标准范围
3. 分析近期驾驶数据和充电记录
4. 如SOH低于80%，申请电池质保索赔
```

**维修工序手册.txt**
```
工序1：12V电池更换
适用车型：全系
工时：0.5小时
步骤：
1. 关闭车辆电源，等待5分钟
2. 拆卸负极接线（先拆负极！）
3. 拆卸正极接线
4. 拆卸电池固定支架
5. 取出旧电池
6. 安装新电池，固定支架
7. 连接正极接线（先接正极！）
8. 连接负极接线
9. 启动车辆，检查电压是否正常（13.5V以上）
注意事项：拆卸顺序先负后正，安装顺序先正后负

工序2：空调滤芯更换
适用车型：全系
工时：0.3小时
步骤：
1. 打开副驾驶手套箱
2. 拆卸手套箱限位器
3. 取出空调滤芯盖板
4. 取出旧滤芯
5. 安装新滤芯（注意箭头方向）
6. 安装盖板和手套箱
注意事项：滤芯箭头朝下表示气流方向

工序3：制动片更换
适用车型：全系
工时：1.0小时
步骤：
1. 举升车辆，拆卸轮胎
2. 拆卸制动卡钳螺栓
3. 取出旧制动片
4. 推回制动分泵活塞
5. 安装新制动片
6. 安装制动卡钳
7. 安装轮胎
8. 启动车辆，踩制动踏板数次恢复行程
注意事项：新制动片需要200km磨合期
```

#### 2.2 构建RAG检索链

```python
# 创建 src/rag.py —— RAG核心模块
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import TextLoader
from src.config import OPENAI_API_KEY, OPENAI_BASE_URL
import os

# 知识库目录
KB_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "knowledge_base")
DB_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "chroma_db")

def build_knowledge_base():
    """从txt文件构建向量知识库（只需运行一次，后续自动加载）"""
    # 1. 加载所有文档
    docs = []
    for filename in os.listdir(KB_DIR):
        if filename.endswith(".txt"):
            loader = TextLoader(os.path.join(KB_DIR, filename), encoding="utf-8")
            docs.extend(loader.load())
    
    # 2. 文档切分
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,       # 每段最多500字
        chunk_overlap=50,     # 相邻段落重叠50字（保证上下文连续）
        separators=["\n\n", "\n", "。", "，", " "]  # 切分优先级
    )
    chunks = splitter.split_documents(docs)
    print(f"文档切分完成：{len(docs)}个文件 → {len(chunks)}个片段")
    
    # 3. 向量化并存入Chroma
    embeddings = OpenAIEmbeddings(
        api_key=OPENAI_API_KEY,
        base_url=OPENAI_BASE_URL
    )
    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=DB_DIR
    )
    print(f"知识库构建完成，保存到 {DB_DIR}")
    return vectorstore

def get_retriever():
    """获取检索器（如果知识库已存在则直接加载）"""
    embeddings = OpenAIEmbeddings(
        api_key=OPENAI_API_KEY,
        base_url=OPENAI_BASE_URL
    )
    
    if os.path.exists(DB_DIR):
        vectorstore = Chroma(
            persist_directory=DB_DIR,
            embedding_function=embeddings
        )
    else:
        vectorstore = build_knowledge_base()
    
    return vectorstore.as_retriever(
        search_type="similarity",
        search_kwargs={"k": 3}  # 返回最相似的3个片段
    )
```

#### 2.3 组装诊断助手

```python
# 创建 src/diagnose.py —— 售后故障诊断
from src.rag import get_retriever
from src.llm import chat

DIAGNOSE_SYSTEM = """你是一个专业的汽车售后诊断助手。

工作流程：
1. 根据用户描述的故障症状，从知识库检索相关案例
2. 基于检索结果，给出可能的原因和诊断步骤
3. 给出维修建议和参考工序

回答要求：
- 必须基于检索到的知识库内容回答，不要编造
- 列出可能的原因（按可能性排序）
- 给出具体的诊断步骤
- 引用来源（"根据XXX文档..."）
- 如果知识库中没有相关信息，如实告知
"""

def diagnose(fault_description: str) -> str:
    """售后故障诊断：输入故障描述，输出诊断建议"""
    # 1. 检索相关知识
    retriever = get_retriever()
    docs = retriever.invoke(fault_description)
    context = "\n\n".join([f"【参考文档{i+1}】{doc.page_content}" 
                           for i, doc in enumerate(docs)])
    
    # 2. 拼接Prompt
    messages = [
        {"role": "system", "content": DIAGNOSE_SYSTEM},
        {"role": "user", "content": f"""
故障描述：{fault_description}

以下是知识库中检索到的相关内容：
{context}

请基于以上信息，给出诊断建议。
"""}
    ]
    
    # 3. 调用大模型
    return chat(messages)
```

```python
# 创建 test_rag.py 测试
from src.diagnose import diagnose

result = diagnose("我的比亚迪秦Plus启动困难，仪表盘显示正常，可能是什么原因？")
print(result)
```

### 知识点复习

```
Q: chunk_size为什么选500？
A: 太小（100）→ 上下文断裂，信息不完整
   太大（2000）→ 检索不精准，混入无关内容
   500是经验值，后续可以调整对比效果

Q: chunk_overlap是什么？
A: 相邻两个片段重叠的字数。防止关键信息正好被切在两段之间。

Q: search_kwargs={"k": 3} 是什么意思？
A: 检索最相似的3个文档片段。k太小可能漏掉相关内容，
   k太大会混入不相关内容且token开销大。3-5是常用值。

Q: RAG怎么减少幻觉？
A: ① Prompt里明确要求"基于检索内容回答，不要编造"
   ② 要求引用来源
   ③ 如果检索不到相关内容，让AI说"知识库中没有相关信息"
```

### ✅ 阶段2交付：输入故障描述，输出有依据的诊断建议

---

## 阶段3：结构化输出——对话信息抽取（2天）

### 你需要知道的（最小知识）

```
1. 结构化输出：让AI返回JSON格式，而不是自由文本
2. 为什么需要：后续要把抽取的信息存数据库、创建工单
3. JSON：一种数据格式，key-value键值对
```

### 知识速查：结构化输出对比

```
普通输出（自由文本）：
  "客户张三有一辆秦Plus，反馈电池故障，比较紧急"

结构化输出（JSON）：
  {
    "customer_name": "张三",
    "vehicle_model": "秦Plus",
    "fault_description": "电池故障",
    "urgency": "高"
  }

结构化输出的好处：
  → 程序可以直接处理（存数据库、创建工单、触发流程）
  → 字段明确，不会遗漏信息
  → 前端可以直接展示
```

### 步骤

```python
# 创建 src/extractor.py —— 信息抽取模块
from src.llm import chat
import json

EXTRACT_SYSTEM = """你是一个汽车CRM信息抽取助手。
从对话或文本中提取结构化信息，严格按JSON格式输出。

提取字段：
- customer_name: 客户姓名
- phone: 联系电话
- vehicle_model: 车型
- fault_description: 故障描述
- urgency: 紧急程度（高/中/低）
- action_items: 行动项列表
- warranty_related: 是否涉及保修（是/否）

如果某个字段无法从文本中提取，填null。
只输出JSON，不要输出其他内容。"""

def extract_info(text: str) -> dict:
    """从文本中提取结构化信息"""
    messages = [
        {"role": "system", "content": EXTRACT_SYSTEM},
        {"role": "user", "content": f"请从以下文本中提取信息：\n\n{text}"}
    ]
    
    result = chat(messages, temperature=0)
    
    # 解析JSON
    try:
        # 去掉可能的markdown代码块标记
        result = result.strip()
        if result.startswith("```"):
            result = result.split("```")[1]
            if result.startswith("json"):
                result = result[4:]
            result = result.strip()
        
        return json.loads(result)
    except json.JSONDecodeError:
        return {"error": "JSON解析失败", "raw_output": result}
```

```python
# 创建 test_extractor.py 测试
from src.extractor import extract_info
import json

# 测试：售后场景
text = """
客户张三打电话来说，他的比亚迪秦Plus启动不了了，
仪表盘上显示正常，但是打火没反应。他说车是2024年买的，
还在保修期内，希望尽快处理。电话是13800138000。
"""
result = extract_info(text)
print(json.dumps(result, ensure_ascii=False, indent=2))
```

### 知识点复习

```
Q: 为什么temperature设0？
A: 信息抽取需要确定性输出，同样的输入应该得到同样的结果。

Q: 为什么要处理markdown代码块？
A: 大模型经常在JSON外面加 ```json ... ```，
   直接json.loads会报错，需要先去掉。

Q: 如果AI输出的JSON格式不对怎么办？
A: 1. Prompt里强调"只输出JSON，不要其他内容"
   2. 用try-except兜底
   3. 后续可以用OpenAI的structured output功能（更可靠）
```

### ✅ 阶段3交付：输入对话文本，输出结构化JSON

---

## 阶段4：Tool Calling——语音创建工单（3天）

### 你需要知道的（最小知识）

```
1. Tool Calling：让AI不只是"说话"，还能"做事"
2. 工作原理：AI判断需要调用工具 → 返回工具名和参数 → 代码执行 → 结果返回AI
3. 对比：普通对话是"嘴炮"，Tool Calling是"实干"
```

### 知识速查：Tool Calling流程图

```
用户："帮张三创建一个维修工单，秦Plus启动困难"
       ↓
AI判断：需要调用 create_work_order 工具
       ↓
AI返回：tool_call = {
  "name": "create_work_order",
  "arguments": {"customer": "张三", "vehicle": "秦Plus", "fault": "启动困难"}
}
       ↓
你的代码：执行 create_work_order 函数，创建工单
       ↓
工具返回："工单WO-20260426-001已创建"
       ↓
AI基于工具结果回复用户："已为您创建维修工单WO-20260426-001..."
```

### 步骤

#### 4.1 搭建模拟数据库

```python
# 创建 src/database.py —— 模拟数据库（SQLite）
import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "mock_db", "crm.db")

def get_connection():
    """获取数据库连接"""
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """初始化数据库表"""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS customers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        phone TEXT,
        region TEXT,
        industry TEXT,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP
    )
    """)
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS work_orders (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        order_id TEXT UNIQUE NOT NULL,
        customer_name TEXT NOT NULL,
        vehicle_model TEXT,
        fault_description TEXT,
        status TEXT DEFAULT '待处理',
        created_at TEXT DEFAULT CURRENT_TIMESTAMP
    )
    """)
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS opportunities (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        customer_name TEXT NOT NULL,
        amount REAL,
        stage TEXT DEFAULT '初步接触',
        probability REAL DEFAULT 0.2,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP
    )
    """)
    
    conn.commit()
    conn.close()
    print("数据库初始化完成")

init_db()
```

#### 4.2 定义工具函数

```python
# 创建 src/tools/crm_tools.py —— CRM系统工具
from src.database import get_connection
from datetime import datetime
import random

def create_work_order(customer: str, vehicle: str, fault: str) -> str:
    """创建维修工单"""
    order_id = f"WO-{datetime.now().strftime('%Y%m%d')}-{random.randint(100,999)}"
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO work_orders (order_id, customer_name, vehicle_model, fault_description) VALUES (?, ?, ?, ?)",
        (order_id, customer, vehicle, fault)
    )
    conn.commit()
    conn.close()
    return f"工单{order_id}已创建，客户：{customer}，车型：{vehicle}，故障：{fault}，状态：待处理"

def query_warranty(customer: str, vehicle: str) -> str:
    """查询保修状态"""
    return f"客户{customer}的{vehicle}，整车保修期至2029年6月，三电保修期至2031年6月，当前在保修期内。"

def update_work_order_status(order_id: str, status: str) -> str:
    """更新工单状态"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE work_orders SET status = ? WHERE order_id = ?", (status, order_id))
    conn.commit()
    affected = cursor.rowcount
    conn.close()
    return f"工单{order_id}状态已更新为：{status}" if affected > 0 else f"未找到工单{order_id}"

def query_work_orders(customer: str = None, status: str = None) -> str:
    """查询工单列表"""
    conn = get_connection()
    cursor = conn.cursor()
    sql = "SELECT * FROM work_orders WHERE 1=1"
    params = []
    if customer:
        sql += " AND customer_name LIKE ?"
        params.append(f"%{customer}%")
    if status:
        sql += " AND status = ?"
        params.append(status)
    sql += " ORDER BY created_at DESC LIMIT 10"
    cursor.execute(sql, params)
    rows = cursor.fetchall()
    conn.close()
    if not rows:
        return "未找到匹配的工单"
    result = f"找到{len(rows)}个工单：\n"
    for row in rows:
        result += f"  - {row['order_id']} | {row['customer_name']} | {row['vehicle_model']} | {row['status']}\n"
    return result
```

#### 4.3 组装Tool Calling对话

```python
# 创建 src/tool_agent.py —— 带工具调用的对话Agent
import json
from openai import OpenAI
from src.config import OPENAI_API_KEY, OPENAI_BASE_URL, MODEL_NAME
from src.tools.crm_tools import create_work_order, query_warranty, update_work_order_status, query_work_orders

client = OpenAI(api_key=OPENAI_API_KEY, base_url=OPENAI_BASE_URL)

# 工具定义（告诉AI有哪些工具可用）
TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "create_work_order",
            "description": "创建维修工单",
            "parameters": {
                "type": "object",
                "properties": {
                    "customer": {"type": "string", "description": "客户姓名"},
                    "vehicle": {"type": "string", "description": "车型"},
                    "fault": {"type": "string", "description": "故障描述"}
                },
                "required": ["customer", "vehicle", "fault"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "query_warranty",
            "description": "查询车辆保修状态",
            "parameters": {
                "type": "object",
                "properties": {
                    "customer": {"type": "string", "description": "客户姓名"},
                    "vehicle": {"type": "string", "description": "车型"}
                },
                "required": ["customer", "vehicle"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "update_work_order_status",
            "description": "更新工单状态",
            "parameters": {
                "type": "object",
                "properties": {
                    "order_id": {"type": "string", "description": "工单号"},
                    "status": {"type": "string", "description": "新状态", "enum": ["待处理", "处理中", "已完成", "已关闭"]}
                },
                "required": ["order_id", "status"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "query_work_orders",
            "description": "查询工单列表",
            "parameters": {
                "type": "object",
                "properties": {
                    "customer": {"type": "string", "description": "客户姓名（可选）"},
                    "status": {"type": "string", "description": "工单状态（可选）"}
                }
            }
        }
    }
]

TOOL_MAP = {
    "create_work_order": create_work_order,
    "query_warranty": query_warranty,
    "update_work_order_status": update_work_order_status,
    "query_work_orders": query_work_orders,
}

SYSTEM_PROMPT = """你是一个汽车CRM助手，可以帮助管理维修工单和查询保修信息。
当用户需要创建工单、查询保修、更新工单状态时，请使用相应工具。
回复时请用中文，语气专业友好。"""

def tool_chat(user_input: str, history: list = None) -> str:
    """带工具调用的对话"""
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    if history:
        messages.extend(history)
    messages.append({"role": "user", "content": user_input})
    
    # 第一次调用：AI决定是否调用工具
    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=messages,
        tools=TOOLS,
        temperature=0.1
    )
    
    message = response.choices[0].message
    
    # 不需要工具，直接返回
    if not message.tool_calls:
        return message.content
    
    # 需要工具，逐个执行
    messages.append(message)
    for tool_call in message.tool_calls:
        func_name = tool_call.function.name
        func_args = json.loads(tool_call.function.arguments)
        print(f"  🔧 调用工具：{func_name}({func_args})")
        
        result = TOOL_MAP[func_name](**func_args) if func_name in TOOL_MAP else f"未知工具：{func_name}"
        
        messages.append({
            "role": "tool",
            "content": str(result),
            "tool_call_id": tool_call.id
        })
    
    # 第二次调用：基于工具结果生成最终回复
    final_response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=messages,
        temperature=0.1
    )
    return final_response.choices[0].message.content
```

### 知识点复习

```
Q: Tool Calling的两次API调用是什么意思？
A: 第1次：把用户消息+工具定义发给AI，AI决定调什么工具、传什么参数
   第2次：把工具执行结果发回给AI，AI基于结果生成最终回复

Q: tools参数里的JSON Schema是什么？
A: 告诉AI每个工具需要什么参数、什么类型。AI会按格式生成参数。

Q: 如果AI调错了工具怎么办？
A: 1. 检查工具的description是否清晰
   2. 检查参数描述是否明确
   3. 在system prompt里加引导
```

### ✅ 阶段4交付：对话中AI自动识别意图，调用工具创建工单/查询保修

---

## 阶段5：Text-to-SQL——智能问数（2天）

### 你需要知道的（最小知识）

```
1. Text-to-SQL：把自然语言问题转成SQL查询
2. 为什么需要：老板想看数据但不会写SQL，AI帮他写
3. 核心：把数据库表结构告诉AI → AI生成SQL → 执行SQL → 格式化结果
```

### 步骤

```python
# 创建 src/text2sql.py —— 智能问数模块
from src.llm import chat
from src.database import get_connection
import json

DB_SCHEMA = """
数据库表结构：

1. customers（客户表）
   - id: 主键
   - name: 客户姓名
   - phone: 联系电话
   - region: 所在区域
   - industry: 所属行业
   - created_at: 创建时间

2. work_orders（工单表）
   - id: 主键
   - order_id: 工单号
   - customer_name: 客户姓名
   - vehicle_model: 车型
   - fault_description: 故障描述
   - status: 状态（待处理/处理中/已完成/已关闭）
   - created_at: 创建时间

3. opportunities（商机表）
   - id: 主键
   - customer_name: 客户姓名
   - amount: 商机金额
   - stage: 阶段（初步接触/需求确认/方案报价/商务谈判/签约）
   - probability: 成交概率
   - created_at: 创建时间
"""

TEXT2SQL_SYSTEM = f"""你是一个数据查询助手。根据用户的自然语言问题，生成对应的SQL查询。

{DB_SCHEMA}

规则：
1. 只生成SQLite兼容的SQL
2. 只输出一条SQL语句，不要其他内容
3. 不要使用DELETE、UPDATE、DROP等危险操作
4. 查询结果限制最多100条（加LIMIT）
5. 日期比较用字符串格式 'YYYY-MM-DD'
"""

def text2sql(question: str) -> str:
    """自然语言转SQL"""
    messages = [
        {"role": "system", "content": TEXT2SQL_SYSTEM},
        {"role": "user", "content": question}
    ]
    sql = chat(messages, temperature=0)
    sql = sql.strip()
    if sql.startswith("```"):
        sql = sql.split("```")[1]
        if sql.startswith("sql"):
            sql = sql[3:]
        sql = sql.strip()
    return sql.rstrip(";")

def smart_query(question: str) -> str:
    """智能问数：自然语言问题 → SQL → 执行 → 格式化结果"""
    # 1. 生成SQL
    sql = text2sql(question)
    print(f"  📊 生成SQL: {sql}")
    
    # 2. 执行SQL
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(sql)
        rows = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]
        conn.close()
    except Exception as e:
        return f"SQL执行出错：{e}\n生成的SQL：{sql}"
    
    # 3. 格式化结果
    if not rows:
        return f"查询无结果。\n生成SQL：{sql}"
    
    results = [dict(zip(columns, row)) for row in rows]
    
    format_prompt = f"""用户问题：{question}
SQL查询结果：{json.dumps(results, ensure_ascii=False, default=str)}

请用简洁的中文回答用户问题，把查询结果整理成易读的格式。"""
    
    return chat([{"role": "user", "content": format_prompt}], temperature=0.1)
```

### 知识点复习

```
Q: Text-to-SQL的核心难点是什么？
A: 1. 表结构要描述清楚（AI不知道你有哪些表）
   2. SQL安全性（防止生成DELETE/DROP）
   3. 复杂查询（多表JOIN）容易出错
   4. 结果格式化（裸SQL结果用户看不懂）

Q: 怎么提升SQL生成准确率？
A: 1. 表结构描述越详细越好（字段含义、枚举值、示例数据）
   2. 加few-shot示例（"类似问题→对应SQL"）
   3. 加安全校验（检查SQL是否包含危险操作）
```

### ✅ 阶段5交付：输入自然语言问题，输出格式化的查询结果

---

## 阶段6：Streamlit界面——5合1 MVP（3天）

### 你需要知道的（最小知识）

```
1. Streamlit：用Python写Web界面的最简方式，不用写HTML/CSS/JS
2. 核心概念：st.title、st.text_input、st.button、st.write
3. 多页面：每个功能一个.py文件，用侧边栏自动导航
```

### 项目结构

```
CRM-AI-Project/
├── app.py                    # 主入口（首页）
├── pages/
│   ├── 1_🔧_故障诊断.py
│   ├── 2_📝_信息抽取.py
│   ├── 3_📋_工单管理.py
│   ├── 4_📊_智能问数.py
│   └── 5_💬_智能助手.py
├── src/
│   ├── config.py
│   ├── llm.py
│   ├── rag.py
│   ├── diagnose.py
│   ├── extractor.py
│   ├── tool_agent.py
│   ├── text2sql.py
│   ├── database.py
│   ├── tools/
│   │   └── crm_tools.py
│   └── agents/
├── data/
│   ├── knowledge_base/
│   ├── mock_db/
│   └── chroma_db/
├── .env
└── requirements.txt
```

### 主入口

```python
# app.py
import streamlit as st

st.set_page_config(page_title="汽车CRM AI智能系统", page_icon="🚗", layout="wide")

st.title("🚗 汽车CRM AI智能系统")
st.markdown("---")

st.markdown("""
### 系统功能

| 模块 | 功能 | 技术实现 |
|------|------|----------|
| 🔧 故障诊断 | 输入故障症状，输出诊断建议 | RAG知识库检索 |
| 📝 信息抽取 | 从对话中提取结构化信息 | LLM结构化输出 |
| 📋 工单管理 | 对话创建/查询工单 | Tool Calling |
| 📊 智能问数 | 自然语言查询业务数据 | Text-to-SQL |
| 💬 智能助手 | 综合对话，自动路由 | LangGraph多Agent |

👈 请从左侧选择功能模块
""")

st.caption("基于 LangGraph + RAG + Tool Calling | 对标纷享销客AI销售助理")
```

### 故障诊断页面

```python
# pages/1_🔧_故障诊断.py
import streamlit as st
from src.diagnose import diagnose

st.title("🔧 售后故障诊断")
st.markdown("输入故障症状描述，AI基于知识库给出诊断建议。")

examples = st.selectbox("选择示例问题", [
    "自定义输入",
    "秦Plus启动困难，仪表盘显示正常",
    "唐DM行驶中底盘异响",
    "宋Plus EV续航突然大幅下降"
])

user_input = "" if examples == "自定义输入" else examples
fault = st.text_area("故障描述", value=user_input, height=100)

if st.button("🔍 开始诊断", type="primary"):
    if fault:
        with st.spinner("正在诊断中..."):
            result = diagnose(fault)
        st.markdown("### 诊断结果")
        st.markdown(result)
    else:
        st.warning("请输入故障描述")
```

### 工单管理页面

```python
# pages/3_📋_工单管理.py
import streamlit as st
from src.tool_agent import tool_chat

st.title("📋 工单管理")
st.markdown("用自然语言创建工单、查询保修、查看工单列表。")

examples = ["自定义输入", "帮张三创建一个维修工单，秦Plus启动困难",
            "查一下张三的秦Plus还在保修期内吗", "查看所有待处理的工单"]

selected = st.selectbox("选择示例", examples)
user_input = "" if selected == "自定义输入" else selected
command = st.text_area("输入指令", value=user_input, height=80)

if st.button("执行", type="primary"):
    if command:
        with st.spinner("处理中..."):
            result = tool_chat(command)
        st.markdown("### 结果")
        st.markdown(result)
    else:
        st.warning("请输入指令")
```

### 智能问数页面

```python
# pages/4_📊_智能问数.py
import streamlit as st
from src.text2sql import smart_query

st.title("📊 智能问数")
st.markdown("用自然语言查询业务数据，AI自动生成SQL。")

examples = ["自定义输入", "总共有多少客户？", "商机金额超过50万的有几个？",
            "各阶段的商机金额分别是多少？", "今天创建了多少工单？"]

selected = st.selectbox("选择示例", examples)
user_input = "" if selected == "自定义输入" else selected
question = st.text_area("输入问题", value=user_input, height=80)

if st.button("查询", type="primary"):
    if question:
        with st.spinner("查询中..."):
            result = smart_query(question)
        st.markdown("### 查询结果")
        st.markdown(result)
    else:
        st.warning("请输入问题")
```

### 运行

```bash
streamlit run app.py
```

### ✅ 阶段6交付：5个功能的Web界面MVP，浏览器可访问

---

## 阶段7：LangGraph多Agent协作（4天）

### 你需要知道的（最小知识）

```
1. LangGraph：用"图"的方式编排多个Agent的协作流程
2. 核心概念：
   - Node（节点）：一个处理步骤（一个Agent/一个函数）
   - Edge（边）：节点之间的跳转条件
   - State（状态）：所有节点共享的数据
3. 为什么需要：单Agent能做的有限，多Agent可以分工协作
```

### 知识速查：LangGraph vs 纯Tool Calling

```
纯Tool Calling（阶段4）：
  用户 → AI决定调什么工具 → 执行 → 回复
  问题：AI不知道什么时候该"诊断"什么时候该"创建工单"

LangGraph多Agent（阶段7）：
  用户 → 路由器判断意图 → 分发给专业Agent → 协作完成
  → 诊断Agent专注诊断，工单Agent专注工单，各司其职
```

### 步骤

```python
# 创建 src/agents/graph.py —— LangGraph多Agent编排
from typing import TypedDict
from langgraph.graph import StateGraph, END
from src.diagnose import diagnose
from src.tool_agent import tool_chat
from src.text2sql import smart_query
from src.extractor import extract_info
from src.llm import chat
import json

# 1. 定义共享状态
class AgentState(TypedDict):
    user_input: str
    intent: str
    result: str

# 2. 意图识别节点
def intent_router(state: AgentState) -> AgentState:
    """识别用户意图"""
    ROUTE_PROMPT = """判断用户的意图，只输出以下之一：
- diagnose：故障诊断（描述故障症状、问怎么修）
- action：执行操作（创建工单、查询保修、更新状态）
- query：数据查询（问数量、问统计、问列表）
- extract：信息抽取（提取对话中的关键信息）
- chat：一般对话（其他情况）

用户输入：{input}
只输出意图类别，不要其他内容。"""
    
    intent = chat([{"role": "user", "content": ROUTE_PROMPT.format(input=state["user_input"])}], temperature=0)
    intent = intent.strip().lower()
    valid_intents = ["diagnose", "action", "query", "extract", "chat"]
    if intent not in valid_intents:
        intent = "chat"
    state["intent"] = intent
    return state

# 3. 各专业Agent节点
def diagnose_agent(state: AgentState) -> AgentState:
    state["result"] = diagnose(state["user_input"])
    return state

def action_agent(state: AgentState) -> AgentState:
    state["result"] = tool_chat(state["user_input"])
    return state

def query_agent(state: AgentState) -> AgentState:
    state["result"] = smart_query(state["user_input"])
    return state

def extract_agent(state: AgentState) -> AgentState:
    result = extract_info(state["user_input"])
    state["result"] = json.dumps(result, ensure_ascii=False, indent=2)
    return state

def chat_agent(state: AgentState) -> AgentState:
    state["result"] = chat([
        {"role": "system", "content": "你是汽车CRM助手，请友好专业地回答用户问题。"},
        {"role": "user", "content": state["user_input"]}
    ])
    return state

# 4. 构建图
def build_graph():
    workflow = StateGraph(AgentState)
    
    workflow.add_node("router", intent_router)
    workflow.add_node("diagnose", diagnose_agent)
    workflow.add_node("action", action_agent)
    workflow.add_node("query", query_agent)
    workflow.add_node("extract", extract_agent)
    workflow.add_node("chat", chat_agent)
    
    workflow.set_entry_point("router")
    
    # 条件边：根据意图路由
    workflow.add_conditional_edges(
        "router",
        lambda state: state["intent"],
        {
            "diagnose": "diagnose",
            "action": "action",
            "query": "query",
            "extract": "extract",
            "chat": "chat"
        }
    )
    
    # 所有Agent执行完都结束
    for node in ["diagnose", "action", "query", "extract", "chat"]:
        workflow.add_edge(node, END)
    
    return workflow.compile()

graph = build_graph()

def run_agent(user_input: str) -> dict:
    """运行多Agent系统"""
    return graph.invoke({"user_input": user_input, "intent": "", "result": ""})
```

### 综合助手页面

```python
# pages/5_💬_智能助手.py
import streamlit as st
from src.agents.graph import run_agent

st.title("💬 智能助手")
st.markdown("统一入口，AI自动识别意图并路由到专业Agent处理。")

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("请输入您的问题..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    with st.chat_message("assistant"):
        with st.spinner("思考中..."):
            result = run_agent(prompt)
        st.markdown(result["result"])
        st.caption(f"🤖 路由到：{result['intent']} Agent")
    
    st.session_state.messages.append({"role": "assistant", "content": result["result"]})
```

### 知识点复习

```
Q: LangGraph的State是什么？
A: 所有节点共享的数据字典。每个节点读取State、修改State、传给下一个节点。
   类似于"流水线上的工件"，每个工位加工一下传下去。

Q: conditional_edges是什么？
A: 条件边。根据当前State决定走哪条路。
   比如intent="diagnose"就走诊断节点，intent="query"就走查询节点。

Q: 为什么比纯Tool Calling好？
A: Tool Calling让一个AI决定一切，容易混乱。
   LangGraph让专业Agent各司其职，流程可控、结果可预期。
```

### ✅ 阶段7交付：统一入口，AI自动路由到专业Agent

---

## 阶段8：知识图谱——联系人关系（3天）

### 你需要知道的（最小知识）

```
1. 知识图谱：用"实体-关系-实体"的三元组表示数据关联
2. 为什么需要：CRM中客户关系是网状的，传统数据库表达不了
3. 三元组示例：(张三) -[属于]-> (华晨汽配)、(李总) -[决策]-> (采购)
```

### 步骤

```python
# 创建 src/knowledge_graph.py —— 知识图谱模块
import networkx as nx
from pyvis.network import Network
from src.llm import chat
import json

# 用NetworkX构建内存图（轻量方案，不需要Neo4j）
G = nx.DiGraph()

# 预置一些示例数据
SAMPLE_TRIPLES = [
    ("华晨汽配", "有联系人", "李总"),
    ("华晨汽配", "有联系人", "王经理"),
    ("李总", "职位", "总经理"),
    ("王经理", "职位", "销售总监"),
    ("李总", "决策", "采购审批"),
    ("王经理", "影响", "李总"),
    ("华晨汽配", "行业", "汽车零部件"),
    ("华晨汽配", "区域", "华东"),
    ("张三", "负责客户", "华晨汽配"),
    ("华晨汽配", "商机阶段", "方案报价"),
    ("华晨汽配", "商机金额", "50万"),
]

for src, rel, tgt in SAMPLE_TRIPLES:
    G.add_edge(src, tgt, label=rel)

def extract_triples(text: str) -> list:
    """从文本中抽取三元组"""
    EXTRACT_TRIPLE_PROMPT = """从以下文本中提取实体关系三元组。

格式：每行一个三元组，用 | 分隔：实体1 | 关系 | 实体2

示例：
华晨汽配 | 有联系人 | 李总
李总 | 职位 | 总经理

文本：
{text}

只输出三元组，每行一个，不要其他内容。"""
    
    result = chat([{"role": "user", "content": EXTRACT_TRIPLE_PROMPT.format(text=text)}], temperature=0)
    
    triples = []
    for line in result.strip().split("\n"):
        parts = [p.strip() for p in line.split("|")]
        if len(parts) == 3:
            triples.append(tuple(parts))
    return triples

def add_triples_to_graph(triples: list):
    """将三元组添加到图"""
    for src, rel, tgt in triples:
        G.add_edge(src, tgt, label=rel)

def query_graph(entity: str, depth: int = 2) -> str:
    """查询实体的关联信息"""
    if entity not in G:
        return f"未找到实体：{entity}"
    
    result = f"实体【{entity}】的关联信息：\n"
    
    # 出边：该实体指向谁
    for src, tgt, data in G.out_edges(entity, data=True):
        result += f"  → [{data['label']}] → {tgt}\n"
    
    # 入边：谁指向该实体
    for src, tgt, data in G.in_edges(entity, data=True):
        result += f"  ← [{data['label']}] ← {src}\n"
    
    return result

def visualize_graph(output_file: str = "graph.html"):
    """生成交互式图谱可视化"""
    net = Network(height="600px", width="100%", directed=True)
    net.from_nx(G)
    net.show(output_file)
    return output_file
```

### 图谱页面

```python
# pages/6_🕸️_关系图谱.py
import streamlit as st
from src.knowledge_graph import extract_triples, add_triples_to_graph, query_graph, visualize_graph

st.title("🕸️ 联系人关系图谱")
tab1, tab2 = st.tabs(["查询关系", "添加关系"])

with tab1:
    entity = st.text_input("输入实体名称", value="华晨汽配")
    if st.button("查询", type="primary"):
        result = query_graph(entity)
        st.markdown(result)

with tab2:
    text = st.text_area("输入文本，AI自动抽取关系", height=100,
        value="今天拜访了明德科技的赵总，赵总是CTO，技术决策权在他手里。他们公司主要做智能座舱，在华南区域。")
    if st.button("抽取并添加", type="primary"):
        triples = extract_triples(text)
        st.write(f"抽取到 {len(triples)} 个三元组：")
        for t in triples:
            st.write(f"  {t[0]} → [{t[1]}] → {t[2]}")
        add_triples_to_graph(triples)
        st.success("已添加到图谱！")
```

### 知识点复习

```
Q: 为什么用NetworkX不用Neo4j？
A: MVP阶段用内存图就够了，不需要装数据库。
   NetworkX是Python库，pip install就有。
   后续如果需要持久化，可以迁移到Neo4j。

Q: 三元组抽取的准确率怎么提升？
A: 1. Prompt里加更多示例（few-shot）
   2. 定义关系类型的枚举（"有联系人/职位/决策/影响/..."）
   3. 让AI先识别实体，再识别关系（两步法）
```

### ✅ 阶段8交付：可查询、可添加、可可视化的联系人关系图谱

---

## 阶段9：打磨包装——准备面试（持续）

### 9.1 写README

```markdown
# 🚗 汽车CRM AI智能系统

> 基于真实汽车行业经验（比亚迪售后+瑞能CRM售前），用AI大模型重构售前售后CRM流程。
> 对标纷享销客AI销售助理，差异化：售后智能诊断 + 跨系统数据关联 + 垂直行业知识图谱。

## 核心功能
- 🔧 售后故障诊断（RAG知识库）
- 📝 对话信息抽取（结构化输出）
- 📋 工单管理（Tool Calling）
- 📊 智能问数（Text-to-SQL）
- 💬 多Agent协作（LangGraph意图路由）
- 🕸️ 联系人关系图谱（知识图谱）

## 技术栈
Python / LangGraph / RAG(Chroma) / Tool Calling / Text-to-SQL / 
Knowledge Graph(NetworkX) / Streamlit / FastAPI / SQLite

## 快速开始
\```bash
pip install -r requirements.txt
streamlit run app.py
\```
```

### 9.2 准备面试故事（STAR法）

```
故事1：RAG诊断（展示你理解RAG原理）
  S：比亚迪售后故障信息碎片化，诊断耗时长
  T：用RAG构建知识库，实现智能诊断
  A：构建了故障案例+保修政策+维修工序的知识库，
     用RecursiveCharacterTextSplitter切分（chunk_size=500），
     Chroma向量检索（k=3），Prompt要求引用来源控制幻觉
  R：诊断建议有依据，可溯源，幻觉率显著降低

故事2：Tool Calling工单（展示你理解Agent交互）
  S：售后需要手动在DMS系统创建工单，效率低
  T：用Tool Calling实现对话式工单创建
  A：定义了4个工具函数，通过OpenAI Tool Calling协议
     实现两次API调用（意图识别→工具执行→结果总结）
  R：一句话即可创建工单，模拟测试效率提升3倍

故事3：LangGraph多Agent（展示你有架构思维）
  S：单Agent无法同时处理诊断、工单、查询等多种意图
  T：用LangGraph构建多Agent路由系统
  A：设计了5个专业Agent + 1个路由器，
     用条件边实现意图路由，各Agent独立维护
  R：意图识别准确率90%+，专业场景回复质量显著提升

故事4：对标纷享销客（展示你有产品思维）
  S：纷享销客AI销售助理只做售前，缺售后诊断
  T：设计差异化方案，补齐售后+图谱+跨系统集成
  A：分析了纷享销客6大能力，找到3个差异化点
  R：方案覆盖售前18环节+售后9环节，比竞品更完整
```

### 9.3 每周自检清单

```
□ 这周项目有没有跑通一个新功能？
□ 我能不能给别人演示这个功能？
□ 我能不能讲清这个功能用了什么技术、为什么选它？
□ 遇到了什么问题，怎么解决的？（记录下来，面试要用）
□ 下周要做什么？（对照里程碑）
```

---

## 附录A：每个阶段对应的技术知识点

| 阶段 | 核心技术 | 必须理解的概念 | 可以先跳过的 |
|------|---------|--------------|------------|
| 0 | Python环境 | pip、venv、.env | poetry、conda |
| 1 | OpenAI API | system/user/assistant、temperature | 流式输出、function calling |
| 2 | RAG | 向量化、检索、chunk切分 | Embedding模型原理、HNSW索引 |
| 3 | 结构化输出 | JSON、Pydantic | OpenAI structured output |
| 4 | Tool Calling | 两次API调用、工具定义 | LangChain Tool装饰器 |
| 5 | Text-to-SQL | SQL基础、Schema描述 | 复杂JOIN、子查询优化 |
| 6 | Streamlit | st.title/input/button/write | 自定义组件、部署 |
| 7 | LangGraph | State、Node、Edge | 持久化、人机交互节点 |
| 8 | 知识图谱 | 三元组、实体关系 | Neo4j、图数据库查询 |

---

## 附录B：遇到问题怎么办

```
1. 报错了，看不懂
   → 复制报错信息，问AI助手（"这个报错是什么意思？怎么修？"）
   → 90%的问题AI都能帮你解决

2. 代码跑通了但效果不好
   → 先记录下来，继续下一个功能
   → 效果优化是后面的事，先跑通最重要

3. 不知道下一步做什么
   → 看上面的路线图，当前阶段做完了吗？
   → 没做完就继续，做完了就进下一阶段

4. 感觉进度太慢
   → 每天推进一点点就是胜利
   → 2小时调一个参数 = 面试多8000块月薪

5. 想到更好的方案
   → 记下来，别现在改
   → MVP完成后再迭代，先跑通再优化
```

---

## 附录C：每日时间分配

```
总学习时间：6-8小时/天

├── 课程学习（3-4小时）  ← 优先级最高，不能丢
├── 项目开发（2-3小时）  ← 每天推进一点点
└── 复习+刷题（1小时）  ← 保持手感

项目开发的"最小推进"原则：
每天至少做一件事（哪怕很小）：
- 改一个Prompt
- 加一个Tool函数
- 修一个Bug
- 写一个测试数据
- 优化一个界面按钮

关键不是每天做多少，而是每天都做。
```

---

## 附录D：Demo到企业级——你的行业经验在这里变现

> 面试中，光能演示Demo只能证明"你会用技术"。
> 能讲清楚Demo和企业级的差距，才证明"你懂业务"。
> **这就是你和培训班出来的纯技术人最大的区别。**

### Demo vs 企业级：差距在哪

```
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│  Demo能跑通：                  企业级还要考虑：              │
│                                                             │
│  ✅ AI能回答问题               → 回答的权限对不对？          │
│  ✅ 能创建工单                 → 谁有权限创建？谁审批？      │
│  ✅ 能查数据                   → 销售只能看自己的客户吗？    │
│  ✅ 单用户测试OK               → 100人同时用怎么办？        │
│  ✅ 模拟数据                   → 真实数据从哪来？怎么同步？  │
│  ✅ API Key明文                → 密钥管理怎么做？            │
│                                                             │
│  你在比亚迪和瑞能见过这些问题的真实场景，                    │
│  这是培训班教不出来的。                                      │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### 企业级必须考虑的6个维度

#### 1. 角色权限控制（RBAC）

```
你在瑞能用纷享销客时就知道：

角色            看到的数据                    能做的操作
─────────────────────────────────────────────────────────
销售专员        只看自己的客户和商机           创建/编辑自己的
销售经理        看本团队所有客户               审批/分配/查看团队
区域总监        看本区域所有数据               审批/导出/跨团队调拨
售后技师        只看分配给自己的工单           更新工单状态/添加维修记录
售后主管        看本店所有工单                 分配工单/审批索赔
系统管理员      全部数据                       用户管理/权限配置

实现方式（Demo里怎么加）：
1. 在SQLite加一张 users 表（id, name, role, team_id）
2. 每次查询加 WHERE 过滤条件
3. 每次操作前检查 role 是否有权限

代码示例：
  def check_permission(user_role: str, action: str) -> bool:
      permissions = {
          "销售专员": ["view_own", "create_customer", "edit_own"],
          "销售经理": ["view_team", "approve", "assign"],
          "区域总监": ["view_region", "export", "transfer"],
      }
      return action in permissions.get(user_role, [])

面试话术：
  "我在瑞能用纷享销客时，销售只能看自己的客户，经理能看全团队的。
   所以我在项目里设计了RBAC权限层，不同角色看到的数据和操作权限不同。"
```

#### 2. 数据权限隔离

```
你在比亚迪就知道：

数据维度        隔离规则
──────────────────────────────────────────────
按组织          4S店A看不到4S店B的客户数据
按团队          华东销售组看不到华南的商机
按个人          销售张三只能编辑自己的客户
按层级          专员看明细，总监看汇总

实现方式：
  # 在每次查询时注入权限过滤
  def get_customers(user):
      base_sql = "SELECT * FROM customers WHERE 1=1"
      if user.role == "销售专员":
          base_sql += f" AND owner_id = {user.id}"
      elif user.role == "销售经理":
          base_sql += f" AND team_id = {user.team_id}"
      elif user.role == "区域总监":
          base_sql += f" AND region = '{user.region}'"
      # 管理员不加过滤
      return execute_sql(base_sql)

面试话术：
  "企业CRM里数据隔离是硬需求。我在比亚迪时，不同4S店的数据是隔离的，
   所以我在Text-to-SQL模块里加了权限注入，生成的SQL自动带上过滤条件。"
```

#### 3. 多租户（SaaS场景）

```
纷享销客为什么能服务几百家企业？多租户架构。

租户A（车企A）的数据 → 完全隔离 → 租户B（车企B）的数据

实现方式：
  - 共享数据库，tenant_id字段隔离（最简单）
  - 独立Schema，每个租户一个Schema
  - 独立数据库（最安全但成本高）

Demo里怎么做：
  # 每张表加 tenant_id
  CREATE TABLE customers (
      id INTEGER PRIMARY KEY,
      tenant_id INTEGER NOT NULL,  -- 租户ID
      name TEXT,
      ...
  );

  # 查询时自动过滤
  SELECT * FROM customers WHERE tenant_id = ? AND ...

面试话术：
  "我了解SaaS CRM的多租户架构。纷享销客用的共享数据库+tenant_id隔离，
   我在项目里也预留了tenant_id字段，方便后续扩展。"
```

#### 4. 系统集成层

```
你在瑞能就知道，CRM不是孤岛：

你的CRM系统 → 需要对接 ↓
  ├─ DMS（经销商管理系统）   → 同步车辆/客户数据
  ├─ ERP（金蝶/用友）       → 同步订单/财务数据
  ├─ 400客服系统            → 同步来电/投诉记录
  ├─ 企微/钉钉              → 同步沟通记录
  ├─ 泛微OA                 → 同步审批流程
  ├─ MES（制造执行）         → 同步生产/备件数据
  ├─ SRM（供应商管理）       → 同步供应商信息
  └─ 物流系统                → 同步配送状态

实现方式（Demo里怎么体现）：
  1. 在Tool Calling里加更多模拟工具
  2. 用统一的API网关模式封装

  @tool
  def query_dms(vin: str) -> str:
      """查询DMS系统中的车辆信息（模拟接口）"""
      # 真实项目：调用DMS的REST API
      return f"VIN: {vin}, 车型: 秦Plus, 购车日期: 2024-03-15, 4S店: 深圳XX店"

  @tool
  def query_erp(order_no: str) -> str:
      """查询ERP系统中的订单状态（模拟接口）"""
      return f"订单: {order_no}, 状态: 已发货, 预计到货: 2026-05-01"

面试话术：
  "我在瑞能时，CRM要对接DMS、ERP、400客服等十几个系统。
   所以我的项目设计了统一的Tool Calling网关，每个外部系统封装成一个工具函数，
   AI可以自动选择调用哪个系统获取数据。"
```

#### 5. 数据安全与合规

```
汽车行业特殊的数据安全要求：

  - 客户手机号/身份证号脱敏显示（138****0000）
  - 操作日志审计（谁在什么时间查了什么数据）
  - 数据导出审批（防止批量泄露客户信息）
  - AI回复过滤（不能把内部成本价告诉客户）

Demo里怎么做：
  def mask_phone(phone: str) -> str:
      """手机号脱敏"""
      return phone[:3] + "****" + phone[-4:]

  def log_access(user, action, target):
      """操作审计日志"""
      log = {"user": user, "action": action, "target": target, "time": now()}
      save_to_audit_log(log)

面试话术：
  "在汽车行业，客户数据安全是红线。我在项目里做了手机号脱敏和操作审计日志，
   AI回复也会经过规则引擎过滤敏感信息。"
```

#### 6. 高可用与性能

```
Demo：1个人用，1秒响应就行
企业：100人同时用，99.9%可用性

需要考虑的：
  - 大模型API超时/降级（备选模型、缓存热门问答）
  - 数据库并发（连接池、读写分离）
  - 异步处理（创建工单不阻塞对话）
  - 会话管理（100人同时对话的状态隔离）

面试话术：
  "企业级AI应用要考虑降级策略。我在项目里设计了双模型方案，
   主模型超时自动切换到轻量模型，热门问答缓存到Redis避免重复调用API。
   这些是在Demo阶段不会遇到、但生产环境必须解决的问题。"
```

### 面试加分结构：三层递进

```
面试官问："你这个项目是Demo还是能上生产的？"

你的回答（三层递进，展示系统思维）：

第一层（承认差距）：
  "目前是Demo阶段，核心功能跑通了，5个模块都能演示。"

第二层（讲清你知道差距在哪）：
  "但我很清楚Demo到企业级还有几个关键差距：
   1. 角色权限控制——不同岗位看到的数据和操作权限不同
   2. 数据隔离——多4S店/多团队的数据要隔离
   3. 系统集成——CRM要对接DMS、ERP、400客服等十几个系统
   4. 数据安全——客户信息脱敏、操作审计、AI回复过滤
   5. 高可用——大模型降级策略、会话状态隔离
   这些我在比亚迪和瑞能都见过真实场景。"

第三层（讲清你已经有方案）：
  "所以我预留了扩展点：
   - 数据库表都设计了owner_id和tenant_id字段
   - Tool Calling工具函数封装了外部系统接口
   - AI回复前加了规则引擎过滤层
   后续扩展只需要加业务逻辑，不需要改架构。"

这个回答的效果：
  面试官心理："这人不只是会写代码，他是真的懂企业怎么做系统的。"
```

### 在项目里如何体现（最小成本）

```
不用真的把6个维度全实现，但要让面试官看到你"想到了"：

1. 数据库加字段（5分钟）
   → 所有表加 owner_id、team_id、tenant_id
   → 查询时注释写 "WHERE owner_id = ? # 数据权限隔离"

2. 加权限检查函数（10分钟）
   → check_permission(user_role, action)
   → 每个Tool Calling工具里调用

3. 加数据脱敏（5分钟）
   → mask_phone()、mask_id_card()
   → AI回复后处理时调用

4. 加审计日志（10分钟）
   → audit_log 表记录所有操作
   → 每次关键操作后写入

5. 在README里写一节"企业级扩展方案"（20分钟）
   → 列出6个维度的设计思路
   → 面试官看到你就不是只会做Demo的人

总成本：50分钟
面试价值：从"会写代码"升级到"懂企业系统"
```

#### 7. 企业级PaaS能力对标（加分项！）

> 这部分来自**纷享销客PaaS平台架构**和**泛微九氚汇方案**，是大多数培训班项目完全没有的。

**四流合一（来自纷享销客）**：

| 流程 | 说明 | 你的项目中对应什么 |
|------|------|------------------|
| 审批流 | 合同评审、报价审核 | LangGraph状态机 + 条件节点 |
| 业务流BPM | 立项→方案→报价→签约→交付 | 阶段推进器 + Next Best Action |
| 工作流 | 任务分配、通知、超时预警 | 自动化Agent + 定时触发 |
| 阶段推进器 | 商机阶段管理 | 商机推进Agent |

**多维度数据权限（来自纷享销客权限架构）**：

面试可以这样说：
> "我在瑞能用纷享销客时，它的权限体系有4个维度——组织维度（总部/子公司/部门）、数据归属（私有/公开/共享）、多维树（按地区/产品线）、角色控制。我在项目里参考这个设计了RBAC+数据权限两层模型。"

**BI数据分析架构（来自纷享销客+泛微）**：

| 能力 | 你怎么在项目里体现 |
|------|-------------------|
| 多维交叉分析 | Text-to-SQL 支持按多维度查询 |
| 下钻查看明细 | 分层聚合 + 点击展开详情 |
| 效果验证器(泛微) | 营销活动→线索→商机→合同的全链路归因分析 |
| 数字名片(泛微) | 电子名片 + 关系网构建 + 微信生态协同 |

> **这些内容在【5个月完整落地.md】中有详细设计和实现计划，8月份全部落地。**

#### 8. 嵌入式AI设计理念（来自纷享销客AI白皮书）⭐面试必讲

**核心理念**："在合适的时间问对问题，才是关键。"

| 对比 | 嵌入式AI（我们主策略） | 对话式AI |
|------|----------------------|---------|
| 触发 | 业务场景自动触发 | 用户主动提问 |
| 用户要求 | 低——系统引导 | 高——需知道怎么问 |

**15种Agent类型**：客户互动/情报洞察/销售教练/智能BI/语音识别/文档生成/智能问答/知识库/智能预警/邮件助手/竞品分析/培训助手/智能审批/对话式Agent/低代码编程

**53个LTC AI场景**：线索获取(4)→线索转化(4)→商机管理(4)→方案报价(4)→招投标合同(3)→订单交付(3)→回款续费(4)→复盘赋能(4)→经营分析(3)→通用能力(10)→BI分析(4)→Agent工作流(6)

> 详细清单见【5个月完整落地.md】

#### 9. AI价值主张 + 建设优先级（来自纷享销客白皮书）

**销售期待 → Agent映射**：工作减负(Tool Calling)、增强获客(线索挖掘+客户分析)、提升赢率(赢率预测+NBA)、辅助成长(销冠复制+培训)

**管理者期待 → 能力映射**：业绩提升(线索评分)、组织提能(知识库+文档生成)、管理提效(质检+看板)、复制赢单(销售助手+方法论)

**建设5原则**：平台优先 > 深度优先；增效 > 降本；**高频 > 低频**（售后诊断先做！）；用户 > 管理员；嵌入式 > 对话式

---

---

## 最重要的提醒

```
你现在最大的风险不是技术不够，而是迟迟不开始。

蓝图已经足够完善了，路线图已经足够清晰了。
再规划下去也不会让项目多跑一行代码。

今天，哪怕只做一件事：
  → 安装依赖
  → 创建项目目录
  → 写第一行API调用代码

只要开始了，后面就会越来越快。
停在规划阶段，蓝图就是废纸。

2小时的枯燥 = 8000块的月薪差距。
这笔账，你算得过来。

开始写代码吧。
```
