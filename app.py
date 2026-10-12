import streamlit as st
import math

# ------------------------------------------------------------------------------
ضبط إعدادات الصفحة
# ------------------------------------------------------------------------------
st.set_page_config(
    page_title="حاسبة ركن التعمير للطاقة الشمسية",
    page_icon="☀️",
    layout="centered"
)

# ------------------------------------------------------------------------------
1. سُلم الأسعار والمعايير الفنية المعتمدة
# ------------------------------------------------------------------------------

PANEL_SPECS = {
    "power_w": 640,
    "price_per_unit": 175,  # شامل الهيكل والتركيب
    "max_string_size": 9,   # الحد الأقصى للألواح بالسلسلة الواحدة
}

DC_ACCESSORIES_PRICE_PER_STRING = 30  # أسلاك + قاطع DC + فيوزات + MC4

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

EARTHING_SYSTEM_PRICE = 160


# ------------------------------------------------------------------------------
2. الدوال الحسابية
# ------------------------------------------------------------------------------

def get_ac_board_price(current_amp):
    if 8 <= current_amp <= 15:
        return 125
    elif 15 < current_amp <= 25:
        return 160
    elif 25 < current_amp <= 40:
        return 180
    elif 40 < current_amp <= 60:
        return 250
    elif 80 <= current_amp <= 120:
        return 350
    elif 120 < current_amp <= 150:
        return 450
    else:
        return 0


def calculate_battery_bank(night_current, night_hours):
    required_kwh = night_current * 0.285 * night_hours
    best_option = None
    min_diff = float('inf')
    
    for bat in BATTERIES:
        if bat["capacity_kwh"] >= required_kwh:
            diff = bat["capacity_kwh"] - required_kwh
            if diff < min_diff:
                min_diff = diff
                best_option = {"model": bat["name"], "capacity": bat["capacity_kwh"], "qty": 1, "price": bat["price"]}
        elif (bat["capacity_kwh"] * 2) >= required_kwh:
            diff = (bat["capacity_kwh"] * 2) - required_kwh
            if diff < min_diff:
                min_diff = diff
                best_option = {"model": bat["name"], "capacity": bat["capacity_kwh"], "qty": 2, "price": bat["price"]}
                
    return required_kwh, best_option


def calculate_panels(day_current, required_battery_kwh):
    day_power_w = day_current * 230 * 1.3
    day_panels_exact = day_power_w / PANEL_SPECS["power_w"]
    
    charging_power_w = (required_battery_kwh * 1000) / 9.0
    charging_panels_exact = charging_power_w / PANEL_SPECS["power_w"]
    
    total_panels_raw = day_panels_exact + charging_panels_exact
    target_panels = math.ceil(total_panels_raw)
    
    for num_strings in range(1, 10):
        panels_per_string = math.ceil(target_panels / num_strings)
        if panels_per_string <= PANEL_SPECS["max_string_size"]:
            final_panel_count = panels_per_string * num_strings
            return {
                "total_panels": final_panel_count,
                "strings_count": num_strings,
                "panels_per_string": panels_per_string
            }
    return {"total_panels": target_panels, "strings_count": 1, "panels_per_string": target_panels}


def select_inverter(day_current):
    load_kw = (day_current * 230) / 1000.0
    required_kw_with_safety = load_kw * 1.2
    
    for inv in INVERTERS:
        if inv["power_kw"] >= required_kw_with_safety and inv["phase"] == "single":
            return inv
    return INVERTERS[-1]


# ------------------------------------------------------------------------------
3. واجهة المستخدم على Streamlit
# ------------------------------------------------------------------------------

st.title("☀️ شركة ركن التعمير للطاقة الشمسية")
st.subheader("حاسبة وتصحيح المنظومات الشمسية - إعداد المهندس مراد")
st.markdown("---")

st.sidebar.header("⚙️ إدخال الأحمال الكهربائية")
day_amp = st.sidebar.number_input("أمبير النهار (A):", min_value=1, max_value=200, value=40)
night_amp = st.sidebar.number_input("أمبير الليل (A):", min_value=1, max_value=200, value=30)
night_hours = st.sidebar.number_input("ساعات الليل (ساعة):", min_value=1, max_value=24, value=4)

if st.sidebar.button("🧮 احسب المنظومة وأظهر التقرير", type="primary"):
    req_kwh, bat_selected = calculate_battery_bank(night_amp, night_hours)
    panels_info = calculate_panels(day_amp, req_kwh)
    inverter = select_inverter(day_amp)
    ac_board_cost = get_ac_board_price(day_amp)
    
    panels_cost = panels_info["total_panels"] * PANEL_SPECS["price_per_unit"]
    dc_acc_cost = panels_info["strings_count"] * DC_ACCESSORIES_PRICE_PER_STRING
    inv_cost = inverter["price"]
    bat_cost = bat_selected["price"] * bat_selected["qty"]
    
    total_cost = panels_cost + dc_acc_cost + inv_cost + bat_cost + ac_board_cost + EARTHING_SYSTEM_PRICE
    
    st.success("✅ تم حساب المنظومة بنجاح!")
    
    st.markdown(f"### 📊 التقرير الفني وعرض السعر للمنظومة: (`{day_amp}A` نهارا، `{night_amp}A` ليلا، `{night_hours}` ساعات)")
    
    # عرض النتائج في جدول أو مربعات منسقة
    st.markdown(f"""
    - **1. بنك البطاريات:** {bat_selected['qty']}x {bat_selected['model']} (`{bat_selected['capacity']} kWh`) ⟵ **${bat_cost}**
    - **2. الألواح الشمسية:** {panels_info['total_panels']} لوح (`{panels_info['strings_count']}` سلاسل × `{panels_info['panels_per_string']}` ألواح) ⟵ **${panels_cost}**
    - **3. ملحقات الـ DC:** {panels_info['strings_count']} سلاسل ⟵ **${dc_acc_cost}**
    - **4. العاكس الهجين:** {inverter['name']} ⟵ **${inv_cost}**
    - **5. بورد الـ AC:** أمبيرية (`{day_amp}A`) ⟵ **${ac_board_cost if ac_board_cost > 0 else 'تقدير مهندس'}**
    - **6. منظومة التأريض:** ثابتة وشاملة ⟵ **${EARTHING_SYSTEM_PRICE}**
    """)
    
    st.markdown("---")
    st.markdown(f"## 💰 الإجمالي النهائي المباشر للمشروع: **${total_cost}**")
else:
    st.info("👈 يرجى إدخال القيم في القائمة الجانبية ثم الضغط على زر **احسب المنظومة** لعرض التقرير والتسعير.")
