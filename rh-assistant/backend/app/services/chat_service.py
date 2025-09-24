import asyncio
from datetime import datetime
from typing import List, Optional, Dict
import json
import random

from app.core.config import settings
from app.data.cdg_data import search_cdg_content, get_cdg_knowledge_base
from app.services.external_api import external_api_service
from loguru import logger

class ChatService:
    def __init__(self):
        self.cdg_kb = get_cdg_knowledge_base()
        self._memory_cache: Dict[str, str] = {}

    async def get_cached_response(self, session_id: str, message: str) -> Optional[dict]:
        cache_key = f"chat:{session_id}:{message}"
        return self._memory_cache.get(cache_key)

    async def set_cached_response(self, session_id: str, message: str, response: dict):
        cache_key = f"chat:{session_id}:{message}"
        self._memory_cache[cache_key] = response

    async def process_chat_query(self, db, chat_query) -> dict:
        start_time = datetime.now()
        
        # Vérifier le cache
        cached_response = await self.get_cached_response(chat_query.session_id, chat_query.message)
        if cached_response:
            return cached_response

        # 1. Recherche dans les données CDG
        cdg_results = search_cdg_content(chat_query.message)
        
        # 2. Contexte externe (météo, jours fériés, etc.)
        external_context = await external_api_service.get_hr_context(chat_query.message)
        
        # 3. Générer une réponse enrichie
        response_data = await self._generate_rich_response(
            chat_query.message, 
            cdg_results, 
            external_context
        )
        
        # 4. Calculer le score de confiance
        confidence_score = self._calculate_confidence_score(response_data, cdg_results)
        
        # 5. Construire la réponse finale
        end_time = datetime.now()
        response_time = (end_time - start_time).total_seconds()
        
        chat_response = {
            "response": response_data["response"],
            "confidence_score": confidence_score,
            "sources": response_data["sources"],
            "requires_validation": False,  # Pas de validation pour l'instant
            "validation_status": "not_required",
            "response_time": response_time,
            "timestamp": datetime.now().isoformat(),
            "additional_info": response_data.get("additional_info", {})
        }
        
        # Mettre en cache
        await self.set_cached_response(chat_query.session_id, chat_query.message, chat_response)
        return chat_response

    async def _generate_rich_response(self, query: str, cdg_results: List, external_context: dict) -> dict:
        """Génère une réponse enrichie basée sur les données CDG et le contexte externe"""
        
        # Réponse de base
        if cdg_results:
            best_result = max(cdg_results, key=lambda x: x["relevance"])
            if best_result["type"] == "faq":
                base_response = best_result["content"]["answer"]
                sources = [f"CDG FAQ - {best_result['content']['category']}"]
            else:
                base_response = f"Selon la politique CDG '{best_result['content']['title']}':\n{best_result['content']['content'][:300]}..."
                sources = [f"CDG Policy - {best_result['content']['category']}"]
        else:
            # Réponse générique enrichie
            base_response = self._get_generic_hr_response(query)
            sources = ["Base de connaissances CDG"]
        
        # Enrichir avec le contexte externe
        additional_info = {}
        enriched_response = base_response
        
        if external_context:
            if "weather" in external_context:
                weather_info = external_context["weather"]
                additional_info["weather"] = weather_info
                if "congé" in query.lower() or "événement" in query.lower():
                    enriched_response += f"\n\n💡 **Conseil météo** : {weather_info['city']} - {weather_info['description']} ({weather_info['temperature']}°C)"
            
            if "holidays" in external_context:
                upcoming_holidays = [h for h in external_context["holidays"] if h['date'] >= datetime.now().strftime('%Y-%m-%d')][:3]
                if upcoming_holidays:
                    additional_info["holidays"] = upcoming_holidays
                    if "congé" in query.lower() or "jour férié" in query.lower():
                        enriched_response += f"\n\n📅 **Prochains jours fériés** : " + ", ".join([f"{h['name']} ({h['date']})" for h in upcoming_holidays])
            
            if "currency" in external_context:
                currency_info = external_context["currency"]
                additional_info["currency"] = currency_info
                if "salaire" in query.lower() or "pension" in query.lower():
                    enriched_response += f"\n\n💱 **Taux de change MAD** : EUR={currency_info['rates']['EUR']}, USD={currency_info['rates']['USD']}"
        
        # Ajouter des conseils contextuels
        enriched_response += self._add_contextual_tips(query, cdg_results)
        
        return {
            "response": enriched_response,
            "sources": sources,
            "additional_info": additional_info
        }

    def _get_generic_hr_response(self, query: str) -> str:
        """Génère une réponse générique basée sur le type de question"""
        query_lower = query.lower()
        
        if any(word in query_lower for word in ["congé", "vacance", "repos"]):
            return """**Gestion des congés à la CDG :**
            
📋 **Types de congés disponibles :**
• Congés annuels : 30 jours ouvrables par an
• Congés de maladie : selon certificat médical
• Congés de maternité : 14 semaines
• Congés exceptionnels : mariage, décès, etc.

⏰ **Procédure de demande :**
1. Remplir le formulaire de demande
2. Obtenir l'accord du supérieur hiérarchique
3. Soumettre au service RH
4. Confirmation sous 48h

💡 **Conseil** : Planifiez vos congés au moins 15 jours à l'avance pour les périodes de pointe."""
        
        elif any(word in query_lower for word in ["salaire", "rémunération", "paie"]):
            return """**Rémunération et salaires à la CDG :**
            
💰 **Composantes du salaire :**
• Salaire de base
• Indemnités de résidence
• Primes de rendement
• Indemnités de fonction

📊 **Calcul des cotisations :**
• Employé : 14% du salaire brut
• Employeur : 28% du salaire brut
• Total : 42% du salaire brut

📅 **Versement :** Le 25 de chaque mois
💳 **Mode de paiement :** Virement bancaire obligatoire"""
        
        elif any(word in query_lower for word in ["formation", "apprentissage", "développement"]):
            return """**Formation et développement professionnel :**
            
🎓 **Types de formations disponibles :**
• Formations techniques et métier
• Formations en management
• Formations en langues
• Certifications professionnelles

📝 **Processus de demande :**
1. Identifier le besoin de formation
2. Discuter avec votre manager
3. Soumettre la demande via l'intranet
4. Validation par le service formation
5. Planification et participation

💡 **Budget annuel :** 3% de la masse salariale dédié à la formation"""
        
        else:
            return """**Assistant RH CDG Maroc**
            
Je suis là pour vous aider avec toutes vos questions RH. Voici quelques sujets sur lesquels je peux vous informer :

📋 **Congés et absences**
💰 **Salaires et rémunération**
🎓 **Formation et développement**
🏥 **Santé et sécurité**
📊 **Retraite et pension**
📝 **Procédures administratives**

N'hésitez pas à me poser des questions spécifiques !"""

    def _add_contextual_tips(self, query: str, cdg_results: List) -> str:
        """Ajoute des conseils contextuels basés sur la question"""
        query_lower = query.lower()
        tips = []
        
        if "congé" in query_lower:
            tips.append("💡 **Conseil** : Consultez le calendrier des jours fériés pour optimiser vos congés.")
        
        if "salaire" in query_lower:
            tips.append("💡 **Conseil** : Vérifiez votre bulletin de paie mensuel pour contrôler vos cotisations.")
        
        if "formation" in query_lower:
            tips.append("💡 **Conseil** : Planifiez vos formations en début d'année pour optimiser votre budget.")
        
        if "retraite" in query_lower:
            tips.append("💡 **Conseil** : Demandez votre relevé de carrière annuellement pour vérifier vos droits.")
        
        if not tips:
            tips.append("💡 **Conseil** : Consultez régulièrement l'intranet CDG pour les dernières actualités RH.")
        
        return "\n\n" + "\n".join(tips)

    def _calculate_confidence_score(self, response_data: dict, cdg_results: List) -> float:
        """Calcule un score de confiance réaliste"""
        if cdg_results:
            # Score basé sur la pertinence des résultats CDG
            return max(result["relevance"] for result in cdg_results)
        
        # Score basé sur la qualité de la réponse
        response = response_data["response"]
        if len(response) > 200:
            return 0.85
        elif len(response) > 100:
            return 0.75
        else:
            return 0.65

chat_service = ChatService()
