import streamlit as st
import math

# ==========================================
# 1. إعدادات الصفحة والشعار
# ==========================================
st.set_page_config(
    page_title="شركة ركن التعمير - حاسبة المنظومات الشمسية",
    page_icon="logo.png",
    layout="wide"
)

# ==========================================
# 2. الهيدر الرئيسي
# ==========================================
col_logo, col_title = st.columns([1, 5])

with col_logo:
    try:
        st.image("logo.png", width=120)
    except Exception:
        st.write("☀️")

with col_title:
    st.title("☀️ حاسبة وتصميم المنظومات الشمسية")
    st.subheader("شركة ركن التعمير للتجارة والمقاولات العامة / الموصل")

st.markdown("---")

# ==========================================
# 3. البيانات الفنية الرسمية والأسعار
# ==========================================
PANEL_OPTIONS = [
    {"brand": "Jinko Solar 725W (Voc 49.12V)", "power_w": 725, "price": 175, "max_string_size": 9},
    {"brand": "Longi Solar 640W (Voc 53.70V)", "power_w": 640, "price": 165, "max_string_size": 8}
]

DC_ACCESSORIES_PRICE_PER_STRING = 30
EARTHING_SYSTEM_PRICE = 160

INVERTER_BRANDS = [
    # GoGo
    {"brand": "GoGo Hybrid", "model": "GoGo-5.5KW", "power_kw": 5.5, "price": 600, "phase": "1ph", "type": "Hybrid", "voltage_level": "LV", "max_charge_idc": 110, "cable_spec": "4 x 4 mm²"},
    {"brand": "GoGo Hybrid", "model": "GoGo-6KW", "power_kw": 6.0, "price": 650, "phase": "1ph", "type": "Hybrid", "voltage_level": "LV", "max_charge_idc": 120, "cable_spec": "4 x 4 mm²"},

    # Growatt
    {"brand": "Growatt Off-Grid", "model": "SPF 5000 ES", "power_kw": 5.0, "price": 650, "phase": "1ph", "type": "Off", "voltage_level": "LV", "max_charge_idc": 100, "cable_spec": "4 x 4 mm²"},
    {"brand": "Growatt Hybrid", "model": "SPH 6000", "power_kw": 6.0, "price": 850, "phase": "1ph", "type": "Hybrid", "voltage_level": "LV", "max_charge_idc": 125, "cable_spec": "4 x 6 mm²"},

    # Deye
    {"brand": "Deye Hybrid", "model": "SUN-5K-SG04LP1-EU-SM2", "power_kw": 5.0, "price": 750, "phase": "1ph", "type": "Hybrid", "voltage_level": "LV", "max_charge_idc": 120, "cable_spec": "4 x 4 mm²"},
    {"brand": "Deye Hybrid", "model": "SUN-12K-SG02LP1-EU-AM3", "power_kw": 12.0, "price": 1800, "phase": "1ph", "type": "Hybrid", "voltage_level": "LV", "max_charge_idc": 250, "cable_spec": "4 x 16 mm²"},
    {"brand": "Deye 3-Phase LV", "model": "SUN-12K-SG04LP3-EU", "power_kw": 12.0, "price": 2300, "phase": "3ph", "type": "Hybrid", "voltage_level": "LV", "max_charge_idc": 240, "cable_spec": "5 x 6 mm²"},
    {"brand": "Deye 3-Phase HV", "model": "SUN-30K-SG01HP3", "power_kw": 30.0, "price": 3800, "phase": "3ph", "type": "Hybrid", "voltage_level": "HV", "max_charge_idc": 100, "cable_spec": "4 x 16 mm²"},
    {"brand": "Deye 3-Phase HV", "model": "SUN-50K-SG01HP3", "power_kw": 50.0, "price": 5200, "phase": "3ph", "type": "Hybrid", "voltage_level": "HV", "max_charge_idc": 150, "cable_spec": "4 x 25 mm²"}
]

BATTERIES = [
    {"name": "AOKLY", "type": "عادية", "capacity_kwh": 5.12, "price": 725},
    {"name": "AOKLY", "type": "جداري", "capacity_kwh": 10.24, "price": 1400},
    {"name": "BICODI", "type": "عادية", "capacity_kwh": 11.78, "price": 1475},
    {"name": "BICODI", "type": "عادية", "capacity_kwh": 16.1, "price": 1800}
]

# ==========================================
# 4. الواجهة الهيكلية (بناءً على التخطيط المرفق)
# ==========================================
st.markdown("### 🏢 اختر نوع التطبيق والمنظومة:")

# 1. المستوى الأول: اختيار القطاع
category = st.radio(
    "نوع القطاع:",
    options=["سكني", "تجاري", "زراعي"],
    horizontal=True
)

st.markdown("---")

# متغيرات الحساب العامة
day_amp = 0
night_amp = 0
night_hours = 4
hp_power = 0
sys_type = "Hybrid"
phase_option = "1ph"
voltage_level = "LV"

# ------------------------------------------
# مسار القطاع السكني
# ------------------------------------------
if category == "سكني":
    c1, c2, c3 = st.columns(3)
    with c1:
        day_amp = st.number_input("أمبير نهار:", min_value=0, max_value=300, value=None, placeholder="أدخل أمبير النهار...")
    with c2:
        night_amp = st.number_input("أمبير ليل:", min_value=0, max_value=300, value=None, placeholder="أدخل أمبير الليل...")
    with c3:
        night_hours = st.number_input("ساعات التشغيل الليلي:", min_value=1, max_value=24, value=4)

    c4, c5 = st.columns(2)
    with c4:
        sys_type = st.radio("نوع المنظومة:", options=["Hybrid", "off"], horizontal=True)
    with c5:
        phase_option = st.radio("عدد الأطوار:", options=["1ph", "3ph"], horizontal=True)

# ------------------------------------------
# مسار القطاع التجاري
# ------------------------------------------
elif category == "تجاري":
    c1, c2, c3 = st.columns(3)
    with c1:
        day_amp = st.number_input("أمبير نهار:", min_value=0, max_value=500, value=None, placeholder="أدخل أمبير النهار...")
    with c2:
        night_amp = st.number_input("أمبير ليل:", min_value=0, max_value=500, value=None, placeholder="أدخل أمبير الليل...")
    with c3:
        night_hours = st.number_input("ساعات التشغيل الليلي:", min_value=1, max_value=24, value=4)

    c4, c5 = st.columns(2)
    with c4:
        sys_type = st.radio("نوع المنظومة:", options=["Hybrid", "ON", "off grid"], horizontal=True)
        # توحيد التسميات للحسابات
        if sys_type == "off grid": sys_type = "off"
        
    with c5:
        phase_option = st.radio("عدد الأطوار:", options=["1ph", "3ph"], horizontal=True)

    # تشعب خاص بالنظام التجاري 3PH (LV / HV)
    if phase_option == "3ph":
        voltage_level = st.radio("مستوى الفولتيّة:", options=["LV", "HV"], horizontal=True)

# ------------------------------------------
# مسار القطاع الزراعي
# ------------------------------------------
elif category == "زراعي":
    c1, c2 = st.columns(2)
    with c1:
        hp_power = st.number_input("القدرة بالحضان (HP):", min_value=1, max_value=500, value=10, step=1)
    with c2:
        phase_option = st.radio("عدد الأطوار:", options=["3ph", "1ph"], horizontal=True)
    
    st.info(f"📌 منظومة زراعية مضخات قدرة **{hp_power} حصان** ({hp_power * 0.746:.2f} kW)")

st.markdown("---")

# ==========================================
# 5. بقية التفاصيل والنتائج والحسابات
# ==========================================
st.markdown("### 📋 بقية التفاصيل والنتائج")

if category == "زراعي":
    if hp_power > 0:
        req_kw = hp_power * 0.746 * 1.3  # معامل البدء للمضخات
        target_panels = math.ceil((req_kw * 1000) / PANEL_OPTIONS[0]["power_w"])
        total_cost = target_panels * PANEL_OPTIONS[0]["price"] + 1200 # تقدير الإنفرتر الزراعي والعكس

        st.success(f"☀️ عدد الألواح الشمسية المطلوبة للربط المباشر: **{target_panels} لوحاً** ({PANEL_OPTIONS[0]['brand']})")
        st.success(f"💰 التكلفة التقديرية لمنظومة الري الشمسية: **${total_cost:,}**")

else:
    if day_amp is None or night_amp is None or day_amp == 0:
        st.warning("👈 يرجى إدخال أمبير النهار والليل لإظهار بقية التفاصيل وتوليد النتائج.")
    else:
        # حساب القدرة والسعة المطلوبة
        load_kw = (day_amp * 230) / 1000.0
        req_kwh = night_amp * 0.285 * night_hours if sys_type != "ON" else 0

        # اختيار الإنفرتر بناءً على مدخلات الشجرة
        filtered_inverters = [
            inv for inv in INVERTER_BRANDS 
            if inv["phase"] == phase_option and (inv["type"].lower() == sys_type.lower() or sys_type in inv["type"])
        ]
        
        if phase_option == "3ph" and category == "تجاري":
            filtered_inverters = [inv for inv in filtered_inverters if inv.get("voltage_level") == voltage_level]

        if not filtered_inverters:
            filtered_inverters = INVERTER_BRANDS

        chosen_inv = filtered_inverters[0]
        inv_qty = math.ceil((load_kw * 1.2) / chosen_inv["power_kw"]) if chosen_inv["power_kw"] > 0 else 1

        # الألواح والبطاريات
        chosen_panel = PANEL_OPTIONS[0]
        day_p_w = day_amp * 230 * 1.3
        chg_p_w = (req_kwh * 1000) / 9.0 if req_kwh > 0 else 0
        total_panels = math.ceil((day_p_w + chg_p_w) / chosen_panel["power_w"])

        bat_qty = math.ceil(req_kwh / BATTERIES[0]["capacity_kwh"]) if req_kwh > 0 else 0
        bat_cost = bat_qty * BATTERIES[0]["price"]

        # التكاليف
        panels_cost = total_panels * chosen_panel["price"]
        inv_cost = inv_qty * chosen_inv["price"]
        total_cost = panels_cost + inv_cost + bat_cost + EARTHING_SYSTEM_PRICE + 150

        # عرض التوصيات بشكل مختصر RTL
        st.markdown('<div style="direction: rtl; text-align: right;">', unsafe_allow_html=True)
        st.success(f"⚡ **الإنفرتر المختار:** {chosen_inv['brand']} {chosen_inv['power_kw']} kW (عدد {inv_qty})")
        if sys_type != "ON":
            st.success(f"🔋 **البطاريات:** {BATTERIES[0]['name']} {BATTERIES[0]['capacity_kwh']} kWh (عدد {bat_qty}) - الإجمالي {bat_qty * BATTERIES[0]['capacity_kwh']:.2f} kWh")
        st.markdown('</div>', unsafe_allow_html=True)

        # جدول التفاصيل
        table_data = [
            {"المكون": "الألواح الشمسية", "التفاصيل": f"لوح {chosen_panel['brand']}", "الكمية": f"{total_panels} لوحاً", "الإجمالي": f"${panels_cost}"},
            {"المكون": "العاكس / الإنفرتر", "التفاصيل": f"{chosen_inv['brand']} ({chosen_inv['model']})", "الكمية": f"{inv_qty}", "الإجمالي": f"${inv_cost}"},
            {"المكون": "بنك البطاريات", "التفاصيل": f"{BATTERIES[0]['name']}" if bat_qty > 0 else "بدون بطاريات", "الكمية": f"{bat_qty}", "الإجمالي": f"${bat_cost}"},
            {"المكون": "ملحقات والتأريض", "التفاصيل": "أسلاك + قواطع + بورد AC + منظومة تأريض", "الكمية": "1", "الإجمالي": f"${EARTHING_SYSTEM_PRICE + 150}"}
        ]
        
        st.table(table_data)
        st.success(f"### 💰 التكلفة الإجمالية النهائية للمنظومة: ${total_cost:,}")
