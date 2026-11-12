"""Pantalla de inicio de sesión."""

import streamlit as st

from controllers import auth_controller as auth
from views.componentes import flash, ir_a


def render(page_destino="inicio"):
    """Dibuja el formulario de login.

    Si las credenciales son correctas, redirige a `page_destino`.
    """
    col_izq, col_centro, col_der = st.columns([1, 1.15, 1])

    with col_centro:
        st.markdown(
            '<div class="login-marca">FACTURACION</div>'
            '<div class="login-subtitulo">Acceso al sistema</div>',
            unsafe_allow_html=True,
        )

        with st.form("form_login", clear_on_submit=False):
            usuario = st.text_input(
                "Usuario",
                max_chars=50,
                key="login_usuario",
                placeholder="Escribe tu usuario",
            )
            contrasena = st.text_input(
                "Contraseña",
                type="password",
                max_chars=128,
                key="login_password",
                placeholder="Escribe tu contraseña",
            )
            enviar = st.form_submit_button(
                "Ingresar", type="primary", use_container_width=True
            )

        if enviar:
            ok, mensaje = auth.iniciar_sesion(usuario, contrasena)
            if ok:
                flash("success", mensaje)
                ir_a(page_destino)
            else:
                st.error(mensaje)

        st.markdown(
            '<div class="login-pie">Solo personal autorizado. '
            "Los intentos fallidos quedan limitados.</div>",
            unsafe_allow_html=True,
        )
