# ==============================================================================
# Solar System Engine & Pricing Calculator - Streamlit Web Version
# Developed for: Eng. Murad
# ==============================================================================

import math
import streamlit as st

# ------------------------------------------------------------------------------
# 1. إعدادات الصفحة وسُلم الأسعار المعايير المعتمدة
# ------------------------------------------------------------------------------

st.set_page_config(page_title="حاسبة المنظومات الشمسية", page_icon="☀️", layout="wide")

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

EARTHING_SYSTEM_PRICE = 160  # وتد نحاسي + أسلاك 30m + مادة تأريض + الحفر والربط

# ------------------------------------------------------------------------------
# 2. الدوال والحسابات الفنية
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
# 3. واجهة المستخدم والتفاعل (Streamlit UI)
# ------------------------------------------------------------------------------

st.title("☀️ حاسبة وتصميم المنظومات الشمسية")
st.subheader("إعداد ودراسة التكلفة الفنية المباشرة - المهندس مراد")

st.markdown("---")

col1, col2, col3 = st.columns(3)
with col1:
    day_amp = st.number_input("أمبيرية النهار (A)", min_value=1, value=20, step=1)
with col2:
    night_amp = st.number_input("أمبيرية الليل (A)", min_value=0, value=10, step=1)
with col3:
    night_hours = st.number_input("ساعات التشغيل الليلي (ساعة)", min_value=0.0, value=4.0, step=0.5)

sys_type = st.radio("نوع النظام الفني:", ["Low Voltage Single Phase (L-VOLT)", "High Voltage 3-Phase (HV-3PH)"])
is_hv_3ph = True if "HV-3PH" in sys_type else False

if st.button("🚀 احسب المنظومة والتكلفة"):
    req_kwh, bat = calculate_battery_bank(night_amp, night_hours)
    p_info = calculate_panels(day_amp, req_kwh)
    inverter, load_kw, req_inv_kw = select_inverter(day_amp, is_hv_3ph)
    ac_board_cost = get_ac_board_price(day_amp)
    
    panels_cost = p_info["total_panels"] * PANEL_SPECS["price_per_unit"]
    dc_acc_cost = p_info["strings_count"] * DC_ACCESSORIES_PRICE_PER_STRING
    inv_cost = inverter["price"]
    bat_cost = bat["price"] * bat["qty"]
    total_cost = panels_cost + dc_acc_cost + inv_cost + bat_cost + ac_board_cost + EARTHING_SYSTEM_PRICE

    st.markdown("---")
    st.header(f"📊 التقرير الفني للمنظومة: ({day_amp}ن {night_amp}ل {night_hours}س)")

    st.subheader("1️⃣ الخطوات والتفاصيل الرياضية")
    
    st.write(f"**أ. بنك البطاريات:**")
    st.write(f"- الطاقة المطلوبة: `{night_amp}A × 0.285 × {night_hours}h = {req_kwh:.2f} kWh`")
    st.write(f"- البطاريات المختارة: **{bat['qty']} × {bat['model']}** (السعة الكلية: {bat['total_cap']:.2f} kWh)")
    
    st.write(f"**ب. الألواح الشمسية (640W):**")
    st.write(f"- ألواح النهار ({day_amp}A): `{p_info['day_power_w']:.1f} W` ➔ **{p_info['day_panels_exact']:.3f} لوح**")
    st.write(f"- ألواح الشحن ({req_kwh:.2f} kWh): `{p_info['charging_power_w']:.1f} W` ➔ **{p_info['charging_panels_exact']:.3f} لوح**")
    st.write(f"- المجموع النظري: **{p_info['total_panels_raw']:.3f} لوح**")
    st.success(f"توزيع السلاسل المعتمد: **{p_info['total_panels']} لوحاً** = **{p_info['strings_count']} سلاسل × {p_info['panels_per_string']} ألواح/سلسلة** (تساوي تام)")
    
    st.write(f"**ج. العاكس الهجين:**")
    st.write(f"- قدرة الحمل: `{load_kw:.2f} kW` + هامش أمان (+20%) = `{req_inv_kw:.2f} kW`")
    st.write(f"- العاكس المعتمد: **{inverter['name']}**")

    st.subheader("2️⃣ جدول المواد والتكلفة (Bill of Materials)")
    
    ac_board_text = f"${ac_board_cost}" if ac_board_cost > 0 else "تقدير المهندس"
    bat_desc = f"{bat['model']} Low Voltage"
    
    bom_data = [
        {"المكون": "الألواح الشمسية", "الوصف الفني": "لوح 640W (شامل الهيكل والتركيب)", "الكمية": f"{p_info['total_panels']} لوحاً", "الإجمالي": f"${panels_cost}"},
        {"المكون": "ملحقات الـ DC", "الوصف الفني": "أسلاك 40m + قاطع + فيوزات + MC4", "الكمية": f"{p_info['strings_count']} سلاسل", "الإجمالي": f"${dc_acc_cost}"},
        {"المكون": "العاكس الهجين", "الوصف الفني": inverter['name'], "الكمية": "1", "الإجمالي": f"${inv_cost}"},
        {"المكون": "بنك البطاريات", "الوصف الفني": bat_desc, "الكمية": str(bat['qty']), "الإجمالي": f"${bat_cost}"},
        {"المكون": "بورد الـ AC", "الوصف الفني": f"بورد حماية (لغاية {day_amp}A)", "الكمية": "1", "الإجمالي": ac_board_text},
        {"المكون": "منظومة التأريض", "الوصف الفني": "شاملة وتد نحاسي وسلك وحفر", "الكمية": "1", "الإجمالي": f"${EARTHING_SYSTEM_PRICE}"},
    ]
    st.table(bom_data)

    st.markdown("---")
    st.metric(label="💰 الكلفة الإجمالية النهائية المباشرة للمشروع", value=f"${total_cost:,}")
