def safe_divide(a, b):
    if b == 0:
        return 0
    return a / b


def calculate_z_score(data):
    x1 = safe_divide(data["working_capital"], data["total_assets"])
    x2 = safe_divide(data["retained_earnings"], data["total_assets"])
    x3 = safe_divide(data["ebit"], data["total_assets"])
    x4 = safe_divide(data["market_value_equity"], data["total_liabilities"])
    x5 = safe_divide(data["sales"], data["total_assets"])
    z_score = 1.2 * x1 + 1.4 * x2 + 3.3 * x3 + 0.6 * x4 + x5
    return {
        "x1": round(x1, 4),
        "x2": round(x2, 4),
        "x3": round(x3, 4),
        "x4": round(x4, 4),
        "x5": round(x5, 4),
        "z_score": round(z_score, 4),
    }


def classify_zone(z_score):
    if z_score > 2.9:
        return "Safe"
    if z_score >= 1.8:
        return "Grey Zone"
    return "Distress"


def build_features(data, values):
    return {
        "z_score": values["z_score"],
        "working_capital_to_assets": values["x1"],
        "retained_earnings_to_assets": values["x2"],
        "ebit_to_assets": values["x3"],
        "market_value_to_liabilities": values["x4"],
        "sales_to_assets": values["x5"],
        "debt_to_assets": safe_divide(data["total_liabilities"], data["total_assets"]),
        "debt_to_market_value": safe_divide(data["total_liabilities"], data["market_value_equity"]),
    }


def fallback_risk(features):
    risk = 50
    risk -= features["z_score"] * 9
    risk += features["debt_to_assets"] * 32
    risk += max(0, -features["working_capital_to_assets"]) * 55
    risk += max(0, -features["ebit_to_assets"]) * 80
    risk -= max(0, features["ebit_to_assets"]) * 22
    risk -= min(features["market_value_to_liabilities"], 3) * 5
    return round(max(1, min(99, risk)), 2)


def risk_level(risk):
    if risk < 30:
        return "Nizak rizik"
    if risk < 60:
        return "Srednji rizik"
    return "Visok rizik"


def recommendation(risk):
    if risk < 30:
        return "Kompanija je finansijski stabilna i može se razmotriti odobrenje."
    if risk < 60:
        return "Potrebna je dodatna provjera prije donošenja kreditne odluke."
    return "Preporučuje se oprez, dodatne garancije ili odbijanje zahtjeva."


def explain(features):
    messages = []

    if features["working_capital_to_assets"] < 0:
        messages.append("Negativan obrtni kapital ukazuje na slabiju kratkoročnu likvidnost.")
    elif features["working_capital_to_assets"] > 0.15:
        messages.append("Dobar odnos obrtnog kapitala i aktive pozitivno utiče na stabilnost.")

    if features["ebit_to_assets"] < 0.03:
        messages.append("Niska operativna profitabilnost povećava rizik poslovanja.")
    elif features["ebit_to_assets"] > 0.1:
        messages.append("Profitabilnost kompanije smanjuje procijenjeni rizik.")

    if features["debt_to_assets"] > 0.75:
        messages.append("Visok odnos obaveza i aktive ukazuje na veću zaduženost.")
    elif features["debt_to_assets"] < 0.45:
        messages.append("Niži nivo zaduženosti pozitivno utiče na procjenu rizika.")

    if features["market_value_to_liabilities"] < 0.5:
        messages.append("Tržišna vrijednost kapitala slabo pokriva ukupne obaveze.")
    elif features["market_value_to_liabilities"] > 1.5:
        messages.append("Tržišna vrijednost kapitala dobro pokriva obaveze kompanije.")

    if not messages:
        messages.append("Kompanija ima mješovite pokazatelje i potrebna je dodatna analiza.")

    return messages


def analyze_company(data, ml_predictor=None):
    values = calculate_z_score(data)
    features = build_features(data, values)
    ml_risk = ml_predictor(features) if ml_predictor else None
    risk = ml_risk if ml_risk is not None else fallback_risk(features)

    return {
        "company_name": data["company_name"],
        "z_score": round(values["z_score"], 2),
        "zone": classify_zone(values["z_score"]),
        "risk_percent": round(risk, 2),
        "risk_level": risk_level(risk),
        "recommendation": recommendation(risk),
        "explanation": explain(features),
        "indicators": values,
        "features": {key: round(value, 4) for key, value in features.items()},
    }
