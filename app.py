import streamlit as st
import hashlib
import pandas as pd
import json
from datetime import datetime
import os

try:
    from dotenv import load_dotenv
    load_dotenv()
    print("✅ .env file loaded (local development)")
except ImportError:
    print("ℹ️ python-dotenv not installed - using system environment variables (production)")

try:
    from langfuse import observe
    LANGFUSE_AVAILABLE = True
except ImportError:
    LANGFUSE_AVAILABLE = False
    def observe(name=None, **kwargs):
        def decorator(func):
            return func
        return decorator

st.set_page_config(
    page_title="Asystent Półmaratoński",
    page_icon="🏃",
    layout="wide",
    initial_sidebar_state="expanded"
)

try:
    from langfuse import Langfuse
    public_key = os.environ.get("LANGFUSE_PUBLIC_KEY") or os.getenv("LANGFUSE_PUBLIC_KEY")
    secret_key = os.environ.get("LANGFUSE_SECRET_KEY") or os.getenv("LANGFUSE_SECRET_KEY")
    host = os.environ.get("LANGFUSE_HOST") or os.environ.get("LANGFUSE_BASE_URL") or os.getenv("LANGFUSE_HOST") or os.getenv("LANGFUSE_BASE_URL")
    
    if public_key and secret_key:
        if host:
            langfuse = Langfuse(
                public_key=public_key,
                secret_key=secret_key,
                host=host
            )
        else:
            langfuse = Langfuse(
                public_key=public_key,
                secret_key=secret_key
            )
        LANGFUSE_ENABLED = True
        print("✅ Langfuse enabled - monitoring active")
    else:
        LANGFUSE_ENABLED = False
        langfuse = None
        print("ℹ️ Langfuse disabled - running without monitoring")
except Exception as e:
    LANGFUSE_ENABLED = False
    langfuse = None
    print(f"⚠️ Langfuse initialization failed: {e}")

def init_session_state():
    if "api_key_verified" not in st.session_state:
        st.session_state["api_key_verified"] = False
    if "messages" not in st.session_state:
        st.session_state["messages"] = []
    if "user_data" not in st.session_state:
        st.session_state["user_data"] = {}
    if "show_prediction" not in st.session_state:
        st.session_state["show_prediction"] = False

def get_api_key_securely():
    if not st.session_state["api_key_verified"]:
        st.markdown("""
        <div style='text-align: center; padding: 100px 20px;'>
            <h1 style='font-size: 4em; margin-bottom: 20px;'>🏃</h1>
            <h1 style='color: #1f77b4; margin-bottom: 10px;'>Twój Asystent w Przygotowaniach do Półmaratonu</h1>
            <p style='font-size: 1.2em; color: #666; margin-bottom: 40px;'>
                Przewiduj swój czas na półmaratonie z pomocą sztucznej inteligencji
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            with st.form("api_key_form"):
                api_key = st.text_input(
                    "🔑 Klucz API OpenAI",
                    type="password",
                    placeholder="sk-...",
                    label_visibility="collapsed"
                )
                submit_button = st.form_submit_button("✅ Zatwierdź", use_container_width=True)
            
                if submit_button and api_key:
                    if api_key.startswith("sk-") and len(api_key) > 20:
                        user_id = hashlib.md5(api_key.encode('utf-8')).hexdigest()
                        st.session_state["openai_api_key"] = api_key
                        st.session_state["user_id"] = user_id
                        st.session_state["api_key_verified"] = True
                        
                        if len(st.session_state["messages"]) == 0:
                            st.session_state["messages"].append({
                                "role": "assistant",
                                "content": """Cześć! Jestem Twoją pomocą naukową w przygotowaniach do Półmaratonu! Pomogę Ci przewidzieć czas na półmaraton z pomocą sztucznej inteligencji i stworzę dla Ciebie profesjonalny plan treningowy! 

**Podaj mi:** Imię, Wiek, Czas na 5 km

**Przykład:** Cześć! Jestem Ania, mam 31 lat i biegnę 5km w 21 minut i 40 sekund""",
                                "timestamp": datetime.now()
                            })
                        
                        st.rerun()
                    else:
                        st.error("❌ Nieprawidłowy format klucza API. Klucz powinien zaczynać się od 'sk-'")
        st.stop()
    return st.session_state["openai_api_key"]

@st.cache_resource
def load_model():
    try:
        from pycaret.regression import load_model as pycaret_load_model
        
        model = pycaret_load_model('final_halfmaraton_model')
        return model
    except FileNotFoundError:
        st.error("Nie znaleziono pliku modelu 'final_halfmaraton_model.pkl'")
        return None
    except Exception as e:
        st.error(f"Błąd podczas ładowania modelu: {e}")
        return None

@observe(name="extract_user_data")
def extract_user_data(user_text, api_key):
    import openai
    client = openai.OpenAI(api_key=api_key)
    
    system_prompt = """Jesteś asystentem, który wyłuskuje dane z tekstu użytkownika.
    Szukasz następujących informacji:
    - Płeć (K dla kobiety, M dla mężczyzny)
    - Wiek (liczba całkowita)
    - Czas na 5 km (w sekundach)
    
    Zwróć dane w formacie JSON z kluczami: "Płeć", "Wiek", "5 km Czas".
    Jeśli jakiejś informacji brakuje, ustaw wartość null.
    
    Przykłady:
    - "30 minut na 5km" -> 1800 sekund
    - "25 min" -> 1500 sekund
    - "20:30" (20 minut 30 sekund) -> 1230 sekund
    
    Odpowiedz TYLKO w formacie JSON, bez dodatkowego tekstu."""
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_text}
            ],
            temperature=0,
            timeout=30
        )
        
        result = response.choices[0].message.content.strip()
        
        if result.startswith("```json"):
            result = result.replace("```json", "").replace("```", "").strip()
        elif result.startswith("```"):
            result = result.replace("```", "").strip()
            
        data = json.loads(result)
        return data
    except TimeoutError:
        st.error("⏱️ Przekroczono limit czasu połączenia z API OpenAI. Sprawdź połączenie internetowe.")
        return None
    except Exception as e:
        error_msg = str(e)
        if "connection" in error_msg.lower() or "timeout" in error_msg.lower():
            st.error("🌐 Problem z połączeniem internetowym. Sprawdź swoją sieć i spróbuj ponownie.")
        elif "api_key" in error_msg.lower() or "authentication" in error_msg.lower():
            st.error("🔑 Nieprawidłowy klucz API OpenAI. Sprawdź klucz i odśwież stronę.")
        else:
            st.error(f"❌ Błąd podczas przetwarzania danych: {e}")
        return None

def check_missing_data(data):
    required_fields = {
        "Płeć": "płeć (kobieta/mężczyzna)",
        "Wiek": "wiek",
        "5 km Czas": "czas na 5 km"
    }
    
    missing = []
    for field, description in required_fields.items():
        if field not in data or data[field] is None or data[field] == "":
            missing.append(description)
    
    return missing

def predict_time(data, model):
    try:
        from pycaret.regression import predict_model
        
        df = pd.DataFrame({
            'Płeć': [data['Płeć']],
            'Wiek': [int(data['Wiek'])],
            '5 km Czas': [int(data['5 km Czas'])]
        })
        
        prediction = predict_model(model, data=df)
        predicted_time = prediction['prediction_label'].iloc[0]
        
        return predicted_time
    except Exception as e:
        st.error(f"Błąd podczas przewidywania: {e}")
        return None

def format_time(seconds):
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    return f"{hours}h {minutes}min {secs}s"

def display_chat_message(message):
    role = message["role"]
    content = message["content"]
    
    if role == "user":
        st.markdown(f"""
        <div style='display: flex; 
                    justify-content: flex-end; 
                    margin: 10px 0;
                    animation: fadeInUp 0.5s ease-out;'>
            <div style='background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); 
                        color: white; 
                        padding: 10px 16px; 
                        border-radius: 20px 20px 5px 20px; 
                        max-width: 70%; 
                        box-shadow: 0 2px 8px rgba(79, 172, 254, 0.3);
                        border: 2px solid rgba(255, 255, 255, 0.2);'>
                <div style='font-size: 0.9em; 
                            line-height: 1.4; 
                            font-weight: 500;'>{content}</div>
            </div>
            <div style='margin-left: 8px; 
                        font-size: 1.8em; 
                        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
                        width: 40px;
                        height: 40px;
                        border-radius: 50%;
                        display: flex;
                        align-items: center;
                        justify-content: center;
                        box-shadow: 0 2px 6px rgba(30, 60, 114, 0.4);'>🤗</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div style='display: flex; 
                    justify-content: flex-start; 
                    margin: 10px 0;
                    animation: fadeInUp 0.5s ease-out;'>
            <div style='margin-right: 8px; 
                        font-size: 1.8em;
                        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
                        width: 40px;
                        height: 40px;
                        border-radius: 50%;
                        display: flex;
                        align-items: center;
                        justify-content: center;
                        box-shadow: 0 2px 6px rgba(79, 172, 254, 0.4);'>🧠</div>
            <div style='background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%); 
                        color: #2d3748; 
                        padding: 10px 16px; 
                        border-radius: 20px 20px 20px 5px; 
                        max-width: 60%; 
                        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
                        border: 2px solid rgba(102, 126, 234, 0.1);'>
                <div style='font-size: 0.9em; 
                            line-height: 1.4; 
                            white-space: pre-wrap;
                            font-weight: 500;'>{content}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

@observe(name="generate_personalized_training_plan")
def generate_personalized_training_plan(data, predicted_seconds, api_key):
    """
    Generuje spersonalizowany plan treningowy za pomocą OpenAI API
    """
    try:
        import openai
        client = openai.OpenAI(api_key=api_key)
        
        age = data.get('Wiek', 'nieznany')
        gender = data.get('Płeć', 'nieznana')
        time_5km = data.get('5 km Czas', 0)
        
        predicted_pace_per_km = predicted_seconds / 21.0975
        pace_minutes = int(predicted_pace_per_km // 60)
        pace_seconds = int(predicted_pace_per_km % 60)
        
        current_5km_pace = time_5km / 5
        current_pace_min = int(current_5km_pace // 60)
        current_pace_sec = int(current_5km_pace % 60)
        
        formatted_time = format_time(predicted_seconds)
        
        prompt = f"""Jesteś ekspertem od treningu biegowego. Stwórz KRÓTKI i KONKRETNY spersonalizowany plan treningowy dla osoby z następującymi danymi:

- Wiek: {age} lat
- Płeć: {gender}
- Obecny czas na 5km: {format_time(time_5km)}
- Obecne tempo (5km): {current_pace_min}:{current_pace_sec:02d} min/km
- Przewidywany czas na półmaraton: {formatted_time}
- Przewidywane tempo (półmaraton): {pace_minutes}:{pace_seconds:02d} min/km

Wygeneruj 6 KRÓTKICH kategorii (każda max 4-5 linijek):

1. 🏃 Plan 8-tygodniowy - dostosowany do wieku i poziomu
2. 💪 Trening Interwałowy - konkretne interwały dla tego poziomu
3. 🥗 Żywienie - dostosowane do wieku i płci
4. 🧘 Regeneracja - uwzględniając wiek
5. 🎯 Strategia Wyścigu - dla tego tempa
6. ⚠️ Ważne Uwagi - personalizowane ostrzeżenia

Format odpowiedzi (DOKŁADNIE W TYM FORMACIE):
[PLAN_8TYG]
Tyg 1-2: ...
Tyg 3-4: ...
[/PLAN_8TYG]

[TRENING_INT]
1x w tygodniu:
• Rozgrzewka: ...
[/TRENING_INT]

[ZYWIENIE]
• 3h przed: ...
• Podczas: ...
[/ZYWIENIE]

[REGENERACJA]
• Sen: ...
• Stretching: ...
[/REGENERACJA]

[STRATEGIA]
• 0-5km: ...
• 5-15km: ...
[/STRATEGIA]

[UWAGI]
• ...
• ...
[/UWAGI]

WAŻNE: Bądź KONKRETNY i KRÓTKI. Każda sekcja max 4-5 linijek."""

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Jesteś ekspertem od treningu biegowego. Tworzysz krótkie, konkretne i spersonalizowane plany treningowe."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=1500
        )
        
        content = response.choices[0].message.content
        
        def extract_section(text, start_tag, end_tag):
            try:
                start = text.index(start_tag) + len(start_tag)
                end = text.index(end_tag)
                return text[start:end].strip()
            except:
                return None
        
        plan_data = {
            'plan_8tyg': extract_section(content, '[PLAN_8TYG]', '[/PLAN_8TYG]'),
            'trening_int': extract_section(content, '[TRENING_INT]', '[/TRENING_INT]'),
            'zywienie': extract_section(content, '[ZYWIENIE]', '[/ZYWIENIE]'),
            'regeneracja': extract_section(content, '[REGENERACJA]', '[/REGENERACJA]'),
            'strategia': extract_section(content, '[STRATEGIA]', '[/STRATEGIA]'),
            'uwagi': extract_section(content, '[UWAGI]', '[/UWAGI]')
        }
        
        return plan_data
        
    except Exception as e:
        st.error(f"Błąd podczas generowania planu: {str(e)}")
        return None

@observe(name="answer_followup_question")
def answer_followup_question(user_question, prediction_data, api_key):
    """
    Odpowiada na pytania follow-up użytkownika po otrzymaniu predykcji
    """
    try:
        import openai
        client = openai.OpenAI(api_key=api_key)
        
        user_data = prediction_data.get("user_data", {})
        predicted_seconds = prediction_data.get("predicted_time", 0)
        
        age = user_data.get('Wiek', 'nieznany')
        gender = user_data.get('Płeć', 'nieznana')
        time_5km = user_data.get('5 km Czas', 0)
        formatted_time = format_time(predicted_seconds)
        
        predicted_pace_per_km = predicted_seconds / 21.0975
        pace_minutes = int(predicted_pace_per_km // 60)
        pace_seconds = int(predicted_pace_per_km % 60)
        
        context = f"""Kontekst rozmowy:
- Użytkownik ma {age} lat, płeć: {gender}
- Obecny czas na 5km: {format_time(time_5km)}
- Przewidywany czas na półmaraton: {formatted_time}
- Przewidywane tempo: {pace_minutes}:{pace_seconds:02d} min/km

Użytkownik otrzymał już predykcję i spersonalizowany plan treningowy."""

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": f"""Jesteś ekspertem od treningu biegowego i asystentem w przygotowaniach do półmaratonu. 
                
{context}

Odpowiadaj na pytania użytkownika w sposób:
- Konkretny i praktyczny
- Dostosowany do jego wieku, płci i poziomu
- Profesjonalny ale przyjazny
- Używaj emotikonów dla lepszej czytelności
- Odpowiedzi powinny być średniej długości (nie za krótkie, nie za długie)"""},
                {"role": "user", "content": user_question}
            ],
            temperature=0.7,
            max_tokens=1000
        )
        
        return response.choices[0].message.content
        
    except Exception as e:
        return f"Przepraszam, wystąpił błąd podczas przetwarzania Twojego pytania: {str(e)}"

def display_prediction_card(data, predicted_seconds, training_plan=None):
    st.markdown("""
    <style>
    @keyframes slideIn {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    .prediction-card {
        animation: slideIn 0.5s ease-out;
    }
    </style>
    """, unsafe_allow_html=True)
    
    formatted_time = format_time(predicted_seconds)
    
    st.markdown(f"""
    <div class='prediction-card' style='background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%); 
                padding: 40px; 
                border-radius: 25px; 
                margin: 30px 0; 
                box-shadow: 0 15px 40px rgba(30, 60, 114, 0.4);
                border: 2px solid rgba(255, 255, 255, 0.2);'>
        <div style='text-align: center; color: white;'>
            <div style='font-size: 1.4em; margin-bottom: 15px; opacity: 0.95; font-weight: 500; letter-spacing: 1px;'>
                🎯 TWÓJ PRZEWIDYWANY CZAS TO:
            </div>
            <div style='font-size: 4.5em; 
                        font-weight: 800; 
                        margin: 30px 0; 
                        text-shadow: 3px 3px 6px rgba(0,0,0,0.3);
                        letter-spacing: 3px;
                        line-height: 1.2;'>
                {formatted_time}
            </div>
            <div style='font-size: 1.1em; 
                        opacity: 0.9; 
                        margin-top: 20px;
                        padding: 15px;
                        background: rgba(255, 255, 255, 0.15);
                        border-radius: 10px;
                        display: inline-block;'>
                📊 Na dystansie 21.0975 km
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    predicted_pace_per_km = predicted_seconds / 21.0975
    pace_minutes = int(predicted_pace_per_km // 60)
    pace_seconds = int(predicted_pace_per_km % 60)
    
    current_5km_pace = data['5 km Czas'] / 5
    current_pace_min = int(current_5km_pace // 60)
    current_pace_sec = int(current_5km_pace % 60)
    
    st.markdown("### 📊 ANALIZA I PLAN TRENINGOWY")
    
    st.markdown(f"""
    <div style='background: white; padding: 20px; border-radius: 12px; margin-bottom: 20px; border-left: 4px solid #667eea; box-shadow: 0 2px 8px rgba(0,0,0,0.1);'>
        <div style='font-weight: 700; margin-bottom: 10px; color: #667eea; font-size: 1.1em;'>⏱️ Analiza Tempa</div>
        <div style='color: #333; line-height: 1.8;'>
            • <strong>Twoje obecne tempo (5km):</strong> {current_pace_min}:{current_pace_sec:02d} min/km<br>
            • <strong>Przewidywane tempo (półmaraton):</strong> {pace_minutes}:{pace_seconds:02d} min/km<br>
            • <strong>Rekomendowane tempo treningowe:</strong> {pace_minutes+1}:{(pace_seconds+30)%60:02d} min/km (wolniejsze o ~10-15%)
        </div>
                </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    if training_plan and all(training_plan.values()):
        plan_8tyg = training_plan['plan_8tyg'].replace('\n', '<br>')
        trening_int = training_plan['trening_int'].replace('\n', '<br>')
        zywienie = training_plan['zywienie'].replace('\n', '<br>')
        regeneracja = training_plan['regeneracja'].replace('\n', '<br>')
        strategia = training_plan['strategia'].replace('\n', '<br>')
        uwagi = training_plan['uwagi'].replace('\n', '<br>')
    else:
        plan_8tyg = "<strong>Tyg 1-2:</strong> 3x bieg 30-40min<br><strong>Tyg 3-4:</strong> 4x bieg 40-50min<br><strong>Tyg 5-6:</strong> Długi bieg 90min + 2x tempo<br><strong>Tyg 7-8:</strong> Tapering - redukcja obciążenia"
        trening_int = "<strong>1x w tygodniu:</strong><br>• Rozgrzewka: 15 min<br>• 6x 800m w tempie 5km + 2min odpoczynku<br>• Wychłodzenie: 10 min"
        zywienie = "• <strong>3h przed:</strong> Posiłek węglowodanowy (owsianka, banan)<br>• <strong>Podczas:</strong> Żele energetyczne co 30-40min<br>• <strong>Po:</strong> Białko + węglowodany w ciągu 30min"
        regeneracja = "• <strong>Sen:</strong> Min. 7-8h dziennie<br>• <strong>Stretching:</strong> 15min po każdym biegu<br>• <strong>Masaż:</strong> Roller piankowy 2-3x/tydzień<br>• <strong>Dzień off:</strong> Min. 1 dzień odpoczynku/tydzień"
        strategia = "• <strong>0-5km:</strong> Tempo konserwatywne (-5-10s/km)<br>• <strong>5-15km:</strong> Tempo docelowe<br>• <strong>15-21km:</strong> Zwiększ jeśli masz siły"
        uwagi = "• Stopniuj obciążenie max 10%/tydzień<br>• Słuchaj swojego ciała<br>• Nawadniaj się regularnie<br>• Testuj żywienie podczas treningów"
    
    with col1:
        st.markdown(f"""
        <div style='background: white; padding: 15px; border-radius: 12px; border-left: 4px solid #667eea; box-shadow: 0 2px 8px rgba(0,0,0,0.05); margin-bottom: 15px;'>
            <div style='font-weight: 600; margin-bottom: 5px;'>🏃 Plan 8-tygodniowy</div>
            <div style='font-size: 0.9em; line-height: 1.6; color: #333;'>
                {plan_8tyg}
            </div>
                </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div style='background: white; padding: 15px; border-radius: 12px; border-left: 4px solid #667eea; box-shadow: 0 2px 8px rgba(0,0,0,0.05); margin-bottom: 15px;'>
            <div style='font-weight: 600; margin-bottom: 5px;'>🥗 Żywienie</div>
            <div style='font-size: 0.9em; line-height: 1.6; color: #333;'>
                {zywienie}
            </div>
                </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div style='background: white; padding: 15px; border-radius: 12px; border-left: 4px solid #667eea; box-shadow: 0 2px 8px rgba(0,0,0,0.05);'>
            <div style='font-weight: 600; margin-bottom: 5px;'>🎯 Strategia Wyścigu</div>
            <div style='font-size: 0.9em; line-height: 1.6; color: #333;'>
                {strategia}
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div style='background: white; padding: 15px; border-radius: 12px; border-left: 4px solid #764ba2; box-shadow: 0 2px 8px rgba(0,0,0,0.05); margin-bottom: 15px;'>
            <div style='font-weight: 600; margin-bottom: 5px;'>💪 Trening Interwałowy</div>
            <div style='font-size: 0.9em; line-height: 1.6; color: #333;'>
                {trening_int}
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div style='background: white; padding: 15px; border-radius: 12px; border-left: 4px solid #764ba2; box-shadow: 0 2px 8px rgba(0,0,0,0.05); margin-bottom: 15px;'>
                <div style='font-weight: 600; margin-bottom: 5px;'>🧘 Regeneracja</div>
            <div style='font-size: 0.9em; line-height: 1.6; color: #333;'>
                {regeneracja}
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div style='background: white; padding: 15px; border-radius: 12px; border-left: 4px solid #764ba2; box-shadow: 0 2px 8px rgba(0,0,0,0.05);'>
            <div style='font-weight: 600; margin-bottom: 5px;'>⚠️ Ważne Uwagi</div>
            <div style='font-size: 0.9em; line-height: 1.6; color: #333;'>
                {uwagi}
        </div>
    </div>
    """, unsafe_allow_html=True)

def display_sidebar():
    with st.sidebar:
        st.markdown("""
        <div style='text-align: center; padding: 20px 0; border-bottom: 2px solid rgba(255, 255, 255, 0.3);'>
            <div style='font-size: 3em; margin-bottom: 10px;'>🏃‍♂️</div>
            <h2 style='color: white; margin: 0; font-weight: 700; letter-spacing: 1px; font-size: 1.2em;'>Dowiedz się, jakie są Twoje możliwości</h2>
            <p style='color: rgba(255, 255, 255, 0.9); font-size: 0.85em; margin-top: 8px; line-height: 1.4;'>Niech asystent pomoże ci wyśrubować nowy personal best!</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<div style='margin: 20px 0;'></div>", unsafe_allow_html=True)
        
        st.markdown("""
        <div style='background: rgba(255, 255, 255, 0.15); 
                    padding: 20px; 
                    border-radius: 15px; 
                    margin: 15px 0;
                    border: 1px solid rgba(255, 255, 255, 0.2);'>
            <div style='font-size: 1.2em; font-weight: 700; margin-bottom: 15px; color: white;'>
                📊 STATYSTYKI SESJI
            </div>
        """, unsafe_allow_html=True)
        
        total_messages = len([m for m in st.session_state.get("messages", []) if m["role"] == "user"])
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"""
            <div style='text-align: center; padding: 10px;'>
                <div style='font-size: 2em; font-weight: 700; color: white;'>{total_messages}</div>
                <div style='font-size: 0.9em; color: rgba(255, 255, 255, 0.8);'>Wiadomości</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            if st.session_state.get("prediction_data"):
                pred_data = st.session_state["prediction_data"]
                pred_time = format_time(pred_data["predicted_time"])
                st.markdown(f"""
                <div style='text-align: center; padding: 10px;'>
                    <div style='font-size: 1.2em; font-weight: 700; color: white;'>{pred_time}</div>
                    <div style='font-size: 0.9em; color: rgba(255, 255, 255, 0.8);'>Predykcja</div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown("""
                <div style='text-align: center; padding: 10px;'>
                    <div style='font-size: 1.2em; font-weight: 700; color: white;'>-</div>
                    <div style='font-size: 0.9em; color: rgba(255, 255, 255, 0.8);'>Predykcja</div>
                </div>
                """, unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
        st.markdown("<div style='margin: 20px 0;'></div>", unsafe_allow_html=True)
        
        st.markdown("""
        <div style='background: rgba(255, 255, 255, 0.15); 
                    padding: 20px; 
                    border-radius: 15px; 
                    margin: 15px 0;
                    border: 1px solid rgba(255, 255, 255, 0.2);
                    text-align: center;'>
            <div style='font-size: 1.8em; margin-bottom: 10px;'>💪</div>
            <div style='color: white; font-size: 0.95em; line-height: 1.6; font-style: italic;'>
                "Każdy maraton zaczyna się od pierwszego kroku. Ty już go zrobiłeś!"
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div style='background: rgba(255, 255, 255, 0.15); 
                    padding: 20px; 
                    border-radius: 15px; 
                    margin: 15px 0;
                    border: 1px solid rgba(255, 255, 255, 0.2);'>
            <div style='font-size: 1.2em; font-weight: 700; margin-bottom: 15px; color: white;'>
                💡 FAQ
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        with st.expander("📝 Jak podać dane?", expanded=False):
            st.markdown("""
            <div style='background: rgba(255, 255, 255, 0.1); padding: 15px; border-radius: 10px;'>
                <p style='color: white; margin-bottom: 10px;'><strong>Możesz napisać naturalnie, np.:</strong></p>
                <ul style='color: rgba(255, 255, 255, 0.9); line-height: 1.8;'>
                    <li>Cześć! Jestem Maria, mam 33 lat i biegnę 5km w 21 minut i 20 sekund</li>
                    <li>Jestem Marek, mam 28 lat, czas na 5km: 22 minuty</li>
                    <li>Witam! Nazywam się Kasia, mam 35 lat, 5km biegnę w 25:40</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
        
        with st.expander("⏱️ Formaty czasu", expanded=False):
            st.markdown("""
            <div style='background: rgba(255, 255, 255, 0.1); padding: 15px; border-radius: 10px;'>
                <p style='color: white; margin-bottom: 10px;'><strong>Akceptowane formaty czasu na 5 km:</strong></p>
                <ul style='color: rgba(255, 255, 255, 0.9); line-height: 1.8;'>
                    <li><strong>Pełny opis:</strong> 21 minut i 40 sekund</li>
                    <li><strong>Minuty:</strong> 25 minut, 22 minuty</li>
                    <li><strong>Format MM:SS:</strong> 21:40, 25:30</li>
                    <li><strong>Sekundy:</strong> 1300 sekund</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
        with st.expander("🧠 O modelu AI", expanded=False):
            st.markdown("""
            <div style='background: rgba(255, 255, 255, 0.1); padding: 15px; border-radius: 10px;'>
                <p style='color: white; margin-bottom: 10px;'><strong>Model został wytrenowany na danych z Półmaratonu Wrocławskiego.</strong></p>
                <p style='color: rgba(255, 255, 255, 0.9); margin-bottom: 10px;'><strong>Dane wejściowe:</strong></p>
                <ul style='color: rgba(255, 255, 255, 0.9); line-height: 1.8;'>
                    <li>Imię</li>
                    <li>Wiek</li>
                    <li>Czas na dystansie 5 km</li>
                </ul>
                <p style='color: rgba(255, 255, 255, 0.9); margin-top: 10px;'>
                    <strong>Przewiduje:</strong> Twój czas na półmaraton (21.0975 km)
                </p>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("<div style='margin: 20px 0;'></div>", unsafe_allow_html=True)
        
        if st.session_state.get("prediction_data"):
            st.markdown("""
            <div style='background: rgba(255, 255, 255, 0.15); 
                        padding: 20px; 
                        border-radius: 15px; 
                        margin: 15px 0;
                        border: 1px solid rgba(255, 255, 255, 0.2);'>
                <div style='font-size: 1.2em; font-weight: 700; margin-bottom: 15px; color: white; text-align: center;'>
                    📥 EKSPORT WYNIKÓW
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            pred_data = st.session_state["prediction_data"]
            training_plan = pred_data.get("training_plan", None)
            
            training_plan_text = ""
            if training_plan:
                training_plan_text = f"""
┌─────────────────────────────────────────────────────┐
│ 🏃 PLAN 8-TYGODNIOWY:                               │
├─────────────────────────────────────────────────────┤
{training_plan.get('plan_8tyg', 'Brak danych').replace(chr(10), chr(10) + '│ ')}
└─────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────┐
│ 💪 TRENING INTERWAŁOWY:                             │
├─────────────────────────────────────────────────────┤
{training_plan.get('trening_int', 'Brak danych').replace(chr(10), chr(10) + '│ ')}
└─────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────┐
│ 🥗 ŻYWIENIE:                                        │
├─────────────────────────────────────────────────────┤
{training_plan.get('zywienie', 'Brak danych').replace(chr(10), chr(10) + '│ ')}
└─────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────┐
│ 🧘 REGENERACJA:                                     │
├─────────────────────────────────────────────────────┤
{training_plan.get('regeneracja', 'Brak danych').replace(chr(10), chr(10) + '│ ')}
└─────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────┐
│ 🎯 STRATEGIA WYŚCIGU:                               │
├─────────────────────────────────────────────────────┤
{training_plan.get('strategia', 'Brak danych').replace(chr(10), chr(10) + '│ ')}
└─────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────┐
│ ⚠️ WAŻNE UWAGI:                                     │
├─────────────────────────────────────────────────────┤
{training_plan.get('uwagi', 'Brak danych').replace(chr(10), chr(10) + '│ ')}
└─────────────────────────────────────────────────────┘
"""
            else:
                training_plan_text = """
┌─────────────────────────────────────────────────────┐
│ 💡 WSKAZÓWKI TRENINGOWE:                            │
├─────────────────────────────────────────────────────┤
│ • To przewidywanie opiera się na Twoich aktualnych  │
│   danych treningowych                               │
│ • Rzeczywisty czas może się różnić w zależności od  │
│   warunków pogodowych i trasy                       │
│ • Regularny trening i odpowiednia dieta mogą        │
│   poprawić Twój wynik                               │
│ • Pamiętaj o odpowiednim rozgrzewaniu i regeneracji!│
└─────────────────────────────────────────────────────┘
"""
            
            export_text = f"""
╔═══════════════════════════════════════════════════════╗
║     WYNIK PREDYKCJI - ASYSTENT PÓŁMARATOŃSKI         ║
╚═══════════════════════════════════════════════════════╝

📅 Data: {datetime.now().strftime('%Y-%m-%d %H:%M')}

┌─────────────────────────────────────────────────────┐
│ TWOJE DANE:                                         │
├─────────────────────────────────────────────────────┤
│ Płeć:           {pred_data['user_data']['Płeć']}                                    │
│ Wiek:           {pred_data['user_data']['Wiek']} lat                                 │
│ Czas na 5 km:   {format_time(pred_data['user_data']['5 km Czas'])}                            │
└─────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────┐
│ 🎯 PRZEWIDYWANY CZAS NA PÓŁMARATON:                 │
├─────────────────────────────────────────────────────┤
│                                                     │
│              {format_time(pred_data['predicted_time'])}                          │
│                                                     │
│           (Dystans: 21.0975 km)                     │
└─────────────────────────────────────────────────────┘

{training_plan_text}

🏃 Powodzenia w treningach i na biegu! 🏃

═══════════════════════════════════════════════════════
Wygenerowano przez Asystent Półmaratoński v1.0
Powered by OpenAI & PyCaret ML model
═══════════════════════════════════════════════════════
"""
            
            col_exp1, col_exp2 = st.columns(2)
            
            with col_exp1:
                st.download_button(
                    label="📄 Pobierz wynik (TXT)",
                    data=export_text,
                    file_name=f"predykcja_polmaraton_{datetime.now().strftime('%Y%m%d_%H%M')}.txt",
                    mime="text/plain",
                    use_container_width=True
                )
            
            with col_exp2:
                conversation_text = f"""
╔═══════════════════════════════════════════════════════╗
║     PEŁNA KONWERSACJA - ASYSTENT PÓŁMARATOŃSKI       ║
╚═══════════════════════════════════════════════════════╝

📅 Data: {datetime.now().strftime('%Y-%m-%d %H:%M')}

"""
                for msg in st.session_state["messages"]:
                    role = "UŻYTKOWNIK" if msg["role"] == "user" else "ASYSTENT"
                    timestamp = msg.get("timestamp", datetime.now()).strftime('%H:%M:%S')
                    conversation_text += f"""
┌─────────────────────────────────────────────────────┐
│ {role} ({timestamp})
├─────────────────────────────────────────────────────┤
{msg['content']}
└─────────────────────────────────────────────────────┘

"""
                
                conversation_text += f"""
═══════════════════════════════════════════════════════
Wygenerowano przez Asystent Półmaratoński v1.0
Powered by OpenAI & PyCaret ML model
═══════════════════════════════════════════════════════
"""
                
                st.download_button(
                    label="💬 Pobierz konwersację (TXT)",
                    data=conversation_text,
                    file_name=f"konwersacja_polmaraton_{datetime.now().strftime('%Y%m%d_%H%M')}.txt",
                    mime="text/plain",
                    use_container_width=True
                )
        
        st.markdown("<div style='margin: 20px 0;'></div>", unsafe_allow_html=True)
        
        st.markdown("""
        <div style='text-align: center; 
                    padding: 20px; 
                    margin-top: 30px;
                    border-top: 2px solid rgba(255, 255, 255, 0.3);'>
            <div style='color: rgba(255, 255, 255, 0.9); 
                        font-size: 0.85em; 
                        line-height: 1.8;
                        font-weight: 500;'>
                <div style='margin-bottom: 8px;'>⚡ Powered by</div>
                <div style='font-weight: 700; font-size: 1.1em; margin-bottom: 8px;'>
                    OpenAI & PyCaret ML model
                </div>
                <div style='opacity: 0.7;'>v1.0 | 2026</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

def main():
    init_session_state()
    
    api_key = get_api_key_securely()
    
    if LANGFUSE_ENABLED and "user_id" in st.session_state:
        try:
            from langfuse import langfuse_context
            langfuse_context.update_current_trace(
                user_id=st.session_state["user_id"],
                session_id=st.session_state.get("user_id"),
                metadata={
                    "app_version": "2.0",
                    "app_name": "Asystent Półmaratoński"
                }
            )
        except:
            pass
    
    display_sidebar()
    
    
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    * {
        font-family: 'Inter', sans-serif;
    }
    
    .main {
        padding-top: 1rem;
        padding-bottom: 100px;
    }
    
    .stTextInput > div > div > input {
        border-radius: 25px;
        border: 2px solid #e0e0e0;
        padding: 12px 20px;
        font-size: 1em;
        transition: all 0.3s;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
    }
    
    .stButton > button {
        border-radius: 25px;
        background: linear-gradient(135deg, #14407a 0%, #0a2a52 100%);
        color: white;
        border: none;
        padding: 12px 30px;
        font-weight: 600;
        transition: all 0.3s;
        box-shadow: 0 4px 15px rgba(20, 64, 122, 0.3);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(20, 64, 122, 0.4);
    }
    
    .stButton > button:active {
        transform: translateY(0);
    }
    
    /* Animacje dla wiadomości */
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    /* Scrollbar styling */
    ::-webkit-scrollbar {
        width: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: #f1f1f1;
    }
    
    ::-webkit-scrollbar-thumb {
        background: #667eea;
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: #764ba2;
    }
    
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1e6bb8 0%, #008fa3 100%);
    }
    
    [data-testid="stSidebar"] * {
        color: white !important;
    }
    
    [data-testid="stSidebar"] .stMarkdown {
        color: white !important;
    }
    
    [data-testid="stSidebar"] hr {
        border-color: rgba(255, 255, 255, 0.3) !important;
    }
    
    /* Hide streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Input container at bottom */
    .input-container {
        position: fixed;
        bottom: 0;
        left: 0;
        right: 0;
        background: white;
        padding: 20px;
        box-shadow: 0 -2px 20px rgba(0,0,0,0.1);
        z-index: 999;
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div style='text-align: center; 
                margin-bottom: 10px; 
                padding: 12px 15px;
                background: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%);
                border-radius: 12px;
                border: 2px solid rgba(102, 126, 234, 0.2);'>
        <h1 style='color: #667eea; 
                   margin: 0 0 5px 0; 
                   font-weight: 800; 
                   font-size: 1.5em;
                   letter-spacing: 1px;'>
            Asystent w przygotowaniach do Półmaratonu
        </h1>
        <p style='color: #666; 
                  font-size: 0.85em; 
                  margin: 0;
                  font-weight: 500;'>
            📊 Wytrenowany na danych Półmaratonu Wrocławskiego
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    if st.session_state.get("show_prediction") and st.session_state.get("prediction_data"):
        prediction_message_idx = None
        for idx, msg in enumerate(st.session_state["messages"]):
            if msg["role"] == "assistant" and ("✅ Gotowe! Oto Twoja analiza" in msg["content"]):
                prediction_message_idx = idx
        
        if prediction_message_idx is not None:
            for i in range(prediction_message_idx + 1):
                display_chat_message(st.session_state["messages"][i])
            
            pred_data = st.session_state["prediction_data"]
            training_plan = pred_data.get("training_plan", None)
            display_prediction_card(pred_data["user_data"], pred_data["predicted_time"], training_plan)
            
            for i in range(prediction_message_idx + 1, len(st.session_state["messages"])):
                display_chat_message(st.session_state["messages"][i])
        else:
            for message in st.session_state["messages"]:
                display_chat_message(message)
            
            pred_data = st.session_state["prediction_data"]
            training_plan = pred_data.get("training_plan", None)
            display_prediction_card(pred_data["user_data"], pred_data["predicted_time"], training_plan)
    else:
        for message in st.session_state["messages"]:
            display_chat_message(message)
    
    st.markdown("<div style='margin: 15px 0;'></div>", unsafe_allow_html=True)
        
    st.markdown("---")
    
    default_value = st.session_state.get("quick_input", "")
    if default_value:
        st.session_state.pop("quick_input", "")
    
    col1, col2 = st.columns([6, 1])
    
    with col1:
        user_input = st.text_input(
            "Wiadomość",
            value=default_value,
            placeholder="Podaj swoje imię, wiek i czas na 5 km",
            key="user_input",
            label_visibility="collapsed"
        )
    
    with col2:
        send_button = st.button("📤 Wyślij", use_container_width=True, type="primary")
    
    user_messages_count = len([m for m in st.session_state["messages"] if m["role"] == "user"])
    total_messages_count = len(st.session_state["messages"])
    
    if user_messages_count == 0 and total_messages_count <= 1 and not (send_button and user_input):
        st.markdown("<div style='margin: 10px 0;'></div>", unsafe_allow_html=True)
        
        st.markdown("""
        <div style='background: rgba(102, 126, 234, 0.05); 
                    padding: 15px 20px; 
                    border-radius: 12px; 
                    border-left: 4px solid #667eea;'>
            <div style='font-weight: 700; color: #667eea; margin-bottom: 12px; font-size: 1em;'>
                ⚡ Szybkie Fakty o Półmaratonie
            </div>
            <div style='display: grid; grid-template-columns: 1fr 1fr 1fr 1fr; gap: 15px; color: #333;'>
                <div style='font-size: 0.9em;'>
                    <strong>📏 Dystans:</strong> 21.0975 km
                </div>
                <div style='font-size: 0.9em;'>
                    <strong>⏱️ Średni czas:</strong> 1h 45min - 2h 15min
                </div>
                <div style='font-size: 0.9em;'>
                    <strong>🏃 Tempo:</strong> ~5:00 - 6:30 min/km
                </div>
                <div style='font-size: 0.9em;'>
                    <strong>🔥 Kalorie:</strong> ~1300-1800 kcal
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<div style='margin: 25px 0;'></div>", unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("""
            <div style='background: linear-gradient(135deg, #ff6b35 0%, #f7931e 100%); 
                        padding: 18px; 
                        border-radius: 12px; 
                        text-align: center;
                        box-shadow: 0 4px 15px rgba(255, 107, 53, 0.3);'>
                <div style='font-size: 2.2em; margin-bottom: 8px;'>🎯</div>
                <div style='color: white; font-weight: 700; font-size: 1em; margin-bottom: 8px;'>
                    Precyzyjne Przewidywanie
                </div>
                <div style='color: rgba(255, 255, 255, 0.9); font-size: 0.85em; line-height: 1.5;'>
                    Model AI wytrenowany na rzeczywistych danych z Półmaratonu Wrocławskiego
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div style='background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%); 
                        padding: 18px; 
                        border-radius: 12px; 
                        text-align: center;
                        box-shadow: 0 4px 15px rgba(17, 153, 142, 0.3);'>
                <div style='font-size: 2.2em; margin-bottom: 8px;'>📋</div>
                <div style='color: white; font-weight: 700; font-size: 1em; margin-bottom: 8px;'>
                    Plan Treningowy
                </div>
                <div style='color: rgba(255, 255, 255, 0.9); font-size: 0.85em; line-height: 1.5;'>
                    Otrzymasz 8-tygodniowy plan przygotowań dostosowany do Twoich możliwości
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown("""
            <div style='background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); 
                        padding: 18px; 
                        border-radius: 12px; 
                        text-align: center;
                        box-shadow: 0 4px 15px rgba(79, 172, 254, 0.3);'>
                <div style='font-size: 2.2em; margin-bottom: 8px;'>💪</div>
                <div style='color: white; font-weight: 700; font-size: 1em; margin-bottom: 8px;'>
                    Wskazówki Ekspertów
                </div>
                <div style='color: rgba(255, 255, 255, 0.9); font-size: 0.85em; line-height: 1.5;'>
                    Profesjonalne porady dotyczące żywienia, regeneracji i strategii wyścigu
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    if send_button and user_input:
        st.session_state["messages"].append({
            "role": "user",
            "content": user_input,
            "timestamp": datetime.now()
        })
        
        extracted_data = extract_user_data(user_input, api_key)
        
        has_new_data = extracted_data and (extracted_data.get('Płeć') or extracted_data.get('Wiek') or extracted_data.get('5 km Czas'))
        
        if has_new_data and st.session_state.get("show_prediction"):
            st.session_state["show_prediction"] = False
            st.session_state["prediction_data"] = None
            if "partial_user_data" in st.session_state:
                del st.session_state["partial_user_data"]
            
            welcome_message = st.session_state["messages"][0]
            new_user_message = st.session_state["messages"][-1]
            st.session_state["messages"] = [welcome_message, new_user_message]
        
        elif not has_new_data and st.session_state.get("show_prediction") and st.session_state.get("prediction_data"):
            with st.spinner("🤔 Myślę nad odpowiedzią..."):
                answer = answer_followup_question(
                    user_input, 
                    st.session_state["prediction_data"], 
                    api_key
                )
                
                st.session_state["messages"].append({
                    "role": "assistant",
                    "content": answer,
                    "timestamp": datetime.now()
                })
            
            st.rerun()
        
        if extracted_data:
                if "partial_user_data" in st.session_state:
                    previous_data = st.session_state["partial_user_data"]
                    for key in ['Płeć', 'Wiek', '5 km Czas']:
                        if not extracted_data.get(key) and previous_data.get(key):
                            extracted_data[key] = previous_data[key]
                
                missing_data = check_missing_data(extracted_data)
                
                if missing_data:
                    st.session_state["partial_user_data"] = extracted_data
                    
                    response = f"Widzę, że podałeś niektóre dane, ale brakuje mi jeszcze: **{', '.join(missing_data)}**.\n\n"
                    
                    if extracted_data.get('Płeć'):
                        response += f"✅ Płeć: {extracted_data['Płeć']}\n"
                    if extracted_data.get('Wiek'):
                        response += f"✅ Wiek: {extracted_data['Wiek']} lat\n"
                    if extracted_data.get('5 km Czas'):
                        response += f"✅ Czas na 5 km: {format_time(extracted_data['5 km Czas'])}\n"
                    
                    response += "\nProszę, uzupełnij brakujące informacje! 😊"
                    
                    st.session_state["messages"].append({
                        "role": "assistant",
                        "content": response,
                        "timestamp": datetime.now()
                    })
                else:
                    if "partial_user_data" in st.session_state:
                        del st.session_state["partial_user_data"]
                    
                    with st.spinner("Ładuję model predykcyjny..."):
                        try:
                            model = load_model()
                            if model is None:
                                st.session_state["messages"].append({
                                    "role": "assistant",
                                    "content": "❌ Nie mogę załadować modelu predykcyjnego. Sprawdź czy plik modelu istnieje.",
                                    "timestamp": datetime.now()
                                })
                                st.rerun()
                        except Exception as e:
                            st.session_state["messages"].append({
                                "role": "assistant",
                                "content": f"❌ Błąd podczas ładowania modelu: {e}",
                                "timestamp": datetime.now()
                            })
                            st.rerun()
                    
                    predicted_seconds = predict_time(extracted_data, model)
                    
                    if predicted_seconds:
                        response = f"""Świetnie! Mam wszystkie dane! 🎉

📊 **Twoje dane:**
• Płeć: {extracted_data['Płeć']}
• Wiek: {extracted_data['Wiek']} lat
• Czas na 5 km: {format_time(extracted_data['5 km Czas'])}

Generuję spersonalizowany plan treningowy... ⏳"""
                        
                        st.session_state["messages"].append({
                            "role": "assistant",
                            "content": response,
                            "timestamp": datetime.now()
                        })
                        
                        with st.spinner("Tworzę spersonalizowany plan treningowy..."):
                            training_plan = generate_personalized_training_plan(
                                extracted_data, 
                                predicted_seconds, 
                                api_key
                            )
                        
                        st.session_state["prediction_data"] = {
                            "user_data": extracted_data,
                            "predicted_time": predicted_seconds,
                            "training_plan": training_plan
                        }
                        st.session_state["show_prediction"] = True
                        
                        if training_plan:
                            st.session_state["messages"].append({
                                "role": "assistant",
                                "content": "✅ Gotowe! Oto Twoja analiza i spersonalizowany plan treningowy! 👇",
                                "timestamp": datetime.now()
                            })
                        else:
                            st.session_state["messages"].append({
                                "role": "assistant",
                                "content": "✅ Gotowe! Oto Twoja analiza i plan treningowy! 👇",
                                "timestamp": datetime.now()
                            })
                    else:
                        st.session_state["messages"].append({
                            "role": "assistant",
                            "content": "Przepraszam, wystąpił błąd podczas przewidywania czasu. Spróbuj ponownie! 😔",
                            "timestamp": datetime.now()
                        })
        elif not has_new_data and not st.session_state.get("show_prediction"):
            st.session_state["messages"].append({
                "role": "assistant",
                "content": "Hmm, nie mogłem wyłuskać danych z Twojej wiadomości. Spróbuj podać informacje w bardziej czytelny sposób! 🤔",
                "timestamp": datetime.now()
            })
        
        st.rerun()
    
    if len(st.session_state["messages"]) > 1:
        if st.button("🗑️ Wyczyść czat", key="clear_chat"):
            st.session_state["messages"] = [st.session_state["messages"][0]]
            st.session_state["show_prediction"] = False
            st.session_state["prediction_data"] = None
            st.rerun()
    
    if LANGFUSE_ENABLED and langfuse:
        try:
            langfuse.flush()
        except:
            pass

if __name__ == "__main__":
    main()
