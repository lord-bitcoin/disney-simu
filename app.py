import streamlit as st
import base64

# Titre et description
st.title(Train)", value=costs["minibus"]["fuel"])
    costs["minibus"]["toll"] = st.sidebar.number_input("Coût péages (Minibus, 90€)", value=costs["minibus"]["toll"])
    costs["minibus"]["parking"] = st.sidebar.number_input("Coût parking (par jour, Minibus, 20€)", value=costs["minibus"]["parking"])
    costs["minibus"]["sarah_train"] = st.sidebar.number_input("Coût train pour Sarah (Minibus, 80€)", value=costs["minibus"]["sarah_train"])

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

    costs["train"]["bordeaux_train"] = st.sidebar.number_input("Coût billet Bordeaux-Paris (94€)", value=costs["train"]["bordeaux_train"])
    costs["train"]["nantes_train"] = st.sidebar.number_input("Coût billet Nantes-Paris (80€)", value=costs["train"]["nantes_train"])
    costs["train"]["rer_paris_disney"] = st.sidebar.number_input("Coût RER Paris-Disney (10€)", value=costs["train"]["rer_paris_disney"])
    costs["train"]["rer_airbnb_disney"] = st.sidebar.number_input("Coût RER Airbnb-Disney (8€)", value=costs["train"]["rer_airbnb_disney"])
    costs["train"]["baggage"] = st.sidebar.number_input("Coût bagagerie (5€)", value=costs["train"]["baggage"])

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
costs["common"]["disney"] = st.sidebar.number_input("Coût Disney (300€)", value=costs["common"]["disney"])
costs["common"]["food"] = st.sidebar.number_input("Coût nourriture (15€)", value=costs["common"]["food"])

total_disney = costs["common"]["disney"] * participants
total_food = costs["common"]["food"] * days * participants

# Total final
# Les coûts totaux sont répartis sur le nombre de participants moins 1 si l'option cadeau est activée
repartition_count = participants - 1 if gift_option else participants

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
        <p><strong>Transport : </strong>{transport_type}</p>
        <ul>
            <li><strong>Transport total :</strong> {total_transport} €</li>
            <li><strong>Hébergement :</strong> {total_lodging} € (à raison de {costs['common']['lodging_per_night']} € par nuit par participant)</li>
            <li><strong>Billets Disney :</strong> {total_disney} €</li>
            <li><strong>Nourriture :</strong> {total_food} € (à raison de {costs['common']['food']} € par jour par participant)</li>
        </ul>
        <p><strong>Coût total :</strong> {total_cost} €</p>
        <p><strong>Coût par personne :</strong> {cost_per_person:.2f} € (réparti sur {repartition_count} participants)</p>
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
   
