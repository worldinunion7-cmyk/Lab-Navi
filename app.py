import streamlit as st
import uuid

# iPhone向けのレイアウト設定
st.set_page_config(page_title="Lab-Navi", layout="centered")

st.title("🧪 Lab-Navi Professional")

# --- 1. プロトコルデータベース（カテゴリー別） ---
# ※手順（リストの中身）は、まずは代表的なステップを仮で入れています。
# ご自身の正確な手順に書き換えてください。
protocol_db = {
    "組織処理・染色": {
        "採取筋肉の固定処理": ["固定液の調製", "筋肉の採取・整形", "4% PFAでの固定", "洗浄・置換"],
        "筋組織の凍結": ["スクロース置換", "OCTコンパウンドへの包埋", "液体窒素/イソペンタンでの凍結", "保存"],
        "凍結組織の薄切": ["クライオスタット温度設定", "サンプルマウント", "薄切(10um)", "スライド回収"],
        "スライドグラス免疫染色": ["ブロッキング", "一次抗体反応(O/N)", "洗浄", "二次抗体反応", "封入"],
        "H染色": ["ヘマトキシリン染色", "分別", "色出し", "脱水・透徹"],
        "DAPI染色": ["PBS洗浄", "DAPI溶液添加", "インキュベート", "洗浄・封入"],
        "Sirius Red染色": ["脱パラ/親水化", "Sirius Red液染色", "分別", "脱水・封入"],
    },
    "細胞培養 (Maintenance)": {
        "凍結細胞おこし": ["37℃ウォーターバスで融解", "培地への懸濁", "遠心分離", "播種"],
        "細胞はがし＆まき直し（凍結なし）": ["培地除去", "PBS洗浄", "トリプシン処理", "カウント・播種"],
        "細胞はがし＆まき直し（凍結あり）": ["細胞回収", "カウント", "一部を播種", "残りを凍結用へ"],
        "細胞凍結": ["細胞回収・カウント", "凍結媒体への懸濁", "バンビーカー等で徐冷", "-80℃保存"],
        "Dish作製（コラーゲンコート）": ["コラーゲン液調製", "Dishへ分注", "インキュベート", "洗浄・乾燥"],
    },
    "細胞培養 (Experiment)": {
        "培養細胞のFIX(Growth, EdU＋)": ["EdU添加", "インキュベート", "4% PFA固定", "透過処理"],
        "培養細胞のFIX(Diff, EdUー)": ["培地除去", "4% PFA固定", "PBS洗浄", "4℃保存"],
        "トランスフェクション": ["試薬混合液調製", "インキュベート", "細胞への添加", "メディア交換"],
        "インフェクション": ["ウイルス液調製", "ポリブレン添加", "細胞への添加", "24h後洗浄"],
    },
    "分子生物学・その他": {
        "Midi Prep用Overnight Culture": ["培地分注", "抗生物質添加", "菌体植菌", "振盪培養"],
        "Midi Prep": ["菌体回収", "溶液I,II,III添加", "カラム精製", "溶出"],
        "アガロースゲル作製": ["TAE/TBE測定", "アガロース溶解", "コーム設置", "固化待機"],
        "サクション廃液処理": ["廃液回収", "次亜塩素酸処理", "中和・廃棄"],
        "RNA用サンプル回収": ["RNAlater添加または液窒凍結", "チューブ移送", "-80℃保存"],
        "細菌液体培地作製（Agarなし）": ["成分計測", "オートクレーブ", "冷却・抗生物質添加"],
        "細菌液体培地作製（Agarあり）": ["成分+Agar計測", "オートクレーブ", "プレート作製"],
    }
}

# --- 2. 進行中の実験を保存するリストを初期化 ---
if 'active_experiments' not in st.session_state:
    st.session_state.active_experiments = []

# --- 3. 新しい実験の追加セクション ---
st.markdown("### ➕ 新しい実験を開始")

# カテゴリー選択 -> 実験選択 の二段階にする
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

if len(st.session_state.active_experiments) == 0:
    st.info("待機中のタスクはありません。")
else:
    for i, exp in enumerate(st.session_state.active_experiments):
        current_step_num = exp['step'] + 1
        total_steps = len(exp['tasks'])
        
        with st.expander(f"{exp['name']} ({current_step_num}/{total_steps})", expanded=True):
            st.progress(current_step_num / total_steps)
            st.warning(f"**Step {current_step_num}:** {exp['tasks'][exp['step']]}")
            
            # 次のステップのプレビュー
            if exp['step'] + 1 < total_steps:
                st.caption(f"Next: {exp['tasks'][exp['step'] + 1]}")
            
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

# サイドバー：計算機（そのまま維持）
with st.sidebar:
    st.header("🔢 試薬計算機")
    c1 = st.number_input("ストック濃度 (mM)", value=10.0)
    c2 = st.number_input("最終濃度 (uM)", value=100.0)
    v2 = st.number_input("最終液量 (uL)", value=1000.0)
    v1 = (c2 * 1e-6 * v2) / (c1 * 1e-3)
    st.metric("添加量 (uL)", f"{v1:.2f}")
