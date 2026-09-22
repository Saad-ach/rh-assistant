"""Synthetic EUBIA HR corpus for local RAG development and evaluation.

All names, dates, amounts and policies in this module are fictional.
They must not be used as real EUBIA policy.
"""

DEMO_DOCUMENTS = [
    {
        "filename": "DEMO_EUBIA_FAQ_RH_FR_DE.txt",
        "category": "faq",
        "language": "fr-de",
        "content": """FAQ DE DEMONSTRATION - ASSISTANT RH EUBIA

Règlement intérieur:
Le règlement intérieur et les procédures internes sont disponibles dans
l'espace documentaire RH du portail EUBIA. Si le document n'est pas visible,
le collaborateur contacte HR ou son manager afin de recevoir la version en
vigueur. Cette réponse est une règle fictive de démonstration.

Congés payés:
La politique fictive de démonstration prévoit 30 jours ouvrés par année.
La demande est saisie dans le portail RH au moins dix jours ouvrés avant le
début de l'absence. Le manager répond sous cinq jours ouvrés.

Frais professionnels:
Une dépense est saisie dans le portail RH avec son justificatif dans les
trente jours. Le manager effectue la première vérification, puis HR réalise
le contrôle final.

Formation:
Une demande de formation indique l'objectif, la durée et le lien avec le
poste. Le manager donne son avis, puis HR confirme la prise en charge.

Télétravail:
Les jours souhaités sont saisis dans le calendrier partagé. Le manager vérifie
la continuité du service et valide ou refuse la demande.

Paie:
Les questions de paie sont déposées dans le portail RH. HR les examine dans
un délai fictif de trois jours ouvrés.

Maladie ou absence urgente:
Un arrêt maladie est signalé au manager le premier jour. Une absence urgente
doit être signalée directement au manager puis régularisée dans le portail RH.

Diese Angaben sind ausschließlich synthetische Testdaten und keine verbindliche
EUBIA-Richtlinie.""",
    },
    {
        "filename": "DEMO_EUBIA_Arbeitszeit_und_Hybridarbeit_DE.txt",
        "category": "policies",
        "language": "de",
        "content": """DEMO-DOKUMENT - FIKTIVE EUBIA-RICHTLINIE
Arbeitszeit und Hybridarbeit, Version 1.0

Die reguläre Wochenarbeitszeit beträgt 38,5 Stunden. Mitarbeitende können
bis zu zwei mobile Arbeitstage pro Woche vereinbaren. Der Teamleiter bestätigt
den Monatsplan bis zum fünften Arbeitstag. Kernzeit ist Montag bis Donnerstag
von 09:30 bis 15:30 Uhr. Ausnahmen müssen schriftlich mit HR abgestimmt werden.
Diese Regel ist ausschließlich für Tests des EUBIA HR Assistant erstellt.""",
    },
    {
        "filename": "DEMO_EUBIA_Congés_et_absences_FR.txt",
        "category": "leave",
        "language": "fr",
        "content": """DOCUMENT DE DEMONSTRATION - REGLE EUBIA FICTIVE
Congés et absences, version 1.0

Chaque collaborateur dispose de 30 jours ouvrés de congés annuels fictifs.
La demande est envoyée dans le portail RH au moins dix jours ouvrés avant
le premier jour d'absence. Le responsable répond sous cinq jours ouvrés.
Un arrêt maladie doit être signalé au manager le premier jour et transmis
à HR selon la procédure interne. Ces chiffres sont inventés pour les tests.""",
    },
    {
        "filename": "DEMO_EUBIA_Onboarding_DE_FR.txt",
        "category": "onboarding",
        "language": "de-fr",
        "content": """DOCUMENT DE DEMONSTRATION - ONBOARDING EUBIA FICTIF

Am ersten Arbeitstag erhält die neue Person den Zugang zum portail RH, une
adresse e-mail et une session de sécurité. La première semaine comprend un
entretien avec le manager, une présentation de l'équipe et une formation
sur la protection des données. HR clôture la checklist après réception des
documents signés. Aucun nom réel ni document légal réel n'est utilisé ici.""",
    },
    {
        "filename": "DEMO_EUBIA_Teletravail_FR.txt",
        "category": "procedures",
        "language": "fr",
        "content": """DOCUMENT DE DEMONSTRATION - PROCEDURE TELETRAVAIL EUBIA

Le collaborateur saisit les jours souhaités dans le calendrier partagé.
Le manager vérifie la continuité du service et valide ou refuse la demande.
En cas de refus, une justification est enregistrée. Le matériel professionnel
reste sous la responsabilité du collaborateur et tout incident est signalé
au support le jour même. Politique entièrement fictive.""",
    },
    {
        "filename": "DEMO_EUBIA_Paie_DE.txt",
        "category": "payroll",
        "language": "de",
        "content": """DEMO-DOKUMENT - FIKTIVE EUBIA-LOHNPROZESS

Die monatliche Abrechnung wird am 25. Kalendertag vorbereitet und am letzten
Bankarbeitstag ausgezahlt. Fragen zur Abrechnung werden über das HR-Portal
eingereicht. HR prüft die Anfrage innerhalb von drei Arbeitstagen. Die hier
genannten Termine und Prozesse sind ausschließlich synthetische Testdaten.""",
    },
    {
        "filename": "DEMO_EUBIA_Formation_FR.txt",
        "category": "training",
        "language": "fr",
        "content": """DOCUMENT DE DEMONSTRATION - FORMATION EUBIA FICTIVE

Un budget de formation fictif de 1 200 euros par collaborateur est prévu
chaque année. La demande décrit l'objectif, la durée et le lien avec le poste.
Le manager donne un avis, puis HR confirme la prise en charge. Les formations
linguistiques allemand-français sont prioritaires dans cet exemple.""",
    },
    {
        "filename": "DEMO_EUBIA_Datenschutz_DE_FR.txt",
        "category": "policies",
        "language": "de-fr",
        "content": """DEMO-DOKUMENT - FIKTIVE DATENSCHUTZREGEL EUBIA

Personaldokumente dürfen nur im geschützten HR-Bereich gespeichert werden.
Les documents RH ne doivent pas être envoyés dans des chats publics ou des
espaces personnels. Der Zugriff wird nach Rolle vergeben und regelmäßig
überprüft. Bei einem Verdacht auf Offenlegung muss HR sofort informiert werden.
Diese Regel ist eine synthetische Schulungsgrundlage.""",
    },
    {
        "filename": "DEMO_EUBIA_Recrutement_FR.txt",
        "category": "recruitment",
        "language": "fr",
        "content": """DOCUMENT DE DEMONSTRATION - RECRUTEMENT EUBIA FICTIF

Les candidatures sont déposées sur le portail recrutement. HR vérifie les
informations de base, puis le manager organise un entretien. Une réponse est
normalement envoyée sous dix jours ouvrés. Les critères de sélection sont liés
aux compétences du poste et à la maîtrise de l'allemand professionnel lorsque
cela est nécessaire.""",
    },
    {
        "filename": "DEMO_EUBIA_Contrat_DE.txt",
        "category": "contracts",
        "language": "de",
        "content": """DEMO-DOKUMENT - FIKTIVER ARBEITSVERTRAG EUBIA

Der Arbeitsvertrag wird vor dem ersten Arbeitstag digital bereitgestellt.
Änderungen der Bankverbindung oder der persönlichen Daten werden über das
geschützte HR-Portal gemeldet. Vertragsfragen werden von HR beantwortet und
nicht über private Messenger geteilt.""",
    },
    {
        "filename": "DEMO_EUBIA_Absence_DE_FR.txt",
        "category": "leave",
        "language": "de-fr",
        "content": """DEMO-DOKUMENT - ABSENCES EUBIA, PROCEDURE FICTIVE

Bei einer Verspätung informiert die Person den Manager so früh wie möglich.
Pour une absence planifiée, la demande passe par le portail RH. En cas
d'urgence, le manager peut être contacté directement, puis la demande est
regularisée dans le portail dès que possible.""",
    },
    {
        "filename": "DEMO_EUBIA_Frais_FR.txt",
        "category": "expenses",
        "language": "fr",
        "content": """DOCUMENT DE DEMONSTRATION - FRAIS PROFESSIONNELS EUBIA

Les frais professionnels sont saisis dans le portail RH avec le justificatif
dans les trente jours. Le manager vérifie la dépense et HR effectue le contrôle
final. Les demandes incomplètes sont renvoyées pour correction.""",
    },
    {
        "filename": "DEMO_EUBIA_Securite_DE_FR.txt",
        "category": "security",
        "language": "de-fr",
        "content": """DEMO-DOKUMENT - SICHERHEIT UND IT-ZUGANG EUBIA

Passwörter werden nicht weitergegeben und müssen im geschützten Passwortmanager
gespeichert werden. En cas de perte d'un appareil ou de suspicion de phishing,
le support IT et HR sont informés immédiatement. Les accès sont retirés lors
du départ après confirmation de HR.""",
    },
    {
        "filename": "DEMO_EUBIA_Entretien_FR.txt",
        "category": "performance",
        "language": "fr",
        "content": """DOCUMENT DE DEMONSTRATION - ENTRETIENS EUBIA FICTIFS

Un entretien de suivi est organisé chaque trimestre entre le collaborateur et
son manager. Les objectifs sont enregistrés dans l'espace RH. Le collaborateur
peut demander un entretien supplémentaire à HR s'il souhaite clarifier ses
objectifs ou son parcours de développement.""",
    },
    {
        "filename": "PUBLIC_DE_EUBIA_Conges_Loi_BUrlG_FR.txt",
        "category": "public-law",
        "language": "de-fr",
        "source": "https://www.gesetze-im-internet.de/burlg/",
        "content": """FICHE DE REFERENCE PUBLIQUE - ALLEMAGNE - CONGES

Cette fiche résume le Bundesurlaubsgesetz (BUrlG), à vérifier avec HR avant
toute décision individuelle. Le congé légal est d'au moins 24 Werktage par
année avec une semaine de six jours comme base légale. Dans un contrat de cinq
jours, cela correspond généralement à 20 jours ouvrés. Le droit et les dates
doivent être vérifiés selon le contrat, la convention collective et la
situation de la personne. Source officielle: gesetze-im-internet.de/burlg.""",
    },
    {
        "filename": "PUBLIC_DE_EUBIA_Temps_Travail_ArbZG_FR.txt",
        "category": "public-law",
        "language": "de-fr",
        "source": "https://www.gesetze-im-internet.de/arbzg/",
        "content": """FICHE DE REFERENCE PUBLIQUE - ALLEMAGNE - TEMPS DE TRAVAIL

Cette fiche résume l'Arbeitszeitgesetz (ArbZG), sans remplacer un avis RH ou
juridique. La durée de travail quotidienne est en principe limitée à huit
heures et peut être portée à dix heures si la moyenne légale est respectée.
Les pauses et les temps de repos doivent être respectés. Les règles peuvent
avoir des exceptions selon le secteur. Source officielle:
gesetze-im-internet.de/arbzg.""",
    },
    {
        "filename": "PUBLIC_DE_EUBIA_Egalite_AGG_FR.txt",
        "category": "public-law",
        "language": "de-fr",
        "source": "https://www.gesetze-im-internet.de/agg/",
        "content": """FICHE DE REFERENCE PUBLIQUE - ALLEMAGNE - EGALITE

L'Allgemeines Gleichbehandlungsgesetz (AGG) vise à prévenir les discriminations
notamment liées à l'origine ethnique, au sexe, à la religion ou conviction, au
handicap, à l'âge et à l'identité sexuelle. Toute situation concrète doit être
signalée à HR selon la procédure interne et évaluée au cas par cas.
Source officielle: gesetze-im-internet.de/agg.""",
    },
    {
        "filename": "PUBLIC_DE_EUBIA_Salaire_Minimum_FR.txt",
        "category": "public-law",
        "language": "fr",
        "source": "https://www.bmas.de/DE/Arbeit/Arbeitsrecht/arbeitsrecht.html",
        "content": """FICHE DE REFERENCE PUBLIQUE - ALLEMAGNE - REMUNERATION

Les règles allemandes de rémunération peuvent dépendre du salaire minimum
légal, d'une convention collective et du contrat de travail. Le montant en
vigueur doit toujours être vérifié sur la source officielle du BMAS et auprès
de HR, car il peut évoluer. Cette fiche ne donne pas de montant fixe afin
d'éviter une information périmée. Source: bmas.de, rubrique Arbeitsrecht.""",
    },
    {
        "filename": "PUBLIC_DE_EUBIA_Protection_Donnees_FR.txt",
        "category": "public-law",
        "language": "de-fr",
        "source": "https://eur-lex.europa.eu/eli/reg/2016/679/oj",
        "content": """FICHE DE REFERENCE PUBLIQUE - RGPD ET DOSSIERS RH

Les données RH doivent être traitées pour une finalité déterminée, avec un
accès limité aux personnes autorisées et des mesures de sécurité adaptées.
Une demande d'accès, de correction ou un incident doit être transmis à HR ou
au responsable de la protection des données selon la procédure EUBIA.
Source publique: règlement (UE) 2016/679.""",
    },
]


DEMO_EVALUATION_QUERIES = [
    {
        "question": "Wie viele mobile Arbeitstage sind erlaubt?",
        "expected_source": "DEMO_EUBIA_Arbeitszeit_und_Hybridarbeit_DE.txt",
    },
    {
        "question": "Combien de jours de congé puis-je demander ?",
        "expected_source": "DEMO_EUBIA_Congés_et_absences_FR.txt",
    },
    {
        "question": "Wann wird das Gehalt ausgezahlt?",
        "expected_source": "DEMO_EUBIA_Paie_DE.txt",
    },
    {
        "question": "Comment demander une formation ?",
        "expected_source": "DEMO_EUBIA_Formation_FR.txt",
    },
    {
        "question": "Où puis-je trouver le règlement intérieur de l'entreprise ?",
        "expected_source": "DEMO_EUBIA_FAQ_RH_FR_DE.txt",
    },
    {
        "question": "Comment me faire rembourser des frais professionnels ?",
        "expected_source": "DEMO_EUBIA_FAQ_RH_FR_DE.txt",
    },
    {
        "question": "Comment fonctionne le télétravail ?",
        "expected_source": "DEMO_EUBIA_FAQ_RH_FR_DE.txt",
    },
]
