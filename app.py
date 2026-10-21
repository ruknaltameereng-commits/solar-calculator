# ==============================================================================
# Solar System Engine & Pricing Calculator - Clean Ultimate Version
# Developed for: Eng. Murad
# ==============================================================================

import math

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

# بطاريات Low Voltage
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
    """تحديد سعر بورد الـ AC بناءً على الأمبيرية النهارية"""
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
        return 0  # تخضع لتقدير المهندس للكشف النهائي


def calculate_battery_bank(night_amp, night_hours):
    """معادلة طاقة البطاريات: Energy = Current * 0.285 * Hours"""
    required_kwh = night_amp * 0.285 * night_hours
    
    best_option = None
    min_diff = float('inf')
    
    # فحص أفضل الخيارات للبطاريات (1 إلى 10 وحدات بالتوازي)
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
    """
    حساب الألواح حسب معادلة المهندس مراد:
    1. ألواح النهار = (التيار * 230 * 1.3) / 640
    2. ألواح الشحن = ((طاقة البطارية * 1000) / 9) / 640
    3. تحقيق التساوي التام بين السلاسل وأن لا تتجاوز أي سلسلة 9 ألواح
    """
    day_power_w = day_amp * 230 * 1.3
    day_panels_exact = day_power_w / PANEL_SPECS["power_w"]
    
    charging_power_w = (required_battery_kwh * 1000) / 9.0
    charging_panels_exact = charging_power_w / PANEL_SPECS["power_w"]
    
    total_panels_raw = day_panels_exact + charging_panels_exact
    target_panels = math.ceil(total_panels_raw)
    
    # حساب الحد الأدنى الممكن للسلاسل لتفادي تجاوز 9 ألواح للسلسلة
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
    """اختيار العاكس المناسب مع هامش أمان +20%"""
    load_kw = (day_amp * 230) / 1000.0
    required_kw_with_safety = load_kw * 1.2
    
    target_phase = "three" if is_hv_3ph else "single"
    
    for inv in INVERTERS:
        if inv["power_kw"] >= required_kw_with_safety and inv["phase"] == target_phase:
            return inv, load_kw, required_kw_with_safety
            
    return INVERTERS[-1], load_kw, required_kw_with_safety


# ------------------------------------------------------------------------------
# 3. دالة المعالجة وطباعة المخرجات (Processing & Output Formatting)
# ------------------------------------------------------------------------------

def process_solar_request(day_amp, night_amp, night_hours, system_type="LV-1PH"):
    is_hv_3ph = True if "HV-3PH" in system_type.upper() else False
    
    # 1. الحسابات
    req_kwh, bat = calculate_battery_bank(night_amp, night_hours)
    p_info = calculate_panels(day_amp, req_kwh)
    inverter, load_kw, req_inv_kw = select_inverter(day_amp, is_hv_3ph)
    ac_board_cost = get_ac_board_price(day_amp)
    
    # 2. التكاليف
    panels_cost = p_info["total_panels"] * PANEL_SPECS["price_per_unit"]
    dc_acc_cost = p_info["strings_count"] * DC_ACCESSORIES_PRICE_PER_STRING
    inv_cost = inverter["price"]
    bat_cost = bat["price"] * bat["qty"]
    
    total_cost = panels_cost + dc_acc_cost + inv_cost + bat_cost + ac_board_cost + EARTHING_SYSTEM_PRICE

    # 3. الطباعة للعرض النهائي
    print("=" * 70)
    print(f"📊 التقرير الفني الشامل للمنظومة: ({day_amp}ن {night_amp}ل {night_hours}س {'HV-3PH' if is_hv_3ph else 'L-VOLT Single Phase'})")
    print("=" * 70)
    
    print("\n1️⃣ الخطوات والتفاصيل الرياضية (Calculations):")
    print("-" * 50)
    print("أ. بنك البطاريات (التفريغ الليلي):")
    print(f"   • Energy (kWh) = {night_amp}A × 0.285 × {night_hours}h = {req_kwh:.2f} kWh")
    print(f"   • البطاريات المختارة: {bat['qty']} × {bat['model']} (سعة إجمالية {bat['total_cap']:.2f} kWh)")
    
    print("\nب. الألواح الشمسية (قدرة 640W):")
    print(f"   • ألواح النهار ({day_amp}A): ({day_amp} × 230 × 1.3) = {p_info['day_power_w']:.1f} W ➔ {p_info['day_panels_exact']:.3f} لوح")
    print(f"   • ألواح الشحن ({req_kwh:.2f} kWh): ({req_kwh:.2f} × 1000 / 9) = {p_info['charging_power_w']:.1f} W ➔ {p_info['charging_panels_exact']:.3f} لوح")
    print(f"   • المجموع النظري للألواح = {p_info['total_panels_raw']:.3f} لوح")
    print(f"   • توزيع السلاسل المعتمد: {p_info['total_panels']} لوحاً = {p_info['strings_count']} سلاسل × {p_info['panels_per_string']} ألواح/سلسلة (تساوي تام)")
    
    print("\nج. العاكس الهجين (Inverter):")
    print(f"   • قدرة الحمل النهاري: {load_kw:.2f} kW + هامش أمان (+20%) = {req_inv_kw:.2f} kW")
    print(f"   • العاكس المعتمد: {inverter['name']}")
    
    print("\nد. بورد الـ AC والتأريض:")
    print(f"   • بورد الـ AC: أمبيرية {day_amp}A ➔ السعر المعتمد: ${ac_board_cost if ac_board_cost > 0 else 'تقدير المهندس'}")
    print(f"   • منظومة التأريض: منظومة كاملة بسعر ثابت ➔ $160")

    print("\n2️⃣ جدول المواد والتفاصيل (Bill of Materials):")
    print("-" * 70)
    print(f"{'المكون / الملحق':<20} | {'المواصفات والوصف الفني':<30} | {'الكمية':<8} | {'الإجمالي ($)':<10}")
    print("-" * 70)
    print(f"{'الألواح الشمسية':<20} | {'لوح 640W (شامل الهيكل والتركيب)':<30} | {p_info['total_panels']:<8} | ${panels_cost:<10}")
    print(f"{'ملحقات الـ DC':<20} | {'أسلاك 40m + قاطع + فيوزات + MC4':<30} | {p_info['strings_count']} سلاسل | ${dc_acc_cost:<10}")
    print(f"{'العاكس الهجين':<20} | {inverter['name']:<30} | 1        | ${inv_cost:<10}")
    print(f"{'بنك البطاريات':<20} | {bat['model'] + ' Low Voltage':<30} | {bat['qty']}        | ${bat_cost:<10}")
    print(f"{'بورد الـ AC':<20} | {f'بورد حماية (لغاية {day_amp}A)':<30} | 1        | ${ac_board_cost:<10}")
    print(f"{'منظومة التأريض':<20} | {'شاملة وتد نحاسي وسلك وحفر':<30} | 1        | ${EARTHING_SYSTEM_PRICE:<10}")
    print("-" * 70)

    print(f"\n3️⃣ الكلفة الإجمالية النهائية المباشرة للمشروع: ${total_cost:,}")
    print("=" * 70 + "\n")


# ------------------------------------------------------------------------------
# 4. تشغيل تجريبي
# ------------------------------------------------------------------------------
if __name__ == "__main__":
    process_solar_request(day_amp=20, night_amp=10, night_hours=4)
