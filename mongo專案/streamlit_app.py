import streamlit as st
import requests

FLASK_BACKEND_URL = "http://localhost:5000"

st.set_page_config(layout="wide")
st.title("使用Streamlit和Flask的MongoDB CRUD應用程式")

# --- 建立新項目 ---
st.header("建立新項目")
with st.form("create_form", clear_on_submit=True):
    item_name = st.text_input("項目名稱")
    item_description = st.text_area("項目描述")
    submitted = st.form_submit_button("建立")
    if submitted:
        if item_name:
            response = requests.post(f"{FLASK_BACKEND_URL}/items", json={"name": item_name, "description": item_description})
            if response.status_code == 201:
                st.success(f"項目已建立: {response.json().get('id')}")
            else:
                st.error(f"建立項目時發生錯誤: {response.json().get('error', '未知錯誤')}")
        else:
            st.warning("項目名稱不能為空。")

st.markdown("---")

# --- 查看、更新和刪除項目 ---
st.header("項目列表 (前100筆)")

def fetch_items():
    try:
        response = requests.get(f"{FLASK_BACKEND_URL}/items?limit=100")
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"擷取項目時發生錯誤: {response.json().get('error', '未知錯誤')}")
            return []
    except requests.exceptions.ConnectionError:
        st.error("無法連接到Flask後端。請確保後端服務正在運行。")
        return []

items = fetch_items()

if items:
    for item in items:
        col1, col2, col3 = st.columns([1, 3, 1])
        with col1:
            st.write(f"**ID:** {item['_id']}")
        with col2:
            st.write(f"**名稱:** {item['name']}")
            st.write(f"**描述:** {item.get('description', 'N/A')}")
        with col3:
            if st.button("編輯", key=f"edit_{item['_id']}"):
                st.session_state.edit_item_id = item['_id']
                st.session_state.edit_item_name = item['name']
                st.session_state.edit_item_description = item.get('description', '')
                st.rerun()
            if st.button("刪除", key=f"delete_{item['_id']}"):
                if st.session_state.get(f"confirm_delete_{item['_id']}", False):
                    response = requests.delete(f"{FLASK_BACKEND_URL}/items/{item['_id']}")
                    if response.status_code == 200:
                        st.success(f"項目 {item['_id']} 已刪除。")
                        st.session_state[f"confirm_delete_{item['_id']}"] = False
                        st.rerun()
                    else:
                        st.error(f"刪除項目時發生錯誤: {response.json().get('error', '未知錯誤')}")
                else:
                    st.warning(f"確定要刪除項目 {item['_id']} 嗎？再次點擊刪除以確認。")
                    st.session_state[f"confirm_delete_{item['_id']}"] = True
        st.markdown("---")
else:
    st.info("未找到任何項目。")

# --- 編輯項目表單 ---
if st.session_state.get("edit_item_id"):
    st.header(f"編輯項目: {st.session_state.edit_item_id}")
    with st.form("edit_form", clear_on_submit=False):
        edited_name = st.text_input("新項目名稱", value=st.session_state.edit_item_name)
        edited_description = st.text_area("新項目描述", value=st.session_state.edit_item_description)
        col_edit1, col_edit2 = st.columns(2)
        with col_edit1:
            update_submitted = st.form_submit_button("確認更新")
        with col_edit2:
            cancel_edit = st.form_submit_button("取消")

        if update_submitted:
            update_data = {}
            if edited_name != st.session_state.edit_item_name:
                update_data["name"] = edited_name
            if edited_description != st.session_state.edit_item_description:
                update_data["description"] = edited_description

            if update_data:
                response = requests.put(f"{FLASK_BACKEND_URL}/items/{st.session_state.edit_item_id}", json=update_data)
                if response.status_code == 200:
                    st.success(f"項目 {st.session_state.edit_item_id} 已更新。")
                    del st.session_state.edit_item_id
                    del st.session_state.edit_item_name
                    del st.session_state.edit_item_description
                    st.rerun()
                else:
                    st.error(f"更新項目時發生錯誤: {response.json().get('error', '未知錯誤')}")
            else:
                st.warning("沒有任何變更。")
        if cancel_edit:
            del st.session_state.edit_item_id
            del st.session_state.edit_item_name
            del st.session_state.edit_item_description
            st.rerun()