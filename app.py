import streamlit as st
import math

st.set_page_config(page_title="跌坎计算器", page_icon="🌊", layout="wide")

st.title("🌊 跌坎计算器")
st.markdown("根据 **B.4.1** 规范进行跌坎高度计算")

# 侧边栏输入
st.sidebar.header("📊 输入参数")

# 基础参数
hk = st.sidebar.number_input("hk - 跌坎上临界水深 (m)", min_value=0.0, value=1.0, step=0.1, format="%.4f")
hdc = st.sidebar.number_input("hdc - 跌坎上收缩水深 (m)", min_value=0.0, value=0.8, step=0.1, format="%.4f")
hds = st.sidebar.number_input("hds - 跌坎后河床水深 (m)", min_value=0.0, value=2.0, step=0.1, format="%.4f")
Pd = st.sidebar.number_input("Pd - 闸坎顶面与下游河底高差 (m)", min_value=0.0, value=1.5, step=0.1, format="%.4f")

st.sidebar.markdown("---")

# 设计参数验证
st.sidebar.header("🔧 设计参数建议")
theta = st.sidebar.slider("θ - 跌坎顶面倾角 (°)", min_value=0, max_value=10, value=5, step=1)
st.sidebar.info(f"✓ 跌坎顶面倾角 θ = {theta}° (宜在 0°~10° 内)")

R_input = st.sidebar.number_input("R - 跌坎反弧半径 (m)", min_value=0.0, value=2.0, step=0.1, format="%.2f")
R_min = 2.5 * hdc
if R_input >= R_min:
    st.sidebar.success(f"✓ 反弧半径 R = {R_input:.2f} m ≥ {R_min:.2f} m (2.5hdc)")
else:
    st.sidebar.warning(f"⚠ 反弧半径 R = {R_input:.2f} m < {R_min:.2f} m，建议不小于 2.5hdc")

Lm_input = st.sidebar.number_input("Lm - 跌坎长度 (m)", min_value=0.0, value=1.2, step=0.1, format="%.2f")
Lm_min = 1.5 * hdc
if Lm_input >= Lm_min:
    st.sidebar.success(f"✓ 跌坎长度 Lm = {Lm_input:.2f} m ≥ {Lm_min:.2f} m (1.5hdc)")
else:
    st.sidebar.warning(f"⚠ 跌坎长度 Lm = {Lm_input:.2f} m < {Lm_min:.2f} m，建议不小于 1.5hdc")

# 主要计算
st.header("📐 跌坎高度计算")

col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("公式 B.4.1-1")
    st.latex(r"P \geq 0.186 \frac{h_k^{2.75}}{h_{ds}^{1.75}}")
    
    P1 = 0.186 * (hk ** 2.75) / (hds ** 1.75)
    st.metric("P₁ (最小值)", f"{P1:.4f} m")
    st.caption("适用条件：基本跌坎高度")

with col2:
    st.subheader("公式 B.4.1-2")
    st.latex(r"P < \frac{2.24h_k - h_{ds}}{1.48\frac{h_k}{P_d} - 0.84}")
    
    denominator2 = 1.48 * (hk / Pd) - 0.84
    if abs(denominator2) > 0.001:
        P2 = (2.24 * hk - hds) / denominator2
        st.metric("P₂ (上限)", f"{P2:.4f} m")
        st.caption("适用条件：考虑闸坎影响")
    else:
        st.error("分母接近零，无法计算")
        P2 = None

with col3:
    st.subheader("公式 B.4.1-3")
    st.latex(r"P > \frac{2.38h_k - h_{ds}}{1.81\frac{h_k}{P_d} - 1.16}")
    
    denominator3 = 1.81 * (hk / Pd) - 1.16
    if abs(denominator3) > 0.001:
        P3 = (2.38 * hk - hds) / denominator3
        st.metric("P₃ (下限)", f"{P3:.4f} m")
        st.caption("适用条件：优化设计")
    else:
        st.error("分母接近零，无法计算")
        P3 = None

# 结果汇总
st.markdown("---")
st.header("📊 计算结果汇总")

result_col1, result_col2 = st.columns([2, 1])

with result_col1:
    st.markdown("### 跌坎高度 P 的取值范围")
    
    results = []
    if P1 is not None:
        results.append(("P₁ (B.4.1-1)", P1, "≥"))
    if P2 is not None:
        results.append(("P₂ (B.4.1-2)", P2, "<"))
    if P3 is not None:
        results.append(("P₃ (B.4.1-3)", P3, ">"))
    
    for name, value, operator in results:
        st.markdown(f"- **{name}**: P {operator} {value:.4f} m")
    
    st.markdown("---")
    st.markdown("### 🎯 推荐设计值")
    
    if P1 is not None and P2 is not None and P3 is not None:
        P_recommended = max(P1, P3)
        if P_recommended < P2:
            st.success(f"✓ 推荐跌坎高度：**P = {P_recommended:.4f} m**")
            st.caption(f"取值说明：P ≥ {P1:.4f} m 且 P > {P3:.4f} m 且 P < {P2:.4f} m")
        else:
            st.warning(f"⚠ 约束条件冲突，建议检查输入参数")
            st.caption(f"P₁ = {P1:.4f} m, P₂ = {P2:.4f} m, P₃ = {P3:.4f} m")
    else:
        st.info("部分公式无法计算，请检查输入参数")

with result_col2:
    st.markdown("### 设计参数检查")
    
    checks = [
        ("跌坎顶面倾角", f"θ = {theta}°", "0° ~ 10°", 0 <= theta <= 10),
        ("反弧半径", f"R = {R_input:.2f} m", f"≥ {R_min:.2f} m", R_input >= R_min),
        ("跌坎长度", f"Lm = {Lm_input:.2f} m", f"≥ {Lm_min:.2f} m", Lm_input >= Lm_min)
    ]
    
    for param, value, requirement, is_ok in checks:
        if is_ok:
            st.markdown(f"✅ **{param}**")
        else:
            st.markdown(f"❌ **{param}**")
        st.caption(f"{value} ({requirement})")

# 跌坎结构示意图
st.markdown("---")
with st.expander("📐 跌坎结构示意图（图 B.4.1）", expanded=True):
    import os
    diagram_path = "images/diagram_b41.png"
    
    if os.path.exists(diagram_path):
        st.image(diagram_path, caption="图 B.4.1 跌坎计算示意图", use_container_width=True)
    else:
        # 备用SVG图示
        st.markdown("""
        <svg width="100%" height="400" style="background-color: #0e1117; border-radius: 5px;">
            <!-- 上下游标注 -->
            <text x="30" y="30" fill="#d4d4d4" font-size="14">上游 ↓</text>
            <text x="450" y="30" fill="#d4d4d4" font-size="14">下游 ↓</text>
            
            <!-- 水位线 -->
            <line x1="20" y1="50" x2="580" y2="50" stroke="#4a90e2" stroke-width="2"/>
            
            <!-- 闸坎顶面 -->
            <text x="200" y="85" fill="#d4d4d4" font-size="12">闸坎顶面</text>
            <line x1="140" y1="100" x2="180" y2="100" stroke="#e0e0e0" stroke-width="2"/>
            <line x1="180" y1="100" x2="200" y2="110" stroke="#e0e0e0" stroke-width="2"/>
            <text x="210" y="105" fill="#d4d4d4" font-size="11">θ (倾角)</text>
            <line x1="200" y1="110" x2="240" y2="110" stroke="#e0e0e0" stroke-width="2"/>
            
            <!-- H标注 -->
            <text x="40" y="120" fill="#ffa500" font-size="12" font-weight="bold">H</text>
            <line x1="50" y1="130" x2="50" y2="160" stroke="#ffa500" stroke-width="2" stroke-dasharray="3,3"/>
            
            <!-- 跌坎主体 -->
            <line x1="140" y1="100" x2="140" y2="160" stroke="#e0e0e0" stroke-width="3"/>
            <line x1="240" y1="110" x2="240" y2="160" stroke="#e0e0e0" stroke-width="3"/>
            <text x="280" y="145" fill="#d4d4d4" font-size="12">跌坎</text>
            
            <!-- 反弧 -->
            <path d="M 240 160 Q 270 180, 300 200" stroke="#e0e0e0" stroke-width="3" fill="none"/>
            <text x="310" y="175" fill="#d4d4d4" font-size="11">R (反弧)</text>
            
            <!-- 水深标注 hk, hdc -->
            <text x="120" y="180" fill="#4a90e2" font-size="12" font-weight="bold">hk</text>
            <line x1="130" y1="185" x2="130" y2="160" stroke="#4a90e2" stroke-width="1.5" marker-start="url(#arrow)" marker-end="url(#arrow)"/>
            
            <text x="220" y="190" fill="#4a90e2" font-size="12" font-weight="bold">hdc</text>
            <line x1="235" y1="195" x2="235" y2="160" stroke="#4a90e2" stroke-width="1.5" marker-start="url(#arrow)" marker-end="url(#arrow)"/>
            
            <!-- 河床 -->
            <line x1="20" y1="200" x2="300" y2="200" stroke="#8b4513" stroke-width="4"/>
            <line x1="300" y1="200" x2="580" y2="230" stroke="#8b4513" stroke-width="4"/>
            <text x="340" y="220" fill="#8b4513" font-size="12">河床</text>
            
            <!-- hds标注 -->
            <text x="480" y="210" fill="#4a90e2" font-size="12" font-weight="bold">hds</text>
            <line x1="490" y1="215" x2="490" y2="230" stroke="#4a90e2" stroke-width="1.5" marker-start="url(#arrow)" marker-end="url(#arrow)"/>
            
            <!-- Lm长度标注 -->
            <line x1="140" y1="245" x2="240" y2="245" stroke="#ff6b6b" stroke-width="2" marker-start="url(#arrow2)" marker-end="url(#arrow2)"/>
            <text x="170" y="240" fill="#ff6b6b" font-size="12" font-weight="bold">Lm</text>
            
            <!-- Pd标注 -->
            <text x="120" y="280" fill="#ffa500" font-size="12" font-weight="bold">Pd</text>
            <text x="145" y="285" fill="#d4d4d4" font-size="10">(闸坎与河底高差)</text>
            <line x1="190" y1="290" x2="190" y2="200" stroke="#ffa500" stroke-width="2" stroke-dasharray="5,5" marker-start="url(#arrow3)" marker-end="url(#arrow3)"/>
            
            <!-- 基准线 -->
            <line x1="20" y1="320" x2="580" y2="320" stroke="#666" stroke-width="3"/>
            
            <!-- P标注 -->
            <text x="280" y="355" fill="#ff1744" font-size="14" font-weight="bold">P (跌坎高度)</text>
            <line x1="300" y1="365" x2="300" y2="200" stroke="#ff1744" stroke-width="2.5" stroke-dasharray="5,5" marker-start="url(#arrow4)" marker-end="url(#arrow4)"/>
            
            <!-- 箭头定义 -->
            <defs>
                <marker id="arrow" markerWidth="10" markerHeight="10" refX="5" refY="5" orient="auto">
                    <polygon points="0,5 5,2.5 5,7.5" fill="#4a90e2"/>
                </marker>
                <marker id="arrow2" markerWidth="10" markerHeight="10" refX="5" refY="5" orient="auto">
                    <polygon points="0,5 5,2.5 5,7.5" fill="#ff6b6b"/>
                </marker>
                <marker id="arrow3" markerWidth="10" markerHeight="10" refX="5" refY="5" orient="auto">
                    <polygon points="0,5 5,2.5 5,7.5" fill="#ffa500"/>
                </marker>
                <marker id="arrow4" markerWidth="10" markerHeight="10" refX="5" refY="5" orient="auto">
                    <polygon points="0,5 5,2.5 5,7.5" fill="#ff1744"/>
                </marker>
            </defs>
        </svg>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    st.markdown("""
    **参数说明：**
    - **P**: 跌坎高度（设计目标值）
    - **hk**: 跌坎上临界水深
    - **hdc**: 跌坎上收缩水深
    - **hds**: 跌坎后河床水深
    - **Pd**: 闸坎顶面与下游河底的高差
    - **θ**: 跌坎顶面倾角（0° ~ 10°）
    - **R**: 跌坎反弧半径（≥ 2.5hdc）
    - **Lm**: 跌坎长度（≥ 1.5hdc）
    
    **公式关系：**
    - B.4.1-1: P ≥ 0.186 × (hk^2.75 / hds^1.75)
    - B.4.1-2: P < (2.24hk - hds) / (1.48×hk/Pd - 0.84)
    - B.4.1-3: P > (2.38hk - hds) / (1.81×hk/Pd - 1.16)
    """)

# 公式详解
with st.expander("📖 公式详解与适用条件", expanded=False):
    st.markdown("""
    ### B.4.1-1 公式
    **P ≥ 0.186 × (hk^2.75 / hds^1.75)**
    - 用途：确定跌坎的最小高度
    - 适用：保证跌坎基本消能功能
    
    ### B.4.1-2 公式
    **P < (2.24hk - hds) / (1.48×hk/Pd - 0.84)**
    - 用途：确定跌坎高度的上限
    - 适用：考虑闸坎顶面影响，避免过高设计
    
    ### B.4.1-3 公式
    **P > (2.38hk - hds) / (1.81×hk/Pd - 1.16)**
    - 用途：确定跌坎高度的优化下限
    - 适用：综合考虑水力条件的优化设计
    
    ### 设计约束
    - **B.4.2**: 跌坎顶面倾角 θ 宜在 0° ~ 10° 内
    - **B.4.3**: 跌坎反弧半径 R 不宜小于跌坎上收缩水深的 2.5 倍 (R ≥ 2.5hdc)
    - **B.4.4**: 跌坎长度 Lm 不宜小于跌坎上收缩水深的 1.5 倍 (Lm ≥ 1.5hdc)
    """)

# 页脚
st.markdown("---")
st.caption("跌坎计算器 | 基于规范 B.4.1 ~ B.4.4 | © 2025")
