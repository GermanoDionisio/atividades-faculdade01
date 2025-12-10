import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
from datetime import datetime
import threading
import time
import re

class DefensoriaAI:
    def __init__(self, root):
        self.root = root
        self.root.title("Defensoria Pública AI - Assistente Jurídico")
        self.root.geometry("1400x950")
        self.root.configure(bg="#e8f5e9")
        self.root.resizable(True, True)

        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.configure_styles()

        self.chat_responding = False
        self.modelos_por_area = {}
        self.historico_conversa = []
        
        self.create_interface()
        self.setup_responsive_layout()
        self.root.bind('<Configure>', self.on_resize)

    def configure_styles(self):
        """Estilos modernos e responsivos"""
        self.verde_escuro = "#1b5e20"
        self.verde_medio = "#2e7d32"
        self.verde_claro = "#a5d6a7"
        self.cinza_fundo = "#e8f5e9"
        self.cinza_card = "#ffffff"
        self.azul_acento = "#1976d2"
        self.azul_claro = "#42a5f5"
        self.vermelho_urgente = "#d32f2f"

        # Título principal
        self.style.configure('Title.TLabel', font=('Segoe UI', 24, 'bold'), 
                           background=self.verde_escuro, foreground='white', padding=20)
        
        # Headers
        self.style.configure('Header.TLabel', font=('Segoe UI', 14, 'bold'), 
                           background=self.verde_medio, foreground='white', padding=12)
        
        # Cards
        self.style.configure('Card.TFrame', background=self.cinza_card, relief='flat')
        
        # Botões MODERNOS e RESPONSIVOS
        self.style.configure('ModernPrimary.TButton', 
                           font=('Segoe UI', 12, 'bold'), 
                           background=self.verde_medio, foreground='white', 
                           relief='flat', borderwidth=0, padding=(25, 12))
        self.style.map('ModernPrimary.TButton', 
                      background=[('active', self.verde_escuro), ('pressed', '#0d4417')],
                      foreground=[('active', 'white')])
        
        self.style.configure('ModernSecondary.TButton', 
                           font=('Segoe UI', 11), 
                           background='#757575', foreground='white', 
                           relief='flat', borderwidth=0, padding=(20, 10))
        self.style.map('ModernSecondary.TButton', 
                      background=[('active', '#616161'), ('pressed', '#424242')])
        
        # Botão Enviar Chat (especial)
        self.style.configure('Send.TButton', 
                           font=('Segoe UI', 12, 'bold'), 
                           background=self.azul_acento, foreground='white', 
                           relief='flat', borderwidth=0, padding=(20, 12))
        self.style.map('Send.TButton', 
                      background=[('active', self.azul_claro), ('pressed', '#0d47a1')])
        
        # Entradas
        self.style.configure('Modern.TEntry', font=('Segoe UI', 12), padding=15, 
                           fieldbackground='#f8f9fa', relief='flat', borderwidth=1)
        self.style.map('Modern.TEntry', 
                      fieldbackground=[('focus', 'white'), ('readonly', '#f0f0f0')])
        
        # Combobox moderno
        self.style.configure('Modern.TCombobox', font=('Segoe UI', 12), padding=12)
        
        # Notebook moderno
        self.style.configure('Modern.TNotebook', background=self.cinza_fundo, borderwidth=0)
        self.style.configure('Modern.TNotebook.Tab', 
                           font=('Segoe UI', 12, 'bold'), padding=(20, 12),
                           background=self.verde_claro)
        self.style.map('Modern.TNotebook.Tab', 
                      background=[('selected', 'white')], 
                      foreground=[('selected', self.verde_escuro)])
        
        # Labels de instrução
        self.style.configure('Instrucao.TLabel', 
                           font=('Segoe UI', 11), 
                           background=self.cinza_fundo, foreground=self.verde_escuro, 
                           relief='solid', borderwidth=1, anchor='w', 
                           justify='left', padding=15)

    def setup_responsive_layout(self):
        """Configura layout responsivo com grid weights"""
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(0, weight=1)

    def create_interface(self):
        # Frame principal responsivo
        main_frame = ttk.Frame(self.root, style='Card.TFrame')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=25, pady=20)
        main_frame.grid_columnconfigure(0, weight=1)
        main_frame.grid_rowconfigure(1, weight=1)

        # Título
        title_frame = ttk.Frame(main_frame, style='Card.TFrame')
        title_frame.pack(fill=tk.X, pady=(0, 15))
        title_label = ttk.Label(title_frame, text="🛡️ Defensoria Pública AI", style='Title.TLabel')
        title_label.pack(fill=tk.X)

        # Container principal (grid responsivo)
        content_frame = ttk.Frame(main_frame, style='Card.TFrame')
        content_frame.pack(fill=tk.BOTH, expand=True)
        content_frame.grid_columnconfigure(0, weight=3)  # Chat 30%
        content_frame.grid_columnconfigure(1, weight=7)  # Tools 70%
        content_frame.grid_rowconfigure(0, weight=1)

        # Chat (esquerda)
        self.chat_frame = ttk.Frame(content_frame, style='Card.TFrame')
        self.chat_frame.grid(row=0, column=0, sticky='nsew', padx=(0, 15))

        # Tools (direita)
        tools_frame = ttk.Frame(content_frame)
        tools_frame.grid(row=0, column=1, sticky='nsew', padx=(15, 0))

        self.create_improved_chat_interface()
        self.create_main_tools(tools_frame)

        # Mensagem de boas-vindas
        self.root.after(300, lambda: self.add_message(
            "AI", 
            "🚀 Bem-vindo ao Assistente Jurídico da Defensoria!\n\n"
            "💬 **Como usar:**\n"
            "• Digite sua dúvida aqui (ex: 'problema familiar')\n"
            "• Selecione abas para ferramentas específicas\n"
            "• Clique 'Gerar Orientação' para instruções COMPLETAS com ARTIGOS!\n\n"
            "✅ **Áreas atendidas:** Família • INSS • Contratos • Criminal • Urgência"
        ))

    def create_improved_chat_interface(self):
        """Chat melhorado com design moderno"""
        # Header
        header_frame = ttk.Frame(self.chat_frame)
        header_frame.pack(fill=tk.X, padx=20, pady=(20, 10))
        header = ttk.Label(header_frame, text="💬 Assistente Inteligente", style='Header.TLabel')
        header.pack()

        # Histórico de chat (expansível)
        self.chat_history = scrolledtext.ScrolledText(
            self.chat_frame, height=12, wrap=tk.WORD, font=('Segoe UI', 11),
            bg='#f8f9fa', fg='#212121', state=tk.DISABLED, relief='flat',
            borderwidth=0, padx=20, pady=15, selectbackground=self.azul_claro
        )
        self.chat_history.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 15))

        # Input frame responsivo
        input_frame = ttk.Frame(self.chat_frame, style='Card.TFrame')
        input_frame.pack(fill=tk.X, padx=20, pady=(0, 20))
        input_frame.grid_columnconfigure(0, weight=1)

        # Entry moderno
        self.chat_entry = ttk.Entry(input_frame, font=('Segoe UI', 12), style='Modern.TEntry')
        self.chat_entry.grid(row=0, column=0, sticky='ew', padx=(0, 12), pady=10)
        self.chat_entry.bind('<Return>', self.send_message)
        self.chat_entry.focus_set()

        # Botão enviar moderno
        send_btn = ttk.Button(input_frame, text="➤ Enviar", command=self.send_message, 
                            style='Send.TButton', width=12)
        send_btn.grid(row=0, column=1, pady=10)

        # Bindings teclado
        self.root.bind('<Return>', lambda e: self.send_message())
        self.root.bind('<Control-Return>', lambda e: self.send_message())

    def add_message(self, autor, mensagem, delay=0):
        def animate():
            self.chat_history.config(state=tk.NORMAL)
            if autor == "AI":
                prefix = "🤖 AI Assistente"
                color_tag = "ai_msg"
                align_tag = "ai_align"
            else:
                prefix = "👤 Você"
                color_tag = "user_msg"
                align_tag = "user_align"
            
            timestamp = datetime.now().strftime('%H:%M')
            msg_text = f"[{timestamp}] {prefix}\n{mensagem}\n\n"
            self.chat_history.insert(tk.END, msg_text, [color_tag, align_tag])
            
            # Configurações de estilo
            self.chat_history.tag_config("ai_msg", foreground=self.verde_medio, font=('Segoe UI', 11))
            self.chat_history.tag_config("user_msg", foreground=self.azul_acento, font=('Segoe UI', 11, 'bold'))
            self.chat_history.tag_config("ai_align", lmargin1=25, lmargin2=25, rmargin=20)
            self.chat_history.tag_config("user_align", rmargin=25, lmargin1=20, lmargin2=20)
            
            self.chat_history.config(state=tk.DISABLED)
            self.chat_history.see(tk.END)
            self.chat_responding = False
        
        self.root.after(delay, animate)

    def send_message(self, event=None):
        if self.chat_responding:
            return
        message = self.chat_entry.get().strip()
        if not message:
            return

        self.add_message("Você", message, 0)
        self.chat_entry.delete(0, tk.END)
        self.add_message("AI", "⏳ Analisando sua situação...", 50)
        self.chat_responding = True
        threading.Thread(target=self.process_message_thread, args=(message,), daemon=True).start()

    def process_message_thread(self, mensagem):
        time.sleep(0.5)  # Simula processamento
        resposta = self.processar_comando_inteligente(mensagem.lower())
        self.root.after(0, lambda: self.add_message("AI", resposta, 100))

    def processar_comando_inteligente(self, mensagem):
        """Chat INTELIGENTE com detecção contextual"""
        self.historico_conversa.append(mensagem)
        
        # Detecta áreas específicas e oferece opções COM ARTIGOS
        if any(palavra in mensagem for palavra in ['família', 'divórcio', 'filho', 'guarda', 'visita', 'pensão']):
            opcoes_familia = self.modelos_por_area.get("Família", [])
            return (f"👨‍👩‍👧 **PROBLEMA FAMILIAR detectado!**\n\n"
                   f"✅ **Opções disponíveis (com artigos):**" + 
                   "\n⚖️ **Art. 1.565 CC** - Divórcio\n⚖️ **Art. 1.583 CC** - Guarda\n⚖️ **Art. 1.694 CC** - Alimentos\n\n"
                   f"📋 **Próximo passo:** Aba **'📋 Classificar Ação'** → Família")

        elif any(palavra in mensagem for palavra in ['inss', 'aposentadoria', 'pensao morte', 'auxílio', 'previdência']):
            return (f"📋 **INSS/PREVIDENCIÁRIO detectado!**\n\n"
                   f"✅ **Artigos principais:**\n"
                   f"⚖️ **Lei 8.213/91 Art. 25** - Qualidade segurado\n"
                   f"⚖️ **Lei 8.213/91 Art. 42** - Pensão por morte\n"
                   f"⚖️ **Lei 8.213/91 Art. 59** - BPC/LOAS\n\n"
                   f"👉 Aba **'📋 Classificar Ação'** → Previdenciário")

        elif any(palavra in mensagem for palavra in ['contrato', 'telefonia', 'banco', 'aluguel', 'financiamento']):
            return ("⚠️ **CONTRATO detectado!**\n\n"
                   "✅ **⚖️ Art. 51 CDC** - Cláusulas abusivas NULAS!\n"
                   "📋 Vá na aba **'📄 Cláusulas Abusivas'**\n"
                   "📍 Leve contrato completo!")

        elif any(palavra in mensagem for palavra in ['urgente', 'violência', 'prisão', 'idoso', 'criança']):
            return ("🚨 **URGÊNCIA detectada!**\n\n"
                   "⚖️ **Art. 5º LXXVIII CF** - Rito prioritário\n"
                   "⚖️ **Lei 11.340/06 Art. 22** - Maria da Penha\n"
                   "⚡ Aba **'🚨 Detector Urgência'** AGORA!")

        else:
            return ("🤖 **Não identifiquei a área específica.**\n\n"
                   "💡 **Dicas (com artigos):**\n"
                   "• 'problema familiar' → **Art. 226 CF**\n"
                   "• 'INSS negou' → **Lei 8.213/91**\n"
                   "• 'contrato abusivo' → **Art. 51 CDC**\n"
                   "• 'violência urgente' → **Lei 11.340/06**\n\n"
                   "👉 Ou use as **abas laterais**!")

    def on_resize(self, event):
        """Ajustes responsivos"""
        pass

    # ========== FERRAMENTAS COM ARTIGOS ESPECÍFICOS ==========
    def create_main_tools(self, parent):
        notebook = ttk.Notebook(parent, style='Modern.TNotebook')
        notebook.pack(fill=tk.BOTH, expand=True, padx=25, pady=(20, 20))

        self.create_classificador_acao_expandido(notebook)
        self.create_identificador_artigos_expandido(notebook)
        self.create_detector_urgencia_expandido(notebook)
        self.create_clausulas_abusivas_expandido(notebook)

    def create_classificador_acao_expandido(self, notebook):
        frame = ttk.Frame(notebook)
        notebook.add(frame, text="📋 Classificar Ação")
        frame.grid_columnconfigure(0, weight=1)

        ttk.Label(frame, text="1️⃣ Escolha sua situação:", 
                 font=('Segoe UI', 14, 'bold')).pack(pady=(30, 15))

        # Área
        area_frame = ttk.Frame(frame)
        area_frame.pack(fill=tk.X, padx=40, pady=5)
        ttk.Label(area_frame, text="🌟 Área:", font=('Segoe UI', 12, 'bold')).pack(side=tk.LEFT)
        
        self.area_var = tk.StringVar()
        self.area_combo = ttk.Combobox(area_frame, textvariable=self.area_var, 
                                     state="readonly", width=40, style='Modern.TCombobox')
        self.area_combo.pack(side=tk.LEFT, padx=(15, 0))
        self.area_combo.bind("<<ComboboxSelected>>", self.atualizar_modelos_area)

        # Modelo (mais opções)
        modelo_frame = ttk.Frame(frame)
        modelo_frame.pack(fill=tk.X, padx=40, pady=15)
        ttk.Label(modelo_frame, text="📋 Situação:", font=('Segoe UI', 12, 'bold')).pack(side=tk.LEFT)
        
        self.modelo_var = tk.StringVar()
        self.modelo_combo = ttk.Combobox(modelo_frame, textvariable=self.modelo_var, 
                                       state="readonly", width=70, style='Modern.TCombobox')
        self.modelo_combo.pack(side=tk.LEFT, padx=(15, 0))

        self.modelos_por_area = {
            "Família": [
                "Divórcio amigável sem filhos", "Divórcio litigioso com partilha", 
                "Regulamentação de guarda/visitas", "Pensão alimentícia filho menor", 
                "Revisão pensão alimentícia", "Guarda compartilhada", "Suspensão visitas",
                "Reconhecimento paternidade", "Alimentos provisórios urgentes"
            ],
            "Previdenciário / INSS": [
                "Aposentadoria por idade", "Aposentadoria invalidez", 
                "Pensão por morte segurado", "Auxílio-doença negado", 
                "Revisão benefício previdenciário", "BPC/LOAS negado", 
                "Aposentadoria especial", "Revisão da vida toda"
            ],
            "Cível": [
                "Cobrança dívida indevida", "Indenização danos morais", 
                "Plano saúde negou", "Escola particular problema", 
                "Despejo indevido", "Consórcio lesado", "Publicidade enganosa"
            ],
            "Criminal": [
                "Defesa crime furto", "Defesa crime ameaça", 
                "Liberdade provisória", "Violência doméstica vítima", 
                "Violência doméstica acusado", "Habeas corpus", "Progressão regime"
            ]
        }

        self.area_combo['values'] = list(self.modelos_por_area.keys())

        # Resultados
        self.resultado_frame = ttk.Frame(frame)
        self.resultado_frame.pack(fill=tk.X, padx=40, pady=25)

        self.resultado_acao_label = ttk.Label(self.resultado_frame, text="", 
                                            font=('Segoe UI', 14, 'bold'), 
                                            foreground=self.verde_medio)
        self.resultado_acao_label.pack(anchor='w')

        self.instrucao_label = ttk.Label(self.resultado_frame, text="", style='Instrucao.TLabel')
        self.instrucao_label.pack(fill=tk.X, pady=(10, 0))

        # Botões modernos
        btn_frame = ttk.Frame(frame)
        btn_frame.pack(pady=25)
        ttk.Button(btn_frame, text="📋 Gerar Orientação", 
                  command=self.classificar_acao, style='ModernPrimary.TButton').pack(side=tk.LEFT, padx=(0, 15))
        ttk.Button(btn_frame, text="🗑️ Limpar Tudo", 
                  command=self.limpar_acao, style='ModernSecondary.TButton').pack(side=tk.LEFT)

    def atualizar_modelos_area(self, event=None):
        area = self.area_var.get()
        modelos = self.modelos_por_area.get(area, [])
        self.modelo_combo['values'] = modelos
        if modelos:
            self.modelo_combo.current(0)
            self.modelo_var.set(modelos[0])

    def classificar_acao(self):
        area = self.area_var.get()
        modelo = self.modelo_var.get()
        if not area or not modelo:
            messagebox.showwarning("⚠️ Atenção", "Selecione **Área** E **Situação**!")
            return
        
        self.resultado_acao_label.config(text=f"✅ {area} - {modelo}")
        instrucao = self.gerar_instrucao_acao_com_artigos(area, modelo)
        self.instrucao_label.config(text=instrucao)

    def gerar_instrucao_acao_com_artigos(self, area, modelo):
        """ARTIGOS ESPECÍFICOS para cada situação"""
        instrucoes_com_artigos = {
            "Família": {
                "Divórcio amigável sem filhos": "⚖️ **Art. 1.565, §6º CC** - Divórcio consensual\n✅ ⏰ 30 dias | 📋 RG + certidão casamento\n📍 Defensoria Família",
                "Divórcio litigioso com partilha": "⚖️ **Art. 1.571 CC** + **Art. 1.659 CC** - Partilha bens\n✅ Separação fato >2 anos | 📋 Comprovantes bens\n📍 Defensoria Família",
                "Regulamentação de guarda/visitas": "⚖️ **Art. 1.583 CC** + **Art. 1.584 CC** - Melhor interesse criança\n✅ Guarda compartilhada | 📋 Certidão nascimento\n⏰ Decisão 30 dias",
                "Pensão alimentícia filho menor": "⚖️ **Art. 1.694 CC** + **Art. 1.699 CC** - Alimentos necessários\n🚨 URGENTE | 📋 RG + comprovante renda\n⏰ 48h decisão",
                "Alimentos provisórios urgentes": "⚖️ **Art. 1.695 CC** - Tutela alimentos\n🚨 **PRIORITÁRIO** | 📋 RG/CPF + certidão\n📍 Defensoria HOJE"
            },
            "Previdenciário / INSS": {
                "Pensão por morte segurado": "⚖️ **Lei 8.213/91 Art. 74** - Pensão morte\n⏰ 90 dias | 📋 Certidão óbito + carnês INSS\n📞 135 + Defensoria URGENTE",
                "Auxílio-doença negado": "⚖️ **Lei 8.213/91 Art. 59** + **Art. 25 I** - Incapacidade\n📋 Laudo médico + carta negativa Meu INSS\n⏰ Revisão administrativa 30 dias",
                "BPC/LOAS negado": "⚖️ **Lei 8.742/93 Art. 20** - Benefício assistencial\n✅ Renda <1/4 salário | 📋 RG/CPF + comprovante renda\n📍 Defensoria + CRAS"
            },
            "Cível": {
                "Indenização danos morais": "⚖️ **Art. 186 + 927 CC** + **Art. 6º VI CDC**\n📋 Provas (prints/fotos) | Juizado Especial\n⏰ Audiência 30-90 dias",
                "Plano saúde negou": "⚖️ **Art. 35-C Lei 9.656/98** + **Súmula 608 STJ**\n🚨 Internação/cirurgia | 📋 Autorização negada\n⏰ Tutela antecipada 48h"
            },
            "Criminal": {
                "Violência doméstica vítima": "⚖️ **Lei 11.340/06 Art. 22** - Maria da Penha\n🚨 **48h decisão** | 📍 Polícia + Defensoria\n✅ Medidas protetivas",
                "Liberdade provisória": "⚖️ **Art. 310 CPP** + **Art. 319 CPP**\n🚨 **PRIMÁRIO** | 📋 RG/CPF + boletim\n📍 Defensoria Criminal 24h"
            }
        }
        default = f"⚖️ **{area}** - Procure Defensoria com RG/CPF + documentos\n✅ **GRATUITO** | 📍 Unidade mais próxima"
        try:
            return instrucoes_com_artigos[area][modelo] or default
        except:
            return default

    def limpar_acao(self):
        self.area_var.set("")
        self.modelo_var.set("")
        self.modelo_combo['values'] = []
        self.resultado_acao_label.config(text="")
        self.instrucao_label.config(text="")

    # ========== ARTIGOS ESPECÍFICOS POR CONTRATO ==========
    def create_clausulas_abusivas_expandido(self, notebook):
        frame = ttk.Frame(notebook)
        notebook.add(frame, text="📄 Cláusulas Abusivas")
        
        ttk.Label(frame, text="1️⃣ Tipo contrato:", font=('Segoe UI', 14, 'bold')).pack(pady=(30, 15))
        
        self.contrato_var = tk.StringVar()
        self.contrato_combo = ttk.Combobox(frame, textvariable=self.contrato_var, 
                                         state="readonly", width=70, style='Modern.TCombobox',
                                         values=["Telefonia", "Banco/cartão", "Financiamento carro", 
                                                "Aluguel", "Plano saúde", "Consórcio"])
        self.contrato_combo.pack(pady=15)

        resultado_frame = ttk.Frame(frame)
        resultado_frame.pack(fill=tk.X, padx=40, pady=25)

        self.resultado_contrato_label = ttk.Label(resultado_frame, text="", 
                                                font=('Segoe UI', 14, 'bold'), 
                                                foreground=self.verde_medio)
        self.resultado_contrato_label.pack(anchor='w')

        self.instrucao_contrato_label = ttk.Label(resultado_frame, text="", style='Instrucao.TLabel')
        self.instrucao_contrato_label.pack(fill=tk.X, pady=(10, 0))

        btn_frame = ttk.Frame(frame)
        btn_frame.pack(pady=25)
        ttk.Button(btn_frame, text="📋 Analisar Cláusulas", command=self.analisar_clausulas, 
                  style='ModernPrimary.TButton').pack(side=tk.LEFT, padx=(0, 15))
        ttk.Button(btn_frame, text="🗑️ Limpar", command=self.limpar_contrato, 
                  style='ModernSecondary.TButton').pack(side=tk.LEFT)

    def analisar_clausulas(self):
        contrato = self.contrato_var.get()
        if not contrato:
            messagebox.showwarning("⚠️ Atenção", "Selecione contrato!")
            return
        
        artigos_por_contrato = {
            "Telefonia": "⚖️ **Art. 51 IV CDC** - Venda casada\n⚖️ **Art. 39 I CDC** - Cobrança indevida\n⚖️ **Art. 46 CDC** - Informação prévia\n✅ Multa rescisão >12x = ABUSIVA",
            "Banco/cartão": "⚖️ **Art. 51 XII CDC** - Juros abusivos\n⚖️ **Art. 39 V CDC** - Cobrança vexatória\n⚖️ **Art. 42 par.ún. CDC** - Juros mora 1%\n✅ ANATOCISMO vedado Súmula 121 STF",
            "Financiamento carro": "⚖️ **Art. 51 XV CDC** - Comissão não informada\n⚖️ **Art. 54 §2º CDC** - TAC abusivo\n⚖️ **Art. 52 §1º CDC** - IOF informado\n✅ Leve contrato + extrato!",
            "Aluguel": "⚖️ **Lei 8.245/91 Art. 23** - Revisão anual\n⚖️ **Art. 51 I CDC** - Renúncia juízo\n⚖️ **Lei 8.245/91 Art. 62** - Garantia locatícia\n✅ IPTU/cigarro PROIBIDO no locatário",
            "Plano saúde": "⚖️ **Art. 35-C Lei 9.656/98** - Negativa cobertura\n⚖️ **Súmula 608 STJ** - Doenças preexistentes\n⚖️ **Art. 16 Lei 9.656** - Rescisão unilateral\n🚨 Cirurgia/tratamento URGENTE",
            "Consórcio": "⚖️ **Lei 11.795/08 Art. 22** - Rescisão\n⚖️ **Art. 51 XIV CDC** - Mudança regras\n⚖️ **Súmula 543 STJ** - Fundo inadimplentes\n✅ Lance embutido ABUSIVO"
        }
        
        self.resultado_contrato_label.config(text=f"⚠️ **Cláusulas abusivas: {contrato}**")
        self.instrucao_contrato_label.config(text=artigos_por_contrato.get(contrato, 
            "✅ **Art. 51 CDC** - Todas cláusulas abusivas = NULAS!\n📋 Leve contrato COMPLETO"))

    def limpar_contrato(self):
        self.contrato_var.set("")
        self.resultado_contrato_label.config(text="")
        self.instrucao_contrato_label.config(text="")

    # ========== DEMAIS ABAS COM ARTIGOS ESPECÍFICOS ==========
    def create_identificador_artigos_expandido(self, notebook):
        frame = ttk.Frame(notebook)
        notebook.add(frame, text="⚖️ Artigos Relevantes")
        
        ttk.Label(frame, text="1️⃣ Escolha o caso:", font=('Segoe UI', 14, 'bold')).pack(pady=(30, 15))
        
        self.tipo_artigo_var = tk.StringVar()
        self.tipo_artigo_combo = ttk.Combobox(frame, textvariable=self.tipo_artigo_var, 
                                            state="readonly", width=70, style='Modern.TCombobox',
                                            values=["Violência doméstica", "Erro médico", "Produto defeituoso", 
                                                   "Publicidade enganosa", "Danos morais"])
        self.tipo_artigo_combo.pack(pady=15)

        resultado_frame = ttk.Frame(frame)
        resultado_frame.pack(fill=tk.X, padx=40, pady=25)

        self.resultado_artigos_label = ttk.Label(resultado_frame, text="", 
                                               font=('Segoe UI', 14, 'bold'), 
                                               foreground=self.verde_medio)
        self.resultado_artigos_label.pack(anchor='w')

        self.instrucao_artigos_label = ttk.Label(resultado_frame, text="", style='Instrucao.TLabel')
        self.instrucao_artigos_label.pack(fill=tk.X, pady=(10, 0))

        btn_frame = ttk.Frame(frame)
        btn_frame.pack(pady=25)
        ttk.Button(btn_frame, text="⚖️ Ver Artigos", command=self.identificar_artigos, 
                  style='ModernPrimary.TButton').pack(side=tk.LEFT, padx=(0, 15))
        ttk.Button(btn_frame, text="🗑️ Limpar", command=self.limpar_artigos, 
                  style='ModernSecondary.TButton').pack(side=tk.LEFT)

    def identificar_artigos(self):
        tipo = self.tipo_artigo_var.get()
        if not tipo:
            messagebox.showwarning("⚠️ Atenção", "Selecione um caso!")
            return
        
        artigos_por_tipo = {
            "Violência doméstica": "🚨 **Lei 11.340/06 Art. 22** - Medidas protetivas 48h\n⚖️ **Art. 5º CF** - Dignidade humana\n📍 Polícia + Defensoria AGORA",
            "Erro médico": "⚖️ **Art. 14 CDC** - Responsabilidade objetiva\n⚖️ **Art. 951 CC** - Erro profissional\n📋 Prontuário + laudo pericial",
            "Produto defeituoso": "⚖️ **Art. 12 CDC** - Defeito produto\n⚖️ **Art. 18 CDC** - Vício oculto\n✅ Nota fiscal + fotos defeito"
        }
        
        self.resultado_artigos_label.config(text=f"✅ Artigos para: {tipo}")
        self.instrucao_artigos_label.config(text=artigos_por_tipo.get(tipo, 
            "⚖️ **Art. 186 + 927 CC** - Responsabilidade civil\n📋 Leve provas à Defensoria"))

    def limpar_artigos(self):
        self.tipo_artigo_var.set("")
        self.resultado_artigos_label.config(text="")
        self.instrucao_artigos_label.config(text="")

    def create_detector_urgencia_expandido(self, notebook):
        frame = ttk.Frame(notebook)
        notebook.add(frame, text="🚨 Detector Urgência")
        
        ttk.Label(frame, text="1️⃣ Situação:", font=('Segoe UI', 14, 'bold')).pack(pady=(30, 15))
        
        self.urgencia_var = tk.StringVar()
        self.urgencia_combo = ttk.Combobox(frame, textvariable=self.urgencia_var, 
                                         state="readonly", width=70, style='Modern.TCombobox',
                                         values=["Idoso sem remédio", "Criança sem creche", "Violência doméstica", 
                                                "Preso audiência", "Cirurgia negada plano"])
        self.urgencia_combo.pack(pady=15)

        resultado_frame = ttk.Frame(frame)
        resultado_frame.pack(fill=tk.X, padx=40, pady=25)

        self.resultado_urgencia_label = ttk.Label(resultado_frame, text="", 
                                                font=('Segoe UI', 16, 'bold'), 
                                                foreground=self.vermelho_urgente)
        self.resultado_urgencia_label.pack(anchor='w')

        self.instrucao_urgencia_label = ttk.Label(resultado_frame, text="", style='Instrucao.TLabel')
        self.instrucao_urgencia_label.pack(fill=tk.X, pady=(10, 0))

        btn_frame = ttk.Frame(frame)
        btn_frame.pack(pady=25)
        ttk.Button(btn_frame, text="🚨 Verificar Urgência", command=self.verificar_urgencia, 
                  style='ModernPrimary.TButton').pack(side=tk.LEFT, padx=(0, 15))
        ttk.Button(btn_frame, text="🗑️ Limpar", command=self.limpar_urgencia, 
                  style='ModernSecondary.TButton').pack(side=tk.LEFT)

    def verificar_urgencia(self):
        situacao = self.urgencia_var.get()
        if not situacao:
            messagebox.showwarning("⚠️ Atenção", "Selecione situação!")
            return
        
        urgencias_artigos = {
            "Violência doméstica": "🚨 **Lei 11.340/06 Art. 22** - 48h decisão",
            "Idoso sem remédio": "🚨 **Art. 230 CF** + **ECA Art. 4º** - Prioridade absoluta"
        }
        
        self.resultado_urgencia_label.config(text="🚨 **URGENTE - PRIORIDADE JUDICIAL**")
        self.instrucao_urgencia_label.config(text=f"✅ **{urgencias_artigos.get(situacao, 'Art. 5º LXXVIII CF')}**\n📍 Defensoria HOJE | ⏰ 48h decisão!")

    def limpar_urgencia(self):
        self.urgencia_var.set("")
        self.resultado_urgencia_label.config(text="")
        self.instrucao_urgencia_label.config(text="")

if __name__ == "__main__":
    root = tk.Tk()
    app = DefensoriaAI(root)
    root.mainloop()