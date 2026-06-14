# CreditScoreAnalyser - Digitalni kreditni službenik

CreditScoreAnalyser je web aplikacija za procjenu finansijskog rizika kompanija. Sistem kombinuje klasični Altman Z-Score pristup i jednostavni model mašinskog učenja kako bi kreditnom analitičaru dao brzu procjenu da li je kompanija stabilna, u sivoj zoni ili rizična.

## Problem

Banke, investicioni fondovi i kreditni analitičari često moraju brzo da procijene finansijsko stanje kompanije. Ručna analiza finansijskih izvještaja traje dugo, posebno kada se posmatra veći broj klijenata. Cilj ovog projekta je da se taj proces ubrza kroz aplikaciju koja automatski računa finansijske pokazatelje i prikazuje rezultat u preglednom dashboardu.

## Glavne funkcionalnosti

- Ručni unos finansijskih podataka jedne kompanije
- Upload CSV ili Excel fajla sa više kompanija
- Računanje originalnog Altman Z-Score-a
- Klasifikacija kompanije u Safe, Grey Zone ili Distress zonu
- Procjena rizika u procentima pomoću ML modela
- Objašnjenje najvažnijih faktora rizika
- Portfolio tabela sa pregledom više kompanija
- Vizuelni prikaz raspodjele rizika
- API dokumentacija kroz FastAPI Swagger interfejs

## Metodologija

Sistem prvo računa Altman Z-Score:

```text
Z = 1.2X1 + 1.4X2 + 3.3X3 + 0.6X4 + 1.0X5
```

Gdje su:

```text
X1 = Working Capital / Total Assets
X2 = Retained Earnings / Total Assets
X3 = EBIT / Total Assets
X4 = Market Value of Equity / Total Liabilities
X5 = Sales / Total Assets
```

Klasifikacija:

```text
Z > 2.9        Safe
1.8 - 2.9      Grey Zone
Z < 1.8        Distress
```

Pored toga, koristi se Random Forest model koji koristi izvedene finansijske pokazatelje:

```text
z_score
working_capital_to_assets
retained_earnings_to_assets
ebit_to_assets
market_value_to_liabilities
sales_to_assets
debt_to_assets
debt_to_market_value
```

Model daje dodatnu procjenu rizika u procentima. U ovoj verziji dataset je pripremljen za demonstraciju rada sistema i može se zamijeniti javnim datasetom kompanija za ozbiljniju produkcionu primjenu.

## Tehnologije

```text
Backend: FastAPI, Python, pandas, scikit-learn
Frontend: HTML, CSS, JavaScript
ML: RandomForestClassifier
Data: CSV / Excel
Server: uvicorn
```

## Struktura projekta

```text
CreditGuard_Final/
│
├── backend/
│   ├── requirements.txt
│   ├── data/
│   │   └── training_companies.csv
│   └── app/
│       ├── __init__.py
│       ├── main.py
│       ├── ml_model.py
│       ├── schemas.py
│       └── scoring.py
│
├── frontend/
│   ├── index.html
│   ├── style.css
│   └── script.js
│
├── data/
│   └── sample_companies.csv
│
├── README.md
└── .gitignore
```

## Pokretanje aplikacije lokalno

### 1. Pokretanje backend-a

U terminalu uđi u backend folder:

```powershell
cd backend
```

Napravi virtualno okruženje:

```powershell
python -m venv venv
```

Aktiviraj okruženje:

```powershell
.\venv\Scripts\Activate.ps1
```

Ako PowerShell blokira aktivaciju, privremeno dozvoli skripte samo za taj prozor:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\venv\Scripts\Activate.ps1
```

Instaliraj biblioteke:

```powershell
pip install -r requirements.txt
```

Pokreni server:

```powershell
python -m uvicorn app.main:app --reload
```

Backend radi na:

```text
http://127.0.0.1:8000
```

API dokumentacija:

```text
http://127.0.0.1:8000/docs
```

### 2. Pokretanje frontend-a

Otvori drugi terminal i uđi u frontend folder:

```powershell
cd frontend
```

Pokreni lokalni server:

```powershell
python -m http.server 5500
```

Frontend radi na:

```text
http://127.0.0.1:5500
```

## Primjer CSV fajla

U projektu postoji fajl:

```text
data/sample_companies.csv
```

Taj fajl može odmah da se učita kroz upload dio aplikacije.

Potrebne kolone su:

```text
company_name
working_capital
total_assets
retained_earnings
ebit
market_value_equity
total_liabilities
sales
```

## Objašnjenje rezultata

Aplikacija za svaku kompaniju prikazuje:

- Altman Z-Score
- zonu rizika
- procenat ML rizika
- nivo rizika
- preporuku
- objašnjenje glavnih faktora koji utiču na rezultat

Primjer tumačenja:

```text
Kompanija sa visokim dugom, slabom profitabilnošću i negativnim obrtnim kapitalom dobija viši procenat rizika. Kompanija sa dobrim Z-Score-om, stabilnom profitabilnošću i manjim dugom dobija niži procenat rizika.
```

## Zaključak

CreditScoreAnalyser pokazuje kako se tradicionalna finansijska analiza može povezati sa mašinskim učenjem i web aplikacijom. Alat je koristan za brzu preliminarnu procjenu rizika i može se proširiti dodatnim datasetima, naprednijim modelima, SHAP objašnjenjima i deploy-om na cloud platformu.
