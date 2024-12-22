import streamlit as st

# Titre et description
st.title("Simulateur de voyage à Disneyland")
st.write("Comparez les coûts des différents scénarios pour votre groupe et ajustez les paramètres selon vos besoins.")

def reset_to_defaults():
    return {
        "minibus": {
            "transport": 1000,  # Location + carburant + péages + parking + train pour Sarah
            "airbnb": 1000,
            "disney": 300,  # Par personne
            "food": 15  # Par jour
        },
        "train_airbnb_loin": {
            "transport": 707,  # Bordeaux/Nantes à Paris, métro Disney, RER, bagagerie
            "airbnb": 1000,
            "disney": 300,  # Par personne
            "food": 15  # Par jour
        },
        "train_airbnb_proche": {
            "transport": 513,  # Bordeaux/Nantes à Paris, métro Disney, bagagerie
            "airbnb": 1200,
            "disney": 300,  # Par personne
            "food": 15  # Par jour
        },
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
costs["minibus"]["transport"] = st.sidebar.number_input("Coût transport (Minibus)", value=costs["minibus"]["transport"])
costs["minibus"]["airbnb"] = st.sidebar.number_input("Coût Airbnb (Minibus)", value=costs["minibus"]["airbnb"])
costs["minibus"]["disney"] = st.sidebar.number_input("Coût Disney (par personne, Minibus)", value=costs["minibus"]["disney"])
costs["minibus"]["food"] = st.sidebar.number_input("Coût nourriture (par jour, Minibus)", value=costs["minibus"]["food"])

costs["train_airbnb_loin"]["transport"] = st.sidebar.number_input("Coût transport (Train + Airbnb loin)", value=costs["train_airbnb_loin"]["transport"])
costs["train_airbnb_loin"]["airbnb"] = st.sidebar.number_input("Coût Airbnb (Train + Airbnb loin)", value=costs["train_airbnb_loin"]["airbnb"])
costs["train_airbnb_loin"]["disney"] = st.sidebar.number_input("Coût Disney (par personne, Train + Airbnb loin)", value=costs["train_airbnb_loin"]["disney"])
costs["train_airbnb_loin"]["food"] = st.sidebar.number_input("Coût nourriture (par jour, Train + Airbnb loin)", value=costs["train_airbnb_loin"]["food"])

costs["train_airbnb_proche"]["transport"] = st.sidebar.number_input("Coût transport (Train + Airbnb proche)", value=costs["train_airbnb_proche"]["transport"])
costs["train_airbnb_proche"]["airbnb"] = st.sidebar.number_input("Coût Airbnb (Train + Airbnb proche)", value=costs["train_airbnb_proche"]["airbnb"])
costs["train_airbnb_proche"]["disney"] = st.sidebar.number_input("Coût Disney (par personne, Train + Airbnb proche)", value=costs["train_airbnb_proche"]["disney"])
costs["train_airbnb_proche"]["food"] = st.sidebar.number_input("Coût nourriture (par jour, Train + Airbnb proche)", value=costs["train_airbnb_proche"]["food"])

# Entrées utilisateur
participants = st.number_input("Nombre de participants", min_value=1, value=7)
days = st.number_input("Nombre de jours/nuitées", min_value=1, value=4)
transport_type = st.selectbox("Mode de transport", ["Minibus", "Train + Airbnb loin", "Train + Airbnb proche"])

# Calculs
if transport_type == "Minibus":
    total_transport = costs["minibus"]["transport"]
    total_airbnb = costs["minibus"]["airbnb"]
    total_disney = costs["minibus"]["disney"] * participants
    total_food = costs["minibus"]["food"] * days * participants
elif transport_type == "Train + Airbnb loin":
    total_transport = costs["train_airbnb_loin"]["transport"]
    total_airbnb = costs["train_airbnb_loin"]["airbnb"]
    total_disney = costs["train_airbnb_loin"]["disney"] * participants
    total_food = costs["train_airbnb_loin"]["food"] * days * participants
elif transport_type == "Train + Airbnb proche":
    total_transport = costs["train_airbnb_proche"]["transport"]
    total_airbnb = costs["train_airbnb_proche"]["airbnb"]
    total_disney = costs["train_airbnb_proche"]["disney"] * participants
    total_food = costs["train_airbnb_proche"]["food"] * days * participants

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
