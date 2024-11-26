# Notitie- en Examengenerator met Flask en Jinja

Dit is een Flask-toepassing met Jinja-sjablonen die gebruikers in staat stelt notities te maken, bewerken en verwijderen. Daarnaast kan de applicatie ChatGPT gebruiken om examenvragen en antwoorden te genereren op basis van de gemaakte notities.

## Inhoudsopgave

- [Installatie](#installatie)
- [Gebruik](#gebruik)

## Installatie

1. Clone deze repository naar je lokale machine.
   ```bash
   git clone https://github.com/Rac-Software-Development/wp2-2023-mvc-1c-racy.git
   cd notitie-generator
   ```
2. Maak een virtuele omgeving en activeer deze.
```bash
python -m venv venv
source venv/bin/activate  
# Voor Windows: venv\Scripts\activate
```

3. Installeer de vereiste afhankelijkheden.
```bash
pip install -r requirements.txt
```
4. Voeg je eigen ChatGPT API-Key toe.
```bash
cp .env.example .env
```
Plaats jouw key in de .env file

5. Run Flask.
```bash
python .\server.py
```


## Gebruik
Navigeer naar http://localhost:8001 in je webbrowser om te gebuiken.