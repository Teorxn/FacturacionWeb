"""Estilos de la aplicación.

[COMPLEMENTO] Streamlit no permite elegir por sí solo el color del menú
lateral ni el de cada botón, así que se agrega un poco de CSS.

Paleta: blanco como base y morado como acento.
"""

CSS = """
<style>
    :root {
        --morado: #6d28d9;
        --morado-oscuro: #4c1d95;
        --morado-medio: #7c3aed;
        --morado-claro: #a78bfa;
        --lavanda: #f5f3ff;
        --lavanda-borde: #e9e1ff;
        --rojo: #dc2626;
        --gris: #6b7280;
        --texto: #1f1b2e;
    }

    /* Barra superior de Streamlit: se deja transparente para que mande la nuestra. */
    header[data-testid="stHeader"] {
        background: transparent;
    }
    [data-testid="stToolbar"] {
        visibility: hidden;
    }
    .block-container {
        padding-top: 1.6rem;
        padding-bottom: 2rem;
    }

    /* ---------------- Barra superior ---------------- */
    .topbar {
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 16px;
        background: linear-gradient(120deg, var(--morado-oscuro), var(--morado-medio));
        padding: 12px 20px;
        border-radius: 10px;
        margin-bottom: 18px;
        box-shadow: 0 4px 14px rgba(76, 29, 149, .22);
    }
    .topbar .marca {
        color: #fff;
        font-weight: 800;
        letter-spacing: 2px;
        font-size: 20px;
    }
    .topbar .enlaces {
        display: flex;
        align-items: center;
        gap: 18px;
        flex-wrap: wrap;
    }
    .topbar a {
        color: #ede9fe;
        text-decoration: none;
        font-size: 14px;
        padding-bottom: 2px;
        border-bottom: 2px solid transparent;
    }
    .topbar a:hover {
        color: #fff;
    }
    .topbar a.activo {
        color: #fff;
        border-bottom-color: #c4b5fd;
    }
    .topbar .login {
        color: #fff;
        border: 1px solid #c4b5fd;
        border-radius: 20px;
        padding: 5px 14px;
        font-size: 13px;
    }

    /* ---------------- Menú lateral ---------------- */
    [data-testid="stSidebar"] {
        background-color: #fff;
        border-right: 1px solid var(--lavanda-borde);
    }
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p,
    [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] span {
        color: #3b0764;
    }
    [data-testid="stSidebar"] details,
    [data-testid="stSidebar"] details > div,
    [data-testid="stSidebar"] [data-testid="stExpander"] {
        border: none;
        background: transparent;
    }
    [data-testid="stSidebar"] details summary {
        color: var(--morado-oscuro);
        font-weight: 700;
        letter-spacing: .6px;
    }
    [data-testid="stSidebar"] svg {
        color: var(--morado);
        fill: var(--morado);
    }
    .marca-sidebar {
        color: var(--morado-oscuro);
        font-weight: 800;
        letter-spacing: 2px;
        font-size: 18px;
        margin: 0 0 14px 2px;
    }
    .menu-link {
        display: block;
        padding: 8px 12px;
        margin: 2px 0;
        border-radius: 6px;
        color: var(--morado-oscuro) !important;
        text-decoration: none;
        font-size: 14px;
        transition: background .15s;
    }
    .menu-link:hover {
        background: var(--lavanda);
    }
    .menu-link.activo {
        background: var(--lavanda-borde);
        border-left: 4px solid var(--morado);
        padding-left: 8px;
        color: var(--morado) !important;
        font-weight: 700;
    }

    /* ---------------- Títulos y cajas ---------------- */
    h2.titulo-pagina {
        color: var(--morado-oscuro);
        font-size: 26px;
        margin: 0 0 14px 0;
        font-weight: 800;
    }
    .well {
        background: var(--lavanda);
        border: 1px solid var(--lavanda-borde);
        border-left: 4px solid var(--morado-claro);
        border-radius: 8px;
        padding: 12px 16px;
        margin-bottom: 14px;
    }
    .aviso-eliminar {
        background: #fff8e1;
        border: 1px solid #fde68a;
        color: #92400e;
        padding: 12px 16px;
        border-radius: 8px;
        font-weight: 600;
        margin-bottom: 14px;
    }

    /* ---------------- Botones con color por acción ---------------- */
    .btn {
        display: inline-block;
        padding: 7px 14px;
        border-radius: 6px;
        color: #fff !important;
        text-decoration: none;
        font-size: 13px;
        font-weight: 600;
        border: 1px solid transparent;
        line-height: 1.4;
    }
    .btn:hover {
        filter: brightness(.92);
    }
    .btn-primary { background: var(--morado); }
    .btn-info { background: var(--morado-medio); }
    .btn-danger { background: var(--rojo); }
    .btn-secondary { background: var(--gris); }
    .btn-success { background: var(--morado-medio); }

    /* El botón real de Streamlit en la confirmación de borrado se pinta de rojo. */
    div[data-testid="column"]:has(.marca-peligro) button,
    div[data-testid="stColumn"]:has(.marca-peligro) button {
        background-color: var(--rojo) !important;
        border-color: var(--rojo) !important;
        color: #fff !important;
    }

    /* ---------------- Tablas ---------------- */
    .tabla-datos {
        width: 100%;
        border-collapse: collapse;
        background: #fff;
        border-radius: 8px;
        overflow: hidden;
        box-shadow: 0 1px 6px rgba(76, 29, 149, .08);
        margin-bottom: 8px;
    }
    .tabla-datos th {
        background: var(--lavanda-borde);
        color: var(--morado-oscuro);
        text-align: left;
        padding: 10px 12px;
        font-size: 13px;
        border-bottom: 2px solid var(--morado-claro);
    }
    .tabla-datos td {
        padding: 9px 12px;
        border-bottom: 1px solid #f1eefe;
        font-size: 14px;
        color: var(--texto);
        vertical-align: middle;
    }
    .tabla-datos tbody tr:hover td {
        background: #faf8ff;
    }
    .tabla-datos td:last-child {
        white-space: nowrap;
    }
    .tabla-detalle {
        width: 100%;
        border-collapse: collapse;
        background: #fff;
        border: 1px solid var(--lavanda-borde);
        border-radius: 8px;
        overflow: hidden;
        margin: 6px 0 16px 0;
    }
    .tabla-detalle th {
        background: var(--lavanda);
        color: var(--morado-oscuro);
        text-align: left;
        padding: 9px 12px;
        width: 190px;
        font-size: 13px;
    }
    .tabla-detalle td {
        padding: 9px 12px;
        border-top: 1px solid #f1eefe;
        font-size: 14px;
    }

    /* ---------------- Formularios y pie ---------------- */
    div[data-testid="stForm"] {
        border: 1px solid var(--lavanda-borde);
        border-radius: 10px;
        padding: 18px 20px;
        background: #fff;
        box-shadow: 0 2px 10px rgba(76, 29, 149, .06);
    }
    .footer {
        border-top: 1px solid var(--lavanda-borde);
        margin-top: 36px;
        padding-top: 12px;
        color: var(--gris);
        font-size: 12px;
        text-align: center;
    }
</style>
"""
