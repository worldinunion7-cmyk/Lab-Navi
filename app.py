import streamlit as st
import uuid
import time

# 数値を 1.0 x 10^6 形式の文字列にする補助関数
def format_sci(val):
    if val == 0: return "0"
    import math
    exponent = int(math.floor(math.log10(abs(val))))
    coeff = val / (10**exponent)
    return f"{coeff:.1f} \\times 10^{{{exponent}}}"

st.set_page_config(page_title="Lab-Navi Pro", layout="centered")
st.title("🧪 Lab-Navi Expert")

# --- サイドバー：高度な計算機 ---
with st.sidebar:
    st.header("🧮 Lab Calculator")
    calc_mode = st.radio("モード選択", ["試薬希釈", "セルカウント・まき直し"])
    
    if calc_mode == "試薬希釈":
        st.subheader("🔢 試薬希釈計算")
        c1 = st.number_input("ストック濃度 (mM)", value=10.0)
        c2 = st.number_input("最終濃度 (uM)", value=100.0)
        v2 = st.number_input("最終液量 (uL)", value=1000.0)
        v1 = (c2 * 1e-6 * v2) / (c1 * 1e-3)
        st.metric("添加量 (uL)", f"{v1:.2f}")

    else:
        st.subheader("🧫 セルカウント・まき直し")
        
        # Step 1: セルカウント
        st.markdown("---")
        st.caption("Step 1: セルカウント")
        count_A = st.number_input("カウント数 A (個/0.1mm^3)", value=50.0)
        vol_B = st.number_input("回収溶液量 B (mL)", value=5.0)
        total_cells = count_A * vol_B * 10000
        st.latex(f"総細胞数: {format_sci(total_cells)} \, [cells]")
        
        # Step 2: 懸濁
        st.markdown("---")
        st.caption("Step 2: 懸濁（細胞溶液の作製）")
        target_C = st.number_input("目標濃度 C (個/mL)", value=1000000.0, format="%.e")
        st.latex(f"目標濃度: {format_sci(target_C)} \, [cells/mL]")
        
        needed_media_vol = total_cells / target_C
        st.info(f"**細胞を懸濁する培地量:** {needed_media_vol:.2f} mL")
        
        # Step 3: まき直し設定
        st.markdown("---")
        st.caption("Step 3: 各Dishへのまき直し")
        
        dish_info = {
            "3 cm": {"vol": 2.0},
            "6 cm": {"vol": 4.0},
            "10 cm": {"vol": 8.0}
        }
        selected_size = st.selectbox("Dishサイズを選択", list(dish_info.keys()))
        dish_count = st.number_input("まくDishの枚数", value=1, min_value=1)
        target_D = st.number_input("1枚あたりの目標細胞数 D (個)", value=100000.0, format="%.e")
        st.latex(f"目標数/dish: {format_sci(target_D)}")
        
        # 分注量の計算
        vol_per_dish_uL = (target_D / target_C) * 1000 
        total_seeding_vol_mL = (vol_per_dish_uL * dish_count) / 1000
        
        # 安全チェック
        if total_seeding_vol_mL > needed_media_vol:
            st.error("⚠️ エラー: 回収した細胞が足りません！")
        else:
            st.success(f"**1枚あたりの細胞溶液:** {vol_per_dish_uL:.1f} uL")
            
            method = st.radio("まき方", ["方法1: 規定量に上乗せ", "方法2: 合計量を合わせる"])
            base_vol = dish_info[selected_size]["vol"]
            
            if method == "方法1: 規定量に上乗せ":
                st.write(f"✅ 各Dishに **{base_vol} mL** の培地を入れ、そこに細胞溶液を **{vol_per_dish_uL:.1f} uL** ずつ加えてください。")
            else:
                base_media_per_dish = base_vol - (vol_per_dish_uL / 1000)
                st.write(f"✅ 各Dishに培地を **{base_media_per_dish:.3f} mL** 入れ、そこに細胞溶液を **{vol_per_dish_uL:.1f} uL** 加えて合計 **{base_vol} mL** にしてください。")

# --- メイン画面：プロトコル表示 (以前のロジックを継続) ---
# ... (ここに進行中実験の表示コードが入ります)
