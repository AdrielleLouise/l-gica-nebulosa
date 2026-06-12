import streamlit as st
import pandas as pd
import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import matplotlib.pyplot as plt

st.title("Sistema Fuzzy para Conforto Térmico")
st.write(""" Este sistema utiliza Lógica Nebulosa para classificar o nível de conforto térmico com base na temperatura e na umidade. """)
st.title("Sistema Fuzzy para Conforto Térmico")

st.header("↳Variáveis Nebulosas")
col1, col2 = st.columns(2)
with col1:
    st.subheader("Entradas")
    st.markdown("""
**Temperatura**
- Frio
- Agradável
- Quente

**Umidade**
- Baixa
- Média
- Alta""")
with col2:
    st.subheader("Saída")
    st.markdown("""
**Conforto**

- Desconfortável
- Moderado
- Confortável""")
# variáveis de entrada
temperatura = ctrl.Antecedent(np.arange(0, 41, 1), 'temperatura')
umidade = ctrl.Antecedent(np.arange(0, 101, 1), 'umidade')

#variável de saída
conforto = ctrl.Consequent(np.arange(0, 101, 1), 'conforto')

#Funções de Pertinência
st.header("Funções de Pertinência")
temperatura['frio'] = fuzz.trimf(temperatura.universe, [0, 0, 20])
temperatura['agradavel'] = fuzz.trimf(temperatura.universe, [10, 20, 30])
temperatura['quente'] = fuzz.trimf(temperatura.universe, [20, 40, 40])
fig, ax = plt.subplots()
ax.plot(temperatura.universe, temperatura['frio'].mf, label='Frio')
ax.plot(temperatura.universe, temperatura['agradavel'].mf, label='Agradável')
ax.plot(temperatura.universe, temperatura['quente'].mf, label='Quente')
ax.set_title("Temperatura")
ax.legend()
st.pyplot(fig)

#umidade
umidade['baixa'] = fuzz.trimf(umidade.universe, [0, 0, 50])
umidade['media'] = fuzz.trimf(umidade.universe, [0, 50, 100])
umidade['alta'] = fuzz.trimf(umidade.universe, [50, 100, 100])
fig, ax = plt.subplots()
ax.plot(umidade.universe, umidade['baixa'].mf, label='Baixa')
ax.plot(umidade.universe, umidade['media'].mf, label='Média')
ax.plot(umidade.universe, umidade['alta'].mf, label='Alta')
ax.set_title("Umidade")
ax.legend()
st.pyplot(fig)

#conforto e desconforto térmico
conforto['desconfortavel'] = fuzz.trimf(conforto.universe, [0, 0, 50])
conforto['moderado'] = fuzz.trimf(conforto.universe, [30, 50, 70])
conforto['confortavel'] = fuzz.trimf(conforto.universe, [50, 100, 100])
fig, ax = plt.subplots()
ax.plot(conforto.universe, conforto['desconfortavel'].mf, label='Desconfortável')
ax.plot(conforto.universe, conforto['moderado'].mf, label='Moderado')
ax.plot(conforto.universe, conforto['confortavel'].mf, label='Confortável')
ax.set_title("Conforto")
ax.legend()
st.pyplot(fig)

#regras nebulosas
st.header("Regras Nebulosas")

st.markdown("""
**Regra 1**

SE Temperatura é Fria E Umidade é Alta

ENTÃO Conforto é Desconfortável

---

**Regra 2**

SE Temperatura é Agradável E Umidade é Média

ENTÃO Conforto é Moderado

---

**Regra 3**

SE Temperatura é Quente E Umidade é Baixa

ENTÃO Conforto é Desconfortável
""")
regra1 = ctrl.Rule(temperatura['frio'] & umidade['alta'], conforto['desconfortavel'])
regra2 = ctrl.Rule(temperatura['agradavel'] & umidade['media'], conforto['moderado'])
regra3 = ctrl.Rule(temperatura['quente'] & umidade['baixa'], conforto['desconfortavel'])
regra4 = ctrl.Rule(temperatura['frio'] & umidade['baixa'], conforto['confortavel'])
regra5 = ctrl.Rule(temperatura['frio'] & umidade['media'], conforto['moderado'])
regra6 = ctrl.Rule(temperatura['agradavel'] & umidade['baixa'], conforto['confortavel'])
regra7 = ctrl.Rule(temperatura['agradavel'] & umidade['alta'], conforto['moderado'])
regra8 = ctrl.Rule(temperatura['quente'] & umidade['alta'], conforto['desconfortavel'])
sistema = ctrl.ControlSystem([regra1, regra2, regra3, regra4, regra5, regra6, regra7, regra8])
st.header("Simulação Interativa")
temp = st.slider("Temperatura (°C)", 0, 40, 22)
umi = st.slider("Umidade (%)", 0, 100, 40)
if st.button("Calcular"):
    simulador = ctrl.ControlSystemSimulation(sistema)
    simulador.input['temperatura'] = temp
    simulador.input['umidade'] = umi
    simulador.compute()
    resultado = simulador.output['conforto']
    st.metric("Conforto Térmico", f"{resultado:.2f}")
    if resultado < 30:
        st.error("Desconfortável")
    elif resultado <= 70:
        st.warning("Moderado")
    else:
        st.success("Confortável")
def calcular_conforto(temp, umi):
    sim = ctrl.ControlSystemSimulation(sistema)
    sim.input['temperatura'] = temp
    sim.input['umidade'] = umi
    sim.compute()
    return sim.output['conforto']
caso1 = calcular_conforto(22, 40)
caso2 = calcular_conforto(35, 25)
st.header("Casos Solicitados pelo Professor Jorge")
df = pd.DataFrame({"Temperatura (°C)": [22, 35], "Umidade (%)": [40, 25], "Conforto": 
    [
        round(caso1, 2), round(caso2, 2)
    ]
})
st.table(df)
st.header("Conclusão")

st.write(f"""
O sistema de lógica nebulosa desenvolvido foi capaz de classificar o nível de conforto térmico a partir dos valores de temperatura e umidade definidos como entradas.

No primeiro caso analisado (22°C e 40% de umidade), o sistema retornou um valor de conforto igual a **{caso1:.2f}**, classificando a condição como **moderada**, conforme as regras nebulosas estabelecidas.

No segundo caso (35°C e 25% de umidade), o valor obtido foi **{caso2:.2f}**, indicando uma condição de **desconforto térmico**, resultado compatível com a regra que associa temperaturas elevadas e baixa umidade a níveis reduzidos de conforto.

Os resultados obtidos demonstram que a lógica nebulosa permite representar situações reais de forma flexível, utilizando conjuntos nebulosos e regras linguísticas para realizar a classificação do conforto térmico de maneira intuitiva e eficiente.
""")
