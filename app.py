import streamlit as st

# Titre et description
st.title("Simulateur de voyage à Disneyland")
st.write("Comparez les coûts des différents scénarios pour votre groupe et ajustez les paramètres selon vos besoins.")

def reset_to_defaults():
    return {
        "common": {
            "disney": 300,  # Par personne
            "food": 15,  # Par jour
            "lodging_per_night": 125  # Coût du logement par nuit et par participant
        },
        "minibus": {
            "location": 500,  # Location du minibus
            "fuel": 250,  # Carburant
            "toll": 90,  # Péages
            "parking": 20,  # Par jour
            "sarah_train": 80  # Train pour Sarah venant de Nantes
        },
        "train": {
            "bordeaux_train": 94,  # Billet Bordeaux-Paris
            "nantes_train": 80,  # Billet Nantes-Paris
            "rer_paris_disney": 10,  # RER Paris-Disney (par jour par personne)
            "rer_airbnb_disney": 8,  # RER Airbnb-Disney (par jour par personne)
            "baggage": 5  # Bagagerie (par personne par jour)
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

# Ajustement du coût du logement
costs["common"]["lodging_per_night"] = st.number_input("Coût du logement par nuit et par participant (par défaut 125€)", value=costs["common"]["lodging_per_night"])
# Correction du calcul total du logement
lodging_per_participant = costs["common"]["lodging_per_night"] * days
total_lodging = lodging_per_participant * participants

# Sélection du mode de transport
transport_type = st.selectbox("Mode de transport", ["Minibus", "Train"])

if transport_type == "Minibus":
    st.sidebar.title("Paramètres spécifiques au Minibus")
    costs["minibus"]["location"] = st.sidebar.number_input("Coût location (Minibus, par défaut 500€)", value=costs["minibus"]["location"])
    costs["minibus"]["fuel"] = st.sidebar.number_input("Coût carburant (Minibus, par défaut 250€)", value=costs["minibus"]["fuel"])
    costs["minibus"]["toll"] = st.sidebar.number_input("Coût péages (Minibus, par défaut 90€)", value=costs["minibus"]["toll"])
    costs["minibus"]["parking"] = st.sidebar.number_input("Coût parking (par jour, Minibus, par défaut 20€)", value=costs["minibus"]["parking"])
    costs["minibus"]["sarah_train"] = st.sidebar.number_input("Coût train pour Sarah (Minibus, par défaut 80€)", value=costs["minibus"]["sarah_train"])

    total_transport = (
        costs["minibus"]["location"] +
        costs["minibus"]["fuel"] +
        costs["minibus"]["toll"] +
        (costs["minibus"]["parking"] * days) +
        costs["minibus"]["sarah_train"]
    )

elif transport_type == "Train":
    st.sidebar.title("Paramètres spécifiques au Train")
    num_bordeaux_train = st.sidebar.number_input("Nombre de participants depuis Bordeaux", min_value=0, value=4)
    num_nantes_train = st.sidebar.number_input("Nombre de participants depuis Nantes", min_value=0, value=1)
    num_rer_paris_disney = st.sidebar.number_input("Nombre de participants utilisant le RER depuis Paris pour Disneyland", min_value=0, value=2)
    num_rer_airbnb_disney = st.sidebar.number_input("Nombre de participants utilisant le RER depuis l'Airbnb pour Disneyland", min_value=0, value=5)

    costs["train"]["bordeaux_train"] = st.sidebar.number_input("Coût billet Bordeaux-Paris (par personne, par défaut 94€)", value=costs["train"]["bordeaux_train"])
    costs["train"]["nantes_train"] = st.sidebar.number_input("Coût billet Nantes-Paris (par personne, par défaut 80€)", value=costs["train"]["nantes_train"])
    costs["train"]["rer_paris_disney"] = st.sidebar.number_input("Coût RER Paris-Disney (par jour par personne, par défaut 10€)", value=costs["train"]["rer_paris_disney"])
    costs["train"]["rer_airbnb_disney"] = st.sidebar.number_input("Coût RER Airbnb-Disney (par jour par personne, par défaut 8€)", value=costs["train"]["rer_airbnb_disney"])
    costs["train"]["baggage"] = st.sidebar.number_input("Coût bagagerie (par personne par jour, par défaut 5€)", value=costs["train"]["baggage"])

    baggage_days = st.sidebar.slider("Nombre de jours d'utilisation de la bagagerie", min_value=0, max_value=2, value=1)

    total_transport = (
        (costs["train"]["bordeaux_train"] * num_bordeaux_train) +
        (costs["train"]["nantes_train"] * num_nantes_train) +
        (costs["train"]["rer_paris_disney"] * days * num_rer_paris_disney) +
        (costs["train"]["rer_airbnb_disney"] * days * num_rer_airbnb_disney) +
        (costs["train"]["baggage"] * participants * baggage_days)
    )

# Options communes
st.sidebar.title("Paramètres communs")
costs["common"]["disney"] = st.sidebar.number_input("Coût Disney (par personne, par défaut 300€)", value=costs["common"]["disney"])
costs["common"]["food"] = st.sidebar.number_input("Coût nourriture (par jour, par personne, par défaut 15€)", value=costs["common"]["food"])

total_disney = costs["common"]["disney"] * participants
total_food = costs["common"]["food"] * days * participants

# Total final
# Les coûts totaux sont répartis sur 6 participants au lieu de 7
total_cost = total_transport + total_lodging + total_disney + total_food
cost_per_person = total_cost / 6

# Affichage des résultats
st.write(f"**Coût total pour {transport_type} :** {total_cost} €")
st.write(f"**Coût par personne (réparti sur 6) :** {cost_per_person:.2f} €")

# Résumé détaillé
st.write("### Détail des coûts")
st.write(f"- **Transport total :** {total_transport} €")
st.write(f"- **Hébergement (par nuit) :** {costs['common']['lodging_per_night']} € par participant")
st.write(f"- **Hébergement total :** {total_lodging} €")
st.write(f"- **Disney billets :** {total_disney} €")
st.write(f"  - Coût par jour par personne : {costs['common']['food']} €")
st.write(f"  - Coût total nourriture : {total_food} €")
