"""
Données de démonstration de la Caisse de Dépôt et de Gestion (CDG) Maroc
Ces données servent de base de connaissances pour l'assistant RH
"""

CDG_FAQ = [
    {
        "question": "Quelles sont les conditions d'adhésion à la CDG ?",
        "answer": "L'adhésion à la CDG est obligatoire pour tous les fonctionnaires et agents de l'État marocain. Les conditions principales sont : être de nationalité marocaine, être en activité de service, et ne pas avoir atteint l'âge de la retraite.",
        "category": "adhésion",
        "confidence": 0.95
    },
    {
        "question": "Comment calculer ma pension de retraite CDG ?",
        "answer": "La pension CDG se calcule selon la formule : Pension = (Salaire de référence × Taux de liquidation × Durée d'assurance) / Durée de référence. Le taux de liquidation est de 2% par année d'assurance, avec un maximum de 80% après 40 ans de service.",
        "category": "retraite",
        "confidence": 0.90
    },
    {
        "question": "Quels sont les délais de versement de la pension ?",
        "answer": "La CDG s'engage à verser les pensions dans un délai maximum de 3 mois suivant la date de cessation d'activité. En cas de retard, des intérêts moratoires sont versés au taux légal en vigueur.",
        "category": "versement",
        "confidence": 0.85
    },
    {
        "question": "Comment effectuer une demande de pension anticipée ?",
        "answer": "La pension anticipée peut être demandée à partir de 55 ans avec au moins 30 ans d'assurance. La demande doit être déposée 6 mois avant la date souhaitée, accompagnée d'un certificat médical et d'un rapport d'expertise.",
        "category": "retraite_anticipée",
        "confidence": 0.80
    },
    {
        "question": "Quels documents pour une demande de pension d'invalidité ?",
        "answer": "Pour une pension d'invalidité, vous devez fournir : certificat médical détaillé, rapport d'expertise médicale, justificatifs de salaire, et formulaire de demande dûment rempli. Le taux d'invalidité doit être d'au moins 66,66%.",
        "category": "invalidité",
        "confidence": 0.75
    },
    {
        "question": "Quels sont les congés payés annuels ?",
        "answer": "Les fonctionnaires CDG bénéficient de 30 jours de congés payés par an. Ces congés peuvent être pris en une ou plusieurs fois, avec un minimum de 5 jours consécutifs. La planification se fait en accord avec le supérieur hiérarchique.",
        "category": "congés",
        "confidence": 0.95
    },
    {
        "question": "Comment fonctionne la mutuelle santé CDG ?",
        "answer": "La mutuelle santé CDG couvre 80% des frais médicaux, hospitaliers et pharmaceutiques. La cotisation est de 2% du salaire brut. Les ayants droit (conjoint et enfants) sont également couverts gratuitement.",
        "category": "santé",
        "confidence": 0.90
    },
    {
        "question": "Quels sont les avantages sociaux ?",
        "answer": "Les avantages sociaux CDG incluent : transport (remboursement 50% abonnement), restaurant d'entreprise (tarif préférentiel), colonies de vacances pour enfants, et prêts à taux préférentiels pour logement et véhicule.",
        "category": "avantages",
        "confidence": 0.85
    }
]

CDG_POLICIES = [
    {
        "title": "Politique de cotisation CDG",
        "content": """
        TAUX DE COTISATION :
        - Employé : 14% du salaire brut
        - Employeur : 28% du salaire brut
        - Total : 42% du salaire brut
        
        ASSIETTE DE COTISATION :
        - Salaire de base
        - Indemnités permanentes
        - Primes de rendement
        - Exclut : indemnités de déplacement, primes exceptionnelles
        
        MODALITÉS DE PAIEMENT :
        - Versement mensuel obligatoire
        - Délai : avant le 15 du mois suivant
        - Sanctions en cas de retard : majoration de 10%
        """,
        "category": "cotisation",
        "source": "CDG_Maroc"
    },
    {
        "title": "Procédure de liquidation de pension",
        "content": """
        ÉTAPES DE LA LIQUIDATION :
        1. Demande de liquidation (6 mois avant départ)
        2. Vérification des droits et durée d'assurance
        3. Calcul de la pension par l'actuaire
        4. Notification du montant au bénéficiaire
        5. Mise en paiement dans les 3 mois
        
        DOCUMENTS REQUIS :
        - Demande de liquidation signée
        - Extrait d'acte de naissance
        - Certificat de travail
        - Justificatifs de salaire (3 dernières années)
        - Photocopie CNI
        """,
        "category": "liquidation",
        "source": "CDG_Maroc"
    },
    {
        "title": "Règles de cumul emploi-retraite",
        "content": """
        CUMUL AUTORISÉ :
        - Pension CDG + activité libérale (plafond 50% du salaire d'activité)
        - Pension CDG + enseignement privé (plafond 30% du salaire d'activité)
        - Pension CDG + consultation (plafond 40% du salaire d'activité)
        
        CUMUL INTERDIT :
        - Pension CDG + fonction publique
        - Pension CDG + poste électif rémunéré
        
        DÉCLARATION OBLIGATOIRE :
        - Toute activité lucrative doit être déclarée
        - Délai : 30 jours après reprise d'activité
        - Sanction : suspension de pension en cas de non-déclaration
        """,
        "category": "cumul",
        "source": "CDG_Maroc"
    },
    {
        "title": "Politique de formation continue",
        "content": """
        BUDGET FORMATION :
        - 3% de la masse salariale annuelle
        - 5 jours de formation obligatoire par an
        - Prise en charge 100% des frais de formation
        
        TYPES DE FORMATIONS :
        - Formations techniques et métier
        - Formations en management et leadership
        - Formations en langues étrangères
        - Certifications professionnelles reconnues
        
        PROCÉDURE DE DEMANDE :
        1. Évaluation des besoins avec le manager
        2. Soumission de la demande via l'intranet
        3. Validation par le service formation
        4. Planification et participation
        5. Évaluation post-formation obligatoire
        """,
        "category": "formation",
        "source": "CDG_Maroc"
    },
    {
        "title": "Gestion des congés et absences",
        "content": """
        CONGÉS PAYÉS :
        - 30 jours ouvrables par an
        - Planification en accord avec le manager
        - Délai de préavis : 15 jours minimum
        
        CONGÉS DE MALADIE :
        - Certificat médical obligatoire
        - Paiement intégral pendant 3 mois
        - Visite médicale de contrôle après 1 mois
        
        CONGÉS EXCEPTIONNELS :
        - Mariage : 4 jours
        - Naissance : 3 jours
        - Décès parent : 3 jours
        - Déménagement : 1 jour
        
        ABSENCES AUTORISÉES :
        - Rendez-vous médicaux (avec justificatif)
        - Formation professionnelle
        - Syndicalisme (droit de retrait)
        """,
        "category": "congés",
        "source": "CDG_Maroc"
    }
]

CDG_PROCEDURES = [
    {
        "title": "Changement d'adresse",
        "procedure": [
            "Remplir le formulaire de changement d'adresse",
            "Joindre une copie de la nouvelle pièce d'identité",
            "Envoyer par recommandé avec AR",
            "Confirmation sous 15 jours ouvrés"
        ],
        "category": "administratif"
    },
    {
        "title": "Demande de relevé de carrière",
        "procedure": [
            "Formulaire de demande signé",
            "Copie de la pièce d'identité",
            "Délai de traitement : 30 jours",
            "Envoi par courrier recommandé"
        ],
        "category": "administratif"
    },
    {
        "title": "Rectification d'erreur administrative",
        "procedure": [
            "Lettre de réclamation motivée",
            "Justificatifs à l'appui",
            "Délai de réponse : 45 jours",
            "Possibilité de recours gracieux"
        ],
        "category": "contentieux"
    },
    {
        "title": "Demande de prêt social",
        "procedure": [
            "Formulaire de demande de prêt",
            "Justificatifs de revenus (3 derniers bulletins)",
            "Attestation de travail",
            "Étude de dossier sous 30 jours",
            "Décision notifiée par courrier"
        ],
        "category": "prêts"
    },
    {
        "title": "Inscription aux colonies de vacances",
        "procedure": [
            "Formulaire d'inscription enfant",
            "Certificat de scolarité",
            "Justificatif de revenus",
            "Délai : 2 mois avant le séjour",
            "Tarification selon quotient familial"
        ],
        "category": "avantages_sociaux"
    }
]

CDG_HOLIDAYS = [
    {"date": "2024-01-01", "name": "Nouvel An", "type": "national"},
    {"date": "2024-01-11", "name": "Manifeste de l'Indépendance", "type": "national"},
    {"date": "2024-05-01", "name": "Fête du Travail", "type": "international"},
    {"date": "2024-07-30", "name": "Fête du Trône", "type": "national"},
    {"date": "2024-08-14", "name": "Oued Ed-Dahab", "type": "national"},
    {"date": "2024-08-20", "name": "Révolution du Roi et du Peuple", "type": "national"},
    {"date": "2024-08-21", "name": "Fête de la Jeunesse", "type": "national"},
    {"date": "2024-11-06", "name": "Marche Verte", "type": "national"},
    {"date": "2024-11-18", "name": "Fête de l'Indépendance", "type": "national"}
]

def get_cdg_knowledge_base():
    """Retourne la base de connaissances CDG complète"""
    return {
        "faq": CDG_FAQ,
        "policies": CDG_POLICIES,
        "procedures": CDG_PROCEDURES,
        "holidays": CDG_HOLIDAYS
    }

def search_cdg_content(query, category=None):
    """Recherche dans le contenu CDG"""
    results = []
    query_lower = query.lower()
    
    # Recherche dans FAQ
    for item in CDG_FAQ:
        if category and item.get("category") != category:
            continue
        if (query_lower in item["question"].lower() or 
            query_lower in item["answer"].lower()):
            results.append({
                "type": "faq",
                "content": item,
                "relevance": 0.9
            })
    
    # Recherche dans politiques
    for item in CDG_POLICIES:
        if category and item.get("category") != category:
            continue
        if query_lower in item["title"].lower() or query_lower in item["content"].lower():
            results.append({
                "type": "policy",
                "content": item,
                "relevance": 0.8
            })
    
    # Recherche dans procédures
    for item in CDG_PROCEDURES:
        if category and item.get("category") != category:
            continue
        if query_lower in item["title"].lower() or any(query_lower in step.lower() for step in item["procedure"]):
            results.append({
                "type": "procedure",
                "content": item,
                "relevance": 0.7
            })
    
    # Recherche dans jours fériés
    for item in CDG_HOLIDAYS:
        if query_lower in item["name"].lower() or "férié" in query_lower or "congé" in query_lower:
            results.append({
                "type": "holiday",
                "content": item,
                "relevance": 0.8
            })
    
    return results
