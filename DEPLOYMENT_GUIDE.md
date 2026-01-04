Przewodnik dla twojego własnego Deploymentu do Digital Ocean App Platform

📋 Przygotowanie przed deploymentem

1. Sprawdź pliki w projekcie

Upewnij się, że masz następujące pliki:

- ✅ `app.py` - główna aplikacja Streamlit
- ✅ `requirements.txt` - lista zależności Python
- ✅ `.gitignore` - wykluczenie pliku `.env` z repozytorium
- ✅ `README.md` - dokumentacja projektu
- ✅ `.streamlit/config.toml` - konfiguracja Streamlit
- ✅ `Procfile` - (opcjonalnie) instrukcje uruchomienia
- ✅ Model ML (`.pkl` file) - jeśli jest lokalnie


Krok po kroku: Deployment

2. **Wypchnij kod do GitHub**
   
   # Inicjalizuj git
   git init
   
   # Dodaj wszystkie pliki
   git add .
   
   # Sprawdź co zostanie commitowane
   git status
   
   # Commit
   git commit -m "Initial commit - Halfmarathon Assistant App"
   
   # Dodaj remote
   git remote add origin https://github.com/TWOJA_NAZWA_UŻYTKOWNIKA/halfmarathon-assistant.git
   
   # Wypchnij kod
   git branch -M main
   git push -u origin main

KROK 2: Konfiguracja Digital Ocean App Platform

1. **Zaloguj się do Digital Ocean**
   - Przejdź do https://cloud.digitalocean.com/
   - Zaloguj się na swoje konto

2. **Utwórz nową aplikację**
   - Kliknij **Create** → **Apps**
   - Lub przejdź bezpośrednio do: https://cloud.digitalocean.com/apps/new

3. **Wybierz źródło (GitHub)**
   - Wybierz **GitHub**
   - Kliknij **Authorize DigitalOcean**
   - Zaloguj się do GitHub i autoryzuj dostęp
   - Wybierz swoje repozytorium: `halfmarathon-assistant`
   - Branch: `main`
   - Kliknij **Next**

KROK 3: Konfiguracja zasobów aplikacji

1. **Typ zasobu**
   - Typ: **Web Service**
   - Name: `halfmarathon-assistant` (lub zostaw domyślną)

2. **Ustawienia Build & Deploy**
   - **Build Command**: (zostaw puste lub domyślne)
   - **Run Command**: 
     ```
     streamlit run app.py --server.port=8080 --server.address=0.0.0.0
     ```
   - **HTTP Port**: `8080`
   - **HTTP Routes**: `/` 
3. **Environment Variables** 
   
   Kliknij **Edit** obok "Environment Variables" i dodaj:
   
   | `LANGFUSE_PUBLIC_KEY` 
   | `LANGFUSE_SECRET_KEY` 
   | `LANGFUSE_HOST` 
   
   **UWAGA**: Jeśli nie używasz Langfuse, pomiń ten krok - aplikacja będzie działać bez monitoringu.

4. Kliknij **Next**

KROK 4: Wybór planu i finalizacja

1. **Wybierz plan**
   - **Basic** - $5/miesiąc (512 MB RAM, 1 vCPU) 

2. **Nazwa aplikacji**
   - Zostaw domyślną lub zmień na własną
   - URL będzie: `https://halfmarathon-assistant-xxxxx.ondigitalocean.app`

3. **Region**
   - Wybierz najbliższy region (np. Frankfurt dla Europy)

4. **Kliknij "Create Resources"**

KROK 5: Czekaj na deployment

1. Digital Ocean automatycznie:
   - Pobierze kod z GitHub
   - Zainstaluje zależności z `requirements.txt`
   - Uruchomi aplikację
   - Przydzieli publiczny URL

2. **Czas deploymentu**: 5-15 minut (pierwsze uruchomienie)

3. **Status deploymentu**:
   - Możesz śledzić postęp w zakładce **Activity**
   - Sprawdź logi w zakładce **Runtime Logs**

KROK 6: Testowanie aplikacji

1. Po zakończeniu deploymentu kliknij **"Live App"** lub skopiuj URL
2. Otwórz aplikację w przeglądarce
3. Wprowadź klucz API OpenAI
4. Przetestuj funkcje:
   - Predykcję czasu
   - Chatbota AI
   - Wizualizacje

🔄 Aktualizacja aplikacji

Po każdej zmianie w kodzie:

```bash
git add .
git commit -m "Opis zmian"
git push origin main
```

Digital Ocean **automatycznie** wykryje zmiany i zrobi re-deploy!

Rozwiązywanie problemów

Problem: Aplikacja nie startuje

**Rozwiązanie**:
1. Sprawdź **Runtime Logs** w Digital Ocean
2. Upewnij się, że `requirements.txt` zawiera wszystkie pakiety
3. Sprawdź czy Run Command jest poprawny:
   ```
   streamlit run app.py --server.port=8080 --server.address=0.0.0.0
   ```

Problem: "ModuleNotFoundError"

**Rozwiązanie**:
1. Dodaj brakujący pakiet do `requirements.txt`
2. Commit i push zmian
3. Digital Ocean automatycznie zrobi re-deploy

Problem: Aplikacja działa, ale Langfuse nie loguje

**Rozwiązanie**:
1. Sprawdź czy zmienne środowiskowe są ustawione w Digital Ocean
2. Sprawdź logi - powinien być komunikat "✅ Langfuse enabled"
3. Jeśli nie chcesz używać Langfuse, po prostu nie ustawiaj zmiennych - aplikacja będzie działać bez monitoringu

Problem: Aplikacja jest wolna

**Rozwiązanie**:
1. Upgrade planu do Professional ($12/miesiąc)
2. Lub zoptymalizuj kod (lazy loading bibliotek)

📊 Monitorowanie

1. **Runtime Logs**: Sprawdź logi aplikacji w czasie rzeczywistym
2. **Metrics**: Zobacz użycie CPU, RAM, bandwidth
3. **Insights**: Analiza wydajności aplikacji

🎉 Gotowe!

Twoja aplikacja jest teraz dostępna publicznie


