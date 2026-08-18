#  Trener Półmaratoński

Aplikacja przeglądarkowa do przewidzenia czasu ukończenia półmaratonu z wykorzystaniem algorytmu Machine Learning i sztucznej Inteligencji.

##  Funkcje

- **Predykcja czasu**: Na podstawie wieku, płci i czasu na 5 km ( Algorytm ML wytrenowany na danych )
- **Chatbot**: Inteligentny interfejs do komunikacji z użytkownikiem o jego wyniki i dalszym działaniu
- **Analiza danych**: Wizualizacje i statystyki dotyczące wyników edycji półmaratonu Wrocławskiego
- **Monitoring**: Integracja z Langfuse do śledzenia dryfu modelu ML/Ai oraz jego metryk

##  Wymagania

- Python 3.11
- Klucz API OpenAI ( wprowadzany przez użytkownika w aplikacji )
- Konto Langfuse do monitoringu

##  Instalacja lokalna


1. Utwórz środowisko conda:
```bash
conda create -n <your-env-name> python= 3.11
```

2. Sklonuj repozytorium:
```bash
conda activate <your-env-name>
git clone <repo-url>
```

3. Zainstaluj zależności:
```bash
pip install -r requirements.txt
```

4. Utwórz plik `.env` dla Langfuse:
```env
LANGFUSE_PUBLIC_KEY=pk-lf-...
LANGFUSE_SECRET_KEY=sk-lf-...
LANGFUSE_HOST=https://cloud.langfuse.com
```

5. Uruchom aplikację:
```bash
streamlit run app.py
```

##  Deployment na Digital Ocean App Platform

### Krok 1: Przygotowanie repozytorium GitHub

1. Utwórz nowe repozytorium na GitHub
2. Upewnij się, że plik `.env` jest w `.gitignore` 
3. Wypchnij kod do GitHub:
```bash
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin <your-github-repo-url>
git push -u origin main
```

### Krok 2: Konfiguracja Digital Ocean App Platform

1. Zaloguj się do [Digital Ocean](https://cloud.digitalocean.com/)
2. Przejdź do **App Platform** → **Create App**
3. Wybierz **GitHub** jako źródło
4. Autoryzuj Digital Ocean do dostępu do twojego repozytorium
5. Wybierz repozytorium i branch `main`

### Krok 3: Konfiguracja aplikacji

1. **Typ aplikacji**: Web Service
2. **Run Command**: 
   ```bash
   streamlit run app.py --server.port=8080 --server.address=0.0.0.0
   ```
3. **HTTP Port**: `8080`
4. **Environment Variables** :
   - `LANGFUSE_PUBLIC_KEY`: `pk-lf-...`
   - `LANGFUSE_SECRET_KEY`: `sk-lf-...`
   - `LANGFUSE_HOST`: `https://cloud.langfuse.com`

### Krok 4: Wybór planu i deployment

1. Wybierz plan (Basic - $5/miesiąc )
2. Kliknij **Launch App**
3. Poczekaj na deployment (5-10 minut)
4. Twoja aplikacja będzie dostępna pod URL: `https://your-app-name.ondigitalocean.app`

## 🔐 Bezpieczeństwo

- ✅ Plik `.env` jest wykluczony z repozytorium (`.gitignore`)
- ✅ Klucz API OpenAI jest wprowadzany przez użytkownika, nie jest przechowywany
- ✅ Zmienne środowiskowe Langfuse są ustawiane bezpośrednio w Digital Ocean
- ✅ Aplikacja działa zarówno lokalnie (z `.env`) jak i w chmurze (bez `.env`)

##  Model ML

Model został wytrenowany na danych z Półmaratonu Wrocławskiego 2024:
- **Algorytm**: Linear Regressor
- **Cechy wejściowe**: Płeć, Wiek, Czas na 5 km
- **Metryka**: MAE
- **Dane treningowe**: ~13,000 zawodników

##  Wsparcie

Jeśli masz pytania lub problemy:
1. Sprawdź logi w Digital Ocean App Platform
2. Upewnij się, że wszystkie zmienne środowiskowe są poprawnie ustawione
3. Zweryfikuj, że `requirements.txt` zawiera wszystkie potrzebne pakiety

## 📝 Licencja

Ten projekt jest dostępny na licencji MIT.
