from io import BytesIO
import sqlite3
from PIL import Image
import streamlit as st

# ReportLab para PDFs
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

# Configuração da Página
st.set_page_config(
    page_title="ColorMatch Pro — Enterprise",
    page_icon="🎨",
    layout="centered",
)


# --- CONEXÃO COM O BANCO DE DADOS ---
def conectar_bd():
    return sqlite3.connect("colormatch_comercial.db")


# --- SISTEMA DE AUTENTICAÇÃO SIMPLIFICADO ---
if "logado" not in st.session_state:
    st.session_state["logado"] = False
    st.session_state["empresa"] = ""

if not st.session_state["logado"]:
    st.title("🎨 ColorMatch Pro — Login")
    st.caption("Acesse sua conta corporativa para gerenciar suas fórmulas.")

    tab_login, tab_cadastro = st.tabs(
        ["🔑 Entrar", "📝 Criar Conta (Novo Cliente)"]
    )

    with tab_login:
        email_login = st.text_input("E-mail do Laboratório / Empresa")
        senha_login = st.text_input("Senha", type="password")

        if st.button("ACESSAR SISTEMA", type="primary"):
            conn = conectar_bd()
            cursor = conn.cursor()
            cursor.execute(
                "SELECT id, empresa FROM usuarios WHERE email=? AND senha=?",
                (email_login, senha_login),
            )
            user = cursor.fetchone()
            conn.close()

            if user:
                st.session_state["logado"] = True
                st.session_state["user_id"] = user[0]
                st.session_state["empresa"] = user[1]
                st.rerun()
            else:
                st.error("E-mail ou senha incorretos.")

    with tab_cadastro:
        nova_empresa = st.text_input("Nome da Fábrica / Empresa")
        novo_email = st.text_input("E-mail Comercial")
        nova_senha = st.text_input("Crie uma Senha", type="password")

        if st.button("CADASTRAR MINHA FÁBRICA"):
            if nova_empresa and novo_email and nova_senha:
                try:
                    conn = conectar_bd()
                    cursor = conn.cursor()
                    cursor.execute(
                        "INSERT INTO usuarios (empresa, email, senha) VALUES (?, ?, ?)",
                        (nova_empresa, novo_email, nova_senha),
                    )
                    conn.commit()
                    conn.close()
                    st.success(
                        "Conta criada com sucesso! Faça login na aba ao lado."
                    )
                except:
                    st.error("Este e-mail ou empresa já está cadastrado.")
            else:
                st.warning("Preencha todos os campos.")

    st.stop()  # Trava o app até o usuário se autenticar

# =====================================================================
# ÁREA LOGADA (SISTEMA DE PRODUÇÃO PRIVADO DO CLIENTE)
# =====================================================================

st.sidebar.title(f"🏢 {st.session_state['empresa']}")
if st.sidebar.button("Sair / Logout"):
    st.session_state["logado"] = False
    st.rerun()

st.title("🎨 COLORMATCH PRO — IA & COLORIMETRIA")
st.caption("Módulo Industrial de Dosagem e Formulação")

# --- LEITURA E FORMULAÇÃO POR FOTO ---
st.subheader("📸 Leitura da Amostra em Tempo Real")
foto = st.camera_input("Tire a foto da tinta / amostra")

if foto:
    img = Image.open(foto).convert("RGB").resize((100, 100))
    pixels = list(img.getdata())
    r_mean = sum(p[0] for p in pixels) / len(pixels)
    g_mean = sum(p[1] for p in pixels) / len(pixels)
    b_mean = sum(p[2] for p in pixels) / len(pixels)

    r_norm, g_norm, b_norm = r_mean / 255.0, g_mean / 255.0, b_mean / 255.0
    L_val = 0.2126 * r_norm + 0.7152 * g_norm + 0.0722 * b_norm
    L_star = max(0.0, min(100.0, L_val * 100.0))
    a_star = (r_norm - g_norm) * 100.0
    b_star = ((r_norm + g_norm) / 2.0 - b_norm) * 100.0

    # Algoritmo Tristímulo / Pigmentos (Base 1kg)
    cb = round(max(0.002, (92.0 - L_star) * 0.008), 4) if L_star < 92.0 else 0.0
    y25 = round(b_star * 0.085, 4) if b_star > 2.0 else 0.0
    v930 = round(a_star * 0.045, 4) if a_star > 1.5 else 0.0
    sh = round(abs(b_star) * 0.035, 4) if b_star < -1.0 else 0.0

    nome_amostra = f"Amostra Custom (R:{int(r_mean)} G:{int(g_mean)})"

    st.success(f"🎯 Fórmula Gerada: *{nome_amostra}*")
    st.write(
        f"*Dosagem Sugerida (g/kg):* CB: {cb}g | Y25: {y25}g | 930: {v930}g | SH: {sh}g"
    )

    if st.button("💾 Salvar Fórmula na Minha Conta"):
        conn = conectar_bd()
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO cores_cliente (usuario_id, id_cor, nome_cor, cb, y25, v930, sh)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
            (
                st.session_state["user_id"],
                nome_amostra,
                nome_amostra,
                cb,
                y25,
                v930,
                sh,
            ),
        )
        conn.commit()
        conn.close()
        st.toast("Fórmula salva com sucesso no seu catálogo exclusivo!")

st.markdown("---")
st.subheader("📋 Ordem de Produção")

# Busca cores salvas no banco do cliente logado
conn = conectar_bd()
cursor = conn.cursor()
cursor.execute(
    "SELECT nome_cor, cb, y25, v930, sh FROM cores_cliente WHERE usuario_id=?",
    (st.session_state["user_id"],),
)
cores_salvas = cursor.fetchall()
conn.close()

if cores_salvas:
    opcoes_cores = {c[0]: c for c in cores_salvas}
    cor_escolhida = st.selectbox(
        "Selecione uma cor do seu catálogo:", list(opcoes_cores.keys())
    )
    qtd_caixas = st.number_input(
        "Quantidade de Caixas/Baldes (ex: 18L)", min_value=1, value=10
    )

    if st.button("🧮 CALCULAR BATELADA DE PRODUÇÃO", type="primary"):
        dados_cor = opcoes_cores[cor_escolhida]
        cb_tot = dados_cor[1] * qtd_caixas * 18
        y25_tot = dados_cor[2] * qtd_caixas * 18
        v930_tot = dados_cor[3] * qtd_caixas * 18
        sh_tot = dados_cor[4] * qtd_caixas * 18

        st.markdown("### ⚖️ Dosagem Total na Balança:")
        st.write(f"• *Preto (CB):* {cb_tot:.2f} g")
        st.write(f"• *Amarelo (Y25):* {y25_tot:.2f} g")
        st.write(f"• *Vermelho (930):* {v930_tot:.2f} g")
        st.write(f"• *Azul (SH):* {sh_tot:.2f} g")

        # Gerador de PDF em Memória
        buffer = BytesIO()
        pdf = canvas.Canvas(buffer, pagesize=A4)
        pdf.setFont("Helvetica-Bold", 16)
        pdf.drawString(
            50,
            800,
            f"ORDEM DE PRODUÇÃO — {st.session_state['empresa'].upper()}",
        )
        pdf.setFont("Helvetica", 12)
        pdf.drawString(
            50, 770, f"Cor: {cor_escolhida} | Batelada: {qtd_caixas} Caixas/Baldes"
        )
        pdf.line(50, 755, 550, 755)

        pdf.drawString(50, 720, "Dosagens de Pigmentos:")
        pdf.drawString(70, 695, f"- Preto (CB): {cb_tot:.2f} g")
        pdf.drawString(70, 675, f"- Amarelo (Y25): {y25_tot:.2f} g")
        pdf.drawString(70, 655, f"- Vermelho (930): {v930_tot:.2f} g")
        pdf.drawString(70, 635, f"- Azul (SH): {sh_tot:.2f} g")
        pdf.save()

        st.download_button(
            label="📄 BAIXAR PDF DA ORDEM",
            data=buffer.getvalue(),
            file_name=f"Ordem_{cor_escolhida}.pdf",
            mime="application/pdf",
        )
else:
    st.info(
        "Nenhuma cor no seu catálogo ainda. Tire uma foto da amostra acima para salvar sua primeira cor!"
    )