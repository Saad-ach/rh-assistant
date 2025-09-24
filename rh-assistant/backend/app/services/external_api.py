"""
Service d'API externe pour enrichir les réponses RH avec des données contextuelles
Utilise des APIs gratuites et des données simulées pour le développement
"""

import asyncio
import aiohttp
from datetime import datetime, timedelta
import random
from typing import Dict, List, Optional

class ExternalAPIService:
    def __init__(self):
        # Clés API gratuites (à configurer dans .env en production)
        self.weather_api_key = "demo_key"  # OpenWeatherMap free tier
        self.currency_api_key = "demo_key"  # Fixer.io free tier
        
        # Données simulées pour le développement
        self._mock_weather_data = {
            "Rabat": {"temp": 22, "description": "Ensoleillé", "humidity": 65},
            "Casablanca": {"temp": 24, "description": "Nuageux", "humidity": 70},
            "Marrakech": {"temp": 28, "description": "Dégagé", "humidity": 45},
            "Fès": {"temp": 25, "description": "Partiellement nuageux", "humidity": 55},
            "Tanger": {"temp": 23, "description": "Brouillard", "humidity": 80}
        }
        
        self._mock_holidays = [
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
        
        self._mock_currency_rates = {
            "EUR": 10.85,
            "USD": 9.95,
            "GBP": 12.45,
            "JPY": 0.067,
            "CHF": 11.20
        }

    async def get_weather_info(self, city: str = "Rabat") -> Dict:
        """Récupère les informations météo pour une ville"""
        try:
            # En production, utiliser l'API OpenWeatherMap
            if self.weather_api_key != "demo_key":
                url = f"http://api.openweathermap.org/data/2.5/weather"
                params = {
                    "q": city,
                    "appid": self.weather_api_key,
                    "units": "metric",
                    "lang": "fr"
                }
                
                async with aiohttp.ClientSession() as session:
                    async with session.get(url, params=params) as response:
                        if response.status == 200:
                            data = await response.json()
                            return {
                                "city": city,
                                "temperature": round(data["main"]["temp"]),
                                "description": data["weather"][0]["description"],
                                "humidity": data["main"]["humidity"],
                                "wind_speed": data["wind"]["speed"]
                            }
            
            # Fallback vers les données simulées
            if city in self._mock_weather_data:
                weather = self._mock_weather_data[city]
                return {
                    "city": city,
                    "temperature": weather["temp"],
                    "description": weather["description"],
                    "humidity": weather["humidity"],
                    "wind_speed": random.uniform(5, 15)
                }
            
            # Ville par défaut
            default_weather = self._mock_weather_data["Rabat"]
            return {
                "city": "Rabat",
                "temperature": default_weather["temp"],
                "description": default_weather["description"],
                "humidity": default_weather["humidity"],
                "wind_speed": random.uniform(5, 15)
            }
            
        except Exception as e:
            # En cas d'erreur, retourner des données par défaut
            return {
                "city": "Rabat",
                "temperature": 22,
                "description": "Données non disponibles",
                "humidity": 65,
                "wind_speed": 10
            }

    async def get_moroccan_holidays(self) -> List[Dict]:
        """Récupère les jours fériés marocains"""
        try:
            # En production, utiliser une API de jours fériés
            # Pour l'instant, utiliser les données simulées
            current_date = datetime.now()
            upcoming_holidays = []
            
            for holiday in self._mock_holidays:
                holiday_date = datetime.strptime(holiday["date"], "%Y-%m-%d")
                if holiday_date >= current_date:
                    upcoming_holidays.append(holiday)
            
            # Trier par date
            upcoming_holidays.sort(key=lambda x: x["date"])
            
            return upcoming_holidays[:5]  # Retourner les 5 prochains
            
        except Exception as e:
            return []

    async def get_currency_rates(self) -> Dict:
        """Récupère les taux de change MAD"""
        try:
            # En production, utiliser l'API Fixer.io
            if self.currency_api_key != "demo_key":
                url = f"http://data.fixer.io/api/latest"
                params = {
                    "access_key": self.currency_api_key,
                    "base": "MAD",
                    "symbols": "EUR,USD,GBP,JPY,CHF"
                }
                
                async with aiohttp.ClientSession() as session:
                    async with session.get(url, params=params) as response:
                        if response.status == 200:
                            data = await response.json()
                            if data["success"]:
                                return {
                                    "base": "MAD",
                                    "date": data["date"],
                                    "rates": data["rates"]
                                }
            
            # Fallback vers les données simulées
            return {
                "base": "MAD",
                "date": datetime.now().strftime("%Y-%m-%d"),
                "rates": self._mock_currency_rates.copy()
            }
            
        except Exception as e:
            return {
                "base": "MAD",
                "date": datetime.now().strftime("%Y-%m-%d"),
                "rates": self._mock_currency_rates.copy()
            }

    async def get_hr_context(self, query: str) -> Dict:
        """Analyse la requête et récupère le contexte externe pertinent"""
        context = {}
        query_lower = query.lower()
        
        # Météo pour les questions liées aux événements, congés, etc.
        if any(word in query_lower for word in ["événement", "congé", "sortie", "météo", "temps"]):
            context["weather"] = await self.get_weather_info()
        
        # Jours fériés pour les questions de congés
        if any(word in query_lower for word in ["congé", "férié", "vacance", "repos", "jour"]):
            context["holidays"] = await self.get_moroccan_holidays()
        
        # Taux de change pour les questions de salaire, pension, etc.
        if any(word in query_lower for word in ["salaire", "pension", "rémunération", "euro", "dollar", "devise"]):
            context["currency"] = await self.get_currency_rates()
        
        # Informations de trafic pour les questions de transport
        if any(word in query_lower for word in ["transport", "trafic", "déplacement", "route"]):
            context["traffic"] = {
                "status": "Fluide",
                "update_time": datetime.now().strftime("%H:%M"),
                "main_routes": ["A1: Rabat-Casablanca", "A2: Rabat-Fès", "A3: Rabat-Tanger"]
            }
        
        # Informations économiques générales
        if any(word in query_lower for word in ["économie", "inflation", "croissance", "marché"]):
            context["economy"] = {
                "inflation": "2.1%",
                "growth": "3.2%",
                "unemployment": "11.8%",
                "update_date": "2024"
            }
        
        return context

    async def get_news_summary(self, category: str = "general") -> List[Dict]:
        """Récupère un résumé des actualités (simulé pour le développement)"""
        mock_news = {
            "general": [
                {"title": "Nouvelle politique RH CDG", "summary": "Mise à jour des procédures de formation continue", "date": "2024-01-15"},
                {"title": "Amélioration des avantages sociaux", "summary": "Extension de la couverture mutuelle santé", "date": "2024-01-10"}
            ],
            "economy": [
                {"title": "Croissance économique marocaine", "summary": "PIB en hausse de 3.2% en 2024", "date": "2024-01-12"},
                {"title": "Stabilité du Dirham", "summary": "Maintien du taux de change face aux devises majeures", "date": "2024-01-08"}
            ]
        }
        
        return mock_news.get(category, mock_news["general"])

# Instance globale du service
external_api_service = ExternalAPIService()
