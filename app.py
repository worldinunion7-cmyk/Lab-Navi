import streamlit as st

# iPhone向けのレイアウト設定
st.set_page_config(page_title="Lab-Navi", layout="centered")

st.title("🧪 Lab-Navi Mobile")

# サイドバーに計算機能を配置（iPhoneでは左からスワイプで出てくる）
with st.sidebar:
    st.header("🔢 試薬計算機")
    c1 = st.number_input("ストック濃度 (mM)", value=10.0)
    c2 = st.number_input("最終濃度 (uM)", value=100.0)
    v2 = st.number_input("最終液量 (uL)", value=1000.0)
    
    # 計算式: v1 = (c2 * v2) / c1 (単位換算含む)
    v1 = (c2 * 1e-6 * v2) / (c1 * 1e-3)
    st.metric("添加量 (uL)", f"{v1:.2f}")

# メイン画面：プロトコルナビ
st.markdown("### 🧬 プロトコル実行中")
step_list = ["サンプル調整", "遠心分離 (12,000rpm)", "洗浄", "溶出"]

if 'step' not in st.session_state:
    st.session_state.step = 0

current = st.session_state.step

# 進捗バーを表示
progress = (current + 1) / len(step_list)
st.progress(progress)

# 現在の指示を大きく表示
st.warning(f"**現在の操作:** {step_list[current]}")

if st.button("✅ 完了して次のステップへ", use_container_width=True):
    if st.session_state.step < len(step_list) - 1:
        st.session_state.step += 1
        st.rerun()
    else:
        st.balloons()
        st.success("全行程終了！")