import pandas as pd
import streamlit as st
import re
import io

st.title("📊 Relatório de Contatos Técnicos")

# Puxar da planilha do google sheets
sheet_id = "1o8WxZootUshy8F7gFMEmmIxDGONtvGvxKjCvBJdgTEI"
aba = "Relat%C3%B3rio%20Contatos%20Tech"
url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={aba}"
df = pd.read_csv(url)
df.columns = df.columns.str.strip()

# Entrada dos IDs
ids_input = st.text_area("Cole os User ID Appmax (separados por vírgula, espaço ou enter):")

if st.button("🔍 Pesquisar"):
    if ids_input.strip() == "":
        st.warning("Por favor, cole os IDs para pesquisar.")
    else:
        # Processa os IDs
        ids = re.split(r"[,\s]+", ids_input.strip())
        ids = [id_.strip() for id_ in ids if id_.strip() != ""]

        # Converte a coluna da planilha para string e filtra
        df["User ID Appmax"] = df["User ID Appmax"].astype(str)
        encontrados = df[df["User ID Appmax"].isin(ids)]
        nao_encontrados = list(set(ids) - set(encontrados["User ID Appmax"]))

        # Vai exibir os resultados encontrados
        colunas_desejadas = [
            "Nome",
            "E-mail",
            "Número de telefone",
            "Modelo de Negócio",
            "Modelo de negócio qualificação",
            "Status atual RFV",
            "Status Notion"
        ]
        resultado = encontrados[["User ID Appmax"] + colunas_desejadas]
        st.success(f"{resultado.shape[0]} resultados encontrados:")
        st.dataframe(resultado, use_container_width=True)

        # Exibe os IDs não encontrados
        if nao_encontrados:
            st.warning(f"{len(nao_encontrados)} IDs não localizados:")
            st.code("\n".join(nao_encontrados), language='text')

        # Exportar para Excel
        excel_buffer = io.BytesIO()
        with pd.ExcelWriter(excel_buffer, engine='xlsxwriter') as writer:
            resultado.to_excel(writer, index=False, sheet_name='Resultados')
            if nao_encontrados:
                pd.DataFrame({"IDs não encontrados": nao_encontrados}).to_excel(writer, index=False, sheet_name='Não encontrados')

        excel_data = excel_buffer.getvalue()

        st.download_button(
            label="📥 Baixar Excel com resultados",
            data=excel_data,
            file_name="resultados_filtrados.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
else:
    st.info("Digite ou cole os User IDs acima e clique em Pesquisar para iniciar a busca.")

st.markdown("---")
st.caption("Desenvolvido por Heverton Vilas Boas")
