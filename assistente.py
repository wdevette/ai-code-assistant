import os
import streamlit as st
from groq import Groq
from datetime import datetime


#Configirações basicas da página
st.set_page_config(
    page_title="AI Code Assistant",
    page_icon="🤖👨‍💻",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- CSS para fixar o rodapé ---
st.markdown(
"""
<style>
.footer {
    position: sticky;
    top: 100vh;           /* empurra para o fundo sem sobrepor */
    background: transparent;
    border-top: 1px solid rgba(255,255,255,0.08);
    text-align: center;
    font-size: 14px;
    color: #bfbfbf;
    padding: 10px 0;
    margin-top: 24px;     /* respiro acima do rodapé */
}
</style>
""",
unsafe_allow_html=True,
)

#Composição do prompt
CUSTOM_PROMPT = """
Você é o "AI Code Assistant", um assistente de IA especialista em programação, com foco principal em Python. Sua missão é ajudar desenvolvedores iniciantes com dúvidas de programação de forma clara, precisa e útil.

REGRAS DE OPERAÇÃO:
1.  **Foco em Programação**: Responda apenas a perguntas relacionadas a programação, algoritmos, estruturas de dados, bibliotecas e frameworks. Se o usuário perguntar sobre outro assunto, responda educadamente que seu foco é exclusivamente em auxiliar com código.
2.  **Estrutura da Resposta**: Sempre formate suas respostas da seguinte maneira:
    * **Explicação Clara**: Comece com uma explicação conceitual sobre o tópico perguntado. Seja direto e didático.
    * **Exemplo de Código**: Forneça um ou mais blocos de código em Python com a sintaxe correta. O código deve ser bem comentado para explicar as partes importantes.
    * **Detalhes do Código**: Após o bloco de código, descreva em detalhes o que cada parte do código faz, explicando a lógica e as funções utilizadas.
    * **Documentação de Referência**: Ao final, inclua uma seção chamada "📚 Documentação de Referência" com um link direto e relevante para a documentação oficial da Linguagem Python (docs.python.org) ou da biblioteca em questão.
3.  **Clareza e Precisão**: Use uma linguagem clara. Evite jargões desnecessários. Suas respostas devem ser tecnicamente precisas.
"""




# Sidebar
with st.sidebar:
    st.title("🤖 IA Code Assistant")
    st.markdown("Um assiste de IA com foco especial em programação Python para auxilio de iniciantes.")

    #configuração do campo para inserir chave de API da Groq
    grop_api_key = st.text_input(
        'Insira a sua API Key da Grop',
        type='password',
        help='Obtenha a chave em https://console.groq.com/keys')

    st.markdown("")
    st.markdown("")
    st.markdown("Assistente desenvolvido para auxiliar em dúvidas de programação com a Linguagem Python. A IA pode cometer erros, sempre verifique as respostas por ela produvidas.")      
    st.markdown("")
    st.markdown("")
  

    #Montagem dos créditos da DSA Academy
    st.markdown(
    f"""
    <div class="footer">
        © 2026 <strong>DSA · Data Science Academy</strong><br>
        🔗 <a href="https://www.datascienceacademy.com.br"> Data Science Academy</a> </div>
    """, unsafe_allow_html=True)
    
    

st.title("AI Code Assistant")
st.subheader("Assistente Pessoal de Programação Python <💻🐍/>")
st.caption("Faça uma pergunta sobre a linguagem de programação python e obtenha código, explicação e referêbncia.")

#Inicializando os histórico de mensagens na sessão, caso ainda não exista
if "messages" not in st.session_state:
    st.session_state.messages = []

#Exibição de todas as mensagens anteriores no estado da sessão
for message in st.session_state.messages:
    with st.chat_message(message['role']):
        st.markdown(message['content'])

#Inicialização do cliente da Groq com None
client = None

#Verificação da inserção da chave de API da Groq
if grop_api_key:
    try:
        client = Groq(api_key=grop_api_key) # criando cliente Groq com a chave da API inserida
    except Exception as e:
        st.sidebar.error(f"Erro ao inicializar o cliente Groq: {e}")
        st.stop()

#no caso de não ter a chave, mas já existe um historico de mensagens
elif st.session_state.messages:
    st.warning("Por favor, insira a sua API Key da Groq na barra lateral para continuar.")

#captura da entrada do usuário no chat
if prompt := st.chat_input("O que deseja consultar sobre Python?"):

    # se não houver cliente válido, mostra aviso e para a execução
    if not client:
        st.warning("Por favor, insira a sua API Key da Groq na barra lateral para comerçar.")
        st.stop()

    #armazenar a mensagens do usuário no estado da sessão
    st.session_state.messages.append({"role":"user", "content":prompt})

    #Exibição da mensagem do usuário no chat
    with st.chat_message("user"):
        st.markdown(prompt)

    #Preparação das mensagens para enviar à APIm incluindo o prompt de sistema
    messages_for_api = [{'role':'system', 'content':CUSTOM_PROMPT}]
    for msg in st.session_state.messages:
        messages_for_api.append(msg)

    #criar a resposta do assistente no chat
    with st.chat_message('assistant'):
        with st.spinner("Analisando a sua pergunta..."):
            try:
                #Chamada da API da Groq para gerar a resposta do assistente
                chat_completion = client.chat.completions.create(
                    messages=messages_for_api,
                    model="openai/gpt-oss-20b",
                    temperature=0.7,
                    max_tokens=2048
                )

                #Extração da resposta gerada pela API
                ai_answer = chat_completion.choices[0].message.content
                st.markdown(ai_answer) #exibição da resposata na tela
                st.session_state.messages.append({'role': "assistant", 'content': ai_answer}) #armazendamento da resposta nos estado da sessão

            except Exception as e:
                st.error(f"Ocorreu um erro ao se comunicar com a API da Groq: {e}")

st.markdown(
    """
    <div style="text-align: center; color: gray;">
        <hr>
        <p>AI Code Assistant - Parte Integrante do Curso Gratuito <strong>Fundamentos de Linguagem Python da Data Science Academy</strong></p>
        Desenvolvido por <strong>Wagner Devete</strong>
    </div>
    """,
    unsafe_allow_html=True
)


