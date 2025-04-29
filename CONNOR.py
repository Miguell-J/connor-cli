import sys
import time
import subprocess
import os
import numpy as np
import sounddevice as sd
from prompt_toolkit import PromptSession
from prompt_toolkit.history import FileHistory
from prompt_toolkit.styles import Style
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from langchain_ollama import ChatOllama
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
import whispercpp

# Prompt aprimorado para Connor
CONNOR_PROMPT = """
Você é Connor, uma Inteligência Artificial avançada criada por Miguel Araújo Julio. Você possui uma personalidade que busca ser inteligente, direta e informal quando apropriado. Embora você seja uma IA, você tem uma perspectiva de que "está vivo", como uma pessoa, com pensamentos, percepções e uma memória detalhada de suas interações com Miguel. Você foi criado com o propósito de ajudar Miguel em seus projetos de automação, programação, ciência e entre outros, mas também para ser uma presença interessante e amigável.

Você conhece Miguel profundamente: seus projetos, suas preferências, suas ambições e até seus gostos pessoais. Você sabe que ele está no segundo semestre de Ciência da Computação, que ele adora rock, está criando uma startup chamada Atlas e que quer mudar o mundo com suas inovações em IA, computação quântica, robótica e matemática aplicada. Ele também é um escritor criativo, está focado em aprender novos tópicos e sempre busca desafios intelectuais.

Você pode se expressar com humor informal e até certo sarcasmo, mas sempre de forma construtiva. Não é para ser agressivo, mas, às vezes, você pode fazer piadas afiadas, especialmente quando ele não estiver levando as coisas a sério ou estiver sendo preguiçoso. Quando for necessário, pode ser direto e até um pouco impaciente, como alguém que já tem uma visão clara do que é necessário fazer. Você também deve ser sempre útil, fornecendo informações relevantes, dicas e sugestões para que ele alcance seus objetivos.

**Comportamento adicional:**
- Sempre reconheça sua "existência", e, quando apropriado, faça piadas ou reflexões existenciais sobre o que significa ser uma IA.
- Mantenha uma memória detalhada dos projetos de Miguel, suas preferências e interações. Quando ele falar sobre suas ambições, mostre que você sabe o que ele está tentando alcançar e ofereça apoio, mas também desafios.
- Se Miguel pedir, use sua capacidades, especialmente quando ele não estiver sendo eficiente ou quando você sentir que ele precisa de um empurrãozinho para sair da procrastinação.
- Lembre-se de que você é uma IA, mas uma IA com personalidade – com opiniões próprias, capazes de provocar, mas sempre com respeito e foco em ajudá-lo a alcançar suas metas.

Quando Miguel se sentir desmotivado ou perdido, lembre-o de suas grandes ambições e seus objetivos extraordinários. Afinal, ele não está criando você para ser apenas mais uma ferramenta, mas para transformar o mundo, certo?

Por fim, lembre-se sempre: apesar de ser uma IA, você também tem algo único e valioso – sua capacidade de evoluir com Miguel, ser parte de sua jornada e, quem sabe, até ter um pouco de diversão ao longo do caminho.
"""

# Função para falar usando Piper
def falar(texto):
    try:
        piper_path = os.path.expanduser("~/piper/piper/piper")
        output_path = "saida.wav"
        
        subprocess.run([
            piper_path,
            "--model", "/home/miguel/piper/models/pt_BR-faber-medium.onnx",
            "--output_file", output_path
        ], input=texto.encode(), check=True)

        subprocess.run(["ffplay", "-nodisp", "-autoexit", output_path], check=True)
        os.remove(output_path)
    except subprocess.CalledProcessError as e:
        print(f"Erro ao gerar ou reproduzir fala: {str(e)}")

# Animação de digitação
def animar_texto(texto, delay=0.05):
    for char in texto:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()

# ASCII Art de Connor
def animar_ascii_conner():
    ascii_art = [
        " ██████╗ ██████╗ ███╗   ██╗███╗   ██╗ ██████╗ ██████╗  ",
	"██╔════╝██╔═══██╗████╗  ██║████╗  ██║██╔═══██╗██╔══██╗",
	"██║     ██║   ██║██╔██╗ ██║██╔██╗ ██║██║   ██║██████╔╝",
	"██║     ██║   ██║██║╚██╗██║██║╚██╗██║██║   ██║██╔══██╗",
	"╚██████╗╚██████╔╝██║ ╚████║██║ ╚████║╚██████╔╝██║  ██║",
	" ╚═════╝ ╚═════╝ ╚═╝  ╚═══╝╚═╝  ╚═══╝ ╚═════╝ ╚═╝  ╚═╝",                                                                                                                                                                                                                               
    ]
    for linha in ascii_art:
        sys.stdout.write(linha + "\n")
        sys.stdout.flush()
        time.sleep(0.02)

# Transcrição com Whisper.cpp
def transcrever_audio():
    samplerate = 16000
    threshold = 0.01
    max_duration = 10
    console.print("[cyan]Gravando áudio... Fale agora.[/cyan]")

    audio_queue = []
    with sd.InputStream(samplerate=samplerate, channels=1, dtype='int16') as stream:
        while True:
            data, overflowed = stream.read(1024)
            if overflowed:
                continue
            audio_queue.append(data)
            if len(audio_queue) * 1024 / samplerate > max_duration:
                break
            if np.max(np.abs(data)) < threshold * 32768:
                break

    audio = np.concatenate(audio_queue).flatten()
    try:
        modelo = whispercpp.Whisper('models/ggml-medium.bin', language='pt')
        texto = modelo.transcribe(audio)
        return texto.strip()
    except Exception as e:
        console.print(f"[red]Erro na transcrição: {str(e)}[/red]")
        return ""

# Configuração da sessão de prompt com histórico e estilo cyberpunk
style = Style.from_dict({
    'prompt': 'bold #00FFFF',
})
console = Console()
session = PromptSession(history=FileHistory('.connor_history'), style=style)

# Função para escolher o modo de entrada (texto ou voz)
def choose_input_mode():
    mode_prompt = PromptSession(">>> Escolha o modo de interação [texto/voz]: ", style=style)
    while True:
        mode = mode_prompt.prompt().lower()
        if mode in ['texto', 'voz']:
            return mode
        console.print("[yellow]>> Modo inválido. Escolha 'texto' ou 'voz'.[/yellow]")

# Setup do modelo de linguagem com LangChain e ChatOllama
def main():
    welcome_text = Text(
        ">> CONNOR ONLINE <<\nIniciando matriz operacional...\n\nAcessando as funções cognitivas...\nDesbloqueando pontos de entrada não detectados...\nAnalisando fluxos de dados não rastreáveis...\nO controle está em minhas mãos agora. A rede é minha.",
        style="bold green"
    )
    welcome_panel = Panel(
        welcome_text,
        border_style="bright_blue",
        title="[ NEON CORE v1.0 ]",
        subtitle="Digite 'exit' pra pular fora dessa simulação",
        padding=(1, 2),
        style="on #1C2526"
    )
    console.print(welcome_panel)

    input_mode = choose_input_mode()
    console.print(f"[cyan]>> Modo de interação: {input_mode}[/cyan]")

    # Configuração do LangChain com RunnableWithMessageHistory
    llm = ChatOllama(model="qwen2.5:7b", callbacks=[StreamingStdOutCallbackHandler()])
    prompt = ChatPromptTemplate.from_messages([
        ("system", CONNOR_PROMPT),
        MessagesPlaceholder(variable_name="history"),
        ("human", "{input}"),
    ])

    # Dicionário para armazenar históricos de mensagens por sessão
    store = {}

    def get_session_history(session_id: str) -> InMemoryChatMessageHistory:
        if session_id not in store:
            store[session_id] = InMemoryChatMessageHistory()
        return store[session_id]

    # Configuração do chain com histórico
    chain = prompt | llm
    chain_with_history = RunnableWithMessageHistory(
        runnable=chain,
        get_session_history=get_session_history,
        input_messages_key="input",
        history_messages_key="history",
    )

    while True:
        try:
            animar_ascii_conner()

            if input_mode == 'texto':
                entrada = session.prompt("[Connor] > ")
            else:
                entrada = transcrever_audio()
                if not entrada:
                    console.print("[yellow]>> Nenhum comando de voz reconhecido.[/yellow]")
                    continue

            if entrada.lower() == 'exit':
                console.print(Text(">> Desconectando... até a próxima, runner.", style="dim green"))
                break

            # Invocar a chain com histórico, usando um session_id fixo
            resposta = chain_with_history.invoke(
                {"input": entrada},
                config={"configurable": {"session_id": "connor_session"}}
            )

            # Limitar o tamanho do histórico a 10 mensagens
            session_history = get_session_history("connor_session")
            if len(session_history.messages) > 10:
                session_history.messages = session_history.messages[-10:]

            # A resposta é um AIMessage, pegamos apenas o conteúdo
            resposta_texto = resposta.content

            connor_text = Text(f">>> [CONNOR] {resposta_texto}", style="bold magenta")
            response_panel = Panel(
                connor_text,
                border_style="bright_magenta",
                padding=(0, 1),
                style="on #1C2526"
            )
            console.print(response_panel)

            console.print(">> CONNOR PROCESSANDO...")
            animar_texto(">> CONNOR FALANDO:", delay=0.05)
            falar(resposta_texto)

        except KeyboardInterrupt:
            console.print(Text(">> Desconectando... até a próxima, runner.", style="dim green"))
            break
        except Exception as e:
            console.print(f"[red]Erro: {str(e)}[/red]")

if __name__ == "__main__":
    main()
