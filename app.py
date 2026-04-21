import streamlit as st
import uuid
import time
import math

# LaTeX形式の指数表記にする関数
def format_sci_latex(val):
    if val <= 0: return "0"
    exponent = int(math.floor(math.log10(abs(val))))
    coeff = val / (10**exponent)
    return f"{coeff:.2f} \\times 10^{{{exponent}}}"

st.set_page_config(page_title="Lab-Navi Pro", layout="centered")
st.title("🧪 Lab-Navi Expert")

# --- サイドバー：セルカウント・まき直し専用計算機 ---
with st.sidebar:
    st.header("🧮 Lab Calculator")
    st.subheader("🧫 セルカウント・まき直し")
    
    # --- Step 1: 現在の細胞数を確認 ---
    st.markdown("---")
    st.caption("Step 1: 現在の細胞数")
    count_A = st.number_input("カウント数 A (個/0.1mm^3)", value=50.0)
    vol_B = st.number_input("回収溶液量 B (mL)", value=5.0)
    total_cells = count_A * vol_B * 10000
    st.latex(f"現在の総細胞数: {format_sci_latex(total_cells)}")

    # --- Step 2: 目標の設定（視覚的入力） ---
    st.markdown("---")
    st.caption("Step 2: 1枚あたりの目標数 D")
    c_col, e_col = st.columns([2, 1])
    with c_col:
        d_coeff = st.number_input("係数", value=1.0, key="d_c")
    with e_col:
        d_expo = st.number_input("指数 10^x", value=5, step=1, key="d_e")
    target_D = d_coeff * (10**d_expo)
    st.latex(f"目標: {format_sci_latex(target_D)} \, [cells/dish]")

    # --- Step 3: Dish設定 ---
    st.markdown("---")
    st.caption("Step 3: Dish設定")
    dish_info = {"3 cm": 2.0, "6 cm": 4.0, "10 cm": 8.0}
    selected_size = st.selectbox("サイズ", list(dish_info.keys()))
    dish_count = st.number_input("枚数", value=1, min_value=1)
    
    # 必要な総細胞数
    required_cells = target_D * dish_count
    st.latex(f"必要総数: {format_sci_latex(required_cells)}")
    
    if required_cells > total_cells:
        st.error("⚠️ 細胞が足りません！")
    else:
        # --- Step 4: まきやすさ（分注量）の指定 ---
        # 1枚あたり何uLずつ分注したいか（これで目標濃度Cが決まる）
        st.markdown("---")
        st.caption("Step 4: まきやすさの調整")
        dispense_uL = st.slider("1枚あたりの細胞溶液分注量 (uL)", 50, 500, 200, step=10)
        
        # 目標濃度 C の計算: C = D / (分注量 mL)
        target_C = target_D / (dispense_uL / 1000)
        # 必要な懸濁用培地量: V = 総細胞数 / C
        suspend_vol = total_cells / target_C
        
        st.latex(f"算出された目標濃度 C: {format_sci_latex(target_C)} \, [cells/mL]")
        st.success(f"✅ **培地 {suspend_vol:.3f} mL** で細胞を溶かしてください。")

        # --- Step 5: 方法別指示 ---
        st.markdown("---")
        method = st.radio("まき方", ["方法1: 規定量に上乗せ", "方法2: 合計量を合わせる"])
        base_vol_mL = dish_info[selected_size]
        
        if method == "方法1: 規定量に上乗せ":
            st.write(f"👉 各Dishに培地 **{base_vol_mL} mL** を入れ、そこに細胞溶液を **{dispense_uL} uL** 加える。")
        else:
            base_media_per_dish = base_vol_mL - (dispense_uL / 1000)
            st.write(f"👉 各Dishに培地 **{base_media_per_dish:.3f} mL** を入れ、そこに細胞溶液を **{dispense_uL} uL** 加えて合計 **{base_vol_mL} mL** にする。")

# --- メイン画面：プロトコル表示（維持） ---
# ... (以前のコードをそのまま使用)
