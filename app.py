import streamlit as st

# Titre et description
st.title("Simulateur de voyage à Disneyland")
st.write("Comparez les coûts des différents scénarios pour votre groupe et ajustez les paramètres selon vos besoins.")

def reset_to_defaults():
    return {
        "common": {
            "disney": 300,  # Par personne
            "food": 15  # Par jour
        },
        "minibus": {
            "location": 500,  # Location du minibus
            "fuel": 250,  # Carburant
            "toll": 90,  # Péages
            "parking": 20,  # Par jour
            "sarah_train": 80  # Train pour Sarah venant de Nantes
        },
        "train_airbnb_loin": {
            "bordeaux_train": 94,  # Billet Bordeaux-Paris
            "nantes_train": 80,  # Billet Nantes-Paris
            "rer_disney": 10,  # RER Paris-Disney (par jour par personne)
            "baggage": 5,  # Bagagerie (par personne par jour)
            "airbnb": 1000  # Airbnb coût total
        },
        "train_airbnb_proche": {
            "bordeaux_train": 94,  # Billet Bordeaux-Paris
            "nantes_train": 80,  # Billet Nantes-Paris
            "metro_disney": 8,  # Métro Paris-Disney (par trajet par personne)
            "baggage": 5,  # Bagagerie (par personne par jour)
            "airbnb": 1200  # Airbnb coût total
        }
    }

# Initialisation des coûts
default_costs = reset_to_defaults()
costs = default_costs.copy()

# Option pour rétablir les valeurs par défaut
if st.button("Rétablir les valeurs par défaut"):
    costs = reset_to_defaults()
    st.experimental_rerun()

# Entrées utilisateur
participants = st.number_input("Nombre de participants", min_value=1, value=7)
days = st.number_input("Nombre de jours/nuitées", min_value=1, value=4)
transport_type = st.selectbox("Mode de transport", ["Minibus", "Train + Airbnb loin", "Train + Airbnb proche"])

# Ajustement des coûts dynamiques en fonction du transport
if transport_type == "Minibus":
    st.sidebar.title("Paramètres spécifiques au Minibus")
    costs["minibus"]["location"] = st.sidebar.number_input("Coût location (Minibus)", value=costs["minibus"]["location"])
    costs["minibus"]["fuel"] = st.sidebar.number_input("Coût carburant (Minibus)", value=costs["minibus"]["fuel"])
    costs["minibus"]["toll"] = st.sidebar.number_input("Coût péages (Minibus)", value=costs["minibus"]["toll"])
    costs["minibus"]["parking"] = st.sidebar.number_input("Coût parking (par jour, Minibus)", value=costs["minibus"]["parking"])
    costs["minibus"]["sarah_train"] = st.sidebar.number_input("Coût train pour Sarah (Minibus)", value=costs["minibus"]["sarah_train"])
    total_transport = (
        costs["minibus"]["location"] +
        costs["minibus"]["fuel"] +
        costs["minibus"]["toll"] +
        (costs["minibus"]["parking"] * days) +
        costs["minibus"]["sarah_train"]
    )
    total_airbnb = 1000  # Coût Airbnb défini pour le Minibus

elif transport_type == "Train + Airbnb loin":
    st.sidebar.title("Paramètres spécifiques au Train + Airbnb loin")
    costs["train_airbnb_loin"]["bordeaux_train"] = st.sidebar.number_input("Coût billet Bordeaux-Paris (par personne)", value=costs["train_airbnb_loin"]["bordeaux_train"])
    costs["train_airbnb_loin"]["nantes_train"] = st.sidebar.number_input("Coût billet Nantes-Paris (par personne)", value=costs["train_airbnb_loin"]["nantes_train"])
    costs["train_airbnb_loin"]["rer_disney"] = st.sidebar.number_input("Coût RER Paris-Disney (par jour par personne)", value=costs["train_airbnb_loin"]["rer_disney"])
    costs["train_airbnb_loin"]["baggage"] = st.sidebar.number_input("Coût bagagerie (par personne par jour)", value=costs["train_airbnb_loin"]["baggage"])
    costs["train_airbnb_loin"]["airbnb"] = st.sidebar.number_input("Coût Airbnb (Train + Airbnb loin)", value=costs["train_airbnb_loin"]["airbnb"])

    baggage_days = st.sidebar.slider("Nombre de jours d'utilisation de la bagagerie", min_value=0, max_value=2, value=1)

    total_transport = (
        (costs["train_airbnb_loin"]["bordeaux_train"] * 4) +
        (costs["train_airbnb_loin"]["nantes_train"] * 1) +
        (costs["train_airbnb_loin"]["rer_disney"] * days * participants) +
        (costs["train_airbnb_loin"]["baggage"] * participants * baggage_days)
    )
    total_airbnb = costs["train_airbnb_loin"]["airbnb"]

elif transport_type == "Train + Airbnb proche":
    st.sidebar.title("Paramètres spécifiques au Train + Airbnb proche")
    costs["train_airbnb_proche"]["bordeaux_train"] = st.sidebar.number_input("Coût billet Bordeaux-Paris (par personne)", value=costs["train_airbnb_proche"]["bordeaux_train"])
    costs["train_airbnb_proche"]["nantes_train"] = st.sidebar.number_input("Coût billet Nantes-Paris (par personne)", value=costs["train_airbnb_proche"]["nantes_train"])
    costs["train_airbnb_proche"]["metro_disney"] = st.sidebar.number_input("Coût métro Paris-Disney (par trajet par personne)", value=costs["train_airbnb_proche"]["metro_disney"])
    costs["train_airbnb_proche"]["baggage"] = st.sidebar.number_input("Coût bagagerie (par personne par jour)", value=costs["train_airbnb_proche"]["baggage"])
    costs["train_airbnb_proche"]["airbnb"] = st.sidebar.number_input("Coût Airbnb (Train + Airbnb proche)", value=costs["train_airbnb_proche"]["airbnb"])

    baggage_days = st.sidebar.slider("Nombre de jours d'utilisation de la bagagerie", min_value=0, max_value=2, value=1)

    total_transport = (
        (costs["train_airbnb_proche"]["bordeaux_train"] * 4) +
        (costs["train_airbnb_proche"]["nantes_train"] * 1) +
        (costs["train_airbnb_proche"]["metro_disney"] * 4 * participants) +
        (costs["train_airbnb_proche"]["baggage"] * participants * baggage_days)
    )
    total_airbnb = costs["train_airbnb_proche"]["airbnb"]

# Options communes
st.sidebar.title("Paramètres communs")
costs["common"]["disney"] = st.sidebar.number_input("Coût Disney (par personne)", value=costs["common"]["disney"])
costs["common"]["food"] = st.sidebar.number_input("Coût nourriture (par jour)", value=costs["common"]["food"])

total_disney = costs["common"]["disney"] * participants
total_food = costs["common"]["food"] * days * participants

# Total final
# Les coûts totaux sont répartis sur 6 participants au lieu de 7
total_cost = total_transport + total_airbnb + total_disney + total_food
cost_per_person = total_cost / 6

# Affichage des résultats
st.write(f"**Coût total pour {transport_type} :** {total_cost} €")
st.write(f"**Coût par personne (réparti sur 6) :** {cost_per_person:.2f} €")

# Résumé détaillé
st.write("### Détail des coûts")
st.write(f"- **Transport total :** {total_transport} €")
st.write(f"- **Hébergement :** {total_airbnb} €")
st.write(f"- **Disney billets :** {total_disney} €")
st.write(f"- **Nourriture :** {total_food} €")
