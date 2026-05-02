"""
AutoCRM AI - CRM售前及售后业务场景AI解决方案
基于售前LTC业务AI场景清单(67个) + 售后服务全流程(36个) + 纷享销客销售Agent白皮书(6大Agent)
企业级B2B SaaS界面 - 售前LTC + 售后服务 全链路AI化
"""

import streamlit as st
from datetime import datetime

# ============================================================
# 全局配置
# ============================================================
st.set_page_config(
    page_title="AutoCRM AI",
    page_icon="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'><rect width='32' height='32' rx='6' fill='%231e3a5f'/><text x='16' y='22' text-anchor='middle' fill='white' font-size='18' font-weight='bold' font-family='Arial'>A</text></svg>",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ============================================================
# Session State
# ============================================================
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "user_info" not in st.session_state:
    st.session_state.user_info = {}

# ============================================================
# 数据定义：售前LTC AI场景
# ============================================================
LTC_SCENARIOS = {
    "线索获取": [
        {"title": "线索智能挖掘", "example": "基于行业名录/公开信息自动挖掘潜在客户并生成线索卡片", "agent": "AI客户分析", "input": "行业名录、公开信息、历史成交", "output": "线索卡片/潜客名单", "role": "销售"},
        {"title": "线索去重与归并", "example": "识别同主体多来源线索并合并，避免重复跟进", "agent": "AI客户分析", "input": "线索数据、客户主数据", "output": "去重合并结果", "role": "销售/CRM管理员"},
        {"title": "线索质量评分", "example": "结合历史成交特征自动打分并优先分配高质量线索", "agent": "AI客户分析", "input": "线索属性、历史胜率", "output": "线索评分/分配建议", "role": "销售经理"},
        {"title": "线索画像补全", "example": "自动补全客户行业、规模、产线、上下游信息", "agent": "AI客户分析", "input": "工商数据、网页信息", "output": "客户画像字段", "role": "销售/售前"},
    ],
    "线索公海池": [
        {"title": "线索回收规则引擎", "example": "自动判断线索是否需要回收（超时未跟进/多次联系未转化/销售离职等）", "agent": "AI智能审批", "input": "线索跟进记录/回收规则", "output": "回收判定/回收通知", "role": "销售经理/CRM管理员"},
        {"title": "公海池线索智能推荐", "example": "根据销售能力/区域/行业/历史成交匹配最适合的线索", "agent": "AI客户分析", "input": "销售画像/线索属性/历史成交", "output": "推荐线索列表/匹配度", "role": "销售/销售经理"},
        {"title": "线索领取优先级排序", "example": "根据线索质量/客户等级/跟进历史/转化概率排序", "agent": "AI智能报表", "input": "线索评分/客户等级/历史数据", "output": "优先级排序/领取建议", "role": "销售"},
        {"title": "公海池线索激活策略", "example": "对长期未领取线索制定激活策略（换行业/换话术/换渠道）", "agent": "AI销售助手", "input": "线索历史/未转化原因", "output": "激活方案/策略调整", "role": "销售经理"},
        {"title": "线索回收预警", "example": "提前预警即将被回收的线索，提醒销售及时跟进", "agent": "AI智能预警", "input": "线索跟进时间/回收规则", "output": "预警通知/跟进提醒", "role": "销售"},
    ],
    "线索转化": [
        {"title": "首次沟通话术建议", "example": "根据客户画像与行业痛点推荐切入话术", "agent": "AI销售助手", "input": "客户画像、行业模板", "output": "话术建议/问答清单", "role": "销售"},
        {"title": "会议助手与纪要生成", "example": "录音转写、纪要生成、行动项拆解并回填CRM", "agent": "AI语音识别", "input": "会议录音、参会人", "output": "纪要/行动项/跟进记录", "role": "销售/售前"},
        {"title": "沟通内容结构化", "example": "电话/会议内容自动写入CRM跟进记录字段", "agent": "AI语音识别", "input": "通话录音、会议文本", "output": "结构化跟进记录", "role": "销售/CRM管理员"},
        {"title": "客户需求识别", "example": "从对话中提取需求点并自动关联商机", "agent": "AI智能问答", "input": "会议纪要、聊天记录", "output": "需求标签/商机关联", "role": "销售/售前"},
    ],
    "客户管理": [
        {"title": "客户信息自动补全", "example": "自动补全客户行业/规模/组织架构/产线/上下游信息", "agent": "AI客户分析", "input": "工商数据、官网、年报", "output": "客户画像字段补全", "role": "销售/CRM管理员"},
        {"title": "客户关系图谱", "example": "识别并绘制客户内部决策链/干系人关系/组织架构", "agent": "AI客户分析", "input": "会议记录、邮件、拜访记录", "output": "关系图谱/决策链", "role": "销售/售前"},
        {"title": "客户健康度评分", "example": "综合评估客户活跃度/满意度/合作潜力/战略价值", "agent": "AI客户分析", "input": "互动频率、订单、满意度", "output": "健康度评分/等级", "role": "销售经理/客户成功"},
        {"title": "客户流失预警", "example": "识别活跃度下降/互动减少/投诉增加的流失风险客户", "agent": "AI智能预警", "input": "行为日志、互动频率", "output": "流失预警/挽回建议", "role": "销售经理/客户成功"},
    ],
    "客户公海池": [
        {"title": "客户回收规则引擎", "example": "自动判断客户是否需要回收（活跃度下降/长期无互动/商机停滞等）", "agent": "AI智能审批", "input": "客户活跃度/互动记录/回收规则", "output": "回收判定/回收通知", "role": "销售经理/CRM管理员"},
        {"title": "公海池客户智能分配", "example": "根据客户价值/销售能力/区域/行业智能分配客户", "agent": "AI客户分析", "input": "客户画像/销售能力/区域分布", "output": "分配方案/匹配度", "role": "销售经理"},
        {"title": "客户领取资格校验", "example": "校验销售是否有能力跟进该客户（行业经验/客户等级/当前负载）", "agent": "AI智能审批", "input": "销售画像/客户等级/当前商机", "output": "资格判定/领取建议", "role": "销售经理"},
        {"title": "公海池客户激活方案", "example": "对沉睡客户制定激活方案（换销售/换策略/换产品线）", "agent": "AI销售助手", "input": "客户历史/沉睡原因/产品线", "output": "激活方案/策略调整", "role": "销售经理"},
        {"title": "客户回收预警", "example": "提前预警即将被回收的客户，提醒销售及时维护", "agent": "AI智能预警", "input": "客户活跃度/回收规则", "output": "预警通知/维护提醒", "role": "销售/客户成功"},
    ],
    "联系人管理": [
        {"title": "联系人关系图谱构建", "example": "自动构建销售-客户联系人关联关系网络", "agent": "AI客户分析", "input": "沟通记录、拜访记录、邮件往来", "output": "关系图谱/关联矩阵", "role": "销售/售前"},
        {"title": "联系人组织关系拓扑", "example": "识别客户内部管理层/技术层/采购层/执行层等关键角色", "agent": "AI客户分析", "input": "组织架构、职位信息、沟通记录", "output": "组织拓扑图/角色分布", "role": "销售/售前"},
        {"title": "关键联系人角色识别", "example": "自动识别决策链中的关键联系人角色", "agent": "AI客户分析", "input": "会议纪要、邮件、跟进记录", "output": "角色标签/决策链定位", "role": "销售/售前"},
        {"title": "联系人互动历史分析", "example": "分析联系人互动深度与关系强度", "agent": "AI客户分析", "input": "沟通频率、互动内容、跟进记录", "output": "互动深度评分/关系强度", "role": "销售经理"},
        {"title": "联系人网络拓扑可视化", "example": "生成联系人关系拓扑图，展示组织架构深度", "agent": "AI客户分析", "input": "联系人数据、组织架构、互动记录", "output": "拓扑图/覆盖度分析", "role": "销售/管理层"},
    ],
    "客户跟进记录": [
        {"title": "跟进记录自动生成", "example": "从会议/电话/邮件/微信中自动提取并生成结构化跟进记录", "agent": "AI语音识别", "input": "会议录音/通话记录/邮件/聊天记录", "output": "结构化跟进记录", "role": "销售"},
        {"title": "跟进内容智能分类", "example": "自动分类跟进类型（拜访/客情维护/客诉处理/需求沟通/方案沟通/验收/回款/售后）", "agent": "AI智能问答", "input": "跟进记录内容", "output": "跟进类型标签", "role": "销售/销售经理"},
        {"title": "客户需求智能提取", "example": "从跟进记录中提取客户痛点/需求/关注点/决策因素", "agent": "AI客户分析", "input": "跟进记录/会议纪要", "output": "需求清单/痛点标签", "role": "销售/售前"},
        {"title": "竞品情报自动收集", "example": "从跟进记录中提取竞品信息/报价/优劣势/客户反馈", "agent": "AI竞品分析", "input": "跟进记录/客户反馈", "output": "竞品情报/对比分析", "role": "销售/市场"},
        {"title": "跟进频率预警", "example": "识别跟进不足的客户，预警回收风险并提醒及时跟进", "agent": "AI智能预警", "input": "跟进记录/客户等级/回收规则", "output": "跟进预警/回收风险", "role": "销售/销售经理"},
        {"title": "研发方向洞察", "example": "从客户需求和反馈中提炼产品研发方向建议", "agent": "AI客户分析", "input": "客户需求/行业趋势/竞品动态", "output": "研发方向建议/产品改进点", "role": "产品/管理层"},
    ],
    "销售外勤管理": [
        {"title": "外勤打卡智能校验", "example": "GPS定位+拍照验证外勤真实性，自动关联客户档案", "agent": "AI智能审批", "input": "GPS定位/打卡照片/客户地址", "output": "打卡校验/客户关联", "role": "销售/销售经理"},
        {"title": "拜访报告自动生成", "example": "从打卡照片/语音/会议记录自动生成拜访报告", "agent": "AI文档生成", "input": "打卡照片/语音记录/会议纪要", "output": "拜访报告/跟进记录", "role": "销售"},
        {"title": "出差记录自动归档", "example": "自动归档出差行程/住宿/交通/拜访记录", "agent": "AI文档生成", "input": "行程数据/发票/打卡记录", "output": "出差报告/费用明细", "role": "销售/财务"},
        {"title": "外勤数据统计分析", "example": "统计外勤频次/效率/覆盖率/客户拜访密度", "agent": "AI智能报表", "input": "外勤打卡数据/拜访记录", "output": "外勤统计/效率分析", "role": "销售经理/管理层"},
        {"title": "OA差旅报销自动对接", "example": "外勤数据自动对接OA差旅报销系统，一键生成报销单", "agent": "AI智能审批", "input": "出差记录/费用明细/报销规则", "output": "报销单/审批流", "role": "销售/财务"},
    ],
    "商机管理": [
        {"title": "商机阶段自动识别", "example": "根据跟进内容与行为自动判断商机阶段", "agent": "AI销售助手", "input": "跟进记录、活动行为", "output": "阶段建议/推进提醒", "role": "销售/经理"},
        {"title": "商机赢率预测", "example": "基于历史胜率数据给出赢率与影响要素", "agent": "AI客户分析", "input": "商机字段、历史成交", "output": "赢率/风险要素", "role": "销售经理/管理层"},
        {"title": "关键人识别", "example": "识别决策链路并提醒补齐关键联系人", "agent": "AI客户分析", "input": "会议/邮件记录", "output": "关键人清单", "role": "销售/售前"},
        {"title": "风险预警", "example": "识别长期未推进/竞争激烈/承诺异常商机", "agent": "AI智能预警", "input": "商机进展、行为日志", "output": "预警列表/建议动作", "role": "销售经理"},
        {"title": "阶段任务自动分解", "example": "将商机各阶段任务自动分解并创建待办（需求确认/方案评审/报价审批等）", "agent": "AI智能审批", "input": "商机阶段/任务模板", "output": "任务清单/待办创建", "role": "销售/售前"},
        {"title": "阶段完成度校验", "example": "自动校验当前阶段任务是否全部完成，未完成项标红提醒", "agent": "AI智能审批", "input": "阶段任务清单/完成状态", "output": "完成度/缺失项提醒", "role": "销售/经理"},
        {"title": "阶段流转条件判断", "example": "AI判断是否满足进入下一阶段的条件（关键人确认/方案签字/报价审批等）", "agent": "AI智能审批", "input": "阶段条件/当前状态", "output": "流转判定/缺失条件", "role": "销售/经理"},
        {"title": "阶段卡点预警", "example": "识别商机在某阶段停留过久，预警并给出推进建议", "agent": "AI智能预警", "input": "商机停留时间/历史数据", "output": "卡点预警/推进建议", "role": "销售经理"},
    ],
    "方案与报价": [
        {"title": "方案生成助手", "example": "根据需求模板生成解决方案初稿", "agent": "AI文档生成", "input": "需求摘要、模板库", "output": "方案初稿/目录", "role": "售前/方案经理"},
        {"title": "竞品对比摘要", "example": "自动总结竞品优劣势与差异化卖点", "agent": "AI竞品分析", "input": "竞品资料、客户关注点", "output": "对比摘要/卖点清单", "role": "销售/售前"},
        {"title": "报价合理性建议", "example": "结合历史成交与成本区间给出报价建议", "agent": "AI销售助手", "input": "成本区间、历史报价", "output": "报价区间/策略", "role": "销售/报价专员"},
        {"title": "报价单校验", "example": "字段完整性/逻辑一致性自动检查", "agent": "AI智能预警", "input": "报价单草稿", "output": "校验结果/修正建议", "role": "销售/财务"},
    ],
    "招投标与合同": [
        {"title": "标书要点抽取", "example": "从招标文件提取关键要求与评分要点", "agent": "AI文档生成", "input": "招标文件", "output": "要点清单/风险点", "role": "售前/投标"},
        {"title": "合同风险审阅", "example": "识别付款、交付、违约条款风险并提示", "agent": "AI智能预警", "input": "合同文本", "output": "风险提示/修改建议", "role": "法务/销售"},
        {"title": "审批材料自动整理", "example": "按流程要求自动打包所需附件", "agent": "AI智能审批", "input": "合同/报价/附件", "output": "审批包/清单", "role": "销售/运营"},
    ],
    "订单与交付": [
        {"title": "交付里程碑跟踪", "example": "关键节点延期风险自动提醒", "agent": "AI智能预警", "input": "项目计划/进度", "output": "延期预警/提醒", "role": "交付/项目经理"},
        {"title": "客户异常反馈聚合", "example": "多渠道反馈自动归类并生成处理建议", "agent": "AI智能问答", "input": "邮件/工单/群消息", "output": "问题分类/建议", "role": "客服/交付"},
        {"title": "验收材料整理", "example": "自动汇总验收证据与文档", "agent": "AI文档生成", "input": "验收记录/文档", "output": "验收包/清单", "role": "交付/售后"},
    ],
    "回款与续费": [
        {"title": "回款风险预警", "example": "基于历史回款周期预测延迟风险", "agent": "AI智能预警", "input": "回款记录/合同条款", "output": "风险预警列表", "role": "财务/销售经理"},
        {"title": "催收话术生成", "example": "按客户特征生成不同强度催收话术", "agent": "AI销售助手", "input": "客户画像/回款状态", "output": "催收话术模板", "role": "销售/财务"},
        {"title": "回款计划调整", "example": "结合合同条款与进度自动更新计划", "agent": "AI智能报表", "input": "合同/项目进度", "output": "更新后的计划表", "role": "财务/销售经理"},
        {"title": "续费/二次销售触发", "example": "识别高满意客户并推荐续费商机", "agent": "AI客户分析", "input": "客户满意度/使用数据", "output": "续费商机推荐", "role": "客户成功/销售"},
    ],
    "目标管理": [
        {"title": "销售目标达成看板", "example": "日/周/月/年销售目标与实际达成对比", "agent": "AI智能报表", "input": "目标设定、商机/订单数据", "output": "目标达成率/GAP分析", "role": "销售/经理/管理层"},
        {"title": "验收目标跟踪", "example": "跟踪各项目验收里程碑，预测完成率", "agent": "AI智能预警", "input": "项目计划、验收标准、进度", "output": "验收达成率/延期预警", "role": "交付/项目经理"},
        {"title": "回款目标达成分析", "example": "回款计划vs实际回款对比，预测缺口", "agent": "AI智能报表", "input": "回款计划、合同条款、到账记录", "output": "回款达成率/缺口预警", "role": "财务/销售经理"},
        {"title": "目标分解与对齐", "example": "自动将团队目标分解到个人", "agent": "AI客户分析", "input": "团队目标、个人商机/客户池", "output": "目标分解方案/缺口提示", "role": "销售经理/管理层"},
        {"title": "目标预测与调整建议", "example": "基于当前管道预测目标达成概率", "agent": "AI销售助手", "input": "商机管道、历史趋势、目标", "output": "达成概率/策略建议", "role": "管理层/销售经理"},
    ],
    "销售复盘与赋能": [
        {"title": "销冠方法论总结", "example": "从高绩效销售行为中提炼可复制打法", "agent": "AI销售助手", "input": "跟进行为/成交数据", "output": "方法论/训练要点", "role": "销售经理/培训"},
        {"title": "个人行为诊断", "example": "发现跟进频率、转化率、成交周期短板", "agent": "AI客户分析", "input": "个人KPI/行为数据", "output": "差距分析/建议", "role": "销售个人"},
        {"title": "知识库自动沉淀", "example": "会议纪要/方案/FAQ自动分类归档", "agent": "AI知识库", "input": "文档/纪要", "output": "结构化知识库", "role": "销售/售前"},
        {"title": "培训内容个性化推荐", "example": "针对短板推送训练与资料", "agent": "AI培训助手", "input": "能力评估/学习记录", "output": "学习路径/课程", "role": "销售个人"},
    ],
    "管理层经营分析": [
        {"title": "预测性业绩看板", "example": "基于商机与赢率预测月度收入", "agent": "AI智能报表", "input": "商机/订单数据", "output": "预测看板", "role": "管理层"},
        {"title": "业绩异常解释", "example": "自动归因本月波动原因", "agent": "AI智能问答", "input": "业绩/行为数据", "output": "归因报告", "role": "管理层/经理"},
        {"title": "团队资源配置建议", "example": "根据商机结构给出人员投放建议", "agent": "AI客户分析", "input": "商机结构/产能", "output": "资源建议", "role": "管理层"},
    ],
    "BI与数据分析": [
        {"title": "自然语言BI查询", "example": "用自然语言提问即可返回指标与图表", "agent": "BI对话助手", "input": "数据仓库/指标库", "output": "图表/指标卡", "role": "管理层/销售经理"},
        {"title": "指标口径自动校验", "example": "自动检测指标口径/粒度/时间维度一致性", "agent": "BI治理助手", "input": "指标定义/报表", "output": "口径校验结果", "role": "数据管理员"},
        {"title": "异常波动归因", "example": "自动分析业绩波动的主要驱动因素", "agent": "BI分析助手", "input": "业绩/行为数据", "output": "数据分析报告", "role": "管理层"},
        {"title": "预测与情景分析", "example": "预测月度收入/回款并给出情景假设", "agent": "BI预测助手", "input": "历史数据/商机", "output": "预测曲线/情景", "role": "管理层"},
    ],
    "Agent工作流": [
        {"title": "语音创建客户", "example": "对话或语音输入客户信息自动建档", "agent": "对话式Agent", "input": "语音/文本输入", "output": "CRM客户记录", "role": "销售"},
        {"title": "语音创建报价单", "example": "对话输入产品/价格/条款自动生成报价单", "agent": "对话式Agent", "input": "语音/文本/产品库", "output": "报价单草稿", "role": "销售/报价专员"},
        {"title": "语音创建商机", "example": "对话总结需求并自动建立商机与阶段", "agent": "对话式Agent", "input": "会议纪要/语音", "output": "商机记录", "role": "销售/售前"},
        {"title": "语音创建合同/审批流", "example": "对话输入合同要素并发起审批流", "agent": "对话式Agent", "input": "合同要素/模板", "output": "合同草稿/审批流", "role": "销售/法务"},
        {"title": "批量数据导入建档", "example": "上传表格自动创建客户/联系人/商机", "agent": "数据导入Agent", "input": "Excel/CSV", "output": "批量建档结果", "role": "销售运营"},
        {"title": "跨系统任务联动", "example": "对话指令自动创建任务/日程/提醒", "agent": "对话式Agent", "input": "语音/文本", "output": "任务/日程", "role": "销售个人"},
    ],
}

# ============================================================
# 数据定义：售后服务全流程AI场景
# ============================================================
AFTERSALES_SCENARIOS = {
    "客服与报修": [
        {"title": "400热线智能接听", "example": "AI语音机器人接听400热线，自动识别客户意图并分类", "agent": "AI语音识别", "input": "客户来电语音", "output": "意图分类/客户信息匹配", "role": "客服"},
        {"title": "报修信息自动录入", "example": "客户电话/小程序报修后自动创建报修记录", "agent": "AI智能问答", "input": "语音/文本报修描述", "output": "报修工单草稿", "role": "客服/客户"},
        {"title": "报修意图识别与分流", "example": "区分维修/咨询/投诉/索赔等意图，自动分配", "agent": "AI智能问答", "input": "对话内容/历史工单", "output": "意图标签/分配建议", "role": "客服主管"},
        {"title": "重复报修智能合并", "example": "识别同一设备/同一故障的重复报修并合并", "agent": "AI客户分析", "input": "报修记录/设备编码", "output": "重复检测/合并建议", "role": "客服"},
    ],
    "工单与派工": [
        {"title": "工单自动创建与填充", "example": "根据报修信息自动填充设备/故障/客户/地址", "agent": "AI文档生成", "input": "报修记录/设备档案", "output": "完整工单", "role": "客服/调度"},
        {"title": "智能派工推荐", "example": "根据故障类型/地理位置/工程师技能智能匹配", "agent": "AI客户分析", "input": "故障描述/工程师排班/位置", "output": "派工推荐/路线优化", "role": "调度/服务经理"},
        {"title": "工单优先级排序", "example": "综合SLA/客户等级/故障紧急度自动排序", "agent": "AI智能预警", "input": "工单属性/SLA规则", "output": "优先级排序/超时预警", "role": "调度/服务经理"},
        {"title": "工程师技能画像匹配", "example": "故障类型自动匹配具备资质的工程师", "agent": "AI客户分析", "input": "故障类型/工程师技能库", "output": "匹配工程师列表", "role": "调度"},
    ],
    "故障诊断": [
        {"title": "TIS系统故障自动检测", "example": "对接TIS远程诊断系统，自动读取故障码", "agent": "AI智能问答", "input": "TIS故障码/设备遥测数据", "output": "故障解析/严重度评估", "role": "工程师/客服"},
        {"title": "上位机故障自动上报", "example": "设备上位机自动发送故障告警，AI解析并创建工单", "agent": "AI智能预警", "input": "上位机告警数据/设备状态", "output": "预警工单/故障初判", "role": "客服/调度"},
        {"title": "故障解决方案智能匹配", "example": "根据故障码匹配历史相似案例与标准维修方案", "agent": "AI知识库", "input": "故障码/描述/设备型号", "output": "匹配方案/维修步骤/所需备件", "role": "工程师/维修店"},
        {"title": "故障根因分析", "example": "结合历史维修记录/TIS数据推断故障根因", "agent": "AI客户分析", "input": "故障码/历史维修/运行日志", "output": "根因分析/关联故障链", "role": "工程师/技术支持"},
        {"title": "维修标准处理流程推送", "example": "厂家接收到故障后匹配标准SOP推送到维修店", "agent": "AI知识库", "input": "故障类型/设备型号/SOP库", "output": "标准处理流程/注意事项", "role": "维修店/工程师"},
    ],
    "维修执行": [
        {"title": "维修过程引导", "example": "步骤化引导维修操作，实时提示关键步骤", "agent": "AI知识库", "input": "维修方案/设备型号", "output": "步骤指引/安全提示", "role": "工程师"},
        {"title": "维修记录自动生成", "example": "工程师口述/拍照后AI自动生成结构化维修记录", "agent": "AI语音识别", "input": "语音/照片/视频", "output": "结构化维修记录", "role": "工程师"},
        {"title": "维修异常实时预警", "example": "维修中发现非预期问题实时预警升级", "agent": "AI智能预警", "input": "维修进展/故障数据", "output": "异常预警/升级建议", "role": "工程师/服务经理"},
        {"title": "小程序到达/签到确认", "example": "工程师小程序定位打卡自动确认到达时间", "agent": "AI智能审批", "input": "GPS定位/工单地址", "output": "到达确认/客户通知", "role": "工程师/客户"},
    ],
    "领料与出库": [
        {"title": "BOM物料智能匹配", "example": "根据设备型号+故障类型自动匹配BOM中所需物料", "agent": "AI客户分析", "input": "设备型号/故障码/BOM数据", "output": "物料清单/替代料建议", "role": "工程师/仓管"},
        {"title": "质保校验-保内外判断", "example": "结合BOM+标准质保政策+协议质保自动校验", "agent": "AI智能问答", "input": "设备SN/出厂日期/BOM关系/质保协议", "output": "保内/保外判定/质保剩余", "role": "客服/索赔专员"},
        {"title": "总成零部件关系自动追溯", "example": "根据BOM层级关系自动追溯总成下的零部件", "agent": "AI客户分析", "input": "BOM树/故障零件编码", "output": "层级关系/索赔范围", "role": "索赔专员"},
        {"title": "库存可用性预测与备货", "example": "预测常用故障备件需求，提前建议仓库备货", "agent": "AI智能报表", "input": "历史故障/库存数据/季节因素", "output": "备货建议/缺货预警", "role": "仓管/采购"},
    ],
    "竣工与验收": [
        {"title": "竣工条件自动校验", "example": "自动检查维修记录/测试报告/物料消耗是否齐全", "agent": "AI智能审批", "input": "维修记录/测试数据/物料单", "output": "校验结果/缺失项", "role": "服务经理"},
        {"title": "维修质量评估", "example": "基于维修前后数据对比评估维修质量", "agent": "AI客户分析", "input": "维修记录/运行参数/回访数据", "output": "质量评分/满意度预测", "role": "服务经理/质量"},
        {"title": "客户验收确认推送", "example": "竣工后自动推送验收单给客户确认并收集评价", "agent": "AI文档生成", "input": "维修记录/竣工数据", "output": "验收单/评价表", "role": "客户/客服"},
        {"title": "外勤报销智能审核", "example": "自动校验差旅/交通/住宿报销合规性", "agent": "AI智能审批", "input": "报销单/工单/标准", "output": "审核结果/异常标记", "role": "工程师/财务"},
    ],
    "索赔申请与审核": [
        {"title": "索赔资格自动校验", "example": "自动校验保内外+质保协议+索赔政策", "agent": "AI智能问答", "input": "保内外判定/质保协议/索赔政策", "output": "索赔资格/可索赔金额", "role": "索赔专员"},
        {"title": "索赔材料自动整理", "example": "自动打包维修记录/故障码/照片/BOM等索赔材料", "agent": "AI文档生成", "input": "工单/维修记录/检测报告", "output": "索赔材料包/清单", "role": "索赔专员"},
        {"title": "索赔金额智能核算", "example": "根据BOM物料价格+工时标准+协议折扣核算", "agent": "AI智能报表", "input": "物料清单/工时/协议价", "output": "索赔金额明细", "role": "索赔专员/财务"},
        {"title": "索赔风险审核", "example": "识别异常索赔模式，标记审核风险", "agent": "AI智能预警", "input": "索赔历史/金额/频次", "output": "风险评分/审核建议", "role": "厂家审核员"},
        {"title": "索赔审批流程自动化", "example": "根据金额/类型自动路由到对应审批人", "agent": "AI智能审批", "input": "索赔单/金额/审批规则", "output": "审批路由/升级通知", "role": "审核员/管理层"},
    ],
    "索赔回款与结案": [
        {"title": "索赔回款进度跟踪", "example": "跟踪厂家到店端/供应商的回款进度", "agent": "AI智能预警", "input": "索赔单/回款计划", "output": "回款进度/逾期预警", "role": "财务/索赔专员"},
        {"title": "回款异常识别", "example": "识别回款金额与索赔金额差异", "agent": "AI智能报表", "input": "索赔金额/实际回款", "output": "差异分析/原因推断", "role": "财务"},
        {"title": "结案条件自动校验", "example": "检查回款完成+客户确认+资料归档是否齐全", "agent": "AI智能审批", "input": "回款记录/客户确认/归档状态", "output": "结案校验结果", "role": "索赔专员"},
        {"title": "结案报告自动生成", "example": "自动汇总维修/索赔/回款全流程数据生成报告", "agent": "AI文档生成", "input": "工单/索赔/回款数据", "output": "结案报告", "role": "索赔专员/管理层"},
    ],
    "供应商反向索赔": [
        {"title": "供应商责任自动认定", "example": "根据故障根因分析+BOM追溯判断供应商责任", "agent": "AI客户分析", "input": "根因分析/BOM/供应商合同", "output": "责任归属/供应商认定", "role": "索赔专员/采购"},
        {"title": "反向索赔金额核算", "example": "根据供应商协议+索赔金额计算可追偿金额", "agent": "AI智能报表", "input": "索赔金额/供应商协议/责任比例", "output": "追偿金额/依据", "role": "索赔专员/财务"},
        {"title": "供应商索赔趋势分析", "example": "按供应商/零部件/时间段分析索赔频率与金额", "agent": "AI客户分析", "input": "索赔历史/供应商数据", "output": "趋势报告/质量预警", "role": "质量/采购/管理层"},
        {"title": "供应商索赔协同流程", "example": "自动向供应商发起索赔通知并跟踪处理进度", "agent": "AI智能审批", "input": "供应商认定/索赔金额", "output": "索赔通知/跟踪状态", "role": "索赔专员/采购"},
    ],
    "满意度回访": [
        {"title": "自动回访任务生成", "example": "维修完成后自动创建回访任务，根据客户等级设定回访频次", "agent": "AI智能审批", "input": "维修完成记录/客户等级", "output": "回访任务/时间表", "role": "客服/客户成功"},
        {"title": "回访话术智能推荐", "example": "根据维修类型/客户画像自动生成个性化回访话术", "agent": "AI销售助手", "input": "维修记录/客户画像", "output": "回访话术/问题清单", "role": "客服"},
        {"title": "满意度智能评分", "example": "从回访对话中自动提取满意度评分并分类", "agent": "AI语音识别", "input": "回访录音/文字记录", "output": "满意度评分/情感分析", "role": "客服主管"},
        {"title": "低满意度预警与跟进", "example": "识别低满意度客户自动升级处理并生成挽回方案", "agent": "AI智能预警", "input": "满意度评分/回访记录", "output": "预警通知/挽回方案", "role": "客户成功/管理层"},
        {"title": "满意度趋势分析", "example": "按客户/区域/产品/时间段分析满意度趋势，识别改进方向", "agent": "AI智能报表", "input": "历史满意度数据", "output": "趋势报告/改进建议", "role": "管理层/质量"},
    ],
    "客诉处理": [
        {"title": "客诉自动分类与分级", "example": "AI自动识别客诉类型(质量/服务/交付/价格)并分级(P0-P3)", "agent": "AI智能问答", "input": "客诉内容/客户信息", "output": "分类标签/优先级", "role": "客服主管"},
        {"title": "客诉根因智能分析", "example": "结合历史客诉/维修记录/产品批次分析客诉根因", "agent": "AI客户分析", "input": "客诉记录/维修数据/产品数据", "output": "根因分析/关联批次", "role": "质量/客服主管"},
        {"title": "客诉处理方案推荐", "example": "根据客诉类型和历史处理案例推荐最优处理方案", "agent": "AI知识库", "input": "客诉类型/客户等级/历史案例", "output": "处理方案/赔偿建议", "role": "客服/客服主管"},
        {"title": "客诉处理时效监控", "example": "实时监控各客诉处理时效，超时自动升级催办", "agent": "AI智能预警", "input": "客诉工单/SLA规则", "output": "超时预警/升级通知", "role": "客服主管/管理层"},
        {"title": "客诉闭环报告", "example": "客诉结案后自动生成闭环报告，包含根因/处理/改进措施", "agent": "AI文档生成", "input": "客诉全流程数据", "output": "闭环报告/改进措施", "role": "客服主管/管理层"},
    ],
    "退换货": [
        {"title": "退换货资格自动校验", "example": "根据质保政策/购买时间/故障情况自动判断退换货资格", "agent": "AI智能问答", "input": "购买记录/质保政策/故障描述", "output": "资格判定/可选方案", "role": "客服/售后"},
        {"title": "退换货流程自动化", "example": "符合条件的退换货申请自动审批并触发物流/财务流程", "agent": "AI智能审批", "input": "退换货申请/审批规则", "output": "审批结果/流程触发", "role": "售后/财务"},
        {"title": "退货质检智能判定", "example": "根据退货照片/检测报告自动判定退货原因和责任归属", "agent": "AI客户分析", "input": "退货照片/检测报告", "output": "质检结果/责任判定", "role": "质检/售后"},
        {"title": "换货物流跟踪", "example": "自动跟踪换货物流状态，异常时主动通知客户", "agent": "AI智能预警", "input": "物流单号/换货订单", "output": "物流状态/异常预警", "role": "客服/物流"},
        {"title": "退换货数据分析", "example": "分析退换货原因/产品/区域分布，识别质量改进方向", "agent": "AI智能报表", "input": "退换货记录/产品数据", "output": "退换货率/原因分布/改进建议", "role": "质量/管理层"},
    ],
}




# ============================================================
# 数据定义：通用AI能力
# ============================================================
GENERAL_CAPABILITIES = [
    {"title": "AI智能问答", "example": "产品/技术问题智能解答，减少重复咨询", "agent": "AI智能问答", "input": "知识库/FAQ", "output": "对话答案", "role": "销售/售前/客服"},
    {"title": "AI智能报表", "example": "销售数据智能分析与自动生成分析报告", "agent": "AI智能报表", "input": "CRM/ERP数据", "output": "分析报告/BI看板", "role": "管理层/销售经理"},
    {"title": "AI知识库", "example": "沉淀产品/案例/FAQ并支持智能检索", "agent": "AI知识库", "input": "文档/案例", "output": "检索式答案", "role": "全员"},
    {"title": "AI智能预警", "example": "客户流失风险/合同到期/异常行为预警", "agent": "AI智能预警", "input": "行为日志/合同数据", "output": "预警清单", "role": "销售经理/客服"},
    {"title": "AI文档生成", "example": "自动生成合同/方案/技术支持文档", "agent": "AI文档生成", "input": "模板/需求摘要", "output": "文档初稿", "role": "售前/法务"},
    {"title": "AI语音识别", "example": "会议录音转文字与关键词提取", "agent": "AI语音识别", "input": "语音/会议录音", "output": "文本/关键词", "role": "销售/售前"},
    {"title": "AI邮件助手", "example": "邮件内容智能分析/自动回复/优先级排序", "agent": "AI邮件助手", "input": "邮件正文/历史往来", "output": "回复草稿/优先级", "role": "销售/客服"},
    {"title": "AI竞品分析", "example": "竞争对手情报收集、价格策略分析", "agent": "AI竞品分析", "input": "竞品资料/市场数据", "output": "竞品报告/趋势", "role": "销售/市场"},
    {"title": "AI培训助手", "example": "个性化培训推荐、能力评估与知识推荐", "agent": "AI培训助手", "input": "学习记录/评测", "output": "学习路径", "role": "销售/新人"},
    {"title": "AI智能审批", "example": "自动化审批流程、智能风险评估", "agent": "AI智能审批", "input": "审批表单/合同", "output": "审批结论", "role": "管理层/法务"},
]

# ============================================================
# 数据定义：6大Agent体系
# ============================================================
AGENT_SYSTEM = {
    "情报Agent": {
        "desc": "AI自动获取市场/客户/关键人情报",
        "capabilities": [
            "企业工商、舆情、招投标、财报等信息自动获取",
            "AI信息提取：客户详情页丰富信息，一键补全客户字段",
            "AI情报订阅：自定义订阅信息情报维度与数据源",
            "AI情报洞察与建议：机会与风险洞察",
            "招投标信息AI挖掘：精准识别标讯关联度与标的物",
        ]
    },
    "客户互动Agent": {
        "desc": "客户现场、电话、邮件等客户互动智能辅助",
        "capabilities": [
            "多模态语料转写：在线会议/电话/录音/文件导入",
            "发言人管理：绑定客户联系人，会中会后识别",
            "客方发言人洞察：态度/关注点/顾虑/竞对信息",
            "销售表现洞察：对话技巧/SOP执行质检/对话建议",
            "互动摘要：关键信息提取/重点议题/互动评价",
        ]
    },
    "客户画像Agent": {
        "desc": "建立客户特征画像，进行客户洞察",
        "capabilities": [
            "线索画像(BANT)：预算/权限/需求/时间线评估",
            "客户画像：多维度AI洞察/综合评分/状态洞察/行动建议",
            "商机画像(C139)：1个决定力+3个趋赢力+9个必清事项",
            "赢率评估：赢单区/抖动区/输单区雷达图",
            "画像动态更新：基于互动语料自动补全画像",
        ]
    },
    "工作赋能Agent": {
        "desc": "日程、待办智能组织，经营状态动态报告",
        "capabilities": [
            "GAP分析建议：目标达成差距与行动建议",
            "重点商机洞察与建议",
            "风险预警：停滞/竞争/异常预警",
            "AI工作建议：智能推荐下一步行动",
            "AI业务报告：日/周/月/季/年报告自动生成",
        ]
    },
    "销售建议Agent": {
        "desc": "智能销售诊断、引导、建议，销售教练",
        "capabilities": [
            "智能风险提示：商机风险/合同风险/流失风险",
            "销冠方法论复制：提炼赢单关键动作和必清事项",
            "智能销售教练：模拟销售过程/实时陪练",
            "差异化分析：竞品对比与差异化卖点推荐",
            "策略建议：基于方法论与客户情况的智能策略",
        ]
    },
    "智能知识库": {
        "desc": "解决方案设计与系统落地，高效知识应用",
        "capabilities": [
            "RAG检索增强生成：智能搜索与问答",
            "方案生成器：提取需求到模板制定到内容填充",
            "知识推荐：基于场景自动推荐相关知识",
            "优秀话术提取：从互动中提取话术转入知识库",
            "多知识库管理：分类/标签/权限/有效期管理",
        ]
    },
}

# ============================================================
# SVG图标定义
# ============================================================
SVG_ICONS = {
    "dashboard": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="3" width="7" height="7" rx="1"/><rect x="14" y="3" width="7" height="7" rx="1"/><rect x="3" y="14" width="7" height="7" rx="1"/><rect x="14" y="14" width="7" height="7" rx="1"/></svg>',
    "pipeline": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M22 12h-4l-3 9L9 3l-3 9H2"/></svg>',
    "settings": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="3"/><path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1-2.83 2.83l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-4 0v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83-2.83l.06-.06A1.65 1.65 0 0 0 4.68 15a1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1 0-4h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 2.83-2.83l.06.06A1.65 1.65 0 0 0 9 4.68a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 4 0v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 2.83l-.06.06A1.65 1.65 0 0 0 19.4 9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 0 4h-.09a1.65 1.65 0 0 0-1.51 1z"/></svg>',
    "intel": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="8"/><path d="M21 21l-4.35-4.35"/></svg>',
    "chat": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/></svg>',
    "user": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>',
    "deal": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 2L2 7l10 5 10-5-10-5z"/><path d="M2 17l10 5 10-5"/><path d="M2 12l10 5 10-5"/></svg>',
    "doc": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/></svg>',
    "wrench": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M14.7 6.3a1 1 0 0 0 0 1.4l1.6 1.6a1 1 0 0 0 1.4 0l3.77-3.77a6 6 0 0 1-7.94 7.94l-6.91 6.91a2.12 2.12 0 0 1-3-3l6.91-6.91a6 6 0 0 1 7.94-7.94l-3.76 3.76z"/></svg>',
    "ticket": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M15 5v2"/><path d="M15 11v2"/><path d="M15 17v2"/><rect x="3" y="4" width="18" height="18" rx="2" ry="2"/><line x1="3" y1="10" x2="21" y2="10"/></svg>',
    "bolt": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/></svg>',
    "target": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><circle cx="12" cy="12" r="6"/><circle cx="12" cy="12" r="2"/></svg>',
    "book": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"/><path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"/></svg>',
    "chart": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="18" y1="20" x2="18" y2="10"/><line x1="12" y1="20" x2="12" y2="4"/><line x1="6" y1="20" x2="6" y2="14"/></svg>',
    "workflow": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="3" width="6" height="6" rx="1"/><rect x="15" y="3" width="6" height="6" rx="1"/><rect x="9" y="15" width="6" height="6" rx="1"/><path d="M6 9v3a2 2 0 0 0 2 2h2"/><path d="M18 9v3a2 2 0 0 1-2 2h-2"/></svg>',
}

def icon_html(name, size=16, color="currentColor"):
    svg = SVG_ICONS.get(name, "")
    return f'<span style="display:inline-block;width:{size}px;height:{size}px;vertical-align:-2px;margin-right:6px;color:{color};">{svg}</span>'


# ============================================================
# SSO登录页
# ============================================================
def render_login_page():
    st.markdown("""
    <style>
    header[data-testid="stHeader"] { display: none !important; }
    [data-testid="stToolbar"] { display: none !important; }
    #MainMenu { display: none !important; }
    footer { display: none !important; }
    .stDeployButton { display: none !important; }
    .block-container {
        padding: 0 !important; max-width: 100% !important;
        margin-top: 0 !important;
    }
    div[data-testid="stVerticalBlock"] {
        padding-top: 0 !important; gap: 0 !important;
    }
    div[data-testid="stVerticalBlock"] > div {
        padding-top: 0 !important; margin-top: 0 !important;
    }
    div[data-testid="stHorizontalBlock"] {
        padding-top: 0 !important; gap: 0 !important;
    }
    div[data-testid="stHorizontalBlock"] > div {
        padding-top: 0 !important; margin-top: 0 !important;
    }
    [data-testid="stHorizontalBlock"] > div:nth-child(1) > div {
        background: linear-gradient(135deg, #2563eb 0%, #7c3aed 50%, #a855f7 100%) !important;
        border-radius: 0 !important; min-height: 100vh !important;
        display: flex !important; align-items: center !important;
    }
    [data-testid="stHorizontalBlock"] > div:nth-child(2) > div {
        background: #fff !important; border-radius: 0 !important;
        min-height: 100vh !important;
        display: flex !important; flex-direction: column !important;
        justify-content: center !important;
        padding: 0 60px !important;
    }
    section[data-testid="stSidebar"] + div div.stButton > button[kind="primary"],
    div[data-testid="stFormSubmitButton"] > button {
        background: linear-gradient(135deg, #1e3a5f 0%, #2563eb 100%) !important;
        border: none !important; color: #fff !important;
        box-shadow: 0 2px 8px rgba(37,99,235,.3) !important;
        padding: 8px 16px !important; font-size: 13px !important;
    }
    div[data-testid="stFormSubmitButton"] > button {
        padding: 8px 16px !important; font-size: 13px !important;
    }
    div[data-testid="stForm"] {
        border: none !important; padding: 0 !important;
    }
    div[data-testid="stForm"] > div {
        gap: 12px !important;
    }
    </style>
    """, unsafe_allow_html=True)

    col_left, col_right = st.columns([1.5, 1])

    with col_left:
        left_html = (
            '<div style="padding:40px 48px;position:relative;min-height:100vh;display:flex;align-items:center;">'
            '<div style="position:relative;z-index:1;width:100%;">'
            '<div style="display:flex;align-items:center;gap:10px;margin-bottom:28px;">'
            '<div style="width:36px;height:36px;border-radius:8px;background:rgba(255,255,255,.2);'
            'backdrop-filter:blur(10px);border:1px solid rgba(255,255,255,.25);'
            'display:flex;align-items:center;justify-content:center;'
            'color:#fff;font-size:18px;font-weight:700;">A</div>'
            '<div style="font-size:18px;font-weight:700;color:#fff;">AutoCRM AI</div>'
            '</div>'
            '<h1 style="font-size:32px;font-weight:700;color:#fff;line-height:1.3;margin:0 0 6px 0;">AutoCRM AI</h1>'
            '<p style="font-size:18px;color:rgba(255,255,255,.7);margin:0 0 24px 0;line-height:1.5;">'
            '售前LTC + 售后服务 全链路AI解决方案</p>'
            '<div style="display:flex;flex-direction:column;gap:10px;margin-bottom:24px;">'
        )
        features = [
            "143个AI场景覆盖售前售后全流程",
            "6大Agent体系 + 10项通用AI能力",
            "企业级数据安全与权限管控",
        ]
        for f in features:
            left_html += (
                '<div style="display:flex;align-items:center;gap:8px;color:rgba(255,255,255,.88);font-size:13px;">'
                '<div style="width:4px;height:4px;border-radius:50%;background:rgba(255,255,255,.5);"></div>'
                f'<span>{f}</span></div>'
            )
        left_html += '</div><div style="display:flex;flex-direction:column;gap:6px;margin-bottom:24px;">'
        values = ["全流程AI场景透明化", "供应链全链路透明化", "售前售后数据一体化"]
        for v in values:
            left_html += (
                '<div style="display:flex;align-items:center;gap:6px;color:rgba(255,255,255,.75);font-size:12px;">'
                '<svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="rgba(96,165,250,.8)" stroke-width="2.5">'
                '<path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/><polyline points="22 4 12 14.01 9 11.01"/></svg>'
                f'<span>{v}</span></div>'
            )
        left_html += '</div>'
        # 系统集成标签
        left_html += (
            '<div style="border-top:1px solid rgba(255,255,255,.12);padding-top:16px;margin-bottom:16px;">'
            '<div style="font-size:11px;font-weight:600;color:rgba(255,255,255,.5);letter-spacing:0.8px;margin-bottom:10px;">系统集成</div>'
            '<div style="display:flex;flex-wrap:wrap;gap:6px;">'
        )
        tags = ["企业微信","钉钉","OA","SAP","MES","BOM","EPCM","TIS","质保系统","售后系统","物流系统"]
        for t in tags:
            left_html += f'<span style="padding:3px 10px;border-radius:4px;background:rgba(255,255,255,.1);color:rgba(255,255,255,.8);font-size:11px;">{t}</span>'
        left_html += '</div></div>'
        left_html += '<div style="margin-top:20px;font-size:11px;color:rgba(255,255,255,.3);">AutoCRM AI v0.3.0 &copy; 2026</div>'
        left_html += '</div></div>'
        st.markdown(left_html, unsafe_allow_html=True)

    with col_right:
        st.markdown(
            '<div style="display:flex;align-items:center;gap:10px;margin-bottom:24px;">'
            '<div style="width:30px;height:30px;border-radius:8px;background:linear-gradient(135deg,#2563eb,#7c3aed);'
            'display:flex;align-items:center;justify-content:center;color:#fff;font-size:13px;font-weight:700;">A</div>'
            '<div style="font-size:15px;font-weight:700;color:#0f172a;">AutoCRM<span style="color:#64748b;font-weight:400;margin-left:6px;font-size:11px;">| 企业账号</span></div>'
            '</div>',
            unsafe_allow_html=True
        )
        st.markdown(
            '<div style="margin-bottom:16px;">'
            '<div style="font-size:18px;font-weight:700;color:#0f172a;">欢迎登录</div>'
            '<div style="font-size:12px;color:#64748b;margin-top:4px;">登录后将获得以下权限</div>'
            '</div>',
            unsafe_allow_html=True
        )

        st.markdown('<div style="height:8px;"></div>', unsafe_allow_html=True)

        if st.button("SSO 统一认证登录", type="primary", use_container_width=True, key="sso_login"):
            st.session_state.authenticated = True
            st.session_state.user_info = {"name": "Admin", "role": "系统管理员", "dept": "信息技术部"}
            st.rerun()

        st.markdown(
            '<div style="display:flex;align-items:center;gap:12px;margin:20px 0;font-size:11px;color:#94a3b8;">'
            '<div style="flex:1;height:1px;background:#e2e8f0;"></div>'
            '<span>或使用账号密码登录</span>'
            '<div style="flex:1;height:1px;background:#e2e8f0;"></div></div>',
            unsafe_allow_html=True
        )

        with st.form("login_form"):
            username = st.text_input("用户名", placeholder="请输入用户名/手机号")
            password = st.text_input("密码", type="password", placeholder="请输入登录密码")
            submitted = st.form_submit_button("授权并登录", type="primary", use_container_width=True)
            if submitted:
                if username and password:
                    st.session_state.authenticated = True
                    st.session_state.user_info = {"name": username, "role": "销售经理", "dept": "销售一部"}
                    st.rerun()
                else:
                    st.error("请输入用户名和密码")

        st.markdown(
            '<div style="display:flex;justify-content:space-between;align-items:center;margin-top:14px;font-size:10px;color:#94a3b8;">'
            '<span>用户协议 | 隐私政策</span><span>AutoCRM AI v0.3.0</span></div>',
            unsafe_allow_html=True
        )


# 未登录则显示登录页
if not st.session_state.authenticated:
    render_login_page()
    st.stop()


# ============================================================
# B端企业级样式 - 深蓝主题
# ============================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
:root {
    --primary: #1e3a5f; --primary-dark: #0f2440; --primary-light: #e8eef6;
    --accent: #2563eb; --accent-light: #eff6ff;
    --success: #059669; --success-bg: #ecfdf5;
    --warning: #d97706; --warning-bg: #fffbeb;
    --danger: #dc2626; --danger-bg: #fef2f2;
    --gray-50: #f8fafc; --gray-100: #f1f5f9; --gray-200: #e2e8f0;
    --gray-500: #64748b; --gray-700: #334155; --gray-900: #0f172a;
    --radius: 6px; --shadow: 0 1px 3px rgba(15,23,42,.06);
    --shadow-md: 0 4px 6px -1px rgba(15,23,42,.07);
}
.stApp { font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif; }
.stApp > .block-container { padding-top: 1.5rem !important; max-width: 1200px; }
div[data-testid="stVerticalBlock"] > div { padding-top: 0 !important; }
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0a1628 0%, #0f2440 40%, #132d4f 100%) !important;
    border-right: 1px solid rgba(37,99,235,.15);
}
section[data-testid="stSidebar"] > div { background: transparent !important; }
section[data-testid="stSidebar"] .stMarkdown,
section[data-testid="stSidebar"] label,
section[data-testid="stSidebar"] span,
section[data-testid="stSidebar"] p,
section[data-testid="stSidebar"] div { color: #94a3b8 !important; }
section[data-testid="stSidebar"] hr { border-color: rgba(37,99,235,.2) !important; opacity: 0.5; }
section[data-testid="stSidebar"] .stRadio label {
    color: #cbd5e1 !important; font-size: 13px !important; padding: 2px 0 !important;
}
section[data-testid="stSidebar"] .stRadio [aria-checked="true"] + div { color: #fff !important; font-weight: 500; }
section[data-testid="stSidebar"] .stRadio > div[data-baseweb] { gap: 0 !important; }
section[data-testid="stSidebar"] .stRadio > div[data-baseweb] > label {
    padding: 7px 10px !important; border-radius: 6px !important; margin: 1px 0 !important; transition: all .15s !important;
}
section[data-testid="stSidebar"] .stRadio > div[data-baseweb] > label:hover { background: rgba(37,99,235,.12) !important; }
section[data-testid="stSidebar"] .stRadio > div[data-baseweb] > label[data-checked="true"] {
    background: rgba(37,99,235,.18) !important; box-shadow: inset 3px 0 0 #2563eb !important;
}
section[data-testid="stSidebar"] button[kind="secondary"] {
    background: rgba(255,255,255,.06) !important; border: 1px solid rgba(255,255,255,.1) !important; color: #94a3b8 !important;
}
section[data-testid="stSidebar"] button[kind="secondary"]:hover {
    background: rgba(220,38,38,.12) !important; border-color: rgba(220,38,38,.3) !important; color: #fca5a5 !important;
}
.sidebar-cat {
    font-size: 10px; font-weight: 600; color: #475569 !important;
    text-transform: uppercase; letter-spacing: 0.8px; padding: 14px 0 4px 8px; margin-top: 2px;
}
.card { background: #fff; border: 1px solid var(--gray-200); border-radius: var(--radius); padding: 20px; box-shadow: var(--shadow); margin-bottom: 12px; }
.card:hover { box-shadow: var(--shadow-md); }
.metric-card { background: #fff; border: 1px solid var(--gray-200); border-radius: var(--radius); padding: 16px 20px; text-align: center; }
.metric-value { font-size: 26px; font-weight: 700; color: var(--gray-900); line-height: 1.2; }
.metric-label { font-size: 12px; color: var(--gray-500); margin-top: 4px; }
.metric-trend-up { color: var(--success); font-size: 12px; font-weight: 600; }
.metric-trend-down { color: var(--danger); font-size: 12px; font-weight: 600; }
.tag { display: inline-block; padding: 2px 8px; border-radius: 4px; font-size: 11px; font-weight: 500; }
.tag-active { background: var(--success-bg); color: var(--success); }
.tag-warning { background: var(--warning-bg); color: var(--warning); }
.tag-danger { background: var(--danger-bg); color: var(--danger); }
.tag-info { background: var(--accent-light); color: var(--accent); }
.tag-default { background: var(--gray-100); color: var(--gray-700); }
.agent-node { background: #fff; border: 1px solid var(--gray-200); border-radius: var(--radius); padding: 14px 16px; margin-bottom: 8px; }
.agent-node.running { border-left: 3px solid var(--accent); }
.agent-node.success { border-left: 3px solid var(--success); }
.agent-node.waiting { border-left: 3px solid var(--warning); }
.tool-call-box { background: var(--accent-light); border: 1px solid #bfdbfe; border-radius: var(--radius); padding: 10px 14px; margin: 6px 0; font-family: 'Courier New', monospace; font-size: 13px; color: var(--primary-dark); }
.data-table { width: 100%; border-collapse: collapse; font-size: 13px; }
.data-table th { background: var(--gray-50); padding: 8px 12px; text-align: left; font-weight: 600; color: var(--gray-700); border-bottom: 2px solid var(--gray-200); }
.data-table td { padding: 8px 12px; border-bottom: 1px solid var(--gray-100); }
.section-title { font-size: 15px; font-weight: 600; color: var(--gray-900); border-left: 3px solid var(--primary); padding-left: 10px; margin-bottom: 14px; }
.scenario-card { background: #fff; border: 1px solid var(--gray-200); border-radius: var(--radius); padding: 14px; margin-bottom: 8px; transition: all .15s; }
.scenario-card:hover { border-color: var(--accent); box-shadow: var(--shadow-md); }
.ltc-flow { display: flex; align-items: center; justify-content: center; gap: 4px; padding: 12px 0; flex-wrap: wrap; }
.ltc-step { background: var(--accent-light); border: 1px solid #bfdbfe; border-radius: 4px; padding: 5px 14px; font-size: 12px; font-weight: 500; color: var(--primary-dark); }
.ltc-arrow { color: var(--gray-500); font-size: 14px; }
.topbar { display: flex; justify-content: space-between; align-items: center; padding: 0 0 16px 0; border-bottom: 1px solid var(--gray-200); margin-bottom: 20px; }
.topbar-title { font-size: 18px; font-weight: 700; color: var(--gray-900); }
.topbar-sub { font-size: 12px; color: var(--gray-500); }
.topbar-user { display: flex; align-items: center; gap: 8px; font-size: 13px; color: var(--gray-700); }
.topbar-avatar { width: 32px; height: 32px; border-radius: 50%; background: var(--primary); color: #fff; display: flex; align-items: center; justify-content: center; font-size: 13px; font-weight: 600; }
</style>
""", unsafe_allow_html=True)


# ============================================================
# 公共组件
# ============================================================
def metric_card(value, label, trend=None, trend_label=None):
    if trend and trend > 0:
        trend_html = f'<div class="metric-trend-up">+{trend_label or f"{trend}%"}</div>'
    elif trend and trend < 0:
        trend_html = f'<div class="metric-trend-down">{trend_label or f"{trend}%"}</div>'
    else:
        trend_html = ''
    return f'<div class="metric-card"><div class="metric-value">{value}</div><div class="metric-label">{label}</div>{trend_html}</div>'

def status_tag(text, level='default'):
    return f'<span class="tag tag-{level}">{text}</span>'

def render_scenario_card(s, idx):
    return f"""
    <div class="scenario-card">
        <div style="display:flex;justify-content:space-between;align-items:center;">
            <strong>{idx+1}. {s['title']}</strong>
            {status_tag(s['agent'], 'info')}
        </div>
        <p style="font-size:13px;color:var(--gray-700);margin:6px 0 4px;">{s['example']}</p>
        <div style="font-size:12px;color:var(--gray-500);">
            Input: {s['input']} &rarr; Output: {s['output']} | Role: {s['role']}
        </div>
    </div>
    """


# ============================================================
# 侧边栏
# ============================================================
with st.sidebar:
    st.markdown(
        '<div style="padding:12px 0 12px 0;display:flex;align-items:center;gap:10px;">'
        '<div style="width:34px;height:34px;border-radius:10px;background:linear-gradient(135deg,#2563eb,#60a5fa);'
        'display:flex;align-items:center;justify-content:center;color:#fff;font-size:16px;font-weight:700;'
        'font-family:Inter,sans-serif;box-shadow:0 2px 8px rgba(37,99,235,.3);">A</div>'
        '<div><div style="font-size:15px;font-weight:700;color:#fff;letter-spacing:-0.3px;">AutoCRM AI</div>'
        '<div style="font-size:10px;color:#64748b;margin-top:1px;">Enterprise AI CRM</div></div></div>',
        unsafe_allow_html=True
    )
    st.markdown('<div style="border-top:1px solid rgba(37,99,235,.15);margin:0 0 4px 0;"></div>', unsafe_allow_html=True)

    st.markdown(f'<div class="sidebar-cat">{icon_html("chart",10,"#475569")} 总览</div>', unsafe_allow_html=True)
    overview = st.radio("nav_overview", ["工作台", "全流程场景", "系统设置"], label_visibility="collapsed")

    st.markdown(f'<div class="sidebar-cat">{icon_html("deal",10,"#475569")} 售前LTC场景</div>', unsafe_allow_html=True)
    presale = st.radio("nav_presale", ["情报Agent", "客户互动Agent", "客户画像Agent", "商机推进", "合同评审"], label_visibility="collapsed")

    st.markdown(f'<div class="sidebar-cat">{icon_html("wrench",10,"#475569")} 售后服务场景</div>', unsafe_allow_html=True)
    aftersale = st.radio("nav_aftersale", ["售后故障诊断", "智能工单"], label_visibility="collapsed")

    st.markdown(f'<div class="sidebar-cat">{icon_html("bolt",10,"#475569")} AI Agent</div>', unsafe_allow_html=True)
    ai_agent = st.radio("nav_agent", ["工作赋能Agent", "销售教练Agent", "智能知识库"], label_visibility="collapsed")

    st.markdown(f'<div class="sidebar-cat">{icon_html("workflow",10,"#475569")} AI能力</div>', unsafe_allow_html=True)
    ai_cap = st.radio("nav_ai", ["智能问数", "Agent工作流"], label_visibility="collapsed")

    # 合并选择
    page = "工作台"
    if overview == "全流程场景":
        page = "全流程场景"
    elif overview == "系统设置":
        page = "系统设置"
    else:
        page = presale or aftersale or ai_agent or ai_cap

    # 底部用户信息
    st.markdown('<div style="border-top:1px solid rgba(37,99,235,.15);margin:12px 0 8px 0;"></div>', unsafe_allow_html=True)
    user = st.session_state.user_info
    st.markdown(
        f'<div style="display:flex;align-items:center;gap:8px;padding:4px 0;">'
        f'<div style="width:28px;height:28px;border-radius:50%;background:linear-gradient(135deg,#2563eb,#1e3a5f);'
        f'display:flex;align-items:center;justify-content:center;color:#fff;font-size:11px;font-weight:600;">'
        f'{user.get("name","A")[0].upper()}</div>'
        f'<div><div style="font-size:12px;color:#e2e8f0;font-weight:500;">{user.get("name","Admin")}</div>'
        f'<div style="font-size:10px;color:#64748b;">{user.get("role","")} | {user.get("dept","")}</div></div></div>',
        unsafe_allow_html=True
    )
    if st.button("退出登录", use_container_width=True, key="logout"):
        st.session_state.authenticated = False
        st.session_state.user_info = {}
        st.rerun()


# ============================================================
# 工作台
# ============================================================
if page == "工作台":
    st.markdown(
        '<div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:24px;">'
        '<div><div style="font-size:22px;font-weight:700;color:#0f172a;">工作台</div>'
        '<div style="font-size:13px;color:#64748b;">AutoCRM AI 智能销售工作台</div></div>'
        f'<div style="font-size:12px;color:#64748b;">{datetime.now().strftime("%Y-%m-%d %H:%M")}</div></div>',
        unsafe_allow_html=True
    )

    col1, col2, col3, col4, col5 = st.columns(5)
    with col1: st.markdown(metric_card("1,247", "本月线索", 12.5), unsafe_allow_html=True)
    with col2: st.markdown(metric_card("89", "活跃商机", 8.3), unsafe_allow_html=True)
    with col3: st.markdown(metric_card("23", "本月成交", -3.2), unsafe_allow_html=True)
    with col4: st.markdown(metric_card("4.2M", "成交金额", 15.7), unsafe_allow_html=True)
    with col5: st.markdown(metric_card("94%", "客户满意度"), unsafe_allow_html=True)

    st.markdown("<br/>", unsafe_allow_html=True)

    # LTC流程图
    st.markdown('<div class="section-title">售前LTC全流程 (92个AI场景)</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="ltc-flow">
        <span class="ltc-step">线索获取(4)</span><span class="ltc-arrow">&rarr;</span>
        <span class="ltc-step" style="background:var(--warning-bg);border-color:var(--warning);color:var(--warning);">线索公海池(5)</span><span class="ltc-arrow">&rarr;</span>
        <span class="ltc-step">线索转化(4)</span><span class="ltc-arrow">&rarr;</span>
        <span class="ltc-step" style="background:var(--danger-bg);border-color:var(--danger);color:var(--danger);">客户管理(4)</span><span class="ltc-arrow">&rarr;</span>
        <span class="ltc-step" style="background:var(--warning-bg);border-color:var(--warning);color:var(--warning);">客户公海池(5)</span><span class="ltc-arrow">&rarr;</span>
        <span class="ltc-step" style="background:var(--danger-bg);border-color:var(--danger);color:var(--danger);">联系人管理(5)</span><span class="ltc-arrow">&rarr;</span>
        <span class="ltc-step" style="background:var(--success-bg);border-color:var(--success);color:var(--success);">跟进记录(6)</span><span class="ltc-arrow">&rarr;</span>
        <span class="ltc-step" style="background:var(--success-bg);border-color:var(--success);color:var(--success);">外勤管理(5)</span>
    </div>
    <div class="ltc-flow" style="margin-top:4px;">
        <span class="ltc-step" style="background:var(--danger-bg);border-color:var(--danger);color:var(--danger);">目标管理(5)</span><span class="ltc-arrow">&rarr;</span>
        <span class="ltc-step" style="background:var(--success-bg);border-color:var(--success);color:var(--success);">销售复盘与赋能(4)</span><span class="ltc-arrow">&rarr;</span>
        <span class="ltc-step" style="background:var(--success-bg);border-color:var(--success);color:var(--success);">管理层经营分析(3)</span><span class="ltc-arrow">&rarr;</span>
        <span class="ltc-step" style="background:var(--warning-bg);border-color:var(--warning);color:var(--warning);">BI与数据分析(4)</span><span class="ltc-arrow">&rarr;</span>
        <span class="ltc-step" style="background:var(--danger-bg);border-color:var(--danger);color:var(--danger);">Agent工作流(6)</span>
    </div>
    """, unsafe_allow_html=True)

    # 售后流程图
    st.markdown('<div class="section-title">售后服务全流程 (51个AI场景)</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="ltc-flow">
        <span class="ltc-step" style="background:#fef7e0;border-color:#e37400;color:#e37400;">客服与报修(4)</span><span class="ltc-arrow">&rarr;</span>
        <span class="ltc-step" style="background:#fef7e0;border-color:#e37400;color:#e37400;">工单与派工(4)</span><span class="ltc-arrow">&rarr;</span>
        <span class="ltc-step" style="background:#e8f0fe;border-color:#1a73e8;color:#1a73e8;">故障诊断(5)</span><span class="ltc-arrow">&rarr;</span>
        <span class="ltc-step" style="background:#e8f0fe;border-color:#1a73e8;color:#1a73e8;">维修执行(4)</span><span class="ltc-arrow">&rarr;</span>
        <span class="ltc-step" style="background:#e8f0fe;border-color:#1a73e8;color:#1a73e8;">领料与出库(4)</span><span class="ltc-arrow">&rarr;</span>
        <span class="ltc-step" style="background:#e6f4ea;border-color:#0d904f;color:#0d904f;">竣工与验收(4)</span>
    </div>
    <div class="ltc-flow" style="margin-top:4px;">
        <span class="ltc-step" style="background:#fce8e6;border-color:#d93025;color:#d93025;">索赔申请与审核(5)</span><span class="ltc-arrow">&rarr;</span>
        <span class="ltc-step" style="background:#fce8e6;border-color:#d93025;color:#d93025;">索赔回款与结案(4)</span><span class="ltc-arrow">&rarr;</span>
        <span class="ltc-step" style="background:#fce8e6;border-color:#d93025;color:#d93025;">供应商反向索赔(4)</span><span class="ltc-arrow">&rarr;</span>
        <span class="ltc-step" style="background:#fef7e0;border-color:#e37400;color:#e37400;">满意度回访(5)</span><span class="ltc-arrow">&rarr;</span>
        <span class="ltc-step" style="background:#fef7e0;border-color:#e37400;color:#e37400;">客诉处理(5)</span><span class="ltc-arrow">&rarr;</span>
        <span class="ltc-step" style="background:#fef7e0;border-color:#e37400;color:#e37400;">退换货(5)</span>
    </div>
    """, unsafe_allow_html=True)

    # Agent状态
    st.markdown('<div class="section-title">6大Agent运行状态</div>', unsafe_allow_html=True)
    agents = [
        ("情报Agent", "running", "处理中：客户舆情监控"),
        ("互动Agent", "running", "处理中：录音转写"),
        ("画像Agent", "success", "已完成：商机画像(C139)"),
        ("赋能Agent", "waiting", "待处理：GAP分析"),
        ("建议Agent", "running", "处理中：NBA推荐"),
        ("知识库", "success", "已完成：方案生成"),
    ]
    cols = st.columns(3)
    for i, (name, status, desc) in enumerate(agents):
        with cols[i % 3]:
            st.markdown(f'<div class="agent-node {status}"><strong>{name}</strong> {status_tag(status, "active" if status == "running" else ("success" if status == "success" else "warning"))}<div style="font-size:12px;color:var(--gray-500);margin-top:4px;">{desc}</div></div>', unsafe_allow_html=True)


# ============================================================
# 全流程场景
# ============================================================
elif page == "全流程场景":
    st.markdown(
        '<h2 style="margin:0;">售前+售后 全流程AI场景</h2>'
        '<div style="color:var(--gray-500);font-size:13px;margin-bottom:20px;">售前LTC 92个场景 + 售后服务 51个场景 = 143个AI落地场景</div>',
        unsafe_allow_html=True
    )

    view_mode = st.radio("选择模块", ["售前LTC场景", "售后服务场景"], horizontal=True)

    if "售前" in view_mode:
        stages = list(LTC_SCENARIOS.keys())
        stage_counts = {k: len(v) for k, v in LTC_SCENARIOS.items()}

        # 售前流程图（两行）
        st.markdown('<div class="section-title">售前LTC全流程闭环</div>', unsafe_allow_html=True)
        row1 = stages[:9]  # 线索获取到回款与续费
        row2 = stages[9:]  # 目标管理到Agent工作流

        flow_html = '<div class="ltc-flow">'
        for i, stage in enumerate(row1):
            flow_html += f'<span class="ltc-step" style="cursor:pointer;">{stage}({stage_counts[stage]})</span>'
            if i < len(row1) - 1:
                flow_html += '<span class="ltc-arrow">&rarr;</span>'
        flow_html += '</div>'
        if row2:
            flow_html += '<div class="ltc-flow" style="margin-top:4px;">'
            for i, stage in enumerate(row2):
                color = 'background:var(--danger-bg);border-color:var(--danger);color:var(--danger);' if '目标' in stage or 'Agent' in stage else 'background:var(--success-bg);border-color:var(--success);color:var(--success);'
                flow_html += f'<span class="ltc-step" style="{color}cursor:pointer;">{stage}({stage_counts[stage]})</span>'
                if i < len(row2) - 1:
                    flow_html += '<span class="ltc-arrow">&rarr;</span>'
            flow_html += '</div>'
        st.markdown(flow_html, unsafe_allow_html=True)

        # 选择阶段
        selected_stage = st.selectbox("选择阶段查看AI场景", stages, index=0, key="presale_stage")

        st.markdown("---")
        st.markdown(f'<div class="section-title">{selected_stage} - {stage_counts[selected_stage]}个AI场景</div>', unsafe_allow_html=True)
        for idx, s in enumerate(LTC_SCENARIOS[selected_stage]):
            st.markdown(render_scenario_card(s, idx), unsafe_allow_html=True)
    else:
        stages = list(AFTERSALES_SCENARIOS.keys())
        stage_counts = {k: len(v) for k, v in AFTERSALES_SCENARIOS.items()}

        # 售后流程图（两行）
        st.markdown('<div class="section-title">售后服务全流程闭环</div>', unsafe_allow_html=True)
        row1 = stages[:6]  # 客服与报修到竣工与验收
        row2 = stages[6:]  # 索赔申请到退换货

        flow_html = '<div class="ltc-flow">'
        for i, stage in enumerate(row1):
            color = 'background:#fef7e0;border-color:#e37400;color:#e37400;' if '客服' in stage or '工单' in stage else 'background:#e8f0fe;border-color:#1a73e8;color:#1a73e8;' if '故障' in stage or '维修' in stage or '领料' in stage else 'background:#e6f4ea;border-color:#0d904f;color:#0d904f;'
            flow_html += f'<span class="ltc-step" style="{color}cursor:pointer;">{stage}({stage_counts[stage]})</span>'
            if i < len(row1) - 1:
                flow_html += '<span class="ltc-arrow">&rarr;</span>'
        flow_html += '</div>'
        if row2:
            flow_html += '<div class="ltc-flow" style="margin-top:4px;">'
            for i, stage in enumerate(row2):
                color = 'background:#fce8e6;border-color:#d93025;color:#d93025;' if '索赔' in stage or '供应商' in stage else 'background:#fef7e0;border-color:#e37400;color:#e37400;'
                flow_html += f'<span class="ltc-step" style="{color}cursor:pointer;">{stage}({stage_counts[stage]})</span>'
                if i < len(row2) - 1:
                    flow_html += '<span class="ltc-arrow">&rarr;</span>'
            flow_html += '</div>'
        st.markdown(flow_html, unsafe_allow_html=True)

        # 选择阶段
        selected_stage = st.selectbox("选择阶段查看AI场景", stages, index=0, key="aftersale_stage")

        st.markdown("---")
        st.markdown(f'<div class="section-title">{selected_stage} - {stage_counts[selected_stage]}个AI场景</div>', unsafe_allow_html=True)
        for idx, s in enumerate(AFTERSALES_SCENARIOS[selected_stage]):
            st.markdown(render_scenario_card(s, idx), unsafe_allow_html=True)

    st.markdown("---")
    st.markdown('<div class="section-title">场景统计概览</div>', unsafe_allow_html=True)
    col1, col2, col3, col4 = st.columns(4)
    with col1: st.markdown(metric_card("143", "AI场景总数"), unsafe_allow_html=True)
    with col2: st.markdown(metric_card("92", "售前LTC场景"), unsafe_allow_html=True)
    with col3: st.markdown(metric_card("51", "售后服务场景"), unsafe_allow_html=True)
    with col4: st.markdown(metric_card("23", "LTC+售后阶段"), unsafe_allow_html=True)


# ============================================================
# 情报Agent
# ============================================================
elif page == "情报Agent":
    st.markdown(
        '<div class="topbar"><div><div class="topbar-title">情报Agent</div>'
        '<div class="topbar-sub">AI自动获取市场/客户/关键人情报</div></div></div>',
        unsafe_allow_html=True
    )
    col1, col2, col3, col4 = st.columns(4)
    with col1: st.markdown(metric_card("1,247", "情报条目/月"), unsafe_allow_html=True)
    with col2: st.markdown(metric_card("89%", "标讯精准率"), unsafe_allow_html=True)
    with col3: st.markdown(metric_card("23", "订阅规则"), unsafe_allow_html=True)
    with col4: st.markdown(metric_card("156", "监控企业"), unsafe_allow_html=True)

    tab1, tab2, tab3 = st.tabs(["企业信息", "招投标挖掘", "舆情监控"])
    with tab1:
        st.markdown('<div class="section-title">企业情报面板</div>', unsafe_allow_html=True)
        customer = st.selectbox("选择客户", ["A集团", "B股份", "C科技", "D新能源"])
        st.markdown(f"""
        <div class="card">
            <table class="data-table">
                <tr><th>项目</th><th>信息</th></tr>
                <tr><td>企业名称</td><td>{customer}</td></tr>
                <tr><td>注册资本</td><td>5,000万</td></tr>
                <tr><td>成立时间</td><td>2010-03</td></tr>
                <tr><td>行业</td><td>新能源/储能</td></tr>
                <tr><td>经营状态</td><td>{status_tag('存续', 'active')}</td></tr>
            </table>
        </div>
        """, unsafe_allow_html=True)
    with tab2:
        st.markdown('<div class="section-title">招投标AI挖掘</div>', unsafe_allow_html=True)
        st.markdown('<div class="card"><strong>AI精准匹配标讯</strong><p style="font-size:13px;color:var(--gray-700);margin-top:8px;">基于客户画像和产品关键词，AI自动从公开招标平台挖掘匹配标讯，精准度89%</p></div>', unsafe_allow_html=True)
    with tab3:
        st.markdown('<div class="section-title">舆情监控</div>', unsafe_allow_html=True)
        st.markdown('<div class="card"><strong>实时舆情预警</strong><p style="font-size:13px;color:var(--gray-700);margin-top:8px;">监控客户相关新闻、公告、社交媒体动态，AI自动分析情感倾向并预警风险</p></div>', unsafe_allow_html=True)


# ============================================================
# 客户互动Agent
# ============================================================
elif page == "客户互动Agent":
    st.markdown(
        '<div class="topbar"><div><div class="topbar-title">客户互动Agent</div>'
        '<div class="topbar-sub">多模态语料转写 · 发言人管理 · 互动摘要 · 需求管理</div></div></div>',
        unsafe_allow_html=True
    )
    for cap in AGENT_SYSTEM["客户互动Agent"]["capabilities"]:
        title = cap.split("：")[0] if "：" in cap else cap
        desc = cap.split("：")[1] if "：" in cap else ""
        st.markdown(f'<div class="agent-node success"><strong>{title}</strong><div style="font-size:12px;color:var(--gray-500);margin-top:4px;">{desc}</div></div>', unsafe_allow_html=True)


# ============================================================
# 客户画像Agent
# ============================================================
elif page == "客户画像Agent":
    st.markdown(
        '<div class="topbar"><div><div class="topbar-title">客户画像Agent</div>'
        '<div class="topbar-sub">线索画像(BANT) · 客户画像 · 商机画像(C139) · 赢率评估</div></div></div>',
        unsafe_allow_html=True
    )
    for cap in AGENT_SYSTEM["客户画像Agent"]["capabilities"]:
        title = cap.split("：")[0] if "：" in cap else cap
        desc = cap.split("：")[1] if "：" in cap else ""
        st.markdown(f'<div class="agent-node success"><strong>{title}</strong><div style="font-size:12px;color:var(--gray-500);margin-top:4px;">{desc}</div></div>', unsafe_allow_html=True)


# ============================================================
# 商机推进
# ============================================================
elif page == "商机推进":
    st.markdown(
        '<div class="topbar"><div><div class="topbar-title">商机推进助手</div>'
        '<div class="topbar-sub">商机阶段识别 · 赢率预测 · 关键人识别 · 风险预警</div></div></div>',
        unsafe_allow_html=True
    )
    for s in LTC_SCENARIOS["商机管理"]:
        st.markdown(render_scenario_card(s, LTC_SCENARIOS["商机管理"].index(s)), unsafe_allow_html=True)


# ============================================================
# 合同评审
# ============================================================
elif page == "合同评审":
    st.markdown(
        '<div class="topbar"><div><div class="topbar-title">合同智能评审</div>'
        '<div class="topbar-sub">标书要点抽取 · 合同风险审阅 · 审批材料整理</div></div></div>',
        unsafe_allow_html=True
    )
    for s in LTC_SCENARIOS["招投标与合同"]:
        st.markdown(render_scenario_card(s, LTC_SCENARIOS["招投标与合同"].index(s)), unsafe_allow_html=True)


# ============================================================
# 售后故障诊断
# ============================================================
elif page == "售后故障诊断":
    st.markdown(
        '<div class="topbar"><div><div class="topbar-title">售后故障智能诊断</div>'
        '<div class="topbar-sub">TIS故障检测 · 上位机告警 · 解决方案匹配 · 根因分析</div></div></div>',
        unsafe_allow_html=True
    )
    for s in AFTERSALES_SCENARIOS["故障诊断"]:
        st.markdown(render_scenario_card(s, AFTERSALES_SCENARIOS["故障诊断"].index(s)), unsafe_allow_html=True)


# ============================================================
# 智能工单
# ============================================================
elif page == "智能工单":
    st.markdown(
        '<div class="topbar"><div><div class="topbar-title">智能工单</div>'
        '<div class="topbar-sub">工单自动创建 · 智能派工 · 优先级排序 · 技能匹配</div></div></div>',
        unsafe_allow_html=True
    )
    for s in AFTERSALES_SCENARIOS["工单与派工"]:
        st.markdown(render_scenario_card(s, AFTERSALES_SCENARIOS["工单与派工"].index(s)), unsafe_allow_html=True)


# ============================================================
# 工作赋能Agent
# ============================================================
elif page == "工作赋能Agent":
    st.markdown(
        '<div class="topbar"><div><div class="topbar-title">工作赋能Agent</div>'
        '<div class="topbar-sub">GAP分析 · 风险预警 · 智能建议 · 业务报告</div></div></div>',
        unsafe_allow_html=True
    )
    col1, col2, col3, col4 = st.columns(4)
    with col1: st.markdown(metric_card("92%", "目标达成率"), unsafe_allow_html=True)
    with col2: st.markdown(metric_card("17", "活跃风险"), unsafe_allow_html=True)
    with col3: st.markdown(metric_card("34", "待办事项"), unsafe_allow_html=True)
    with col4: st.markdown(metric_card("8", "已生成报告"), unsafe_allow_html=True)
    st.markdown("---")
    for cap in AGENT_SYSTEM["工作赋能Agent"]["capabilities"]:
        title = cap.split("：")[0] if "：" in cap else cap
        desc = cap.split("：")[1] if "：" in cap else ""
        st.markdown(f'<div class="agent-node success"><strong>{title}</strong><div style="font-size:12px;color:var(--gray-500);margin-top:4px;">{desc}</div></div>', unsafe_allow_html=True)


# ============================================================
# 销售教练Agent
# ============================================================
elif page == "销售教练Agent":
    st.markdown(
        '<div class="topbar"><div><div class="topbar-title">销售教练Agent</div>'
        '<div class="topbar-sub">销冠方法论 · 风险诊断 · 策略推荐 · 实时陪练</div></div></div>',
        unsafe_allow_html=True
    )
    col1, col2, col3, col4 = st.columns(4)
    with col1: st.markdown(metric_card("87", "教练评分"), unsafe_allow_html=True)
    with col2: st.markdown(metric_card("5", "风险商机"), unsafe_allow_html=True)
    with col3: st.markdown(metric_card("12", "最佳实践"), unsafe_allow_html=True)
    with col4: st.markdown(metric_card("93%", "方法论遵循"), unsafe_allow_html=True)
    st.markdown("---")
    for cap in AGENT_SYSTEM["销售建议Agent"]["capabilities"]:
        title = cap.split("：")[0] if "：" in cap else cap
        desc = cap.split("：")[1] if "：" in cap else ""
        st.markdown(f'<div class="agent-node success"><strong>{title}</strong><div style="font-size:12px;color:var(--gray-500);margin-top:4px;">{desc}</div></div>', unsafe_allow_html=True)


# ============================================================
# 智能知识库
# ============================================================
elif page == "智能知识库":
    st.markdown(
        '<div class="topbar"><div><div class="topbar-title">智能知识库</div>'
        '<div class="topbar-sub">RAG检索 · 方案生成 · 知识推荐 · 话术提取</div></div></div>',
        unsafe_allow_html=True
    )
    col1, col2, col3, col4 = st.columns(4)
    with col1: st.markdown(metric_card("2,847", "知识条目"), unsafe_allow_html=True)
    with col2: st.markdown(metric_card("96%", "检索准确率"), unsafe_allow_html=True)
    with col3: st.markdown(metric_card("156", "解决方案"), unsafe_allow_html=True)
    with col4: st.markdown(metric_card("89", "FAQ条目"), unsafe_allow_html=True)
    st.markdown("---")
    for cap in AGENT_SYSTEM["智能知识库"]["capabilities"]:
        title = cap.split("：")[0] if "：" in cap else cap
        desc = cap.split("：")[1] if "：" in cap else ""
        st.markdown(f'<div class="agent-node success"><strong>{title}</strong><div style="font-size:12px;color:var(--gray-500);margin-top:4px;">{desc}</div></div>', unsafe_allow_html=True)


# ============================================================
# 智能问数
# ============================================================
elif page == "智能问数":
    st.markdown(
        '<div class="topbar"><div><div class="topbar-title">智能问数 / 自然语言BI</div>'
        '<div class="topbar-sub">用自然语言提问，AI返回指标与图表</div></div></div>',
        unsafe_allow_html=True
    )
    query = st.text_input("输入查询", placeholder="例如：本月销售额是多少？")
    if query:
        st.markdown(f'<div class="card"><div class="section-title">查询结果</div><div class="tool-call-box">查询: {query}<br/>AI解析: 销售指标查询<br/>结果: 本月销售额 4,230,000元，环比+12.5%</div></div>', unsafe_allow_html=True)


# ============================================================
# Agent工作流
# ============================================================
elif page == "Agent工作流":
    st.markdown(
        '<div class="topbar"><div><div class="topbar-title">Agent工作流 - 对话式业务操作</div>'
        '<div class="topbar-sub">语音/对话 -> AI理解 -> 槽位填充 -> 自动创建CRM记录</div></div></div>',
        unsafe_allow_html=True
    )
    workflows = LTC_SCENARIOS["Agent工作流"]
    tab_names = [w['title'] for w in workflows]
    tabs = st.tabs(tab_names)
    for i, w in enumerate(workflows):
        with tabs[i]:
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f'<div class="card" style="border-left:3px solid var(--accent);"><strong>场景说明</strong><p style="font-size:13px;color:var(--gray-700);margin-top:8px;">{w["example"]}</p><div style="font-size:12px;color:var(--gray-500);margin-top:8px;">Input: {w["input"]}<br/>Output: {w["output"]}<br/>Role: {w["role"]}</div></div>', unsafe_allow_html=True)
            with col2:
                st.markdown('<div class="section-title">Agent执行过程</div>', unsafe_allow_html=True)
                st.markdown(f'<div class="tool-call-box">1. 意图识别 -> {w["title"]}<br/>2. 槽位填充 -> 从对话中提取关键字段<br/>3. 数据校验 -> 检查字段完整性<br/>4. 系统调用 -> CRM API 创建记录<br/>-> {w["output"]}已创建</div>', unsafe_allow_html=True)


# ============================================================
# 系统设置
# ============================================================
elif page == "系统设置":
    st.markdown(
        '<div class="topbar"><div><div class="topbar-title">系统设置</div>'
        '<div class="topbar-sub">模型配置 · Agent管理 · 数据合规 · 场景总览</div></div></div>',
        unsafe_allow_html=True
    )
    tab1, tab2, tab3, tab4 = st.tabs(["模型配置", "Agent管理", "数据合规", "场景总览"])
    with tab1:
        st.markdown("""
        <div class="card">
            <div class="section-title">LLM 模型配置</div>
            <table class="data-table">
                <tr><th>配置项</th><th>当前值</th><th>说明</th></tr>
                <tr><td>主模型</td><td>通义千问 / DeepSeek</td><td>国产、成本低、稳定</td></tr>
                <tr><td>Temperature</td><td>0.1</td><td>低随机性，保证输出稳定</td></tr>
                <tr><td>向量模型</td><td>text-embedding-v2</td><td>文本向量化</td></tr>
            </table>
        </div>
        """, unsafe_allow_html=True)
    with tab2:
        st.markdown('<div class="section-title">6大Agent + 专用模块</div>', unsafe_allow_html=True)
        for name, data in AGENT_SYSTEM.items():
            st.markdown(f'<div class="agent-node success"><strong>{name}</strong> {status_tag("运行中", "active")}<div style="font-size:12px;color:var(--gray-500);margin-top:4px;">{" | ".join(data["capabilities"][:3])} ...</div></div>', unsafe_allow_html=True)
    with tab3:
        st.markdown("""
        <div class="card">
            <div class="section-title">数据安全与合规</div>
            <table class="data-table">
                <tr><th>安全项</th><th>状态</th><th>说明</th></tr>
                <tr><td>数据权限</td><td><span class="tag tag-active">Enabled</span></td><td>AI数据访问严格遵循用户权限</td></tr>
                <tr><td>数据脱敏</td><td><span class="tag tag-active">Enabled</span></td><td>敏感数据Masking传输</td></tr>
                <tr><td>审计日志</td><td><span class="tag tag-active">Enabled</span></td><td>支持脱敏与明文模式配置</td></tr>
                <tr><td>数据零留存</td><td><span class="tag tag-active">Enabled</span></td><td>LLM零留存协议</td></tr>
            </table>
        </div>
        """, unsafe_allow_html=True)
    with tab4:
        st.markdown('<div class="section-title">143个AI场景总览</div>', unsafe_allow_html=True)
        total = 0
        for stage, scenes in LTC_SCENARIOS.items():
            total += len(scenes)
            with st.expander(f"{stage} ({len(scenes)}个场景)"):
                for idx, s in enumerate(scenes):
                    st.markdown(render_scenario_card(s, idx), unsafe_allow_html=True)
        for stage, scenes in AFTERSALES_SCENARIOS.items():
            total += len(scenes)
            with st.expander(f"{stage} ({len(scenes)}个场景)"):
                for idx, s in enumerate(scenes):
                    st.markdown(render_scenario_card(s, idx), unsafe_allow_html=True)
        st.markdown(f"**共 {total} 个AI场景 + {len(GENERAL_CAPABILITIES)} 项通用能力**")


