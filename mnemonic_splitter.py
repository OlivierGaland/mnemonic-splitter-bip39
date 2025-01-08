import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.dialogs import Messagebox
import random

from src.bip39 import generate_random_private_key, Bip39Secret
from src.mnemonic_manager import MnemonicSplitter, MnemonicMerger
from src.mnemonic_sss_manager import MnemonicSSSSplitter, MnemonicSSSMerger

TEXT_WIDGETS_LIST = []

def update_fields(*args):
    """Met à jour les champs et ajuste les valeurs de n et m selon l'algorithme."""
    global m_dropdown  # Assurez-vous de déclarer m_dropdown global si utilisé dans update_m_dropdown

    # Ajuster n en fonction des limites de l'algorithme sélectionné
    try:
        n = int(n_value.get())
    except ValueError:
        n = 4  # Valeur par défaut

    if selected_option.get() == "Standard":
        if n < 2 or n > 10:
            n_value.set("4")  # Valeur par défaut pour Standard

    elif selected_option.get() == "Shamir Shared Secret":
        if n < 4 or n > 10:
            n_value.set("4")  # Valeur par défaut pour Shamir

        # Ajuster m en fonction de n
        try:
            m = int(m_value.get())
        except ValueError:
            m = 3  # Valeur par défaut pour m

        if m < 3 or m >= n:
            m_value.set(str(n - 1))  # Valeur par défaut pour m selon les limites

    # **Recalculer m pour Shamir si nécessaire**
    if selected_option.get() == "Shamir Shared Secret":
        # Lorsque n_value est remis par défaut, recalculer m_value
        n = int(n_value.get())
        m = int(m_value.get()) if m_value.get().isdigit() else n - 1
        if m < 3 or m >= n:
            m_value.set(str(n - 1))  # Réinitialiser m_value en fonction des limites

    # Réinitialiser les widgets de la fenêtre
    for widget in dynamic_frame.winfo_children():
        widget.destroy()

    if selected_option.get() == "Standard":
        # Menu déroulant pour n (2 à 10)
        tk.Label(dynamic_frame, text="Share count:").grid(row=0, column=1, padx=5)
        n_dropdown = ttk.Combobox(
            dynamic_frame,
            textvariable=n_value,
            values=list(range(2, 11)),
            state="readonly",
            width=5,
        )
        n_dropdown.grid(row=0, column=2, padx=5)

    elif selected_option.get() == "Shamir Shared Secret":
        # Menu déroulant pour n (4 à 10)
        tk.Label(dynamic_frame, text="Share count :").grid(row=0, column=1, padx=5)
        n_dropdown = ttk.Combobox(
            dynamic_frame,
            textvariable=n_value,
            values=list(range(4, 11)),
            state="readonly",
            width=5,
        )
        n_dropdown.grid(row=0, column=2, padx=5)

        # Menu déroulant pour m (3 à n-1)
        tk.Label(dynamic_frame, text="Minimum required :").grid(row=0, column=3, padx=5)
        m_dropdown = ttk.Combobox(
            dynamic_frame,
            textvariable=m_value,
            state="readonly",
            width=5,
        )
        m_dropdown.grid(row=0, column=4, padx=5)

        # Mettre à jour les options de m lorsque n change
        def update_m_dropdown(*args):
            try:
                n = int(n_value.get())
                if "m_dropdown" in globals() and m_dropdown.winfo_exists():
                    m_dropdown["values"] = list(range(3, n))
                    if int(m_value.get()) >= n:
                        m_value.set(str(n - 1))  # Réinitialiser si m est hors des limites
            except ValueError:
                pass

        n_value.trace_add("write", update_m_dropdown)
        update_m_dropdown()

    # Boutons "Split" et "Merge"
    tk.Button(dynamic_frame, text="Split", command=on_split_button_click, width=10).grid(row=0, column=5, padx=5)
    tk.Button(dynamic_frame, text="Reconstruct", command=on_merge_button_click, width=10).grid(row=0, column=6, padx=5)

    # Générer dynamiquement les zones de texte selon la valeur de "n"
    generate_dynamic_text_fields()


def generate_dynamic_text_fields():
    """Génère dynamiquement des zones de texte en fonction de la valeur de 'n'."""
    try:
        n = int(n_value.get())
    except ValueError:
        n = 4  # Valeur par défaut si la conversion échoue

    n = max(2, min(10, n))  # Appliquer les limites
    for widget in dynamic_text_fields_frame.winfo_children():
        widget.destroy()

    TEXT_WIDGETS_LIST.clear()
    for i in range(n):
        tk.Label(dynamic_text_fields_frame, text=f"Share {i + 1} mnemonic:").grid(row=i, column=0, padx=5, sticky="w")
        text_widget = tk.Text(dynamic_text_fields_frame, height=2, width=90, wrap=tk.WORD)
        text_widget.grid(row=i, column=1, padx=5, pady=2)
        TEXT_WIDGETS_LIST.append(text_widget)

def clear_shares_text_fields():
    for text_widget in TEXT_WIDGETS_LIST:
        text_widget.delete("1.0", tk.END)

def on_split_button_click():
    try:
        clear_shares_text_fields()
        m = input_text.get("1.0", tk.END).rstrip("\n")
        if selected_option.get() == "Standard":
            s = MnemonicSplitter(mnemonic=m)
            s.split(int(n_value.get()))
            l = s.mnemonic_list
            for i in range(len(l)):
                TEXT_WIDGETS_LIST[i].insert("1.0", l[i])
        elif selected_option.get() == "Shamir Shared Secret":
            s = MnemonicSSSSplitter(mnemonic=m)
            s.split(int(n_value.get()), int(m_value.get()))
            l = s.mnemonic_with_index_list
            for i in range(len(l)):
                TEXT_WIDGETS_LIST[i].insert("1.0", l[i])
        else:
            raise ValueError("ERROR: Unknown algorithm")
    except Exception as e:
        Messagebox.show_error("Error : "+str(e))

def on_merge_button_click():
    try:
        on_clear_button_click()
        ml = [w.get("1.0", tk.END).rstrip("\n") for w in TEXT_WIDGETS_LIST if w.get("1.0", tk.END).rstrip("\n") != ""]
        if selected_option.get() == "Standard":
            s = MnemonicMerger(mnemonic_list=ml)
            s.merge()
            input_text.insert("1.0", s.mnemonic)
        elif selected_option.get() == "Shamir Shared Secret":
            s = MnemonicSSSMerger(mnemonic_list=ml)
            s.merge()
            input_text.insert("1.0", s.mnemonic)
        else:
            raise ValueError("ERROR: Unknown algorithm")
    except Exception as e:
        Messagebox.show_error("Error : "+str(e))

def on_generate_button_click():
    try:
        on_clear_button_click()
        input_text.insert("1.0", Bip39Secret(key=generate_random_private_key()).mnemonic)
    except Exception as e:
        Messagebox.show_error("Error : "+str(e))


def on_clear_button_click():
    input_text.delete("1.0", tk.END)

def on_copy_button_click():
    """Copier le contenu de toutes les zones de texte."""
    clipboard_text = "\n".join([w.get("1.0", tk.END).rstrip("\n") for w in TEXT_WIDGETS_LIST])
    root.clipboard_clear()
    root.clipboard_append(clipboard_text)

def on_paste_button_click():
    """Coller dans toutes les zones de texte."""
    clipboard_text = root.clipboard_get()
    # Séparer le texte par lignes et ignorer les lignes vides à la fin
    texts = clipboard_text.split("\n")
    # Filtrer les lignes vides à la fin du texte
    while texts and not texts[-1].strip():
        texts.pop()  # Supprimer les lignes vides à la fin

    # Vérifier si le nombre de lignes dépasse le nombre de zones de texte
    if len(texts) > len(TEXT_WIDGETS_LIST):
        Messagebox.show_error("The clipboard contains more lines than available text fields.")
    else:
        # Remplir les zones de texte avec les lignes du presse-papiers ou les laisser vides
        for i, text_widget in enumerate(TEXT_WIDGETS_LIST):
            text_widget.delete("1.0", tk.END)
            if i < len(texts):
                text_widget.insert("1.0", texts[i])
            else:
                text_widget.insert("1.0", "")  # Si pas assez de lignes, laisser vide

# Fonction pour mélanger les textes
def on_shuffle_button_click():
    try:
        # Récupérer les textes actuels dans les champs
        current_texts = [w.get("1.0", tk.END).rstrip("\n") for w in TEXT_WIDGETS_LIST]

        # Mélanger les textes de manière aléatoire
        random.shuffle(current_texts)

        # Remettre les textes mélangés dans les zones de texte
        for i, text in enumerate(current_texts):
            TEXT_WIDGETS_LIST[i].delete("1.0", tk.END)  # Supprimer l'ancien texte
            TEXT_WIDGETS_LIST[i].insert("1.0", text)  # Insérer le texte mélangé

    except Exception as e:
        Messagebox.show_error("Error: " + str(e))


def on_copy_button_click2():
    """Copier le contenu du champ de texte principal (input_text) dans le presse-papiers."""
    clipboard_text = input_text.get("1.0", tk.END).rstrip("\n")
    root.clipboard_clear()
    root.clipboard_append(clipboard_text)

def on_paste_button_click2():
    """Coller le contenu du presse-papiers dans le champ de texte principal (input_text)."""
    clipboard_text = root.clipboard_get()
    if clipboard_text.strip():  # Vérifier si le texte n'est pas vide
        input_text.delete("1.0", tk.END)
        input_text.insert("1.0", clipboard_text)

root = ttk.Window(themename="darkly")
root.title("Mnemonic Concealer")
root.minsize(850, 0)
root.resizable(False, False) 

# Cadre principal
text_frame = tk.Frame(root)
text_frame.pack(pady=5, padx=10)

# Zone de texte et premiers boutons (Random et Clear)
tk.Label(text_frame, text="Master Mnemonic:").grid(row=0, column=0, padx=5)
input_text = tk.Text(text_frame, height=2, width=90, wrap=tk.WORD)
input_text.grid(row=0, column=1, padx=5)

# Premier ensemble de boutons (Random et Clear)
# Deuxième ensemble de boutons (Copy et Paste) en dessous
buttons_frame2 = tk.Frame(root)
buttons_frame2.pack(pady=5, padx=10)
tk.Button(buttons_frame2, text="Clear", command=on_clear_button_click, width=10).grid(row=0, column=0, padx=5)
tk.Button(buttons_frame2, text="Copy", command=on_copy_button_click2, width=10).grid(row=0, column=1, padx=5)
tk.Button(buttons_frame2, text="Paste", command=on_paste_button_click2, width=10).grid(row=0, column=2, padx=5)
tk.Button(buttons_frame2, text="Random", command=on_generate_button_click, width=10).grid(row=0, column=3, padx=5)

separator1 = tk.Frame(root, height=2, bd=1, relief="sunken", bg="gray")
separator1.pack(fill="x", padx=10, pady=5)

main_frame = tk.Frame(root)
main_frame.pack(pady=5, padx=10)

tk.Label(main_frame, text="Split algorithm:").grid(row=0, column=0, padx=5)
selected_option = tk.StringVar(value="Standard")
dropdown = ttk.OptionMenu(main_frame, selected_option, "Standard", "Standard", "Shamir Shared Secret", command=update_fields)
dropdown.grid(row=0, column=1, padx=5)

dynamic_frame = tk.Frame(main_frame)
dynamic_frame.grid(row=0, column=2, padx=5)

n_value = tk.StringVar(value="4")
m_value = tk.StringVar(value="3")
n_value.trace_add("write", lambda *args: generate_dynamic_text_fields())

separator2 = tk.Frame(root, height=2, bd=1, relief="sunken", bg="gray")
separator2.pack(fill="x", padx=10, pady=5)

dynamic_text_fields_frame = tk.Frame(root)
dynamic_text_fields_frame.pack(pady=5, padx=10)

buttons_frame = tk.Frame(root)
buttons_frame.pack(pady=5, padx=10)
tk.Button(buttons_frame, text="Clear", command=clear_shares_text_fields, width=10).grid(row=0, column=0, padx=5)
tk.Button(buttons_frame, text="Copy", command=on_copy_button_click, width=10).grid(row=0, column=1, padx=5)
tk.Button(buttons_frame, text="Paste", command=on_paste_button_click, width=10).grid(row=0, column=2, padx=5)
shuffle_button = tk.Button(buttons_frame, text="Shuffle", command=on_shuffle_button_click, width=10)
shuffle_button.grid(row=0, column=3, padx=5)

update_fields()
root.mainloop()
