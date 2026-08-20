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

# عرض الشعار في القائمة الجانبية
try:
    st.sidebar.image("logo.png", use_container_width=True)
except Exception:
    pass

# مفتاح تحكم لإظهار أو إخفاء المعادلات الحسابية
with st.sidebar:
    st.header("⚙️ إعدادات العرض")
    show_formulas = st.toggle("إظهار المعادلات والآلية الحسابية", value=False)
    st.caption("تفعيل هذا الخيار سيظهر الشرح الرياضي والمعادلات المستخدمة في الحسابات.")

# ==========================================
# 2. الهيدر الرئيسي (الشعار + العنوان + صورة واجهة الشركة)
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

# عرض صورة واجهة الشركة
try:
    st.image("company.png", use_container_width=True, caption="شركة ركن التعمير للحلول والمنظومات الشمسية")
except Exception:
    pass

st.markdown("---")

# ==========================================
# 3. قاعدة البيانات الفنية والأسعار المعتمدة
# ==========================================
PANEL_OPTIONS = [
    {"brand": "Jinko Solar 725W (Voc 49.12V)", "power_w": 725, "price": 175, "max_string_size": 9},
    {"brand": "Longi Solar 640W (Voc 53.70V)", "power_w": 640, "price": 165, "max_string_size": 8}
]

DC_ACCESSORIES_PRICE_PER_STRING = 30
EARTHING_SYSTEM_PRICE = 160

INVERTER_BRANDS = [
    # GoGo Inverters (IP21)
    {"brand": "GoGo Hybrid (IP21)", "model": "GoGo-5.5KW", "power_kw": 5.5, "price": 600, "phase": "single", "type": "Hybrid", "max_charge_idc": 110, "cable_spec": "4 x 4 mm²"},
    {"brand": "GoGo Hybrid (IP21)", "model": "GoGo-6KW", "power_kw": 6.0, "price": 650, "phase": "single", "type": "Hybrid", "max_charge_idc": 120, "cable_spec": "4 x 4 mm²"},

    # Growatt Inverters (IP21 / IP20)
    {"brand": "Growatt Off-Grid (IP21)", "model": "SPF 5000 ES", "power_kw": 5.0, "price": 650, "phase": "single", "type": "Off-Grid", "max_charge_idc": 100, "cable_spec": "4 x 4 mm²"},
    {"brand": "Growatt Off-Grid/Hybrid (IP21)", "model": "SPE 12000 ES", "power_kw": 12.0, "price": 1450, "phase": "single", "type": "Off-Grid", "max_charge_idc": 200, "cable_spec": "4 x 16 mm²"},
    {"brand": "Growatt Off-Grid/Hybrid (IP21)", "model": "SPE 12000 ES", "power_kw": 12.0, "price": 1450, "phase": "single", "type": "Hybrid", "max_charge_idc": 200, "cable_spec": "4 x 16 mm²"},

    # Deye Inverters (IP65)
    {"brand": "Deye Hybrid (IP65)", "model": "SUN-5K-SG04LP1-EU-SM2", "power_kw": 5.0, "price": 750, "phase": "single", "type": "Hybrid", "max_charge_idc": 120, "cable_spec": "4 x 4 mm²"},
    {"brand": "Deye Hybrid (IP65)", "model": "SUN-6K-SG04LP1-EU-SM2", "power_kw": 6.0, "price": 875, "phase": "single", "type": "Hybrid", "max_charge_idc": 135, "cable_spec": "4 x 6 mm²"},
    {"brand": "Deye Hybrid (IP65)", "model": "SUN-8K-SG05LP1-EU-SM2", "power_kw": 8.0, "price": 1225, "phase": "single", "type": "Hybrid", "max_charge_idc": 190, "cable_spec": "4 x 10 mm²"},
    {"brand": "Deye Hybrid (IP65)", "model": "SUN-12K-SG02LP1-EU-AM3", "power_kw": 12.0, "price": 1800, "phase": "single", "type": "Hybrid", "max_charge_idc": 250, "cable_spec": "4 x 16 mm²"},
    {"brand": "Deye Hybrid (IP65)", "model": "SUN-16K-SG01LP1-EU", "power_kw": 16.0, "price": 2000, "phase": "single", "type": "Hybrid", "max_charge_idc": 290, "cable_spec": "4 x 16 mm²"},
    {"brand": "Deye Off-Grid", "model": "SUN-6K-OG", "power_kw": 6.0, "price": 700, "phase": "single", "type": "Off-Grid", "max_charge_idc": 120, "cable_spec": "4 x 4 mm²"},
    {"brand": "Deye On-Grid", "model": "SUN-16K-G04", "power_kw": 16.0, "price": 1300, "phase": "single", "type": "On-Grid", "max_charge_idc": 0, "cable_spec": "4 x 16 mm²"},

    # Solis Inverters (IP65)
    {"brand": "Solis Hybrid (IP65)", "model": "S6-EH1P5K-L-PLUS", "power_kw": 5.0, "price": 750, "phase": "single", "type": "Hybrid", "max_charge_idc": 112, "cable_spec": "4 x 4 mm²"},
    {"brand": "Solis Hybrid (IP65)", "model": "S6-EH1P6K-L-PLUS", "power_kw": 6.0, "price": 800, "phase": "single", "type": "Hybrid", "max_charge_idc": 135, "cable_spec": "4 x 6 mm²"},
    {"brand": "Solis Hybrid (IP65)", "model": "S6-EH1P8K-L-PLUS", "power_kw": 8.0, "price": 1300, "phase": "single", "type": "Hybrid", "max_charge_idc": 190, "cable_spec": "4 x 10 mm²"},
    {"brand": "Solis Hybrid (IP65)", "model": "S6-EH1P10K-L-PLUS", "power_kw": 10.0, "price": 1650, "phase": "single", "type": "Hybrid", "max_charge_idc": 210, "cable_spec": "4 x 10 mm²"},
    {"brand": "Solis Hybrid (IP65)", "model": "S6-EH1P12K03-NV-YD-L", "power_kw": 12.0, "price": 1900, "phase": "single", "type": "Hybrid", "max_charge_idc": 250, "cable_spec": "4 x 16 mm²"},
    {"brand": "Solis On-Grid", "model": "S6-GR1P5K", "power_kw": 5.0, "price": 500, "phase": "single", "type": "On-Grid", "max_charge_idc": 0, "cable_spec": "4 x 4 mm²"},
    {"brand": "Solis On-Grid", "model": "S6-GR1P10K", "power_kw": 10.0, "price": 950, "phase": "single", "type": "On-Grid", "max_charge_idc": 0, "cable_spec": "4 x 10 mm²"},

    # SRNE
    {"brand": "SRNE Off-Grid (IP21)", "model": "SRNE-16K-IP20", "power_kw": 16.0, "price": 1600, "phase": "single", "type": "Off-Grid", "max_charge_idc": 200, "cable_spec": "4 x 10 mm²"},

    # 3-Phase Systems
    {"brand": "Deye 3-Phase", "model": "SUN-30K-SG01HP3", "power_kw": 30.0, "price": 3800, "phase": "three", "type": "Hybrid", "max_charge_idc": 100, "cable_spec": "4 x 16 mm²"},
    {"brand": "Deye 3-Phase", "model": "SUN-50K-SG01HP3", "power_kw": 50.0, "price": 5200, "phase": "three", "type": "Hybrid", "max_charge_idc": 150, "cable_spec": "4 x 25 mm²"}
]

BATTERIES = [
    {"name": "AOKLY", "type": "عادية", "capacity_kwh": 5.12, "price": 725},
    {"name": "AOKLY", "type": "جداري", "capacity_kwh": 10.24, "price": 1400},
    {"name": "AOKLY", "type": "أرضي", "capacity_kwh": 10.24, "price": 1420},
    {"name": "AOKLY", "type": "عادية", "capacity_kwh": 15.36, "price": 1650},
    {"name": "BICODI", "type": "عادية", "capacity_kwh": 5.12, "price": 700},
    {"name": "BICODI", "type": "جداري", "capacity_kwh": 10.24, "price": 1400},
    {"name": "BICODI", "type": "أرضي", "capacity_kwh": 10.24, "price": 1420},
    {"name": "BICODI", "type": "عادية", "capacity_kwh": 11.78, "price": 1475},
    {"name": "BICODI", "type": "عادية", "capacity_kwh": 16.1, "price": 1800},
    {"name": "BICODI", "type": "عادية", "capacity_kwh": 17.66, "price": 1950}
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

def calculate_optimal_battery(net_req_kwh):
    if net_req_kwh <= 0:
        return {"brand": "بدون بطاريات", "unit_cap": 0, "total_cap": 0, "qty": 0, "unit_price": 0, "total_price": 0}
    
    gross_kwh_needed = net_req_kwh / 0.80 
    best_match = None
    min_cost = float('inf')

    for bat in BATTERIES:
        qty = math.ceil(gross_kwh_needed / bat["capacity_kwh"])
        total_price = qty * bat["price"]
        if total_price < min_cost:
            min_cost = total_price
            best_match = {
                "brand": f"{bat['name']} ({bat['type']})" if bat['type'] != 'عادية' else bat['name'],
                "unit_cap": bat["capacity_kwh"],
                "total_cap": round(bat["capacity_kwh"] * qty, 2),
                "qty": qty,
                "unit_price": bat["price"],
                "total_price": total_price
            }
    return best_match

# ==========================================
# 5. واجهة المستخدم والتفرعات
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
    with c1: day_amp = st.number_input("أمبير النهار (ن):", min_value=0, max_value=300, value=None, placeholder="أدخل أمبير النهار...")
    with c2: night_amp = st.number_input("أمبير الليل (ل):", min_value=0, max_value=300, value=None, placeholder="أدخل أمبير الليل...")
    with c3: night_hours = st.number_input("ساعات التشغيل الليلي:", min_value=1, max_value=24, value=4)

    c4, c5 = st.columns(2)
    with c4: sys_type = st.radio("نوع المنظومة:", options=["Hybrid", "Off-Grid"], horizontal=True)
    with c5: phase_radio = st.radio("عدد الأطوار:", options=["1PH", "3PH"], horizontal=True)
    phase_option = "single" if phase_radio == "1PH" else "three"

elif category == "تجاري":
    c1, c2, c3 = st.columns(3)
    with c1: day_amp = st.number_input("أمبير النهار (ن):", min_value=0, max_value=500, value=None, placeholder="أدخل أمبير النهار...")
    with c2: night_amp = st.number_input("أمبير الليل (ل):", min_value=0, max_value=500, value=None, placeholder="أدخل أمبير الليل...")
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
    st.info(f"📌 منظومة زراعية لمضخات الري قدرة **{hp_power} حصان** ({hp_power * 0.746:.2f} kW)")

st.markdown("---")

# ==========================================
# 6. الحسابات والنتائج
# ==========================================
if category == "زراعي":
    if hp_power > 0:
        req_kw = hp_power * 0.746 * 1.3
        target_panels = math.ceil((req_kw * 1000) / PANEL_OPTIONS[0]["power_w"])
        total_cost = target_panels * PANEL_OPTIONS[0]["price"] + (req_kw * 120) 
        st.success(f"☀️ عدد الألواح المطلوبة: **{target_panels} لوحاً** ({PANEL_OPTIONS[0]['brand']})")
        st.success(f"💰 التكلفة التقديرية الإجمالية للمنظومة الزراعية: **${total_cost:,.0f}**")
else:
    if day_amp is None or night_amp is None or day_amp == 0:
        st.info("👈 يرجى إدخال أمبير النهار والليل لبدء الحسابات وتوليد النتائج تلقائياً.")
    else:
        load_kw = (day_amp * 230) / 1000.0
        recommended_kw = load_kw * 1.2
        net_night_kwh = (night_amp * 0.285 * night_hours) if sys_type != "On-Grid" else 0

        st.subheader("⚙️ تحديد المواصفات والتعديل المباشر")
        col_p, col_i, col_b = st.columns(3)

        # --- الألواح الشمسية ---
        with col_p:
            st.markdown("##### ☀️ الألواح الشمسية")
            panel_names = [f"{p['brand']} - (${p['price']})" for p in PANEL_OPTIONS]
            selected_p_str = st.selectbox("نوع اللوح:", options=panel_names)
            chosen_panel = PANEL_OPTIONS[panel_names.index(selected_p_str)]

            day_p_val = day_amp * 230 * 1.3
            chg_p_val = (net_night_kwh * 1000) / 9.0
            auto_panels = math.ceil((day_p_val + chg_p_val) / chosen_panel["power_w"])

            if st.checkbox("تعديل يدوي لعدد الألواح"):
                final_panels = st.number_input("حدد عدد الألواح المطلوب:", min_value=1, max_value=200, value=auto_panels, step=1)
            else:
                final_panels = auto_panels

        # --- الإنفرتر (العاكس) ---
        with col_i:
            st.markdown("##### 🔌 الإنفرتر / العاكس")
            filtered_inverters = [inv for inv in INVERTER_BRANDS if inv["phase"] == phase_option and inv["type"] == sys_type]
            if not filtered_inverters:
                filtered_inverters = [inv for inv in INVERTER_BRANDS if inv["phase"] == phase_option]

            inv_names = [f"{inv['brand']} [{inv['model']}] - {inv['power_kw']} kW (${inv['price']})" for inv in filtered_inverters]
            selected_inv_idx = st.selectbox("اختر ماركة ونوع الإنفرتر:", range(len(inv_names)), format_func=lambda x: inv_names[x])
            chosen_single_inv = filtered_inverters[selected_inv_idx]

            calc_inv_qty = math.ceil(recommended_kw / chosen_single_inv["power_kw"]) if chosen_single_inv["power_kw"] > 0 else 1
            inv_qty = st.number_input("عدد الإنفرترات المطلوبة:", min_value=1, max_value=10, value=calc_inv_qty, step=1)

            chosen_inv_combo = {
                "inverter": chosen_single_inv,
                "qty": inv_qty,
                "total_power": chosen_single_inv["power_kw"] * inv_qty,
                "total_price": chosen_single_inv["price"] * inv_qty
            }

        # --- بنك البطاريات ---
        with col_b:
            st.markdown("##### 🔋 بنك البطاريات")
            if sys_type == "On-Grid":
                st.caption("ℹ️ نظام On-Grid لا يحتاج إلى بطاريات لتخزين الطاقة.")
                chosen_bat = {"brand": "بدون بطاريات", "unit_cap": 0, "total_cap": 0, "qty": 0, "unit_price": 0, "total_price": 0}
            else:
                opt_bat = calculate_optimal_battery(net_night_kwh)
                bat_brand_options = [f"{b['name']} ({b['capacity_kwh']} kWh{' - ' + b['type'] if b['type'] != 'عادية' else ''}) - (${b['price']})" for b in BATTERIES]
                
                default_idx = next((i for i, b in enumerate(BATTERIES) if b["capacity_kwh"] == opt_bat["unit_cap"]), 0)
                selected_bat_str = st.selectbox("اختر نوع/سعة البطارية:", options=bat_brand_options, index=default_idx)
                chosen_single_bat = BATTERIES[bat_brand_options.index(selected_bat_str)]

                calc_bat_qty = math.ceil((net_night_kwh / 0.80) / chosen_single_bat["capacity_kwh"]) if chosen_single_bat["capacity_kwh"] > 0 else 1
                bat_qty = st.number_input("عدد البطاريات المطلوبة:", min_value=1, max_value=20, value=calc_bat_qty, step=1)

                total_bat_cap = round(chosen_single_bat["capacity_kwh"] * bat_qty, 2)
                st.info(f"📌 **السعة الإجمالية:** `{total_bat_cap} kWh` | **احتياج التفريغ الصافي:** `{net_night_kwh:.2f} kWh`")

                chosen_bat = {
                    "brand": f"{chosen_single_bat['name']} ({chosen_single_bat['type']})" if chosen_single_bat['type'] != 'عادية' else chosen_single_bat['name'],
                    "unit_cap": chosen_single_bat["capacity_kwh"],
                    "total_cap": total_bat_cap,
                    "qty": bat_qty,
                    "unit_price": chosen_single_bat["price"],
                    "total_price": chosen_single_bat["price"] * bat_qty
                }

        st.markdown("---")

        # ==========================================
        # 7. التكاليف والمعادلات والتنبيهات
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

            # عرض الشرح والمعادلات
            if show_formulas:
                st.subheader("📐 المعادلات الرياضية والآلية الحسابية للمنظومة")
                st.write(f"1. قدرة أحمال النهار المطلوبة: **{load_kw:.2f} kW**")
                st.latex(r"\text{Load Power (kW)} = \frac{\text{Day Amp} \times 230}{1000}")
                st.write(f"2. السعة الصافية المطلوبة للبطاريات ليلاً: **{net_night_kwh:.2f} kWh**")
                st.latex(r"\text{Battery Gross (kWh)} = \frac{\text{Night Amp} \times 0.285 \times \text{Night Hours}}{0.80}")
                st.write(f"3. إجمالي عدد الألواح الشمسية المطلوبة: **{final_panels} لوحاً**")
                st.latex(rf"\text{{Day Power}} = {day_amp} \times 230 \times 1.3 = {day_p_val:.0f}\text{{ W}}")
                st.latex(rf"\text{{Charging Power}} = \frac{{{net_night_kwh:.2f} \times 1000}}{{9.0}} = {chg_p_val:.0f}\text{{ W}}")
                st.write(f"4. تيار الشحن المسحوب من الشبكة الوطنية (AC): **{charge_iac_210v:.1f} A**")
                st.latex(rf"\text{{AC Current}} = \frac{{{actual_charge_idc:.1f} \times 51.5}}{{210 \times 0.95}} = {charge_iac_210v:.1f}\text{{ A (AC)}}")
                st.markdown("---")

            # التنبيهات والتوصيات الفنية
            st.subheader("💡 التنبيهات والتوصيات الفنية")
            st.markdown('<div style="direction: rtl; text-align: right;">', unsafe_allow_html=True)
            
            st.success(f"⚡ **الإنفرتر المختار:** {single_inv['brand']} ({single_inv['model']}) {single_inv['power_kw']} kW (عدد {inv_qty}) - القدرة الكلية: **{single_inv['power_kw'] * inv_qty} kW**")
                
            if "IP21" in single_inv["brand"] or "IP20" in single_inv["brand"]:
                st.warning("⚠️ **ملاحظة حماية المكان:** هذا الجهاز تصنيفه **IP21**، يجب تركيبه داخل مكان مغلق وجاف بعيداً عن الأمطار والأتربة المباشرة مع مراعاة التهوية الجيدة.")

            if sys_type != "On-Grid":
                actual_hours = (chosen_bat["total_cap"] * 0.80) / (0.285 * night_amp) if night_amp > 0 else 0
                actual_amp_avail = (chosen_bat["total_cap"] * 0.80) / (0.285 * night_hours) if night_hours > 0 else 0
                
                st.success(f"🔋 **البطاريات المختارة:** {chosen_bat['brand']} {chosen_bat['unit_cap']} kWh (عدد {chosen_bat['qty']}) - السعة الكلية **{chosen_bat['total_cap']} kWh**")

                if chosen_bat["total_cap"] < net_night_kwh * 0.95:
                    st.warning(f"⚠️ تنبيه: سعة بنك البطاريات تكفي لتشغيل حمل ({night_amp}A) لمدة **{actual_hours:.1f} ساعة** فقط.")
                
                st.info(f"الأمبير المتاح المستمر خلال ({night_hours}) ساعات: **{actual_amp_avail:.1f} أمبير** | مدة تشغيل حمل ({night_amp}A): **{int(actual_hours)} ساعة و {int((actual_hours % 1) * 60)} دقيقة**")
                
                if charge_iac_210v > 0:
                    st.warning(f"🔌 تيار الشحن المسحوب من الوطنية: **{charge_iac_210v:.1f}A AC** (عند ضبط نسبة الشحن 80%) | مقطع كابل AC المطلوب: **({single_inv['cable_spec']}) لكل إنفرتر**.")

            st.markdown('</div>', unsafe_allow_html=True)
            st.markdown("---")

            # جدول المواد والتكاليف التفصيلي
            st.subheader("📋 جدول المواد والتكاليف التفصيلي - شركة ركن التعمير")
            table_data = [
                {"المكون / الملحق": "الألواح الشمسية", "المواصفات والوصف": f"لوح {chosen_panel['brand']} (شامل الهيكل والتركيب)", "الكمية": f"{final_panels} لوحاً", "سعر الوحدة ($)": f"${chosen_panel['price']}", "الإجمالي ($)": f"${panels_cost}"},
                {"المكون / الملحق": "ملحقات الـ DC", "المواصفات والوصف": "أسلاك + قواطع + فيوزات + MC4 + أنابيب", "الكمية": f"{num_strings} سلاسل", "سعر الوحدة ($)": f"${DC_ACCESSORIES_PRICE_PER_STRING}", "الإجمالي ($)": f"${dc_acc_cost}"},
                {"المكون / الملحق": "العاكس / الإنفرتر", "المواصفات والوصف": f"{inv_qty}x {single_inv['brand']} ({single_inv['model']})", "الكمية": f"{inv_qty}", "سعر الوحدة ($)": f"${single_inv['price']}", "الإجمالي ($)": f"${inv_cost}"},
                {"المكون / الملحق": "بنك البطاريات", "المواصفات والوصف": f"{chosen_bat['brand']} ({chosen_bat['unit_cap']} kWh)" if chosen_bat['qty'] > 0 else "بدون بطاريات", "الكمية": f"{chosen_bat['qty']}", "سعر الوحدة ($)": f"${chosen_bat['unit_price']}", "الإجمالي ($)": f"${bat_cost}"},
                {"المكون / الملحق": "بورد الـ AC", "المواصفات والوصف": f"بورد حماية وتوازي AC لغاية ({day_amp}A)", "الكمية": "1", "سعر الوحدة ($)": f"${ac_board_cost}", "الإجمالي ($)": f"${ac_board_cost}"},
                {"المكون / الملحق": "منظومة التأريض", "المواصفات والوصف": "وتد نحاسي + أسلاك 30m + مادة تأريض + الحفر والربط", "الكمية": "1", "سعر الوحدة ($)": f"${EARTHING_SYSTEM_PRICE}", "الإجمالي ($)": f"${EARTHING_SYSTEM_PRICE}"},
            ]
            st.table(table_data)
            st.success(f"### 💰 التكلفة الإجمالية النهائية للمنظومة: ${total_cost:,}")
