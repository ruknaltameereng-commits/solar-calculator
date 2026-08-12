import streamlit as st
import math

# ==========================================
# 1. إعدادات الصفحة
# ==========================================
st.set_page_config(
    page_title="حاسبة المنظومات الشمسية - المهندس مراد",
    page_icon="☀️",
    layout="wide"
)

# ==========================================
# 2. سُلم الأسعار والمعايير الفنية M3
# ==========================================
PANEL_SPECS = {
    "power_w": 640,
    "price_per_unit": 175,
    "max_string_size": 9,
}

DC_ACCESSORIES_PRICE_PER_STRING = 30
EARTHING_SYSTEM_PRICE = 160

INVERTERS = [
    {"name": "Growatt 6 kW Single Phase (IP21)", "power_kw": 6.0, "price": 400, "phase": "single"},
    {"name": "Deye / Solis 6 kW Single Phase (IP65)", "power_kw": 6.0, "price": 1350, "phase": "single"},
    {"name": "Deye / Solis 8 kW Single Phase (IP65)", "power_kw": 8.0, "price": 1550, "phase": "single"},
    {"name": "Deye 10 kW Single Phase (IP65)", "power_kw": 10.0, "price": 1750, "phase": "single"},
    {"name": "Deye 12 kW Single Phase", "power_kw": 12.0, "price": 1900, "phase": "single"},
    {"name": "Deye High Voltage 30 kW 3-Phase (HV-3PH)", "power_kw": 30.0, "price": 3800, "phase": "three"},
    {"name": "Deye High Voltage 50 kW 3-Phase (HV-3PH)", "power_kw": 50.0, "price": 5200, "phase": "three"}
]

BATTERIES = [
    {"name": "AOKLY جدارية / أرضية", "capacity_kwh": 10.24, "price": 1350},
    {"name": "BICODI", "capacity_kwh": 12.0, "price": 1450},
    {"name": "AOKLY بعجلات", "capacity_kwh": 15.0, "price": 1700},
    {"name": "BICODI", "capacity_kwh": 16.1, "price": 1850},
    {"name": "BICODI", "capacity_kwh": 17.66, "price": 2100},
]

# ==========================================
# 3. الدوال الحسابية
# ==========================================
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
        elif (bat["capacity_kwh"] * 3) >= required_kwh:
            diff = (bat["capacity_kwh"] * 3) - required_kwh
            if diff < min_diff:
                min_diff = diff
                best_option = {"model": bat["name"], "capacity": bat["capacity_kwh"], "qty": 3, "price": bat["price"]}
                
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
                "day_panels_exact": day_panels_exact,
                "charging_panels_exact": charging_panels_exact,
                "total_panels_raw": total_panels_raw,
                "total_panels": final_panel_count,
                "strings_count": num_strings,
                "panels_per_string": panels_per_string
            }

def select_inverter(day_current, is_hv_3ph):
    load_kw = (day_current * 230) / 1000.0
    required_kw_with_safety = load_kw * 1.2
    
    target_phase = "three" if is_hv_3ph else "single"
    
    for inv in INVERTERS:
        if inv["power_kw"] >= required_kw_with_safety and inv["phase"] == target_phase:
            return inv, load_kw, required_kw_with_safety
    
    # في حال تجاوز القدرة المتاحة
    filtered = [i for i in INVERTERS if i["phase"] == target_phase]
    return filtered[-1], load_kw, required_kw_with_safety

# ==========================================
# 4. واجهة المستخدم (User Interface)
# ==========================================
st.title("☀️ حاسبة وتصميم المنظومات الشمسية")
st.caption("إعداد المهندس مراد - حساب وتكلفة المكونات تلقائياً")

st.markdown("---")

# إدخال البيانات
col1, col2, col3 = st.columns(3)

with col1:
    day_amp = st.number_input("أمبير النهار (ن)", min_value=1, max_value=200, value=20, step=1)

with col2:
    night_amp = st.number_input("أمبير الليل (ل)", min_value=1, max_value=200, value=10, step=1)

with col3:
    night_hours = st.number_input("ساعات التشغيل الليلي (س)", min_value=1, max_value=24, value=4, step=1)

is_hv_3ph = st.checkbox("تطبيق نظام HV-3PH (ثلاثي الأطوار / High Voltage)", value=False)

st.markdown("---")

if st.button("🚀 احسب المنظومة الآن", type="primary", use_container_width=True):
    # الحسابات
    req_kwh, bat_selected = calculate_battery_bank(night_amp, night_hours)
    panels_info = calculate_panels(day_amp, req_kwh)
    inverter, load_kw, required_kw_with_safety = select_inverter(day_amp, is_hv_3ph)
    ac_board_cost = get_ac_board_price(day_amp)
    
    panels_cost = panels_info["total_panels"] * PANEL_SPECS["price_per_unit"]
    dc_acc_cost = panels_info["strings_count"] * DC_ACCESSORIES_PRICE_PER_STRING
    inv_cost = inverter["price"]
    bat_cost = bat_selected["price"] * bat_selected["qty"]
    total_cost = panels_cost + dc_acc_cost + inv_cost + bat_cost + ac_board_cost + EARTHING_SYSTEM_PRICE
    
    # 1. التفاصيل الرياضية
    st.subheader("1️⃣ الخطوات والتفاصيل الرياضية")
    
    with st.expander("عرض التفاصيل الرياضية الحسابية", expanded=True):
        st.write(f"**أ. بنك البطاريات:**")
        st.write(f"- الطاقة المطلوبة ليلاً: `{night_amp}A × 0.285 × {night_hours}h` = **{req_kwh:.2f} kWh**")
        st.write(f"- الاختيار المعتمد: **{bat_selected['qty']}x {bat_selected['model']} ({bat_selected['capacity']} kWh)** بسعة إجمالية `{bat_selected['capacity'] * bat_selected['qty']} kWh`.")
        
        st.write(f"**ب. الألواح الشمسية (640W):**")
        st.write(f"- ألواح الحمل النهاري: `{panels_info['day_panels_exact']:.2f}` لوح")
        st.write(f"- ألواح شحن البطارية: `{panels_info['charging_panels_exact']:.2f}` لوح")
        st.write(f"- المجموع النظري: `{panels_info['total_panels_raw']:.2f}` لوح")
        st.write(f"- التقريب وتوزيع السلاسل المتساوي: **{panels_info['total_panels']} لوحاً** موزعة على **{panels_info['strings_count']} سلاسل × {panels_info['panels_per_string']} ألواح/سلسلة**.")
        
        st.write(f"**ج. العاكس الهجين:**")
        st.write(f"- حمل النهار الصافي: `{load_kw:.2f} kW` | مع هامش أمان (+20%): `{required_kw_with_safety:.2f} kW`")
        st.write(f"- العاكس المعتمد: **{inverter['name']}**")

    # 2. جدول المواد
    st.subheader("2️⃣ جدول المواد والتفاصيل")
    
    table_data = [
        {"المكون / الملحق": "الألواح الشمسية", "المواصفات والوصف": "لوح 640W (شامل الهيكل والتركيب)", "الكمية": f"{panels_info['total_panels']} لوحاً", "سعر الوحدة ($)": f"${PANEL_SPECS['price_per_unit']}", "الإجمالي ($)": f"${panels_cost}"},
        {"المكون / الملحق": "ملحقات الـ DC", "المواصفات والوصف": "أسلاك 40m + قاطع DC + فيوزات + MC4 + أنابيب", "الكمية": f"{panels_info['strings_count']} سلاسل", "سعر الوحدة ($)": f"${DC_ACCESSORIES_PRICE_PER_STRING}", "الإجمالي ($)": f"${dc_acc_cost}"},
        {"المكون / الملحق": "العاكس الهجين", "المواصفات والوصف": inverter["name"], "الكمية": "1", "سعر الوحدة ($)": f"${inv_cost}", "الإجمالي ($)": f"${inv_cost}"},
        {"المكون / الملحق": "بنك البطاريات", "المواصفات والوصف": f"{bat_selected['model']} ({bat_selected['capacity']} kWh)", "الكمية": f"{bat_selected['qty']}", "سعر الوحدة ($)": f"${bat_selected['price']}", "الإجمالي ($)": f"${bat_cost}"},
        {"المكون / الملحق": "بورد الـ AC", "المواصفات والوصف": f"بورد حماية AC لغاية ({day_amp}A)", "الكمية": "1", "سعر الوحدة ($)": f"${ac_board_cost}", "الإجمالي ($)": f"${ac_board_cost}"},
        {"المكون / الملحق": "منظومة التأريض", "المواصفات والوصف": "وتد نحاسي + أسلاك 30m + مادة تأريض + الحفر والربط", "الكمية": "1", "سعر الوحدة ($)": f"${EARTHING_SYSTEM_PRICE}", "الإجمالي ($)": f"${EARTHING_SYSTEM_PRICE}"},
    ]
    
    st.table(table_data)

    # 3. الكلفة الإجمالية
    st.subheader("3️⃣ الكلفة الإجمالية النهائية")
    st.success(f"💰 **الكلفة الإجمالية المباشرة للمشروع: ${total_cost:,}**")
