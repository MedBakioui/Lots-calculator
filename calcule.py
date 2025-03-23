import tkinter as tk
from tkinter import messagebox, filedialog, ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Dictionnaire des valeurs de pip pour différents instruments financiers
VALEUR_PIP = {
    "EURUSD": 10,  # Valeur du pip pour 1 lot standard
    "GBPUSD": 10,
    "USDJPY": 9.09,  # Exemple de valeur ajustée pour USDJPY
    "XAUUSD": 1,    # Or (Gold), valeur du pip pour 1 lot standard
    "NQ": 20,       # Nasdaq 100, valeur du pip pour 1 lot standard
}

# Fonction pour calculer la taille du lot
def calculer_taille_lot():
    try:
        # Récupérer les valeurs saisies
        capital = float(entry_capital.get())
        risque = float(entry_risque.get())
        stop_loss_pips = float(entry_stop_loss.get())
        
        # Récupérer la valeur du pip en fonction de l'instrument sélectionné
        instrument = combo_instrument.get()
        valeur_pip = VALEUR_PIP.get(instrument, 10)  # Valeur par défaut si l'instrument n'est pas trouvé
        
        # Calculer le montant à risquer
        if var_risque.get() == "pourcentage":
            montant_risque = capital * (risque / 100)
        else:
            montant_risque = risque
        
        # Calculer la taille du lot
        taille_lot = montant_risque / (stop_loss_pips * valeur_pip)
        
        # Afficher le résultat
        resultat.config(text=f"Taille du lot recommandée : {taille_lot:.2f} lots")
        
        # Afficher les détails du calcul
        details.config(text=f"Détails du calcul :\n"
                            f"Montant à risquer : {montant_risque:.2f} $\n"
                            f"Stop-loss : {stop_loss_pips} pips\n"
                            f"Valeur du pip : {valeur_pip} $ par lot")
        
        # Mettre à jour le graphique
        mettre_a_jour_graphique(capital, montant_risque, taille_lot)
    except ValueError:
        messagebox.showerror("Erreur", "Veuillez saisir des valeurs valides.")

# Fonction pour mettre à jour le graphique
def mettre_a_jour_graphique(capital, montant_risque, taille_lot):
    ax.clear()
    labels = ['Capital', 'Montant à risquer', 'Taille du lot']
    valeurs = [capital, montant_risque, taille_lot]
    ax.bar(labels, valeurs, color=['blue', 'orange', 'green'])
    ax.set_ylabel('Montant ($)')
    ax.set_title('Résumé du calcul')
    canvas.draw()

# Fonction pour charger les paramètres
def charger_parametres():
    fichier = filedialog.askopenfilename(filetypes=[("Fichiers texte", "*.txt")])
    if fichier:
        with open(fichier, 'r') as f:
            parametres = f.readlines()
            entry_capital.delete(0, tk.END)
            entry_capital.insert(0, parametres[0].strip())
            entry_risque.delete(0, tk.END)
            entry_risque.insert(0, parametres[1].strip())
            entry_stop_loss.delete(0, tk.END)
            entry_stop_loss.insert(0, parametres[2].strip())
            combo_instrument.set(parametres[3].strip())

# Fonction pour sauvegarder les paramètres
def sauvegarder_parametres():
    fichier = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Fichiers texte", "*.txt")])
    if fichier:
        with open(fichier, 'w') as f:
            f.write(entry_capital.get() + "\n")
            f.write(entry_risque.get() + "\n")
            f.write(entry_stop_loss.get() + "\n")
            f.write(combo_instrument.get() + "\n")

# Création de la fenêtre principale
app = tk.Tk()
app.title("Calculateur de Taille de Lot Forex")
app.geometry("800x600")  # Taille initiale de la fenêtre

# Configurer les colonnes et les lignes pour qu'elles s'adaptent à la taille de la fenêtre
app.grid_columnconfigure(0, weight=1)
app.grid_columnconfigure(1, weight=1)
app.grid_rowconfigure(9, weight=1)  # La ligne du graphique s'étire

# Titre principal
titre_principal = tk.Label(app, text="Calculateur de Taille de Lot Forex", font=("Arial", 16, "bold"))
titre_principal.grid(row=0, column=0, columnspan=2, pady=10, sticky="ew")

# Section : Instrument financier
frame_instrument = tk.LabelFrame(app, text="1. Instrument Financier", padx=10, pady=10)
frame_instrument.grid(row=1, column=0, columnspan=2, padx=10, pady=5, sticky="ew")
frame_instrument.grid_columnconfigure(1, weight=1)

label_instrument = tk.Label(frame_instrument, text="Choisissez l'instrument financier :")
label_instrument.grid(row=0, column=0, padx=5, pady=5, sticky="w")
combo_instrument = ttk.Combobox(frame_instrument, values=list(VALEUR_PIP.keys()))
combo_instrument.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
combo_instrument.set("EURUSD")  # Valeur par défaut

# Section : Capital
frame_capital = tk.LabelFrame(app, text="2. Votre Capital", padx=10, pady=10)
frame_capital.grid(row=2, column=0, columnspan=2, padx=10, pady=5, sticky="ew")
frame_capital.grid_columnconfigure(1, weight=1)

label_capital = tk.Label(frame_capital, text="Capital disponible (en dollars) :")
label_capital.grid(row=0, column=0, padx=5, pady=5, sticky="w")
entry_capital = tk.Entry(frame_capital)
entry_capital.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

# Section : Risque
frame_risque = tk.LabelFrame(app, text="3. Risque", padx=10, pady=10)
frame_risque.grid(row=3, column=0, columnspan=2, padx=10, pady=5, sticky="ew")
frame_risque.grid_columnconfigure(1, weight=1)

var_risque = tk.StringVar(value="pourcentage")
tk.Radiobutton(frame_risque, text="Risque en %", variable=var_risque, value="pourcentage").grid(row=0, column=0, padx=5, pady=5, sticky="w")
tk.Radiobutton(frame_risque, text="Risque en $", variable=var_risque, value="montant").grid(row=0, column=1, padx=5, pady=5, sticky="w")

label_risque = tk.Label(frame_risque, text="Montant du risque :")
label_risque.grid(row=1, column=0, padx=5, pady=5, sticky="w")
entry_risque = tk.Entry(frame_risque)
entry_risque.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

# Section : Stop-loss
frame_stop_loss = tk.LabelFrame(app, text="4. Stop-loss", padx=10, pady=10)
frame_stop_loss.grid(row=4, column=0, columnspan=2, padx=10, pady=5, sticky="ew")
frame_stop_loss.grid_columnconfigure(1, weight=1)

label_stop_loss = tk.Label(frame_stop_loss, text="Distance du stop-loss (en pips) :")
label_stop_loss.grid(row=0, column=0, padx=5, pady=5, sticky="w")
entry_stop_loss = tk.Entry(frame_stop_loss)
entry_stop_loss.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

# Boutons pour charger et sauvegarder les paramètres
frame_fichier = tk.Frame(app)
frame_fichier.grid(row=5, column=0, columnspan=2, pady=10, sticky="ew")
frame_fichier.grid_columnconfigure(0, weight=1)
frame_fichier.grid_columnconfigure(1, weight=1)

bouton_charger = tk.Button(frame_fichier, text="Charger les paramètres", command=charger_parametres)
bouton_charger.grid(row=0, column=0, padx=5, sticky="ew")

bouton_sauvegarder = tk.Button(frame_fichier, text="Sauvegarder les paramètres", command=sauvegarder_parametres)
bouton_sauvegarder.grid(row=0, column=1, padx=5, sticky="ew")

# Bouton pour calculer
bouton_calculer = tk.Button(app, text="Calculer la Taille du Lot", command=calculer_taille_lot, bg="blue", fg="white", font=("Arial", 12, "bold"))
bouton_calculer.grid(row=6, column=0, columnspan=2, pady=20, sticky="ew")

# Affichage du résultat
resultat = tk.Label(app, text="Taille du lot recommandée : ", font=("Arial", 12, "bold"), fg="green")
resultat.grid(row=7, column=0, columnspan=2, pady=10, sticky="ew")

# Détails du calcul
details = tk.Label(app, text="Détails du calcul :", font=("Arial", 10))
details.grid(row=8, column=0, columnspan=2, pady=10, sticky="ew")

# Graphique
fig, ax = plt.subplots(figsize=(6, 3))
canvas = FigureCanvasTkAgg(fig, master=app)
canvas.get_tk_widget().grid(row=9, column=0, columnspan=2, pady=10, sticky="nsew")

# Lancer l'application
app.mainloop()