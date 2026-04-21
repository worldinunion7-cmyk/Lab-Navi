import streamlit as st
import uuid
import time

# iPhone向けのレイアウト設定
st.set_page_config(page_title="Lab-Navi Pro", layout="centered")

st.title("🧪 Lab-Navi with Timer")

# --- 1. プロトコルデータベース（タイマー設定付き） ---
# timer: 0 はタイマーなし、数値は秒単位（例: 900 = 15分）
protocol_db = {
    "組織処理・染色": {
        "採取筋肉の固定処理": [
            {"task": "固定液の調製", "timer": 0},
            {"task": "筋肉の採取・整形", "timer": 0},
            {"task": "4% PFAでの固定", "timer": 900},
            {"task": "洗浄・置換", "timer": 300}
        ],
        "DAPI染色": [
            {"task": "PBS洗浄", "timer": 300},
            {"task": "DAPI溶液添加・静置", "timer": 600},
            {"task": "洗浄・封入", "timer": 0}
        ],
    },
    "細胞培養": {
        "凍結細胞おこし": [
            {"task": "37℃ウォーターバスで融解", "timer": 120},
            {"task": "培地への懸濁", "timer": 0},
            {"task": "遠心分離 (1000rpm)", "timer": 180},
            {"task": "播種", "timer": 0}
        ],
    },
    # 他のプロトコルも同様に {"task": "...", "timer": 秒数} の形式で追加可能です。
}

# --- 2. 進行中の実験を保存するリストを初期化 ---
if 'active_experiments' not in st.session_state:
    st.session_state.active_experiments = []

# --- 3. 新しい実験の追加セクション ---
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
            "tasks": protocol_db[selected_cat][selected_proto]
        }
        st.session_state.active_experiments.append(new_exp)
        st.rerun()

st.divider()

# --- 4. 進行中の実験一覧セクション ---
st.markdown("### 🏃‍♂️ 進行中の実験")

for i, exp in enumerate(st.session_state.active_experiments):
    current_step_num = exp['step'] + 1
    total_steps = len(exp['tasks'])
    step_info = exp['tasks'][exp['step']]
    
    with st.expander(f"{exp['name']} ({current_step_num}/{total_steps})", expanded=True):
        st.progress(current_step_num / total_steps)
        st.warning(f"**Step {current_step_num}:** {step_info['task']}")
        
        # --- タイマー機能の表示 ---
        if step_info['timer'] > 0:
            timer_sec = step_info['timer']
            # タイマー表示用の枠
            timer_placeholder = st.empty()
            
            if st.button(f"⏱️ タイマー開始 ({timer_sec // 60}分)", key=f"t_{exp['id']}"):
                for t in range(timer_sec, -1, -1):
                    mins, secs = divmod(t, 60)
                    timer_placeholder.metric("残り時間", f"{mins:02d}:{secs:02d}")
                    time.sleep(1)
                st.success("時間です！")
        
        # 操作ボタン
        b1, b2 = st.columns(2)
        with b1:
            if st.button("✅ 完了", key=f"n_{exp['id']}", use_container_width=True):
                if exp['step'] < total_steps - 1:
                    st.session_state.active_experiments[i]['step'] += 1
                else:
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
    c1 = st.number_input("ストック濃度 (mM)", value=10.0)
    c2 = st.number_input("最終濃度 (uM)", value=100.0)
    v2 = st.number_input("最終液量 (uL)", value=1000.0)
    v1 = (c2 * 1e-6 * v2) / (c1 * 1e-3)
    st.metric("添加量 (uL)", f"{v1:.2f}")
