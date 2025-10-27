import tkinter as tk
from tkinter import messagebox, filedialog, ttk, simpledialog
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import json
import webbrowser
from datetime import datetime

# Valeurs de pip pour différents instruments
VALEUR_PIP = {
    # Forex Majors
    "EURUSD": 10,    # 1 lot standard = $10 par pip
    "GBPUSD": 10,
    "USDJPY": 9.09,   # Valeur approximative
    "AUDUSD": 10,
    "USDCAD": 7.58,   # Valeur approximative
    "USDCHF": 10.10,  # Valeur approximative
    "NZDUSD": 10,
    
    # Métaux
    "XAUUSD": 1,      # Or (1 lot standard = $1 par pip)
    "XAGUSD": 50,     # Argent (1 lot standard = $50 par pip)
    
    # Indices
    "NQ": 20,         # Nasdaq 100
    "US30": 5,        # Dow Jones
    "SPX500": 50,     # S&P 500
    "DAX": 25,        # DAX allemand
    
    # Crypto (valeurs d'exemple)
    "BTCUSD": 100,    # Bitcoin
    "ETHUSD": 50,     # Ethereum
}

# Paramètres de gestion des risques
MAX_RISK_PERCENT = 2  # Pourcentage de risque maximum recommandé
MIN_LOT_SIZE = 0.01   # Taille de lot minimale
MAX_LOT_SIZE = 100    # Taille de lot maximale

class AdvancedLotSizeCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Calculateur de Position Forex Pro")
        self.root.geometry("1000x750")
        
        # Configuration des couleurs
        self.bg_color = "#f0f0f0"
        self.frame_bg = "#e0e0e0"
        self.root.configure(bg=self.bg_color)
        
        # Variables
        self.instrument_var = tk.StringVar(value="EURUSD")
        self.capital_var = tk.StringVar(value="10000")
        self.risk_amount_var = tk.StringVar(value="1")
        self.risk_type = tk.StringVar(value="percent")
        self.sl_var = tk.StringVar(value="20")
        self.result_var = tk.StringVar(value="Taille de lot calculée ici")
        self.details_var = tk.StringVar(value="Détails du calcul")
        self.position_method = tk.StringVar(value="fixed")
        self.account_currency = tk.StringVar(value="USD")
        self.leverage_var = tk.StringVar(value="100")
        self.margin_result_var = tk.StringVar(value="Marge requise: -")
        
        # Initialisation de l'interface
        self.setup_ui()
        self.create_menu()
        
    def setup_ui(self):
        # Configuration de la grille
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_columnconfigure(2, weight=1)
        self.root.grid_rowconfigure(10, weight=1)
        
        # Titre principal
        title = tk.Label(self.root, text="Calculateur de Position Forex Pro", 
                        font=("Arial", 18, "bold"), bg=self.bg_color)
        title.grid(row=0, column=0, columnspan=3, pady=(10, 20))
        
        # Cadres principaux
        self.create_instrument_frame()
        self.create_capital_frame()
        self.create_risk_frame()
        self.create_stoploss_frame()
        self.create_position_method_frame()
        self.create_margin_calculator_frame()
        self.create_currency_frame()
        self.create_file_buttons()
        self.create_calculate_button()
        self.create_results_display()
        self.create_trade_journal_frame()
        self.create_chart()
    
    def create_instrument_frame(self):
        frame = tk.LabelFrame(self.root, text="1. Instrument", 
                            bg=self.frame_bg, padx=10, pady=10)
        frame.grid(row=1, column=0, columnspan=2, padx=10, pady=5, sticky="ew")
        
        tk.Label(frame, text="Instrument:", bg=self.frame_bg
                ).grid(row=0, column=0, padx=5, pady=5, sticky="w")
        
        instruments = sorted(VALEUR_PIP.keys())
        self.instrument_combo = ttk.Combobox(frame, textvariable=self.instrument_var, 
                                           values=instruments, state="readonly")
        self.instrument_combo.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        
        # Info-bulle
        tk.Label(frame, text="ℹ️ Sélectionnez votre paire/instrument", 
                bg=self.frame_bg, fg="blue", cursor="question_arrow"
                ).grid(row=0, column=2, padx=5)
    
    def create_capital_frame(self):
        frame = tk.LabelFrame(self.root, text="2. Capital", 
                            bg=self.frame_bg, padx=10, pady=10)
        frame.grid(row=2, column=0, columnspan=2, padx=10, pady=5, sticky="ew")
        
        tk.Label(frame, text="Capital ($):", bg=self.frame_bg
                ).grid(row=0, column=0, padx=5, pady=5, sticky="w")
        
        self.capital_entry = tk.Entry(frame, textvariable=self.capital_var)
        self.capital_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
    
    def create_risk_frame(self):
        frame = tk.LabelFrame(self.root, text="3. Risque", 
                             bg=self.frame_bg, padx=10, pady=10)
        frame.grid(row=3, column=0, columnspan=2, padx=10, pady=5, sticky="ew")
        
        # Type de risque
        tk.Radiobutton(frame, text="Risque en %", variable=self.risk_type, 
                      value="percent", bg=self.frame_bg).grid(row=0, column=0, sticky="w")
        tk.Radiobutton(frame, text="Risque en $", variable=self.risk_type, 
                      value="fixed", bg=self.frame_bg).grid(row=0, column=1, sticky="w")
        
        # Montant du risque
        tk.Label(frame, text="Montant du risque:", bg=self.frame_bg
                ).grid(row=1, column=0, padx=5, pady=5, sticky="w")
        
        self.risk_amount_entry = tk.Entry(frame, textvariable=self.risk_amount_var)
        self.risk_amount_entry.grid(row=1, column=1, padx=5, pady=5, sticky="ew")
        
        # Avertissement risque
        self.risk_warning = tk.Label(frame, text="", bg=self.frame_bg, fg="red")
        self.risk_warning.grid(row=2, column=0, columnspan=2, sticky="w")
    
    def create_stoploss_frame(self):
        frame = tk.LabelFrame(self.root, text="4. Stop-loss", 
                            bg=self.frame_bg, padx=10, pady=10)
        frame.grid(row=4, column=0, columnspan=2, padx=10, pady=5, sticky="ew")
        
        tk.Label(frame, text="Stop-loss (pips):", bg=self.frame_bg
                ).grid(row=0, column=0, padx=5, pady=5, sticky="w")
        
        self.sl_entry = tk.Entry(frame, textvariable=self.sl_var)
        self.sl_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
    
    def create_position_method_frame(self):
        frame = tk.LabelFrame(self.root, text="Méthode de Position", 
                             bg=self.frame_bg, padx=10, pady=10)
        frame.grid(row=1, column=2, rowspan=4, padx=10, pady=5, sticky="ns")
        
        methods = [
            ("Fraction Fixe", "fixed"),
            ("Volatilité", "volatility"),
            ("Critère de Kelly", "kelly")
        ]
        
        for text, mode in methods:
            tk.Radiobutton(frame, text=text, variable=self.position_method,
                         value=mode, bg=self.frame_bg).pack(anchor="w")
        
        # Bouton info
        tk.Button(frame, text="ℹ️ Info", command=self.show_position_method_info,
                 bg=self.frame_bg).pack(pady=5)
    
    def create_margin_calculator_frame(self):
        frame = tk.LabelFrame(self.root, text="Calculateur de Marge", 
                            bg=self.frame_bg, padx=10, pady=10)
        frame.grid(row=5, column=2, padx=10, pady=5, sticky="nsew")
        
        # Effet de levier
        tk.Label(frame, text="Levier:", bg=self.frame_bg
                ).pack(anchor="w")
        self.leverage_entry = tk.Entry(frame, textvariable=self.leverage_var)
        self.leverage_entry.pack(fill="x", pady=5)
        
        # Résultat marge
        tk.Label(frame, textvariable=self.margin_result_var, bg=self.frame_bg
                ).pack(anchor="w")
        
        # Bouton calculer marge
        tk.Button(frame, text="Calculer Marge", command=self.calculate_margin,
                 bg="#2196F3", fg="white").pack(pady=5)
    
    def create_currency_frame(self):
        frame = tk.LabelFrame(self.root, text="Devise du Compte", 
                            bg=self.frame_bg, padx=10, pady=10)
        frame.grid(row=6, column=2, padx=10, pady=5, sticky="ew")
        
        currencies = ["USD", "EUR", "GBP", "JPY", "AUD", "CAD", "CHF"]
        self.currency_combo = ttk.Combobox(frame, textvariable=self.account_currency,
                                         values=currencies, state="readonly")
        self.currency_combo.pack(fill="x")
    
    def create_file_buttons(self):
        frame = tk.Frame(self.root, bg=self.bg_color)
        frame.grid(row=5, column=0, columnspan=2, pady=10, sticky="ew")
        
        tk.Button(frame, text="Charger Paramètres", command=self.load_settings
                ).grid(row=0, column=0, padx=5, sticky="ew")
        tk.Button(frame, text="Sauvegarder Paramètres", command=self.save_settings
                ).grid(row=0, column=1, padx=5, sticky="ew")
    
    def create_calculate_button(self):
        self.calc_btn = tk.Button(self.root, text="CALCULER LA POSITION", 
                                 command=self.calculate, bg="#4CAF50", fg="white",
                                 font=("Arial", 12, "bold"))
        self.calc_btn.grid(row=6, column=0, columnspan=2, pady=20, sticky="ew")
    
    def create_results_display(self):
        # Résultat
        self.result_label = tk.Label(self.root, textvariable=self.result_var,
                                    font=("Arial", 12, "bold"), fg="green", bg=self.bg_color)
        self.result_label.grid(row=7, column=0, columnspan=3, pady=10, sticky="ew")
        
        # Détails
        self.details_label = tk.Label(self.root, textvariable=self.details_var,
                                     font=("Arial", 10), bg=self.bg_color, justify="left")
        self.details_label.grid(row=8, column=0, columnspan=3, pady=10, sticky="ew")
    
    def create_trade_journal_frame(self):
        frame = tk.LabelFrame(self.root, text="Journal de Trading", 
                            bg=self.frame_bg, padx=10, pady=10)
        frame.grid(row=9, column=2, rowspan=2, padx=10, pady=5, sticky="nsew")
        
        # Notes de trade
        tk.Label(frame, text="Notes:", bg=self.frame_bg).pack(anchor="w")
        self.notes_text = tk.Text(frame, height=8, width=30)
        self.notes_text.pack(fill="both", expand=True)
        
        # Bouton sauvegarder
        tk.Button(frame, text="Sauvegarder Trade", command=self.save_trade_journal,
                 bg="#673AB7", fg="white").pack(pady=5)
    
    def create_chart(self):
        self.fig, self.ax = plt.subplots(figsize=(8, 4))
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)
        self.canvas.get_tk_widget().grid(row=9, column=0, columnspan=2, 
                                        rowspan=2, padx=10, pady=10, sticky="nsew")
    
    def create_menu(self):
        menubar = tk.Menu(self.root)
        
        # Menu Fichier
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Nouveau", command=self.reset_calculator)
        file_menu.add_command(label="Ouvrir...", command=self.load_settings)
        file_menu.add_command(label="Enregistrer sous...", command=self.save_settings)
        file_menu.add_separator()
        file_menu.add_command(label="Quitter", command=self.root.quit)
        menubar.add_cascade(label="Fichier", menu=file_menu)
        
        # Menu Outils
        tools_menu = tk.Menu(menubar, tearoff=0)
        tools_menu.add_command(label="Calculateur de Pip", command=self.show_pip_calculator)
        tools_menu.add_command(label="Calculateur de Marge", command=self.show_margin_calculator)
        tools_menu.add_command(label="Convertisseur de Devise", command=self.show_currency_converter)
        menubar.add_cascade(label="Outils", menu=tools_menu)
        
        # Menu Aide
        help_menu = tk.Menu(menubar, tearoff=0)
        help_menu.add_command(label="Guide d'utilisation", command=self.show_user_guide)
        help_menu.add_command(label="À propos", command=self.show_about)
        menubar.add_cascade(label="Aide", menu=help_menu)
        
        self.root.config(menu=menubar)
    
    def validate_inputs(self):
        try:
            capital = float(self.capital_var.get())
            risk_amount = float(self.risk_amount_var.get())
            sl_pips = float(self.sl_var.get())
            
            if capital <= 0:
                messagebox.showerror("Erreur", "Le capital doit être positif")
                return False
                
            if self.risk_type.get() == "percent" and (risk_amount <= 0 or risk_amount > 10):
                self.risk_warning.config(text="⚠️ Risque recommandé: 0.5%-2% du compte")
                if risk_amount > 2:
                    if not messagebox.askyesno("Avertissement", 
                        "Le risque dépasse 2% du compte. Continuer?"):
                        return False
            else:
                self.risk_warning.config(text="")
                
            if sl_pips <= 0:
                messagebox.showerror("Erreur", "Le stop-loss doit être positif")
                return False
                
            return True
            
        except ValueError:
            messagebox.showerror("Erreur", "Veuillez entrer des nombres valides")
            return False
    
    def calculate(self):
        if not self.validate_inputs():
            return
            
        try:
            # Obtenir les valeurs
            instrument = self.instrument_var.get()
            capital = float(self.capital_var.get())
            risk_amount = float(self.risk_amount_var.get())
            sl_pips = float(self.sl_var.get())
            pip_value = VALEUR_PIP.get(instrument, 10)  # Valeur par défaut
            
            # Calculer selon la méthode
            method = self.position_method.get()
            if method == "fixed":
                lot_size = self.calculate_fixed_fractional(capital, risk_amount, sl_pips, pip_value)
            elif method == "volatility":
                lot_size = self.calculate_volatility_based(capital, risk_amount, sl_pips, pip_value)
            elif method == "kelly":
                lot_size = self.calculate_kelly_criterion(capital, risk_amount, sl_pips, pip_value)
            
            # Appliquer les limites
            lot_size = max(MIN_LOT_SIZE, min(lot_size, MAX_LOT_SIZE))
            
            # Mettre à jour les résultats
            self.update_results_display(instrument, capital, risk_amount, sl_pips, pip_value, lot_size)
            self.update_chart(capital, risk_amount * (capital/100 if self.risk_type.get() == "percent" else 1), 
                            lot_size)
            
            # Calculer la marge si levier est défini
            if self.leverage_var.get().isdigit():
                self.calculate_margin(lot_size)
                
        except Exception as e:
            messagebox.showerror("Erreur de calcul", f"Une erreur est survenue: {str(e)}")
    
    def calculate_fixed_fractional(self, capital, risk_amount, sl_pips, pip_value):
        """Méthode standard de positionnement fractionnaire fixe"""
        if self.risk_type.get() == "percent":
            risk_dollars = capital * (risk_amount / 100)
        else:
            risk_dollars = risk_amount
        return risk_dollars / (sl_pips * pip_value)
    
    def calculate_volatility_based(self, capital, risk_amount, sl_pips, pip_value):
        """Position basée sur la volatilité du marché"""
        # Facteur de volatilité (dans une vraie application, utiliser des données réelles)
        volatility_factor = 1.0
        base_size = self.calculate_fixed_fractional(capital, risk_amount, sl_pips, pip_value)
        return base_size * volatility_factor
    
    def calculate_kelly_criterion(self, capital, risk_amount, sl_pips, pip_value):
        """Position utilisant le critère de Kelly"""
        # Taux de gain et ratio gain/pertes (exemples)
        win_rate = 0.55  # Taux de gain
        payoff_ratio = 2.0  # Ratio gain/pertes
        kelly_fraction = win_rate - (1 - win_rate)/payoff_ratio
        base_size = self.calculate_fixed_fractional(capital, risk_amount, sl_pips, pip_value)
        return base_size * kelly_fraction * 0.5  # Demi-Kelly pour approche conservative
    
    def calculate_margin(self, lot_size=None):
        """Calculer la marge requise pour le trade"""
        try:
            if lot_size is None:
                # Obtenir une taille de lot approximative
                capital = float(self.capital_var.get())
                risk_amount = float(self.risk_amount_var.get())
                sl_pips = float(self.sl_var.get())
                instrument = self.instrument_var.get()
                pip_value = VALEUR_PIP.get(instrument, 10)
                
                if self.risk_type.get() == "percent":
                    risk_dollars = capital * (risk_amount / 100)
                else:
                    risk_dollars = risk_amount
                    
                lot_size = risk_dollars / (sl_pips * pip_value)
            
            leverage = int(self.leverage_var.get())
            instrument = self.instrument_var.get()
            
            # Calcul simplifié de la marge
            if instrument in ["XAUUSD", "XAGUSD"]:
                contract_size = 100  # onces pour les métaux
            elif instrument.startswith("USD"):
                contract_size = 100000  # lot standard pour Forex
            else:
                contract_size = 100000  # valeur par défaut
            
            margin_required = (contract_size * lot_size) / leverage
            self.margin_result_var.set(f"Marge requise: ${margin_required:,.2f}")
            
        except ValueError:
            messagebox.showerror("Erreur", "Veuillez entrer un levier valide")
    
    def update_results_display(self, instrument, capital, risk_amount, sl_pips, pip_value, lot_size):
        """Mettre à jour l'affichage des résultats"""
        # Résultat principal
        self.result_var.set(f"Taille de lot recommandée: {lot_size:.2f}")
        
        # Détails du calcul
        risk_dollars = risk_amount * (capital/100 if self.risk_type.get() == "percent" else 1)
        method_name = {
            "fixed": "Fraction Fixe",
            "volatility": "Ajustée à la Volatilité",
            "kelly": "Critère de Kelly"
        }.get(self.position_method.get(), "Fraction Fixe")
        
        details = (
            f"Détails du calcul:\n"
            f"• Instrument: {instrument} (Valeur du pip: ${pip_value:.2f} par lot)\n"
            f"• Capital: ${capital:,.2f} {self.account_currency.get()}\n"
            f"• Montant à risquer: ${risk_dollars:,.2f} "
            f"({risk_amount:.2f}{'%' if self.risk_type.get() == 'percent' else '$'})\n"
            f"• Stop-loss: {sl_pips} pips\n"
            f"• Taille de position: {lot_size:.2f} lots\n"
            f"• Méthode: {method_name}\n"
            f"• Ratio Risque/Récompense: 1:{self.calculate_reward_ratio(sl_pips):.1f}"
        )
        self.details_var.set(details)
    
    def calculate_reward_ratio(self, sl_pips):
        """Calculer le ratio risque/récompense"""
        return 2.0  # Ratio par défaut 1:2
    
    def update_chart(self, capital, risk, lot_size):
        """Mettre à jour le graphique"""
        self.ax.clear()
        
        labels = ['Capital', 'Montant Risqué', 'Taille de Lot']
        values = [capital, risk, lot_size * 1000]  # Mise à l'échelle pour visibilité
        
        colors = ['#4CAF50', '#FF9800', '#2196F3']
        bars = self.ax.bar(labels, values, color=colors)
        
        # Ajouter les valeurs sur les barres
        for bar in bars:
            height = bar.get_height()
            self.ax.text(bar.get_x() + bar.get_width()/2., height,
                        f'{height:,.2f}' if height < 1000 else f'{height:,.0f}',
                        ha='center', va='bottom')
        
        self.ax.set_ylabel('Montant ($) | Taille de Lot (Mise à l\'échelle)')
        self.ax.set_title('Résumé de la Position')
        self.fig.tight_layout()
        self.canvas.draw()
    
    def save_trade_journal(self):
        """Sauvegarder le trade dans le journal"""
        trade_data = {
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "instrument": self.instrument_var.get(),
            "lot_size": self.result_var.get().split(":")[1].strip(),
            "risk": self.risk_amount_var.get() + ("%" if self.risk_type.get() == "percent" else "$"),
            "stop_loss": f"{self.sl_var.get()} pips",
            "notes": self.notes_text.get("1.0", "end-1c"),
            "calculation_method": self.position_method.get()
        }
        
        try:
            # Charger le journal existant
            with open("trade_journal.json", "r") as f:
                journal = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            journal = []
            
        journal.append(trade_data)
        
        with open("trade_journal.json", "w") as f:
            json.dump(journal, f, indent=2)
            
        messagebox.showinfo("Succès", "Trade enregistré dans le journal")
        self.notes_text.delete("1.0", "end")
    
    def save_settings(self):
        """Sauvegarder les paramètres"""
        filepath = filedialog.asksaveasfilename(defaultextension=".txt",
                                               filetypes=[("Fichiers texte", "*.txt")])
        if filepath:
            try:
                with open(filepath, 'w') as f:
                    f.write(f"{self.capital_var.get()}\n")
                    f.write(f"{self.risk_amount_var.get()}\n")
                    f.write(f"{self.sl_var.get()}\n")
                    f.write(f"{self.instrument_var.get()}\n")
                    f.write(f"{self.risk_type.get()}\n")
                    f.write(f"{self.position_method.get()}\n")
                    f.write(f"{self.leverage_var.get()}\n")
                    f.write(f"{self.account_currency.get()}\n")
            except Exception as e:
                messagebox.showerror("Erreur", f"Échec de la sauvegarde: {str(e)}")
    
    def load_settings(self):
        """Charger les paramètres"""
        filepath = filedialog.askopenfilename(filetypes=[("Fichiers texte", "*.txt")])
        if filepath:
            try:
                with open(filepath, 'r') as f:
                    lines = [line.strip() for line in f.readlines()]
                    if len(lines) >= 8:
                        self.capital_var.set(lines[0])
                        self.risk_amount_var.set(lines[1])
                        self.sl_var.set(lines[2])
                        self.instrument_var.set(lines[3])
                        self.risk_type.set(lines[4])
                        self.position_method.set(lines[5])
                        self.leverage_var.set(lines[6])
                        self.account_currency.set(lines[7])
            except Exception as e:
                messagebox.showerror("Erreur", f"Échec du chargement: {str(e)}")
    
    def reset_calculator(self):
        """Réinitialiser le calculateur"""
        self.capital_var.set("10000")
        self.risk_amount_var.set("1")
        self.sl_var.set("20")
        self.instrument_var.set("EURUSD")
        self.risk_type.set("percent")
        self.position_method.set("fixed")
        self.leverage_var.set("100")
        self.account_currency.set("USD")
        self.notes_text.delete("1.0", "end")
        self.result_var.set("Taille de lot calculée ici")
        self.details_var.set("Détails du calcul")
        self.margin_result_var.set("Marge requise: -")
        self.ax.clear()
        self.canvas.draw()
    
    # Fonctions d'aide et dialogues
    def show_position_method_info(self):
        info_text = (
            "Méthodes de positionnement:\n\n"
            "1. Fraction Fixe - Méthode standard basée sur un % du compte\n"
            "2. Volatilité - Ajuste la position selon la volatilité du marché\n"
            "3. Critère de Kelly - Optimise la position selon la probabilité de gain"
        )
        messagebox.showinfo("Méthodes de Positionnement", info_text)
    
    def show_pip_calculator(self):
        simpledialog.askstring("Calculateur de Pip", 
                             "Cette fonctionnalité sera implémentée dans une future version")
    
    def show_margin_calculator(self):
        self.calculate_margin()
        messagebox.showinfo("Calculateur de Marge", 
                          f"Exigence de marge actuelle:\n{self.margin_result_var.get()}")
    
    def show_currency_converter(self):
        simpledialog.askstring("Convertisseur de Devise", 
                             "Cette fonctionnalité sera implémentée dans une future version")
    
    def show_user_guide(self):
        webbrowser.open("https://www.example.com/guide-utilisateur")
    
    def show_about(self):
        about_text = (
            "Calculateur de Position Forex Pro\n"
            "Version 2.0\n\n"
            "© 2023 Outils Forex\n"
            "Tous droits réservés"
        )
        messagebox.showinfo("À propos", about_text)

if __name__ == "__main__":
    root = tk.Tk()
    app = AdvancedLotSizeCalculator(root)
    root.mainloop()