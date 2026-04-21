import streamlit as st
import uuid
import time

# iPhone向けのレイアウト設定
st.set_page_config(page_title="Lab-Navi Pro", layout="centered")

st.title("🧪 Lab-Navi Expert")

# --- サイドバー：高度な計算機 ---
with st.sidebar:
    st.header("🧮 Lab Calculator")
    calc_mode = st.radio("モード選択", ["試薬希釈", "セルカウント・まき直し"])
    
    if calc_mode == "試薬希釈":
        st.subheader("🔢 試薬希釈計算")
        c1 = st.number_input("ストック濃度 (mM)", value=10.0, step=0.1)
        c2 = st.number_input("最終濃度 (uM)", value=100.0, step=1.0)
        v2 = st.number_input("最終液量 (uL)", value=1000.0, step=10.0)
        v1 = (c2 * 1e-6 * v2) / (c1 * 1e-3)
        st.metric("添加量 (uL)", f"{v1:.2f}")

    else:
        st.subheader("🧫 セルカウント・まき直し")
        # Step 1: セルカウント
        st.markdown("---")
        st.caption("Step 1: セルカウント")
        count_A = st.number_input("カウント数 A (個/0.1mm^3)", value=50.0, step=1.0)
        vol_B = st.number_input("回収溶液量 B (mL)", value=5.0, step=0.1)
        
        total_cells = count_A * vol_B * 10000
        st.metric("総細胞数 (個)", f"{total_cells:,.0f}")
        
        # Step 2: 懸濁（細胞溶液の作製）
        st.markdown("---")
        st.caption("Step 2: 懸濁（細胞溶液の作製）")
        target_C = st.number_input("目標濃度 C (個/mL)", value=1000000.0, step=10000.0, format="%.1e")
        
        needed_media_vol = total_cells / target_C
        st.info(f"**細胞を溶かす培地量:** {needed_media_vol:.2f} mL")
        
        # Step 3: まき直し
        st.markdown("---")
        st.caption("Step 3: 各Dishへのまき直し")
        target_D = st.number_input("1枚あたりの目標細胞数 D (個)", value=100000.0, step=1000.0, format="%.1e")
        vol_per_dish = (target_D / target_C) * 1000 # uL換算
        
        st.success(f"**1枚あたりの細胞溶液分注量:** {vol_per_dish:.1f} uL")
        
        # 方法の選択
        method = st.radio("まき方を選択", ["方法1: 規定量に上乗せ", "方法2: 合計量を規定量に合わせる"])
        dish_base_vol = st.number_input("Dishの規定培地量 (mL)", value=2.0, step=0.1)
        
        if method == "方法1: 規定量に上乗せ":
            st.write(f"👉 各Dishに **{dish_base_vol} mL** の培地を入れ、そこに細胞溶液を **{vol_per_dish:.1f} uL** 加えてください。")
        else:
            base_media_needed = (dish_base_vol * 1000) - vol_per_dish
            st.write(f"👉 各Dishに培地を **{base_media_needed/1000:.3f} mL** 入れ、そこに細胞溶液を **{vol_per_dish:.1f} uL** 加えて合計 **{dish_base_vol} mL** にしてください。")

# --- メイン画面：プロトコル管理（前回のコードを維持） ---
# (ここには以前の active_experiments などのロジックが入ります)
# 簡略化のため、新しいプロトコル追加と一覧表示のロジックを継続して使用してください。
