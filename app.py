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
            "transport": 707,  # Bordeaux/Nantes à Paris, métro Disney, RER, bagagerie
            "airbnb": 1000
        },
        "train_airbnb_proche": {
            "transport": 513,  # Bordeaux/Nantes à Paris, métro Disney, bagagerie
            "airbnb": 1200
        }
    }

# Initialisation des coûts
default_costs = reset_to_defaults()
costs = default_costs.copy()

# Option pour rétablir les valeurs par défaut
if st.button("Rétablir les valeurs par défaut"):
    costs = reset_to_defaults()
    st.experimental_rerun()

# Ajustement des coûts
st.sidebar.title("Paramètres des coûts")

# Options communes
costs["common"]["disney"] = st.sidebar.number_input("Coût Disney (par personne)", value=costs["common"]["disney"])
costs["common"]["food"] = st.sidebar.number_input("Coût nourriture (par jour)", value=costs["common"]["food"])

# Options spécifiques au Minibus
costs["minibus"]["location"] = st.sidebar.number_input("Coût location (Minibus)", value=costs["minibus"]["location"])
costs["minibus"]["fuel"] = st.sidebar.number_input("Coût carburant (Minibus)", value=costs["minibus"]["fuel"])
costs["minibus"]["toll"] = st.sidebar.number_input("Coût péages (Minibus)", value=costs["minibus"]["toll"])
costs["minibus"]["parking"] = st.sidebar.number_input("Coût parking (par jour, Minibus)", value=costs["minibus"]["parking"])
costs["minibus"]["sarah_train"] = st.sidebar.number_input("Coût train pour Sarah (Minibus)", value=costs["minibus"]["sarah_train"])

# Options spécifiques au Train + Airbnb loin
costs["train_airbnb_loin"]["transport"] = st.sidebar.number_input("Coût transport (Train + Airbnb loin)", value=costs["train_airbnb_loin"]["transport"])
costs["train_airbnb_loin"]["airbnb"] = st.sidebar.number_input("Coût Airbnb (Train + Airbnb loin)", value=costs["train_airbnb_loin"]["airbnb"])

# Options spécifiques au Train + Airbnb proche
costs["train_airbnb_proche"]["transport"] = st.sidebar.number_input("Coût transport (Train + Airbnb proche)", value=costs["train_airbnb_proche"]["transport"])
costs["train_airbnb_proche"]["airbnb"] = st.sidebar.number_input("Coût Airbnb (Train + Airbnb proche)", value=costs["train_airbnb_proche"]["airbnb"])

# Entrées utilisateur
participants = st.number_input("Nombre de participants", min_value=1, value=7)
days = st.number_input("Nombre de jours/nuitées", min_value=1, value=4)
transport_type = st.selectbox("Mode de transport", ["Minibus", "Train + Airbnb loin", "Train + Airbnb proche"])

# Calculs
if transport_type == "Minibus":
    total_transport = (
        costs["minibus"]["location"] +
        costs["minibus"]["fuel"] +
        costs["minibus"]["toll"] +
        (costs["minibus"]["parking"] * days) +
        costs["minibus"]["sarah_train"]
    )
    total_airbnb = 1000  # Coût Airbnb défini pour le Minibus
elif transport_type == "Train + Airbnb loin":
    total_transport = costs["train_airbnb_loin"]["transport"]
    total_airbnb = costs["train_airbnb_loin"]["airbnb"]
elif transport_type == "Train + Airbnb proche":
    total_transport = costs["train_airbnb_proche"]["transport"]
    total_airbnb = costs["train_airbnb_proche"]["airbnb"]

total_disney = costs["common"]["disney"] * participants
total_food = costs["common"]["food"] * days * participants

# Total final
total_cost = total_transport + total_airbnb + total_disney + total_food
cost_per_person = total_cost / participants

# Affichage des résultats
st.write(f"**Coût total pour {transport_type} :** {total_cost} €")
st.write(f"**Coût par personne :** {cost_per_person:.2f} €")

# Résumé détaillé
st.write("### Détail des coûts")
st.write(f"- **Transport total :** {total_transport} €")
st.write(f"- **Hébergement :** {total_airbnb} €")
st.write(f"- **Disney billets :** {total_disney} €")
st.write(f"- **Nourriture :** {total_food} €")
