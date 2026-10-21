# ==============================================================================
# Solar System Engine & Pricing Calculator - Streamlit Web Version
# Developed for: Eng. Murad
# ==============================================================================

import streamlit as st
import math

# ضبط إعدادات الصفحة
st.set_page_config(
    page_title="حاسبة ركن التعمير للطاقة الشمسية",
    page_icon="☀️",
    layout="centered"
)

# ------------------------------------------------------------------------------
# 1. سُلم الأسعار والمعايير المعتمدة (System Pricing Matrix & System Rules)
# ------------------------------------------------------------------------------

PANEL_SPECS = {
    "power_w": 640,
    "price_per_unit": 175,  # يشمل اللوح + الهيكل الحديدي + التوصيل والتركيب
    "max_string_size": 9,   # الحد الأقصى للألواح بالسلسلة الواحدة
}

DC_ACCESSORIES_PRICE_PER_STRING = 30  # 40m أسلاك DC + قاطع DC + فيوزات + MC4 + أنابيب

INVERTERS = [
    {"name": "Growatt 6 kW (IP21)", "power_kw": 6.0, "price": 400, "phase": "single"},
    {"name": "Deye / Solis 6 kW (IP65)", "power_kw": 6.0, "price": 1350, "phase": "single"},
    {"name": "Deye / Solis 8 kW (IP65)", "power_kw": 8.0, "price": 1550, "phase": "single"},
    {"name": "Deye 10 kW (IP65)", "power_kw": 10.0, "price": 1750, "phase": "single"},
    {"name": "Deye 12 kW Single Phase", "power_kw": 12.0, "price": 1900, "phase": "single"},
    {"name": "Deye High Voltage 30 kW 3-Phase", "power_kw": 30.0, "price": 3800, "phase": "three"},
    {"name": "Deye High Voltage 50 kW 3-Phase", "power_kw": 50.0, "price": 5200, "phase": "three"}
]

BATTERIES = [
    {"name": "AOKLY جدارية / أرضية", "capacity_kwh": 10.24, "price": 1350},
    {"name": "BICODI", "capacity_kwh": 12.0, "price": 1450},
    {"name": "AOKLY بعجلات", "capacity_kwh": 15.0, "price": 1700},
    {"name": "BICODI", "capacity_kwh": 16.1, "price": 1850},
    {"name": "BICODI", "capacity_kwh": 17.66, "price": 2100},
]

EARTHING_SYSTEM_PRICE = 160  # وتد نحاسي + أسلاك 30m + مادة تأريض + أجور الحفر والربط

# ------------------------------------------------------------------------------
# 2. الدوال والقواعد الحسابية (Engine Calculation Logic)
# ------------------------------------------------------------------------------

def get_ac_board_price(day_amp):
    if 8 <= day_amp <= 15:
        return 125
    elif 15 < day_amp <= 25:
        return 160
    elif 25 < day_amp <= 40:
        return 180
    elif 40 < day_amp <= 60:
        return 250
    elif 80 <= day_amp <= 120:
        return 350
    elif 120 < day_amp <= 150:
        return 450
    else:
        return 0


def calculate_battery_bank(night_amp, night_hours):
    required_kwh = night_amp * 0.285 * night_hours
    best_option = None
    min_diff = float('inf')
    
    for bat in BATTERIES:
        for qty in range(1, 11):
            total_cap = bat["capacity_kwh"] * qty
            if total_cap >= required_kwh:
                diff = total_cap - required_kwh
                if diff < min_diff:
                    min_diff = diff
                    best_option = {
                        "model": bat["name"],
                        "unit_cap": bat["capacity_kwh"],
                        "total_cap": total_cap,
                        "qty": qty,
                        "price": bat["price"]
                    }
                break
                
    return required_kwh, best_option


def calculate_panels(day_amp, required_battery_kwh):
    day_power_w = day_amp * 230 * 1.3
    day_panels_exact = day_power_w / PANEL_SPECS["power_w"]
    
    charging_power_w = (required_battery_kwh * 1000) / 9.0
    charging_panels_exact = charging_power_w / PANEL_SPECS["power_w"]
    
    total_panels_raw = day_panels_exact + charging_panels_exact
    target_panels = math.ceil(total_panels_raw)
    
    min_strings = math.ceil(target_panels / PANEL_SPECS["max_string_size"])
    
    for num_strings in range(min_strings, 100):
        panels_per_string = math.ceil(target_panels / num_strings)
        if panels_per_string <= PANEL_SPECS["max_string_size"]:
            final_panel_count = panels_per_string * num_strings
            return {
                "day_power_w": day_power_w,
                "day_panels_exact": day_panels_exact,
                "charging_power_w": charging_power_w,
                "charging_panels_exact": charging_panels_exact,
                "total_panels_raw": total_panels_raw,
                "total_panels": final_panel_count,
                "strings_count": num_strings,
                "panels_per_string": panels_per_string
            }


def select_inverter(day_amp, is_hv_3ph=False):
    load_kw = (day_amp * 230) / 1000.0
    required_kw_with_safety = load_kw * 1.2
    target_phase = "three" if is_hv_3ph else "single"
    
    for inv in INVERTERS:
        if inv["power_kw"] >= required_kw_with_safety and inv["phase"] == target_phase:
            return inv, load_kw, required_kw_with_safety
            
    return INVERTERS[-1], load_kw, required_kw_with_safety


# ------------------------------------------------------------------------------
# 3. واجهة المستخدم على Streamlit (Web Interface)
# ------------------------------------------------------------------------------

st.title("☀️ شركة ركن التعمير للطاقة الشمسية")
st.subheader("حاسبة وتصحيح المنظومات الشمسية - إعداد المهندس مراد")
st.markdown("---")

st.sidebar.header("⚙️ إدخال بيانات المنظومة")
day_amp = st.sidebar.number_input("أمبير النهار (A):", min_value=1, max_value=300, value=20)
night_amp = st.sidebar.number_input("أمبير الليل (A):", min_value=1, max_value=300, value=10)
night_hours = st.sidebar.number_input("ساعات التفريغ الليلي:", min_value=1, max_value=24, value=4)
system_type = st.sidebar.selectbox("نوع النظام:", ["LV-Single Phase", "HV-3Phase"])

if st.sidebar.button("🧮 احسب المنظومة وأظهر التقرير", type="primary"):
    is_hv_3ph = True if "HV-3PH" in system_type.upper() else False
    
    req_kwh, bat = calculate_battery_bank(night_amp, night_hours)
    p_info = calculate_panels(day_amp, req_kwh)
    inverter, load_kw, req_inv_kw = select_inverter(day_amp, is_hv_3ph)
    ac_board_cost = get_ac_board_price(day_amp)
    
    panels_cost = p_info["total_panels"] * PANEL_SPECS["price_per_unit"]
    dc_acc_cost = p_info["strings_count"] * DC_ACCESSORIES_PRICE_PER_STRING
    inv_cost = inverter["price"]
    bat_cost = bat["price"] * bat["qty"]
    
    total_cost = panels_cost + dc_acc_cost + inv_cost + bat_cost + ac_board_cost + EARTHING_SYSTEM_PRICE

    st.success("✅ تم احتساب المنظومة وإعداد التقرير بنجاح!")
    
    st.markdown(f"### 📊 التقرير الفني الشامل للمنظومة: (`{day_amp}A` نهارا، `{night_amp}A` ليلا، `{night_hours}` ساعات)")
    
    st.markdown("---")
    st.markdown("#### 1️⃣ التفاصيل الرياضية:")
    st.markdown(f"""
    - **بنك البطاريات:** استهلاك `{req_kwh:.2f} kWh` ⟵ مختار `{bat['qty']} × {bat['model']}` (سعة إجمالية `{bat['total_cap']:.2f} kWh`)
    - **الألواح الشمسية (640W):** ألواح نهار `{p_info['day_power_w']:.1f}W` + ألواح شحن `{p_info['charging_power_w']:.1f}W` ⟵ توزيع `{p_info['total_panels']}` لوح (`{p_info['strings_count']}` سلاسل × `{p_info['panels_per_string']}` ألواح).
    - **العاكس الهجين:** حمل `{load_kw:.2f} kW` مع هامش الأمان ⟵ `{inverter['name']}`.
    - **بورد الـ AC والتأريض:** بورد أمبيرية `{day_amp}A` + منظومة تأريض كاملة.
    """)
    
    st.markdown("---")
    st.markdown("#### 2️⃣ جدول المواد والتفاصيل (Bill of Materials):")
    
    st.markdown(f"""
| المكون / الملحق | المواصفات والوصف الفني | الكمية | الإجمالي ($ |
| :--- | :--- | :---: | :---: |
| **الألواح الشمسية** | لوح 640W (شامل الهيكل والتركيب) | {p_info['total_panels']} | ${panels_cost:,} |
| **ملحقات الـ DC** | أسلاك 40m + قاطع + فيوزات + MC4 | {p_info['strings_count']} سلاسل | ${dc_acc_cost:,} |
| **العاكس الهجين** | {inverter['name']} | 1 | ${inv_cost:,} |
| **بنك البطاريات** | {bat['model']} Low Voltage | {bat['qty']} | ${bat_cost:,} |
| **بورد الـ AC** | بورد حماية لغاية {day_amp}A | 1 | ${ac_board_cost:,} |
| **منظومة التأريض** | وتد نحاسي وسلك وحفر وترابط | 1 | ${EARTHING_SYSTEM_PRICE:,} |
    """)
    
    st.markdown("---")
    st.markdown(f"## 💰 الكلفة الإجمالية النهائية للمشروع: **${total_cost:,}**")

else:
    st.info("👈 يرجى إدخال القيم المطلوبة في القائمة الجانبية باليمين ثم الضغط على زر **احسب المنظومة** لعرض النتائج.")
