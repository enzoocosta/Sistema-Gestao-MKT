import streamlit as st

def delete_modal(item_type, item_id, item_name, delete_callback):
    """Componente reutilizável para confirmação de exclusão"""
    modal_key = f"delete_modal_{item_type}_{item_id}"
    
    # Botão que abre o modal
    if st.button(f"🗑️ Excluir", key=f"btn_delete_{item_id}"):
        st.session_state[modal_key] = True
    
    # Modal de confirmação
    if st.session_state.get(modal_key, False):
        st.warning(f"Tem certeza que deseja excluir {item_type.lower()} '{item_name}'?")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("✅ Confirmar", type="primary"):
                result = delete_callback(item_id)
                if result["success"]:
                    st.success(result["message"])
                else:
                    st.error(result["message"])
                st.session_state[modal_key] = False
                st.rerun()
        
        with col2:
            if st.button("❌ Cancelar"):
                st.session_state[modal_key] = False