import streamlit as st
import math

# ==========================================
# 1. إعدادات الصفحة
# ==========================================
st.set_page_config(
    page_title="RUK calculator - المهندس محمد",
    page_icon="☀️",
    layout="wide"
)

# ==========================================
# 2. البيانات والمعايير الفنية والماركات
# ==========================================

# أ. أنواع الألواح المتوفرة (تم إضافة Longi 640W وسلسلتها القصوى 8 ألواح)
PANEL_OPTIONS = [
    {"brand": "Longi Solar 640W (Voc 53.70V)", "power_w": 640, "price": 175, "max_string_size": 8},
    {"brand": "Jinko Solar 725W (Voc 49.12V)", "power_w": 725, "price": 195, "max_string_size": 9},
    {"brand": "لوح قياسي 640W", "power_w": 640, "price": 175, "max_string_size": 9}
]

DC_ACCESSORIES_PRICE_PER_STRING = 30
EARTHING_SYSTEM_PRICE = 160

# ب. قائمة العواكس حسب القدرة والنوع والماركة
INVERTER_BRANDS = [
    {"brand": "Growatt 6 kW Single Phase (IP21)", "power_kw": 6.0, "price": 400, "phase": "single"},
    {"brand": "Solis / Deye 6 kW Single Phase (IP65)", "power_kw": 6.0, "price": 1350, "phase": "single"},
    {"brand": "Solis / Deye 8 kW Single Phase (IP65)", "power_kw": 8.0, "price": 1550, "phase": "single"},
    {"brand": "Deye 10 kW Single Phase (IP65)", "power_kw": 10.0, "price": 1750, "phase": "single"},
    {"brand": "Deye 12 kW Single Phase", "power_kw": 12.0, "price": 1900, "phase": "single"},
    {"brand": "Deye High Voltage 30 kW 3-Phase (HV-3PH)", "power_kw": 30.0, "price": 3800, "phase": "three"},
    {"brand": "Deye High Voltage 50 kW 3-Phase (HV-3PH)", "power_kw": 50.0, "price": 5200, "phase": "three"}
]

# ج. قائمة البطاريات المتوفرة
BATTERIES = [
    {"name": "AOKLY جدارية / أرضية (10.24 kWh)", "capacity_kwh": 10.24, "price": 1350},
    {"name": "BICODI (12.0 kWh)", "capacity_kwh": 12.0, "price": 1450},
    {"name": "AOKLY بعجلات (15.0 kWh)", "capacity_kwh": 15.0, "price": 1700},
    {"name": "BICODI (16.1 kWh)", "capacity_kwh": 16.1, "price": 1850},
    {"name": "BICODI (17.66 kWh)", "capacity_kwh": 17.66, "price": 2100},
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
    
    matching_options = []
    for bat in BATTERIES:
        for qty in [1, 2, 3]:
            total_cap = bat["capacity_kwh"] * qty
            if total_cap >= required_kwh:
                matching_options.append({
                    "display": f"{qty}x {bat['name']} - بسعة إجمالية ({total_cap:.1f} kWh) - بسعر (${bat['price'] * qty})",
                    "model": bat["name"],
                    "capacity": bat["capacity_kwh"],
                    "qty": qty,
                    "unit_price": bat["price"],
                    "total_price": bat["price"] * qty,
                    "diff": total_cap - required_kwh
                })
                break
                
    matching_options.sort(key=lambda x: x["diff"])
    return required_kwh, matching_options

def calculate_panels(day_current, required_battery_kwh, selected_panel):
    panel_watt = selected_panel["power_w"]
    max_string = selected_panel["max_string_size"]
    
    day_power_w = day_current * 230 * 1.3
    day_panels_exact = day_power_w / panel_watt
    
    charging_power_w = (required_battery_kwh * 1000) / 9.0
    charging_panels_exact = charging_power_w / panel_watt
    
    total_panels_raw = day_panels_exact + charging_panels_exact
    target_panels = math.ceil(total_panels_raw)
    
    for num_strings in range(1, 10):
        panels_per_string = math.ceil(target_panels / num_strings)
        if panels_per_string <= max_string:
            final_panel_count = panels_per_string * num_strings
            return {
                "day_panels_exact": day_panels_exact,
                "charging_panels_exact": charging_panels_exact,
                "total_panels_raw": total_panels_raw,
                "total_panels": final_panel_count,
                "strings_count": num_strings,
                "panels_per_string": panels_per_string
            }

# ==========================================
# 4. واجهة المستخدم (User Interface)
# ==========================================
st.title("☀️ حاسبة وتصميم المنظومات الشمسية")
st.caption("إعداد المهندس مراد - حساب المكونات والماركات المتاحة")

# إعدادات العرض في القائمة الجانبية (Sidebar)
st.sidebar.header("⚙️ إعدادات العرض")
show_math_steps = st.sidebar.checkbox("إظهار الخطوات والحسابات الرياضية", value=False)

st.markdown("---")

# 1. إدخال أحمال المنظومة
st.subheader("📥 1. إدخال بيانات المنظومة")
col1, col2, col3 = st.columns(3)

with col1:
    day_amp = st.number_input("أمبير النهار (ن)", min_value=1, max_value=200, value=20, step=1)

with col2:
    night_amp = st.number_input("أمبير الليل (ل)", min_value=1, max_value=200, value=10, step=1)

with col3:
    night_hours = st.number_input("ساعات التشغيل الليلي (س)", min_value=1, max_value=24, value=4, step=1)

is_hv_3ph = st.checkbox("تطبيق نظام HV-3PH (ثلاثي الأطوار / High Voltage)", value=False)

st.markdown("---")

# 2. تحديد الماركات للألواح والعاكس والبطارية
st.subheader("⚙️ 2. اختيار ماركات الأجهزة المتوفرة")

col_p, col_i = st.columns(2)

# أ. اختيار ماركة الألواح
with col_p:
    panel_names = [f"{p['brand']} - بسعر (${p['price']})" for p in PANEL_OPTIONS]
    selected_p_str = st.selectbox("اختر ماركة اللوح الشمسي:", options=panel_names)
    chosen_panel = PANEL_OPTIONS[panel_names.index(selected_p_str)]

# ب. تصفية واختيار ماركة العاكس
load_kw = (day_amp * 230) / 1000.0
required_kw_with_safety = load_kw * 1.2
target_phase = "three" if is_hv_3ph else "single"

suitable_inverters = [
    inv for inv in INVERTER_BRANDS 
    if inv["phase"] == target_phase and inv["power_kw"] >= required_kw_with_safety
]

if not suitable_inverters:
    suitable_inverters = [inv for inv in INVERTER_BRANDS if inv["phase"] == target_phase]

with col_i:
    inverter_names = [f"{inv['brand']} - بسعر (${inv['price']})" for inv in suitable_inverters]
    selected_i_str = st.selectbox("اختر ماركة العاكس المتوفرة لطلبك:", options=inverter_names)
    chosen_inverter = suitable_inverters[inverter_names.index(selected_i_str)]

# ج. تصفية واختيار ماركة البطارية
req_kwh, bat_options = calculate_battery_bank(night_amp, night_hours)

if bat_options:
    bat_names = [b["display"] for b in bat_options]
    selected_b_str = st.selectbox("اختر ماركة وتجميعة البطارية المناسبة:", options=bat_names)
    chosen_bat = bat_options[bat_names.index(selected_b_str)]
else:
    st.error("لم يتم العثور على خيار بطارية مناسب للطلب.")

st.markdown("---")

if st.button("🚀 احسب المنظومة والتكلفة الإجمالية", type="primary", use_container_width=True):
    panels_info = calculate_panels(day_amp, req_kwh, chosen_panel)
    ac_board_cost = get_ac_board_price(day_amp)
    
    panels_cost = panels_info["total_panels"] * chosen_panel["price"]
    dc_acc_cost = panels_info["strings_count"] * DC_ACCESSORIES_PRICE_PER_STRING
    inv_cost = chosen_inverter["price"]
    bat_cost = chosen_bat["total_price"]
    
    total_cost = panels_cost + dc_acc_cost + inv_cost + bat_cost + ac_board_cost + EARTHING_SYSTEM_PRICE
    
    if chosen_inverter["power_kw"] < required_kw_with_safety:
        st.warning(f"⚠️ تنبيه: قدرة العاكس المختار ({chosen_inverter['power_kw']} kW) أقل من الحمل المطلوب مع هامش الأمان ({required_kw_with_safety:.2f} kW). يُفضل اختيار قدرة أعلى.")

    # 1. التفاصيل الرياضية
    if show_math_steps:
        st.subheader("1️⃣ الخطوات والتفاصيل الرياضية")
        with st.expander("عرض التفاصيل الرياضية الحسابية", expanded=True):
            st.write(f"**أ. بنك البطاريات:**")
            st.write(f"- الطاقة المطلوبة ليلاً: `{night_amp}A × 0.285 × {night_hours}h` = **{req_kwh:.2f} kWh**")
            st.write(f"- الاختيار المعتمد: **{chosen_bat['qty']}x {chosen_bat['model']}** بسعة إجمالية `{chosen_bat['capacity'] * chosen_bat['qty']:.2f} kWh`.")
            
            st.write(f"**ب. الألواح الشمسية ({chosen_panel['brand']}):**")
            st.write(f"- ألواح الحمل النهاري: `{panels_info['day_panels_exact']:.2f}` لوح")
            st.write(f"- ألواح شحن البطارية: `{panels_info['charging_panels_exact']:.2f}` لوح")
            st.write(f"- المجموع النظري: `{panels_info['total_panels_raw']:.2f}` لوح")
            st.write(f"- التقريب وتوزيع السلاسل المتساوي: **{panels_info['total_panels']} لوحاً** موزعة على **{panels_info['strings_count']} سلاسل × {panels_info['panels_per_string']} ألواح/سلسلة** (بحد أقصى {chosen_panel['max_string_size']} ألواح للسلسلة).")
            
            st.write(f"**ج. العاكس الهجين المختار:**")
            st.write(f"- حمل النهار الصافي: `{load_kw:.2f} kW` | مع هامش أمان (+20%): `{required_kw_with_safety:.2f} kW`")
            st.write(f"- الماركة المختارة: **{chosen_inverter['brand']}**")

    # 2. جدول المواد والتفاصيل
    st.subheader("📋 جدول المواد والتفاصيل")
    
    table_data = [
        {"المكون / الملحق": "الألواح الشمسية", "المواصفات والوصف": f"لوح {chosen_panel['brand']} (شامل الهيكل والتركيب)", "الكمية": f"{panels_info['total_panels']} لوحاً", "سعر الوحدة ($)": f"${chosen_panel['price']}", "الإجمالي ($)": f"${panels_cost}"},
        {"المكون / الملحق": "ملحقات الـ DC", "المواصفات والوصف": "أسلاك 40m + قاطع DC + فيوزات + MC4 + أنابيب", "الكمية": f"{panels_info['strings_count']} سلاسل", "سعر الوحدة ($)": f"${DC_ACCESSORIES_PRICE_PER_STRING}", "الإجمالي ($)": f"${dc_acc_cost}"},
        {"المكون / الملحق": "العاكس الهجين المختار", "المواصفات والوصف": chosen_inverter["brand"], "الكمية": "1", "سعر الوحدة ($)": f"${inv_cost}", "الإجمالي ($)": f"${inv_cost}"},
        {"المكون / الملحق": "بنك البطاريات", "المواصفات والوصف": f"{chosen_bat['model']}", "الكمية": f"{chosen_bat['qty']}", "سعر الوحدة ($)": f"${chosen_bat['unit_price']}", "الإجمالي ($)": f"${bat_cost}"},
        {"المكون / الملحق": "بورد الـ AC", "المواصفات والوصف": f"بورد حماية AC لغاية ({day_amp}A)", "الكمية": "1", "سعر الوحدة ($)": f"${ac_board_cost}", "الإجمالي ($)": f"${ac_board_cost}"},
        {"المكون / الملحق": "منظومة التأريض", "المواصفات والوصف": "وتد نحاسي + أسلاك 30m + مادة تأريض + الحفر والربط", "الكمية": "1", "سعر الوحدة ($)": f"${EARTHING_SYSTEM_PRICE}", "الإجمالي ($)": f"${EARTHING_SYSTEM_PRICE}"},
    ]
    
    st.table(table_data)

    # 3. الكلفة الإجمالية
    st.subheader("💰 الكلفة الإجمالية النهائية")
    st.success(f"**الكلفة الإجمالية المباشرة للمشروع بناءً على اختيار الماركات: ${total_cost:,}**")
