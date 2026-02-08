# ✅ Deployment Checklist

Użyj tej checklisty przed i podczas deploymentu do Digital Ocean.


📋 **Przed deploymentem**


1. Weryfikacja plików
- [ ] `app.py` - aplikacja główna
- [ ] `requirements.txt` - wszystkie zależności
- [ ] `.gitignore` - zawiera `.env`
- [ ] `README.md` - dokumentacja
- [ ] `.streamlit/config.toml` - konfiguracja Streamlit
- [ ] `Procfile` - instrukcje uruchomienia
- [ ] Model ML (`.pkl`) - jeśli jest potrzebny


2. Sprawdzenie bezpieczeństwa
- [ ] Plik `.env` jest w `.gitignore`
- [ ] Uruchom: `git status` - upewnij się, że `.env` NIE jest na liście
- [ ] Brak hardcoded API keys w kodzie
- [ ] Brak haseł w kodzie


3. Test lokalny
- [ ] Aplikacja działa lokalnie: `streamlit run app.py`
- [ ] Predykcja działa
- [ ] Chatbot działa
- [ ] Wizualizacje działają
- [ ] Brak błędów w konsoli


🐙 **GitHub**


4. Przygotowanie repozytorium
- [ ] Utworzono nowe repo na GitHub
- [ ] Nazwa: `halfmarathon-assistant` (lub inna)
- [ ] Public lub Private (wybrane)


5. Push do GitHub
```bash
git init
git add .
git status 
git commit -m "Initial commit - Halfmarathon Assistant"
git remote add origin https://github.com/TWOJA_NAZWA/halfmarathon-assistant.git
git branch -M main
git push -u origin main
```


- [ ] Kod jest na GitHub
- [ ] Sprawdź na GitHub - plik `.env` NIE jest widoczny
- [ ] Wszystkie inne pliki są widoczne


☁️ **Digital Ocean**


6. Utworzenie aplikacji
- [ ] Zalogowano do Digital Ocean
- [ ] Kliknięto: Create → Apps
- [ ] Wybrano GitHub jako źródło
- [ ] Autoryzowano Digital Ocean
- [ ] Wybrano repozytorium: `halfmarathon-assistant`
- [ ] Wybrano branch: `main`


7. Konfiguracja
- [ ] Typ: Web Service
- [ ] Run Command: `streamlit run app.py --server.port=8080 --server.address=0.0.0.0`
- [ ] HTTP Port: `8080`


8. Environment Variables (OPCJONALNIE - tylko dla Langfuse)
Jeśli używasz Langfuse:
- [ ] `LANGFUSE_PUBLIC_KEY` 
- [ ] `LANGFUSE_SECRET_KEY` 
- [ ] `LANGFUSE_HOST` 


9. Plan i region
- [ ] Wybrano plan: Basic ($5/miesiąc) - zalecane
- [ ] Wybrano region: Frankfurt (lub najbliższy)
- [ ] Nazwa aplikacji: (zostaw domyślną lub zmień)


10. Launch
- [ ] Kliknięto: "Create Resources"
- [ ] Czekaj 5 minut na deployment


**Po deploymencie**


11. Weryfikacja
- [ ] Status: "Deployed" (zielony)
- [ ] Sprawdź Runtime Logs - brak błędów
- [ ] Kliknij "Live App" - aplikacja się otwiera
- [ ] Wprowadź klucz API OpenAI
- [ ] Test predykcji - działa
- [ ] Test chatbota - działa
- [ ] Test wizualizacji - działa


12. Monitoring
- [ ] Sprawdź Runtime Logs - komunikaty o starcie
- [ ] Sprawdź Metrics - użycie CPU/RAM
- [ ] Jeśli Langfuse: sprawdź czy logi się pojawiają


🎉 Gotowe!


- [ ] Aplikacja działa publicznie


🔄 **Aktualizacje**


Przy każdej zmianie w kodzie:
```bash
git add .
git commit -m "Opis zmian"
git push origin main
```

- [ ] Digital Ocean automatycznie wykryje zmiany
- [ ] Poczekaj 2-5 minut na re-deploy
- [ ] Sprawdź czy zmiany są widoczne


**Troubleshooting**


Jeśli coś nie działa:
- [ ] Sprawdź Runtime Logs w Digital Ocean
- [ ] Sprawdź czy Run Command jest poprawny
- [ ] Sprawdź czy wszystkie pakiety są w `requirements.txt`
- [ ] Sprawdź czy zmienne środowiskowe są ustawione
- [ ] Zobacz `DEPLOYMENT_GUIDE.md` dla szczegółów


**Pomoc**


Dokumentacja:
- `README.md` - ogólna dokumentacja
- `DEPLOYMENT_GUIDE.md` - szczegółowy przewodnik

