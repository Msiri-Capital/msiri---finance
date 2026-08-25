# api_client.py - Client API-Sports.io V3

import requests
import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
import streamlit as st
import time

class APISportsClient:
    """
    Client pour l'API API-Sports.io V3
    Documentation: https://www.api-football.com/documentation-v3
    """
    
    BASE_URL = "https://v3.football.api-sports.io"
    
    def __init__(self, api_key: str):
        """
        Initialise le client avec la clé API
        
        Args:
            api_key: Clé API obtenue sur dashboard.api-football.com
        """
        self.api_key = api_key
        self.headers = {
            "x-apisports-key": api_key
        }
        self.session = requests.Session()
        self.session.headers.update(self.headers)
        
        # Suivi des limites de taux
        self.rate_limit_remaining = None
        self.rate_limit_limit = None
        
    def _get(self, endpoint: str, params: Dict = None) -> Dict:
        """
        Effectue une requête GET vers l'API
        
        Args:
            endpoint: Point d'accès API (ex: "/fixtures")
            params: Paramètres de la requête
            
        Returns:
            Réponse JSON de l'API
        """
        url = f"{self.BASE_URL}{endpoint}"
        
        try:
            response = self.session.get(url, params=params, timeout=30)
            
            # Récupération des limites de taux
            self.rate_limit_remaining = int(response.headers.get('X-RateLimit-Remaining', 0))
            self.rate_limit_limit = int(response.headers.get('X-RateLimit-Limit', 0))
            
            if response.status_code == 429:
                st.warning("⚠️ Limite de requêtes atteinte. Attendez quelques secondes...")
                time.sleep(5)
                return self._get(endpoint, params)
                
            if response.status_code != 200:
                st.error(f"Erreur API {response.status_code}: {response.text}")
                return {"response": [], "results": 0}
                
            data = response.json()
            return data
            
        except requests.exceptions.Timeout:
            st.error("⏰ Timeout - L'API ne répond pas")
            return {"response": [], "results": 0}
        except Exception as e:
            st.error(f"❌ Erreur: {e}")
            return {"response": [], "results": 0}
    
    def get_teams_by_name(self, team_name: str, league_id: int = None) -> List[Dict]:
        """
        Recherche une équipe par son nom
        
        Args:
            team_name: Nom de l'équipe
            league_id: ID de la ligue (optionnel pour filtrer)
            
        Returns:
            Liste des équipes trouvées
        """
        params = {"search": team_name}
        if league_id:
            params["league"] = league_id
            
        data = self._get("/teams", params)
        return data.get("response", [])
    
    def get_team_id(self, team_name: str, league_id: int = None) -> Optional[int]:
        """
        Récupère l'ID d'une équipe par son nom
        
        Args:
            team_name: Nom de l'équipe
            league_id: ID de la ligue
            
        Returns:
            ID de l'équipe ou None
        """
        teams = self.get_teams_by_name(team_name, league_id)
        if teams:
            # Prendre la première correspondance
            for team in teams:
                if team_name.lower() in team['team']['name'].lower():
                    return team['team']['id']
        return None
    
    def get_fixtures_by_team(self, team_id: int, last_n: int = 3) -> List[Dict]:
        """
        Récupère les derniers matchs d'une équipe
        
        Args:
            team_id: ID de l'équipe
            last_n: Nombre de derniers matchs à récupérer
            
        Returns:
            Liste des matchs
        """
        params = {
            "team": team_id,
            "last": last_n,
            "status": "FT"  # Matchs terminés
        }
        
        data = self._get("/fixtures", params)
        return data.get("response", [])
    
    def get_fixtures_h2h(self, team1_id: int, team2_id: int, last_n: int = 5) -> List[Dict]:
        """
        Récupère l'historique des confrontations directes
        
        Args:
            team1_id: ID de l'équipe 1
            team2_id: ID de l'équipe 2
            last_n: Nombre de matchs à récupérer
            
        Returns:
            Liste des matchs
        """
        params = {
            "h2h": f"{team1_id}-{team2_id}",
            "last": last_n
        }
        
        data = self._get("/fixtures", params)
        return data.get("response", [])
    
    def get_team_stats(self, team_id: int, season: int = 2024) -> Dict:
        """
        Récupère les statistiques d'une équipe sur une saison
        
        Args:
            team_id: ID de l'équipe
            season: Saison (ex: 2024)
            
        Returns:
            Statistiques de l'équipe
        """
        # D'abord, récupérer les matchs de la saison
        params = {
            "team": team_id,
            "season": season,
            "status": "FT"
        }
        
        data = self._get("/fixtures", params)
        fixtures = data.get("response", [])
        
        # Calculer les statistiques
        stats = {
            "played": 0,
            "wins": 0,
            "draws": 0,
            "losses": 0,
            "goals_for": 0,
            "goals_against": 0,
            "clean_sheets": 0,
            "form": []
        }
        
        for match in fixtures:
            home = match["teams"]["home"]
            away = match["teams"]["away"]
            goals = match["goals"]
            
            if home["id"] == team_id:
                # Match à domicile
                stats["goals_for"] += goals["home"] or 0
                stats["goals_against"] += goals["away"] or 0
                if goals["home"] > goals["away"]:
                    stats["wins"] += 1
                    stats["form"].append("W")
                elif goals["home"] == goals["away"]:
                    stats["draws"] += 1
                    stats["form"].append("D")
                else:
                    stats["losses"] += 1
                    stats["form"].append("L")
                if goals["away"] == 0:
                    stats["clean_sheets"] += 1
            else:
                # Match à l'extérieur
                stats["goals_for"] += goals["away"] or 0
                stats["goals_against"] += goals["home"] or 0
                if goals["away"] > goals["home"]:
                    stats["wins"] += 1
                    stats["form"].append("W")
                elif goals["away"] == goals["home"]:
                    stats["draws"] += 1
                    stats["form"].append("D")
                else:
                    stats["losses"] += 1
                    stats["form"].append("L")
                if goals["home"] == 0:
                    stats["clean_sheets"] += 1
            
            stats["played"] += 1
        
        # Garder les 5 derniers résultats pour la forme
        stats["form"] = stats["form"][-5:] if stats["form"] else []
        
        # Calcul des moyennes
        if stats["played"] > 0:
            stats["avg_goals_for"] = stats["goals_for"] / stats["played"]
            stats["avg_goals_against"] = stats["goals_against"] / stats["played"]
            stats["win_rate"] = (stats["wins"] / stats["played"]) * 100
        else:
            stats["avg_goals_for"] = 0
            stats["avg_goals_against"] = 0
            stats["win_rate"] = 0
        
        return stats
    
    def search_leagues_by_name(self, name: str) -> List[Dict]:
        """
        Recherche une ligue par son nom
        
        Args:
            name: Nom de la ligue
            
        Returns:
            Liste des ligues trouvées
        """
        data = self._get("/leagues", {"search": name})
        return data.get("response", [])
    
    def get_league_id(self, name: str, season: int = 2024) -> Optional[int]:
        """
        Récupère l'ID d'une ligue par son nom
        
        Args:
            name: Nom de la ligue
            season: Saison
            
        Returns:
            ID de la ligue ou None
        """
        leagues = self.search_leagues_by_name(name)
        for league in leagues:
            if name.lower() in league["league"]["name"].lower():
                # Vérifier que la saison est disponible
                seasons = [s["season"] for s in league["seasons"]]
                if season in seasons:
                    return league["league"]["id"]
        return None
    
    def get_predictions(self, fixture_id: int) -> Dict:
        """
        Récupère les prédictions pour un match
        
        Args:
            fixture_id: ID du match
            
        Returns:
            Prédictions du match
        """
        data = self._get("/predictions", {"fixture": fixture_id})
        response = data.get("response", [])
        if response:
            return response[0]  # La première prédiction
        return {}

    def get_odds(self, fixture_id: int, bookmaker_id: int = None) -> List[Dict]:
        """
        Récupère les cotes pour un match
        
        Args:
            fixture_id: ID du match
            bookmaker_id: ID du bookmaker (optionnel)
            
        Returns:
            Cotes du match
        """
        params = {"fixture": fixture_id}
        if bookmaker_id:
            params["bookmaker"] = bookmaker_id
        
        data = self._get("/odds", params)
        return data.get("response", [])
