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

with st.sidebar:
    st.header("⚙️ إعدادات العرض")
    show_formulas = st.toggle("إظهار المعادلات والآلية الحسابية", value=False)

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
# 3. قاعدة البيانات للقطع والأسعار
# ==========================================
PANEL_OPTIONS = [
    {"brand": "Jinko Solar 725W", "power_w": 725, "price": 175, "max_string_size": 9},
    {"brand": "Longi Solar 640W", "power_w": 640, "price": 165, "max_string_size": 8}
]

DC_ACCESSORIES_PRICE_PER_STRING = 30
EARTHING_SYSTEM_PRICE = 160

INVERTER_BRANDS = [
    # GoGo
    {"brand": "GoGo Hybrid", "model": "GoGo-5.5KW", "power_kw": 5.5, "price": 600, "phase": "single", "type": "Hybrid", "max_charge_idc": 110, "cable_spec": "4 x 4 mm²"},
    {"brand": "GoGo Hybrid", "model": "GoGo-6KW", "power_kw": 6.0, "price": 650, "phase": "single", "type": "Hybrid", "max_charge_idc": 120, "cable_spec": "4 x 4 mm²"},

    # Deye
    {"brand": "Deye Hybrid", "model": "SUN-5K-SG04LP1-EU", "power_kw": 5.0, "price": 750, "phase": "single", "type": "Hybrid", "max_charge_idc": 120, "cable_spec": "4 x 4 mm²"},
    {"brand": "Deye Hybrid", "model": "SUN-6K-SG04LP1-EU", "power_kw": 6.0, "price": 875, "phase": "single", "type": "Hybrid", "max_charge_idc": 135, "cable_spec": "4 x 6 mm²"},
    {"brand": "Deye Hybrid", "model": "SUN-8K-SG05LP1-EU", "power_kw": 8.0, "price": 1225, "phase": "single", "type": "Hybrid", "max_charge_idc": 190, "cable_spec": "4 x 10 mm²"},
    {"brand": "Deye Hybrid", "model": "SUN-12K-SG02LP1-EU", "power_kw": 12.0, "price": 1800, "phase": "single", "type": "Hybrid", "max_charge_idc": 250, "cable_spec": "4 x 16 mm²"},
    {"brand": "Deye 3-Phase", "model": "SUN-12K-SG04LP3-EU", "power_kw": 12.0, "price": 2300, "phase": "three", "type": "Hybrid", "max_charge_idc": 240, "cable_spec": "5 x 6 mm²"},
    {"brand": "Deye 3-Phase", "model": "SUN-30K-SG01HP3", "power_kw": 30.0, "price": 3800, "phase": "three", "type": "Hybrid", "max_charge_idc": 100, "cable_spec": "4 x 16 mm²"},

    # Solis
    {"brand": "Solis Hybrid", "model": "S6-EH1P5K-L-PLUS", "power_kw": 5.0, "price": 750, "phase": "single", "type": "Hybrid", "max_charge_idc": 112, "cable_spec": "4 x 4 mm²"},
    {"brand": "Solis Hybrid", "model": "S6-EH1P10K-L-PLUS", "power_kw": 10.0, "price": 1650, "phase": "single", "type": "Hybrid", "max_charge_idc": 210, "cable_spec": "4 x 10 mm²"},
    {"brand": "Solis On-Grid", "model": "S6-GR1P5K", "power_kw": 5.0, "price": 500, "phase": "single", "type": "On-Grid", "max_charge_idc": 0, "cable_spec": "4 x 4 mm²"},
    {"brand": "Solis On-Grid", "model": "S6-GR1P10K", "power_kw": 10.0, "price": 950, "phase": "single", "type": "On-Grid", "max_charge_idc": 0, "cable_spec": "4 x 10 mm²"},

    # Growatt
    {"brand": "Growatt Off-Grid", "model": "SPF 5000 ES", "power_kw": 5.0, "price": 650, "phase": "single", "type": "Off-Grid", "max_charge_idc": 100, "cable_spec": "4 x 4 mm²"},
    {"brand": "Growatt Hybrid", "model": "SPH 6000", "power_kw": 6.0, "price": 850, "phase": "single", "type": "Hybrid", "max_charge_idc": 125, "cable_spec": "4 x 6 mm²"}
]

BATTERIES = [
    {"name": "AOKLY", "type": "عادية", "capacity_kwh": 5.12, "price": 725},
    {"name": "AOKLY", "type": "جداري", "capacity_kwh": 10.24, "price": 1400},
    {"name": "BICODI", "type": "عادية", "capacity_kwh": 5.12, "price": 700},
    {"name": "BICODI", "type": "جداري", "capacity_kwh": 10.24, "price": 1400},
    {"name": "BICODI", "type": "عادية", "capacity_kwh": 11.78, "price": 1475},
    {"name": "BICODI", "type": "عادية", "capacity_kwh": 16.1, "price": 1800}
]

# ==========================================
# 4. الدوال الحسابية المعدلة والدقيقة
# ==========================================
def get_ac_board_price(current_amp):
    if current_amp <= 15: return 125
    elif current_amp <= 25: return 160
    elif current_amp <= 40: return 180
    elif current_amp <= 60: return 250
    elif current_amp <= 120: return 350
    else: return 450

def calculate_optimal_battery(net_req_kwh):
    """تحديد أقرب بطارية سعةً لمنع تقفيز التكلفة دون داعي"""
    if net_req_kwh <= 0:
        return {"brand": "بدون بطاريات", "unit_cap": 0, "total_cap": 0, "qty": 0, "unit_price": 0, "total_price": 0}
    
    # نسبة تفريغ آمنة DoD = 80%
    gross_kwh_needed = net_req_kwh / 0.80 

    best_match = None
    min_cost = float('inf')

    for bat in BATTERIES:
        qty = math.ceil(gross_kwh_needed / bat["capacity_kwh"])
        total_price = qty * bat["price"]
        
        # اختيار الخيار الأقل تكلفة الذي يغطي الاحتياج
        if total_price < min_cost:
            min_cost = total_price
            best_match = {
                "brand": f"{bat['name']} ({bat['type']})",
                "unit_cap": bat["capacity_kwh"],
                "total_cap": round(bat["capacity_kwh"] * qty, 2),
                "qty": qty,
                "unit_price": bat["price"],
                "total_price": total_price
            }
            
    return best_match

# ==========================================
# 5. الواجهة الهيكلية (التصميم الشجري)
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

if category == "سكني":
    c1, c2, c3 = st.columns(3)
    with c1: day_amp = st.number_input("أمبير نهار:", min_value=0, max_value=300, value=None)
    with c2: night_amp = st.number_input("أمبير ليل:", min_value=0, max_value=300, value=None)
    with c3: night_hours = st.number_input("ساعات التشغيل الليلي:", min_value=1, max_value=24, value=4)

    c4, c5 = st.columns(2)
    with c4: sys_type = st.radio("نوع المنظومة:", options=["Hybrid", "Off-Grid"], horizontal=True)
    with c5: phase_radio = st.radio("عدد الأطوار:", options=["1PH", "3PH"], horizontal=True)
    phase_option = "single" if phase_radio == "1PH" else "three"

elif category == "تجاري":
    c1, c2, c3 = st.columns(3)
    with c1: day_amp = st.number_input("أمبير نهار:", min_value=0, max_value=500, value=None)
    with c2: night_amp = st.number_input("أمبير ليل:", min_value=0, max_value=500, value=None)
    with c3: night_hours = st.number_input("ساعات التشغيل الليلي:", min_value=1, max_value=24, value=4)

    c4, c5 = st.columns(2)
    with c4: sys_type = st.radio("نوع المنظومة:", options=["Hybrid", "On-Grid", "Off-Grid"], horizontal=True)
    with c5: phase_radio = st.radio("عدد الأطوار:", options=["1PH", "3PH"], horizontal=True)
    phase_option = "single" if phase_radio == "1PH" else "three"

elif category == "زراعي":
    c1, c2 = st.columns(2)
    with c1: hp_power = st.number_input("القدرة بالحصان (HP):", min_value=1, max_value=500, value=10, step=1)
    with c2: phase_radio = st.radio("عدد الأطوار:", options=["3PH", "1PH"], horizontal=True)
    phase_option = "single" if phase_radio == "1PH" else "three"

st.markdown("---")

# ==========================================
# 6. الحسابات واختيار المكونات
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
        # حساب قدرة الأحمال الفعلية
        load_kw = (day_amp * 230) / 1000.0
        
        # صافي الطاقة الليلية المطلوبة للبطاريات (kWh)
        net_night_kwh = (night_amp * 230 * night_hours) / 1000.0 if sys_type != "On-Grid" else 0

        st.subheader("⚙️ تفاصيل المنظومة والماركات والمواصفات")
        col_i, col_b, col_p = st.columns(3)

        # --- 1. اختيار الإنفرتر بمرونة كاملة ---
        with col_i:
            st.markdown("##### 🔌 الإنفرتر / العاكس")
            filtered_inverters = [inv for inv in INVERTER_BRANDS if inv["phase"] == phase_option and inv["type"] == sys_type]
            if not filtered_inverters:
                filtered_inverters = [inv for inv in INVERTER_BRANDS if inv["phase"] == phase_option]

            inv_names = [f"{inv['brand']} - {inv['model']} ({inv['power_kw']} kW)" for inv in filtered_inverters]
            selected_inv_idx = st.selectbox("اختر ماركة ونوع الإنفرتر:", range(len(inv_names)), format_func=lambda x: inv_names[x])
            chosen_single_inv = filtered_inverters[selected_inv_idx]

            # حساب العدد الدقيق على أساس الإنفرتر المختار
            calculated_inv_qty = math.ceil(load_kw / chosen_single_inv["power_kw"]) if chosen_single_inv["power_kw"] > 0 else 1
            inv_qty = st.number_input("عدد الإنفرترات:", min_value=1, max_value=10, value=calculated_inv_qty, step=1)

            chosen_inv_combo = {
                "inverter": chosen_single_inv,
                "qty": inv_qty,
                "total_power": chosen_single_inv["power_kw"] * inv_qty,
                "total_price": chosen_single_inv["price"] * inv_qty
            }

        # --- 2. حساب البطاريات الدقيق ---
        with col_b:
            st.markdown("##### 🔋 بنك البطاريات")
            if sys_type == "On-Grid":
                st.caption("ℹ️ نظام On-Grid لا يحتاج إلى بطاريات.")
                chosen_bat = {"brand": "بدون بطاريات", "unit_cap": 0, "total_cap": 0, "qty": 0, "unit_price": 0, "total_price": 0}
            else:
                optimal_bat = calculate_optimal_battery(net_night_kwh)
                bat_names = [f"{b['name']} {b['type']} ({b['capacity_kwh']} kWh)" for b in BATTERIES]
                
                default_bat_idx = next((i for i, b in enumerate(BATTERIES) if b["capacity_kwh"] == optimal_bat["unit_cap"]), 0)
                selected_bat_idx = st.selectbox("اختر البطارية:", range(len(bat_names)), index=default_bat_idx, format_func=lambda x: bat_names[x])
                chosen_single_bat = BATTERIES[selected_bat_idx]

                # العدد الموصى به بدون زيادة مفرطة
                rec_bat_qty = math.ceil((net_night_kwh / 0.80) / chosen_single_bat["capacity_kwh"]) if chosen_single_bat["capacity_kwh"] > 0 else 1
                bat_qty = st.number_input("عدد البطاريات:", min_value=1, max_value=20, value=rec_bat_qty, step=1)

                total_bat_cap = round(chosen_single_bat["capacity_kwh"] * bat_qty, 2)
                st.info(f"📌 **السعة الإجمالية:** `{total_bat_cap} kWh` | **المطلوب الفعلي:** `{net_night_kwh:.2f} kWh`")

                chosen_bat = {
                    "brand": f"{chosen_single_bat['name']} ({chosen_single_bat['type']})",
                    "unit_cap": chosen_single_bat["capacity_kwh"],
                    "total_cap": total_bat_cap,
                    "qty": bat_qty,
                    "unit_price": chosen_single_bat["price"],
                    "total_price": chosen_single_bat["price"] * bat_qty
                }

        # --- 3. حساب الألواح الشمسية ---
        with col_p:
            st.markdown("##### ☀️ الألواح الشمسية")
            panel_names = [f"{p['brand']} - (${p['price']})" for p in PANEL_OPTIONS]
            selected_p_idx = st.selectbox("نوع اللوح:", range(len(panel_names)), format_func=lambda x: panel_names[x])
            chosen_panel = PANEL_OPTIONS[selected_p_idx]

            # حساب احتياج النهار + احتياج شحن البطاريات
            day_energy_kwh = load_kw * 6.0  # معدل 6 ساعات ذروة
            total_kwh_needed = day_energy_kwh + net_night_kwh
            
            req_panel_watts = (total_kwh_needed * 1000) / 4.5  # 4.5 ساعات شمس فعيلة
            calc_panels = math.ceil(req_panel_watts / chosen_panel["power_w"])

            if st.checkbox("تعديل يدوي لعدد الألواح"):
                final_panels = st.number_input("حدد عدد الألواح:", min_value=1, max_value=200, value=calc_panels, step=1)
            else:
                final_panels = calc_panels

        st.markdown("---")

        # ==========================================
        # 7. التكاليف والنتائج النهائية
        # ==========================================
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

        if show_formulas:
            st.subheader("📐 المعادلات الرياضية والآلية الحسابية المعدلة")
            st.write(f"1. قدرة الحمل النهارية: **{load_kw:.2f} kW**")
            st.latex(r"\text{Load Power (kW)} = \frac{\text{Day Amp} \times 230}{1000}")
            st.write(f"2. الطاقة الليلية الصافية: **{net_night_kwh:.2f} kWh** (تفريغ آمن 80%)")
            st.latex(r"\text{Battery Gross (kWh)} = \frac{\text{Night Amp} \times 230 \times \text{Hours}}{1000 \times 0.80}")
            st.markdown("---")

        st.subheader("💡 التنبيهات والتوصيات الفنية")
        st.markdown('<div style="direction: rtl; text-align: right;">', unsafe_allow_html=True)
        
        st.success(f"⚡ **الإنفرتر المختار:** {single_inv['brand']} ({single_inv['model']}) - عدد **{inv_qty}** بقدرة إجمالية **{single_inv['power_kw'] * inv_qty} kW**")
            
        if sys_type != "On-Grid":
            actual_hours = (chosen_bat["total_cap"] * 0.80 * 1000) / (night_amp * 230) if night_amp > 0 else 0
            st.success(f"🔋 **البطاريات:** {chosen_bat['brand']} - عدد **{chosen_bat['qty']}** بسعة إجمالية **{chosen_bat['total_cap']} kWh**")
            st.info(f"المدة التشغيلية المتوقعة عند سحب ({night_amp}A) ليلًا: **{int(actual_hours)} ساعة و {int((actual_hours % 1) * 60)} دقيقة**")

        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown("---")

        # جدول الكلفة التفصيلي
        st.subheader("📋 جدول المواد والتكاليف - شركة ركن التعمير")
        table_data = [
            {"المكون / الملحق": "الألواح الشمسية", "المواصفات والوصف": f"لوح {chosen_panel['brand']}", "الكمية": f"{final_panels}", "سعر الوحدة": f"${chosen_panel['price']}", "الإجمالي": f"${panels_cost}"},
            {"المكون / الملحق": "ملحقات الـ DC", "المواصفات والوصف": "أسلاك + قواطع + MC4", "الكمية": f"{num_strings} سلاسل", "سعر الوحدة": f"${DC_ACCESSORIES_PRICE_PER_STRING}", "الإجمالي": f"${dc_acc_cost}"},
            {"المكون / الملحق": "العاكس / الإنفرتر", "المواصفات والوصف": f"{single_inv['brand']} ({single_inv['model']})", "الكمية": f"{inv_qty}", "سعر الوحدة": f"${single_inv['price']}", "الإجمالي": f"${inv_cost}"},
            {"المكون / الملحق": "بنك البطاريات", "المواصفات والوصف": f"{chosen_bat['brand']}", "الكمية": f"{chosen_bat['qty']}", "سعر الوحدة": f"${chosen_bat['unit_price']}", "الإجمالي": f"${bat_cost}"},
            {"المكون / الملحق": "بورد الـ AC", "المواصفات والوصف": f"بورد حماية لغاية ({day_amp}A)", "الكمية": "1", "سعر الوحدة": f"${ac_board_cost}", "الإجمالي": f"${ac_board_cost}"},
            {"المكون / الملحق": "منظومة التأريض", "المواصفات والوصف": "منظومة تأريض كاملة", "الكمية": "1", "سعر الوحدة": f"${EARTHING_SYSTEM_PRICE}", "الإجمالي": f"${EARTHING_SYSTEM_PRICE}"},
        ]
        st.table(table_data)
        st.success(f"### 💰 التكلفة الإجمالية النهائية للمنظومة: ${total_cost:,}")
