import streamlit as st
import base64

# Titre et description
st.title("Simulateur de voyage à Disneyland")
st.write("Comparez les coûts des différents scénarios pour votre groupe et ajustez les paramètres selon vos besoins.")

def reset_to_defaults():
    return {
        "common": {
            "disney": 300,  # Par personne
            "food": 15,  # Par jour
            "lodging_per_night": 40  # Coût du logement par nuit et par participant
        },
        "minibus": {
            "location": 500,  # Location du minibus
            "fuel": 250,  # Carburant
            "toll": 90,  # Péages
            "parking": 20,  # Par jour
            "sarah_train": 90  # Train pour Sarah venant de Nantes
        },
        "train": {
            "bordeaux_train": 90,  # Billet Bordeaux-Paris
            "nantes_train": 90,  # Billet Nantes-Paris
            "rer_paris_disney": 10,  # RER Paris-Disney
            "rer_airbnb_disney": 10,  # RER Airbnb-Disney (par jour par personne)
            "baggage": 5  # Bagagerie (par personne par jour)
        }
    }

# Mise en cache des données
def load_data():
    if "cached_costs" not in st.session_state:
        st.session_state["cached_costs"] = reset_to_defaults()
    return st.session_state["cached_costs"]

# Chargement des données sauvegardées
costs = load_data()

# Entrées utilisateur
participants = st.number_input("Nombre de participants", min_value=1, value=7)
days = st.number_input("Nombre de jours/nuitées", min_value=1, value=4)

# Calcul dynamique des participants pour RER
num_bordeaux_train = st.sidebar.number_input("Nombre de participants depuis Bordeaux", min_value=0, value=4)
num_nantes_train = st.sidebar.number_input("Nombre de participants depuis Nantes", min_value=0, value=1)

total_rer_paris_disney_participants = 2 + num_bordeaux_train + num_nantes_train
total_rer_airbnb_disney_participants = participants - total_rer_paris_disney_participants

# Choix Airbnb proche Disney
airbnb_proche_disney = st.checkbox("Airbnb proche Disney (accessible à pieds)")
if airbnb_proche_disney:
    costs["common"]["lodging_per_night"] = 60  # Modifier le coût par nuit par participant
    costs["train"]["rer_airbnb_disney"] = 0  # Désactiver l'option RER Airbnb-Disney
if not airbnb_proche_disney:
    costs["common"]["lodging_per_night"] = 40  # Modifier le coût par nuit par participant
    costs["train"]["rer_airbnb_disney"] = 10

# Ajustement du coût du logement
costs["common"]["lodging_per_night"] = st.number_input("Coût du logement par nuit et par participant", value=costs["common"]["lodging_per_night"])
# Correction du calcul total du logement
lodging_per_participant = costs["common"]["lodging_per_night"] * days
total_lodging = lodging_per_participant * participants

# Sélection du mode de transport
transport_type = st.selectbox("Mode de transport", ["Minibus", "Train"])

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

elif transport_type == "Train":
    st.sidebar.title("Paramètres spécifiques au Train")

    costs["train"]["bordeaux_train"] = st.sidebar.number_input("Coût billet Bordeaux-Paris", value=costs["train"]["bordeaux_train"])
    costs["train"]["nantes_train"] = st.sidebar.number_input("Coût billet Nantes-Paris", value=costs["train"]["nantes_train"])
    costs["train"]["rer_paris_disney"] = st.sidebar.number_input("Coût RER Paris-Disney", value=costs["train"]["rer_paris_disney"])
    costs["train"]["rer_airbnb_disney"] = st.sidebar.number_input("Coût RER Airbnb-Disney", value=costs["train"]["rer_airbnb_disney"], disabled=airbnb_proche_disney)
    costs["train"]["baggage"] = st.sidebar.number_input("Coût bagagerie", value=costs["train"]["baggage"])

    baggage_days = st.sidebar.slider("Nombre de jours d'utilisation de la bagagerie", min_value=0, max_value=2, value=1)

    total_transport = (
        (costs["train"]["bordeaux_train"] * num_bordeaux_train) +
        (costs["train"]["nantes_train"] * num_nantes_train) +
        (costs["train"]["rer_paris_disney"] * 2 * total_rer_paris_disney_participants) +
        (costs["train"]["rer_airbnb_disney"] * days * total_rer_airbnb_disney_participants) +
        (costs["train"]["baggage"] * participants * baggage_days)
    )

# Options communes
st.sidebar.title("Paramètres communs")
costs["common"]["disney"] = st.sidebar.number_input("Coût Disney", value=costs["common"]["disney"])
costs["common"]["food"] = st.sidebar.number_input("Coût nourriture", value=costs["common"]["food"])

total_disney = costs["common"]["disney"] * participants
total_food = costs["common"]["food"] * days * participants

# Total final
# Les coûts totaux sont répartis sur le nombre de participants moins 1 si l'option cadeau est activée
repartition_count = participants - 1 if st.checkbox("Activer l'option cadeau d'anniversaire") else participants

# Calcul des totaux
total_cost = total_transport + total_lodging + total_disney + total_food
cost_per_person = total_cost / repartition_count

# Fonction pour générer le contenu HTML
def generate_html_report():
    html_content = f"""
    <html>
    <head><title>Résumé des coûts - Disneyland</title></head>
    <body>
        <h1>Résumé des coûts pour le voyage à Disneyland</h1>
        <h2>Détails des coûts par catégorie</h2>

        <h3>Transport ({transport_type})</h3>
        <ul>
            <li><strong>Coût total :</strong> {total_transport} €</li>
    """
    if transport_type == "Minibus":
        html_content += f"""
            <li>Location du minibus : {costs['minibus']['location']} €</li>
            <li>Carburant : {costs['minibus']['fuel']} €</li>
            <li>Péages : {costs['minibus']['toll']} €</li>
            <li>Parking (pour {days} jours) : {costs['minibus']['parking'] * days} €</li>
            <li>Train pour Sarah : {costs['minibus']['sarah_train']} €</li>
        """
    elif transport_type == "Train":
        html_content += f"""
            <li>Billets Bordeaux-Paris (pour {num_bordeaux_train} participants) : {costs['train']['bordeaux_train'] * num_bordeaux_train} €</li>
            <li>Billets Nantes-Paris (pour {num_nantes_train} participants) : {costs['train']['nantes_train'] * num_nantes_train} €</li>
            <li>RER Paris-Disney (pour {total_rer_paris_disney_participants} participants) : {costs['train']['rer_paris_disney'] * 2 * total_rer_paris_disney_participants} €</li>
            <li>RER Airbnb-Disney (pour {total_rer_airbnb_disney_participants} participants sur {days} jours) : {costs['train']['rer_airbnb_disney'] * total_rer_airbnb_disney_participants * days} €</li>
            <li>Bagagerie (pour {participants} participants sur {baggage_days} jours) : {costs['train']['baggage'] * participants * baggage_days} €</li>
        """

    html_content += f"""
        </ul>

        <h3>Hébergement</h3>
        <ul>
            <li><strong>Coût total :</strong> {total_lodging} €</li>
            <li>Coût par nuit et par participant : {costs['common']['lodging_per_night']} €</li>
        </ul>

        <h3>Billets Disney</h3>
        <ul>
            <li><strong>Coût total :</strong> {total_disney} €</li>
            <li>Coût par participant : {costs['common']['disney']} €</li>
        </ul>

        <h3>Nourriture</h3>
        <ul>
            <li><strong>Coût total :</strong> {total_food} €</li>
            <li>Coût par jour et par participant : {costs['common']['food']} €</li>
        </ul>

        <h2>Résumé final</h2>
        <ul>
            <li><strong>Coût total :</strong> {total_cost} €</li>
            <li><strong>Coût par personne :</strong> {cost_per_person:.2f} € (réparti sur {repartition_count} participants)</li>
        </ul>
    </body>
    </html>
    """
    return html_content

# Affichage des résultats
st.header("Résumé des coûts")
st.markdown(f"### **Coût total pour {transport_type} :** {total_cost} €")
st.markdown(f"### **Coût par personne (réparti sur {repartition_count}) :** {cost_per_person:.2f} €")

# Affichage convivial des détails
st.subheader("Détail des coûts")
st.markdown(f"- **Transport total :** {total_transport} €")
st.markdown(f"- **Hébergement :** {total_lodging} € (à raison de {costs['common']['lodging_per_night']} € par nuit par participant)")
st.markdown(f"- **Billets Disney :** {total_disney} €")
st.markdown(f"- **Nourriture :** {total_food} € (à raison de {costs['common']['food']} € par jour par participant)")

# Génération de la page HTML
if st.button("Générer le résumé HTML"):
    html_report = generate_html_report()
    b64_html = base64.b64encode(html_report.encode()).decode()
    href = f'<a href="data:text/html;base64,{b64_html}" download="disney_trip_summary.html" target="_blank">Télécharger ou ouvrir le résumé HTML</a>'
    st.markdown(href, unsafe_allow_html=True)
