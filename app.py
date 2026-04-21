import streamlit as st
import uuid  # 各実験に固有のIDをつけるためのライブラリ

# iPhone向けのレイアウト設定
st.set_page_config(page_title="Lab-Navi", layout="centered")

st.title("🧪 Lab-Navi Mobile")

# --- サイドバー：試薬計算機 ---
with st.sidebar:
    st.header("🔢 試薬計算機")
    c1 = st.number_input("ストック濃度 (mM)", value=10.0)
    c2 = st.number_input("最終濃度 (uM)", value=100.0)
    v2 = st.number_input("最終液量 (uL)", value=1000.0)
    v1 = (c2 * 1e-6 * v2) / (c1 * 1e-3)
    st.metric("添加量 (uL)", f"{v1:.2f}")

# --- 1. 登録されているプロトコル（実験のレシピ） ---
protocols = {
    "🧬 DNA抽出": ["サンプルにバッファー添加", "56℃で10分インキュベート", "エタノール添加・撹拌", "遠心分離", "上清除去"],
    "🧫 細胞継代": ["培地をアスピレート", "PBSで洗浄", "トリプシン添加・3分待機", "培地を加えて回収", "遠心分離"],
    "💧 PCR準備": ["MasterMixの分注", "プライマーの添加", "テンプレートDNAの添加", "スピンダウン"]
}

# --- 2. 進行中の実験を保存するリストを初期化 ---
if 'active_experiments' not in st.session_state:
    st.session_state.active_experiments = []

# --- 3. 新しい実験の追加セクション ---
st.markdown("### ➕ 新しい実験を開始")
col1, col2 = st.columns([3, 1]) # 入力枠とボタンの幅の比率
with col1:
    selected_protocol = st.selectbox("プロトコルを選択", list(protocols.keys()), label_visibility="collapsed")
with col2:
    if st.button("追加", use_container_width=True):
        # 新しい実験をリストに追加する
        new_exp = {
            "id": str(uuid.uuid4())[:8], # プログラムが混同しないよう短いIDを付与
            "name": selected_protocol,
            "step": 0,                   # 初期ステップは0
            "tasks": protocols[selected_protocol]
        }
        st.session_state.active_experiments.append(new_exp)
        st.rerun()

st.divider() # 区切り線

# --- 4. 進行中の実験一覧セクション ---
st.markdown("### 🏃‍♂️ 進行中の実験")

if len(st.session_state.active_experiments) == 0:
    st.info("現在進行中の実験はありません。上のメニューから追加してください。")
else:
    # リストに保存されている実験を一つずつ表示
    for i, exp in enumerate(st.session_state.active_experiments):
        
        current_step_num = exp['step'] + 1
        total_steps = len(exp['tasks'])
        
        # 実験ごとに折りたたみ可能な枠（expander）を作る
        with st.expander(f"{exp['name']} (Step {current_step_num}/{total_steps})", expanded=True):
            
            # 進捗バー
            st.progress(current_step_num / total_steps)
            
            # 現在の指示
            current_task = exp['tasks'][exp['step']]
            st.warning(f"**現在の操作:** {current_task}")
            
            # 次の指示（予測しやすくなるよう、次のステップも小さく表示）
            if exp['step'] + 1 < total_steps:
                next_task = exp['tasks'][exp['step'] + 1]
                st.caption(f"次の操作: {next_task}")
            
            # アクションボタンを横並びに
            btn_col1, btn_col2 = st.columns(2)
            
            with btn_col1:
                # 完了ボタン（ボタンが混同しないよう key に固有IDを設定）
                if st.button("✅ 完了して次へ", key=f"next_{exp['id']}", use_container_width=True):
                    if exp['step'] < total_steps - 1:
                        st.session_state.active_experiments[i]['step'] += 1
                    else:
                        # 最後のステップならリストから削除
                        st.session_state.active_experiments.pop(i)
                        st.success("実験完了です！お疲れ様でした。")
                        st.balloons()
                    st.rerun()
                    
            with btn_col2:
                # 中止・削除ボタン
                if st.button("🗑️ 中止する", key=f"cancel_{exp['id']}", use_container_width=True):
                    st.session_state.active_experiments.pop(i)
                    st.rerun()
