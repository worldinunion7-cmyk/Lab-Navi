import streamlit as st
import uuid
import time

# iPhone向けのレイアウト設定
st.set_page_config(page_title="Lab-Navi Expert", layout="centered")

st.title("🧪 Lab-Navi Expert")

# --- 1. プロトコルデータベース（詳細情報付き） ---
protocol_db = {
    "組織処理・染色": {
        "採取筋肉の固定処理": [
            {
                "task": "固定液の調製", 
                "timer": 0, 
                "details": "4% PFAは冷蔵庫の2段目。ドラフト内で作業すること。"
            },
            {
                "task": "4% PFAでの固定", 
                "timer": 900, 
                "details": "待ち時間に次のステップで使うスクロース溶液を準備。場所：棚B-3。"
            },
        ],
        "DAPI染色": [
            {
                "task": "DAPI溶液添加・静置", 
                "timer": 600, 
                "details": "遮光を忘れないこと。アルミホイルはシンク下の引き出し。"
            },
        ],
    },
    # 他のプロトコルも同様に details を追加可能です。
}

# --- 2. 状態の初期化 ---
if 'active_experiments' not in st.session_state:
    st.session_state.active_experiments = []

# --- 3. 新しい実験の追加 ---
st.markdown("### ➕ 新しい実験を開始")
cat_list = list(protocol_db.keys())
selected_cat = st.selectbox("カテゴリーを選択", cat_list)

col1, col2 = st.columns([3, 1])
with col1:
    proto_list = list(protocol_db[selected_cat].keys())
    selected_proto = st.selectbox("プロトコルを選択", proto_list, label_visibility="collapsed")
with col2:
    if st.button("開始", use_container_width=True):
        new_exp = {
            "id": str(uuid.uuid4())[:8],
            "name": selected_proto,
            "step": 0,
            "tasks": protocol_db[selected_cat][selected_proto],
            "notes": "" # 実験ごとのメモ欄
        }
        st.session_state.active_experiments.append(new_exp)
        st.rerun()

st.divider()

# --- 4. 進行中の実験一覧 ---
st.markdown("### 🏃‍♂️ 進行中の実験")

for i, exp in enumerate(st.session_state.active_experiments):
    current_step_num = exp['step'] + 1
    total_steps = len(exp['tasks'])
    step_info = exp['tasks'][exp['step']]
    
    with st.expander(f"{exp['name']} ({current_step_num}/{total_steps})", expanded=True):
        # 進捗
        st.progress(current_step_num / total_steps)
        
        # 指示
        st.warning(f"**Step {current_step_num}:** {step_info['task']}")
        
        # 【新機能】詳細・コツの表示
        if "details" in step_info and step_info["details"]:
            with st.status("📌 手順の詳細・物品場所", expanded=False):
                st.write(step_info["details"])
        
        # タイマー
        if step_info['timer'] > 0:
            timer_sec = step_info['timer']
            timer_placeholder = st.empty()
            if st.button(f"⏱️ タイマー開始 ({timer_sec // 60}分)", key=f"t_{exp['id']}"):
                for t in range(timer_sec, -1, -1):
                    mins, secs = divmod(t, 60)
                    timer_placeholder.metric("残り時間", f"{mins:02d}:{secs:02d}")
                    time.sleep(1)
                st.success("時間です！")
        
        # 【新機能】実験メモ欄（入力すると即座にsession_stateに保存される）
        # iPhoneでの入力を考慮し、少し高さを抑えています
        st.session_state.active_experiments[i]['notes'] = st.text_area(
            "メモ（気づき、サンプル名など）", 
            value=exp['notes'], 
            key=f"memo_{exp['id']}",
            height=100
        )
        
        # ボタン
        b1, b2 = st.columns(2)
        with b1:
            if st.button("✅ 完了", key=f"n_{exp['id']}", use_container_width=True):
                if exp['step'] < total_steps - 1:
                    st.session_state.active_experiments[i]['step'] += 1
                else:
                    # 完了時にメモをどうするか？（現在は消えますが、保存も可能です）
                    st.session_state.active_experiments.pop(i)
                    st.balloons()
                st.rerun()
        with b2:
            if st.button("🗑️ 中止", key=f"c_{exp['id']}", use_container_width=True):
                st.session_state.active_experiments.pop(i)
                st.rerun()

# サイドバー：計算機（維持）
with st.sidebar:
    st.header("🔢 試薬計算機")
    # ... (前回の計算機コードをそのまま配置)
