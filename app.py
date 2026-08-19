import streamlit as st
import math

# ==========================================
# 1. إعدادات الصفحة والشعار والقائمة الجانبية
# ==========================================
st.set_page_config(
    page_title="شركة ركن التعمير - حاسبة المنظومات الشمسية",
    page_icon="logo.png",
    layout="wide"
)

# مفتاح تحكم لإظهار أو إخفاء المعادلات الحسابية
with st.sidebar:
    st.header("⚙️ إعدادات العرض")
    show_formulas = st.toggle("إظهار المعادلات والآلية الحسابية", value=False)
    st.caption("تفعيل هذا الخيار سيظهر الشرح الرياضي والمعادلات المستخدمة في الحسابات.")

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
    # GOGO Inverters
    {"brand": "GoGo Hybrid", "model": "GoGo-5.5KW", "power_kw": 5.5, "price": 600, "phase": "single", "type": "Hybrid", "max_charge_idc": 110, "cable_spec": "4 x 4 mm²"},
    {"brand": "GoGo Hybrid", "model": "GoGo-6KW", "power_kw": 6.0, "price": 650, "phase": "single", "type": "Hybrid", "max_charge_idc": 120, "cable_spec": "4 x 4 mm²"},

    # Growatt Inverters
    {"brand": "Growatt Off-Grid", "model": "SPF 5000 ES", "power_kw": 5.0, "price": 650, "phase": "single", "type": "Off-Grid", "max_charge_idc": 100, "cable_spec": "4 x 4 mm²"},
    {"brand": "Growatt Hybrid", "model": "SPH 6000", "power_kw": 6.0, "price": 850, "phase": "single", "type": "Hybrid", "max_charge_idc": 125, "cable_spec": "4 x 6 mm²"},
    {"brand": "Growatt Hybrid", "model": "SPH 10000", "power_kw": 10.0, "price": 1500, "phase": "single", "type": "Hybrid", "max_charge_idc": 200, "cable_spec": "4 x 10 mm²"},

    # Deye Hybrid Inverters
    {"brand": "Deye Hybrid", "model": "SUN-5K-SG04LP1-EU-SM2", "power_kw": 5.0, "price": 750, "phase": "single", "type": "Hybrid", "max_charge_idc": 120, "cable_spec": "4 x 4 mm²"},
    {"brand": "Deye Hybrid", "model": "SUN-6K-SG04LP1-EU-SM2", "power_kw": 6.0, "price": 875, "phase": "single", "type": "Hybrid", "max_charge_idc": 135, "cable_spec": "4 x 6 mm²"},
    {"brand": "Deye Hybrid", "model": "SUN-8K-SG05LP1-EU-SM2", "power_kw": 8.0, "price": 1225, "phase": "single", "type": "Hybrid", "max_charge_idc": 190, "cable_spec": "4 x 10 mm²"},
    {"brand": "Deye Hybrid", "model": "SUN-12K-SG02LP1-EU-AM3", "power_kw": 12.0, "price": 1800, "phase": "single", "type": "Hybrid", "max_charge_idc": 250, "cable_spec": "4 x 16 mm²"},
    
    # Solis Hybrid Inverters
    {"brand": "Solis Hybrid", "model": "S6-EH1P5K-L-PLUS", "power_kw": 5.0, "price": 750, "phase": "single", "type": "Hybrid", "max_charge_idc": 112, "cable_spec": "4 x 4 mm²"},
    {"brand": "Solis Hybrid", "model": "S6-EH1P10K-L-PLUS", "power_kw": 10.0, "price": 1650, "phase": "single", "type": "Hybrid", "max_charge_idc": 210, "cable_spec": "4 x 10 mm²"},

    # Off-Grid Inverters
    {"brand": "Deye Off-Grid", "model": "SUN-6K-OG", "power_kw": 6.0, "price": 700, "phase": "single", "type": "Off-Grid", "max_charge_idc": 120, "cable_spec": "4 x 4 mm²"},
    {"brand": "SRNE Off-Grid", "model": "SRNE-16K-IP20", "power_kw": 16.0, "price": 1600, "phase": "single", "type": "Off-Grid", "max_charge_idc": 200, "cable_spec": "4 x 10 mm²"},

    # On-Grid Inverters
    {"brand": "Solis On-Grid", "model": "S6-GR1P5K", "power_kw": 5.0, "price": 500, "phase": "single", "type": "On-Grid", "max_charge_idc": 0, "cable_spec": "4 x 4 mm²"},
    {"brand": "Solis On-Grid", "model": "S6-GR1P10K", "power_kw": 10.0, "price": 950, "phase": "single", "type": "On-Grid", "max_charge_idc": 0, "cable_spec": "4 x 10 mm²"},

    # 3-Phase Systems
    {"brand": "Deye 3-Phase", "model": "SUN-12K-SG04LP3-EU", "power_kw": 12.0, "price": 2300, "phase": "three", "type": "Hybrid", "max_charge_idc": 240, "cable_spec": "5 x 6 mm²"},
    {"brand": "Deye 3-Phase", "model": "SUN-30K-SG01HP3", "power_kw": 30.0, "price": 3800, "phase": "three", "type": "Hybrid", "max_charge_idc": 100, "cable_spec": "4 x 16 mm²"},
    {"brand": "Deye 3-Phase", "model": "SUN-50K-SG01HP3", "power_kw": 50.0, "price": 5200, "phase": "three", "type": "Hybrid", "max_charge_idc": 150, "cable_spec": "4 x 25 mm²"}
]

BATTERIES = [
    {"name": "AOKLY", "type": "عادية", "capacity_kwh": 5.12, "price": 725},
    {"name": "AOKLY", "type": "جداري", "capacity_kwh": 10.24, "price": 1400},
    {"name": "AOKLY", "type": "أرضي", "capacity_kwh": 10.24, "price": 1420},
    {"name": "BICODI", "type": "عادية", "capacity_kwh": 5.12, "price": 700},
    {"name": "BICODI", "type": "جداري", "capacity_kwh": 10.24, "price": 1400},
    {"name": "BICODI", "type": "عادية", "capacity_kwh": 11.78, "price": 1475},
    {"name": "BICODI", "type": "عادية", "capacity_kwh": 16.1, "price": 1800}
]

# ==========================================
# 4. الدوال الحسابية
# ==========================================
def get_ac_board_price(current_amp):
    if 8 <= current_amp <= 15: return 125
    elif 15 < current_amp <= 25: return 160
    elif 25 < current_amp <= 40: return 180
    elif 40 < current_amp <= 60: return 250
    elif 80 <= current_amp <= 120: return 350
    elif 120 < current_amp <= 150: return 450
    else: return 550

def calculate_panels_auto(day_current, required_battery_kwh, selected_panel):
    panel_watt = selected_panel["power_w"]
    max_string = selected_panel["max_string_size"]
    day_power_w = day_current * 230 * 1.3
    charging_power_w = (required_battery_kwh * 1000) / 9.0
    target_panels = math.ceil((day_power_w + charging_power_w) / panel_watt)
    for num_strings in range(1, 15):
        panels_per_string = math.ceil(target_panels / num_strings)
        if panels_per_string <= max_string:
            return panels_per_string * num_strings, num_strings, panels_per_string
    return target_panels, 1, target_panels

def determine_battery_size_and_qty(req_kwh):
    all_combos = []
    for bat in BATTERIES:
        for qty in range(1, 6):
            total_cap = bat["capacity_kwh"] * qty
            diff = total_cap - req_kwh
            if diff >= -0.2:
                all_combos.append({"bat": bat, "unit_cap": bat["capacity_kwh"], "qty": qty, "total_cap": round(total_cap, 2), "diff": diff})
    if all_combos:
        all_combos.sort(key=lambda x: (x["diff"], x["qty"]))
        return all_combos[0]
    return {"bat": BATTERIES[1], "unit_cap": 10.24, "qty": 1, "total_cap": 10.24}

# ==========================================
# 5. الواجهة الهيكلية (التخطيط الشجري)
# ==========================================
st.markdown("### 🏢 اختر نوع التطبيق والمنظومة:")

category = st.radio("نوع القطاع:", options=["سكني", "تجاري", "زراعي"], horizontal=True)
st.markdown("---")

day_amp = None
night_amp = None
night_hours = 4
hp_power = 0
sys_type = "Hybrid"
phase_option = "single"

# --- القطاع السكني ---
if category == "سكني":
    c1, c2, c3 = st.columns(3)
    with c1: day_amp = st.number_input("أمبير نهار:", min_value=0, max_value=300, value=None)
    with c2: night_amp = st.number_input("أمبير ليل:", min_value=0, max_value=300, value=None)
    with c3: night_hours = st.number_input("ساعات التشغيل الليلي:", min_value=1, max_value=24, value=4)

    c4, c5 = st.columns(2)
    with c4: sys_type = st.radio("نوع المنظومة:", options=["Hybrid", "Off-Grid"], horizontal=True)
    with c5: phase_radio = st.radio("عدد الأطوار:", options=["1PH", "3PH"], horizontal=True)
    phase_option = "single" if phase_radio == "1PH" else "three"

# --- القطاع التجاري ---
elif category == "تجاري":
    c1, c2, c3 = st.columns(3)
    with c1: day_amp = st.number_input("أمبير نهار:", min_value=0, max_value=500, value=None)
    with c2: night_amp = st.number_input("أمبير ليل:", min_value=0, max_value=500, value=None)
    with c3: night_hours = st.number_input("ساعات التشغيل الليلي:", min_value=1, max_value=24, value=4)

    c4, c5 = st.columns(2)
    with c4: sys_type = st.radio("نوع المنظومة:", options=["Hybrid", "On-Grid", "Off-Grid"], horizontal=True)
    with c5: phase_radio = st.radio("عدد الأطوار:", options=["1PH", "3PH"], horizontal=True)
    phase_option = "single" if phase_radio == "1PH" else "three"

# --- القطاع الزراعي ---
elif category == "زراعي":
    c1, c2 = st.columns(2)
    with c1: hp_power = st.number_input("القدرة بالحصان (HP):", min_value=1, max_value=500, value=10, step=1)
    with c2: phase_radio = st.radio("عدد الأطوار:", options=["3PH", "1PH"], horizontal=True)
    phase_option = "single" if phase_radio == "1PH" else "three"
    st.info(f"📌 منظومة زراعية مضخات قدرة **{hp_power} حصان** ({hp_power * 0.746:.2f} kW)")

st.markdown("---")

# ==========================================
# 6. قسم التفاصيل والحسابات المعمقة
# ==========================================
if category == "زراعي":
    if hp_power > 0:
        req_kw = hp_power * 0.746 * 1.3
        target_panels = math.ceil((req_kw * 1000) / PANEL_OPTIONS[0]["power_w"])
        total_cost = target_panels * PANEL_OPTIONS[0]["price"] + (req_kw * 120) 
        st.success(f"☀️ عدد الألواح المطلوبة: **{target_panels} لوحاً** ({PANEL_OPTIONS[0]['brand']})")
        st.success(f"💰 التكلفة التقديرية التقريبية: **${total_cost:,.0f}**")
else:
    if day_amp is None or night_amp is None or day_amp == 0:
        st.warning("👈 يرجى إدخال أمبير النهار والليل لإظهار بقية التفاصيل وتوليد النتائج تلقائياً.")
    else:
        load_kw = (day_amp * 230) / 1000.0
        recommended_kw = load_kw * 1.2
        req_kwh = night_amp * 0.285 * night_hours if sys_type != "On-Grid" else 0

        st.subheader("⚙️ تفاصيل المنظومة والماركات والمواصفات")
        col_p, col_i, col_b = st.columns(3)

        # --- الألواح ---
        with col_p:
            st.markdown("##### ☀️ الألواح الشمسية")
            panel_names = [f"{p['brand']} - (${p['price']})" for p in PANEL_OPTIONS]
            selected_p_str = st.selectbox("نوع اللوح:", options=panel_names)
            chosen_panel = PANEL_OPTIONS[panel_names.index(selected_p_str)]
            
            auto_panels, auto_strings, auto_per_string = calculate_panels_auto(day_amp, req_kwh, chosen_panel)
            if st.checkbox("تعديل يدوي لعدد الألواح"):
                final_panels = st.number_input("حدد عدد الألواح:", min_value=1, max_value=200, value=auto_panels, step=1)
            else:
                final_panels = auto_panels

        # --- الإنفرتر ---
        with col_i:
            st.markdown("##### 🔌 الإنفرتر / العاكس")
            available_inverters = [inv for inv in INVERTER_BRANDS if inv["phase"] == phase_option and inv["type"] == sys_type]
            if not available_inverters:
                available_inverters = [inv for inv in INVERTER_BRANDS if inv["phase"] == phase_option]

            if available_inverters:
                brand_options = [f"{inv['brand']} [{inv['model']}] - {inv['power_kw']}kW" for inv in available_inverters]
                selected_brand_str = st.selectbox("اختر ماركة الإنفرتر:", options=brand_options)
                chosen_single_inv = available_inverters[brand_options.index(selected_brand_str)]
                
                calculated_inv_qty = math.ceil(recommended_kw / chosen_single_inv["power_kw"]) if chosen_single_inv["power_kw"] > 0 else 1
                chosen_inv_combo = {
                    "inverter": chosen_single_inv,
                    "qty": calculated_inv_qty,
                    "total_power": chosen_single_inv["power_kw"] * calculated_inv_qty,
                    "total_price": chosen_single_inv["price"] * calculated_inv_qty
                }
                st.info(f"📌 العدد التلقائي المطلوب لتغطية الحمل: `{calculated_inv_qty}`")
            else:
                st.error("لا تتوفر ماركات متطابقة مع هذه المدخلات.")
                chosen_inv_combo = None

        # --- البطاريات ---
        with col_b:
            st.markdown("##### 🔋 بنك البطاريات")
            if sys_type == "On-Grid":
                st.caption("ℹ️ نظام On-Grid لا يحتاج إلى بطاريات.")
                chosen_bat = {"brand": "بدون بطاريات", "unit_cap": 0, "total_cap": 0, "qty": 0, "unit_price": 0, "total_price": 0}
            else:
                bat_spec = determine_battery_size_and_qty(req_kwh)
                bat_brand_options = [f"{b['name']} ({b['capacity_kwh']} kWh - {b['type']})" for b in BATTERIES]
                
                default_index = next((i for i, b in enumerate(BATTERIES) if b["capacity_kwh"] == bat_spec["unit_cap"]), 0)
                selected_bat_brand_str = st.selectbox("اختر البطارية:", options=bat_brand_options, index=default_index)
                chosen_single_bat = BATTERIES[bat_brand_options.index(selected_bat_brand_str)]
                
                calculated_bat_qty = math.ceil(req_kwh / chosen_single_bat["capacity_kwh"]) if chosen_single_bat["capacity_kwh"] > 0 else 1
                bat_qty = st.number_input("عدد البطاريات:", min_value=1, max_value=20, value=calculated_bat_qty, step=1)
                
                total_bat_cap = round(chosen_single_bat["capacity_kwh"] * bat_qty, 2)
                st.info(f"📌 **السعة الإجمالية:** `{total_bat_cap} kWh` | **المطلوب:** `{req_kwh:.2f} kWh`")

                chosen_bat = {
                    "brand": f"{chosen_single_bat['name']} ({chosen_single_bat['type']})",
                    "unit_cap": chosen_single_bat["capacity_kwh"],
                    "total_cap": total_bat_cap,
                    "qty": bat_qty,
                    "unit_price": chosen_single_bat["price"],
                    "total_price": chosen_single_bat["price"] * bat_qty
                }

        st.markdown("---")

        # ==========================================
        # 7. الحسابات النهائية والتنبيهات
        # ==========================================
        if chosen_inv_combo:
            max_string = chosen_panel["max_string_size"]
            num_strings = math.ceil(final_panels / max_string)
            
            ac_board_cost = get_ac_board_price(day_amp)
            panels_cost = final_panels * chosen_panel["price"]
            dc_acc_cost = num_strings * DC_ACCESSORIES_PRICE_PER_STRING
            inv_cost = chosen_inv_combo["total_price"]
            bat_cost = chosen_bat["total_price"]
            total_cost = panels_cost + dc_acc_cost + inv_cost + bat_cost + ac_board_cost + EARTHING_SYSTEM_PRICE

            single_inv = chosen_inv_combo["inverter"]
            inv_qty = chosen_inv_combo["qty"]
            
            actual_charge_idc = single_inv["max_charge_idc"] * 0.80 * inv_qty
            charge_power_w = actual_charge_idc * 51.5
            charge_iac_210v = charge_power_w / (210.0 * 0.95) if charge_power_w > 0 else 0

            # عرض المعادلات (إذا مفعلة)
            if show_formulas:
                st.subheader("📐 المعادلات الرياضية والآلية الحسابية")
                st.write(f"1. قدرة أحمال النهار: **{load_kw:.2f} kW**")
                st.latex(r"\text{Load Power} = \frac{\text{Day Amp} \times 230}{1000}")
                st.write(f"2. سعة البطاريات: **{req_kwh:.2f} kWh**")
                st.latex(r"\text{Battery kWh} = \text{Night Amp} \times 0.285 \times \text{Night Hours}")
                st.write(f"3. تيار الشحن من الوطنية: **{charge_iac_210v:.1f} A (AC)**")
                st.markdown("---")

            # التنبيهات والتوصيات الفنية (RTL)
            st.subheader("💡 التنبيهات والتوصيات الفنية")
            st.markdown('<div style="direction: rtl; text-align: right;">', unsafe_allow_html=True)
            
            st.success(f"⚡ **الإنفرتر المختار:** {single_inv['brand']} {single_inv['power_kw']} kW (عدد {inv_qty})")
                
            if sys_type != "On-Grid":
                actual_hours = chosen_bat["total_cap"] / (0.285 * night_amp) if night_amp > 0 else 0
                actual_amp_avail = chosen_bat["total_cap"] / (0.285 * night_hours) if night_hours > 0 else 0
                
                st.success(f"🔋 **البطاريات:** {chosen_bat['brand']} {chosen_bat['unit_cap']} kWh (عدد {chosen_bat['qty']}) - الإجمالي {chosen_bat['total_cap']} kWh")

                if chosen_bat["total_cap"] < req_kwh * 0.95:
                    st.warning(f"⚠️ تكفي لتشغيل {night_amp}A لمدة **{actual_hours:.1f} ساعة** فقط.")
                
                st.info(f"الأمبير المتاح خلال ({night_hours}) ساعات: **{actual_amp_avail:.1f} أمبير** | مدة تشغيل ({night_amp}A): **{int(actual_hours)} ساعة و {int((actual_hours % 1) * 60)} دقيقة**")
                
                if charge_iac_210v > 0:
                    st.warning(f"🔌 تيار الشحن المسحوب من الوطنية: **{charge_iac_210v:.1f}A AC** (عند ضبط الشحن 80%) | كابل AC المطلوب: **({single_inv['cable_spec']}) لكل إنفرتر**.")

            st.markdown('</div>', unsafe_allow_html=True)
            st.markdown("---")

            # جدول المواد والتفاصيل
            st.subheader("📋 جدول المواد والتفاصيل - شركة ركن التعمير")
            table_data = [
                {"المكون / الملحق": "الألواح الشمسية", "المواصفات والوصف": f"لوح {chosen_panel['brand']} (شامل الهيكل)", "الكمية": f"{final_panels}", "سعر الوحدة": f"${chosen_panel['price']}", "الإجمالي": f"${panels_cost}"},
                {"المكون / الملحق": "ملحقات الـ DC", "المواصفات والوصف": "أسلاك + قواطع + MC4 + أنابيب", "الكمية": f"{num_strings} سلاسل", "سعر الوحدة": f"${DC_ACCESSORIES_PRICE_PER_STRING}", "الإجمالي": f"${dc_acc_cost}"},
                {"المكون / الملحق": "العاكس / الإنفرتر", "المواصفات والوصف": f"{single_inv['brand']} ({single_inv['model']})", "الكمية": f"{inv_qty}", "سعر الوحدة": f"${single_inv['price']}", "الإجمالي": f"${inv_cost}"},
                {"المكون / الملحق": "بنك البطاريات", "المواصفات والوصف": f"{chosen_bat['brand']} ({chosen_bat['unit_cap']} kWh)" if chosen_bat['qty'] > 0 else "بدون", "الكمية": f"{chosen_bat['qty']}", "سعر الوحدة": f"${chosen_bat['unit_price']}", "الإجمالي": f"${bat_cost}"},
                {"المكون / الملحق": "بورد الـ AC", "المواصفات والوصف": f"بورد حماية لغاية ({day_amp}A)", "الكمية": "1", "سعر الوحدة": f"${ac_board_cost}", "الإجمالي": f"${ac_board_cost}"},
                {"المكون / الملحق": "منظومة التأريض", "المواصفات والوصف": "وتد + أسلاك + مادة تأريض", "الكمية": "1", "سعر الوحدة": f"${EARTHING_SYSTEM_PRICE}", "الإجمالي": f"${EARTHING_SYSTEM_PRICE}"},
            ]
            st.table(table_data)
            st.success(f"### 💰 التكلفة الإجمالية النهائية للمنظومة: ${total_cost:,}")
