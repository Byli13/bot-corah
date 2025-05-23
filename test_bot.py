#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script de test pour CorahBot
"""

from corahbot.main import CorahBot
from corahbot.logger import get_logger

log = get_logger("TestBot")

def main():
    """
    Fonction principale pour tester le bot
    """
    try:
        # Créer et démarrer le bot
        log.info("Démarrage du test du bot...")
        bot = CorahBot()
        bot.start()
        
    except KeyboardInterrupt:
        log.info("Test interrompu par l'utilisateur")
    except Exception as e:
        log.exception(f"Erreur pendant le test: {str(e)}")

if __name__ == "__main__":
    main()
