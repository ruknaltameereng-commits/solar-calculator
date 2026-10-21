def calculate_panels(day_amp, required_battery_kwh):
    day_power_w = day_amp * 230 * 1.3
    day_panels_exact = day_power_w / PANEL_SPECS["power_w"]
    
    charging_power_w = (required_battery_kwh * 1000) / 9.0
    charging_panels_exact = charging_power_w / PANEL_SPECS["power_w"]
    
    total_panels_raw = day_panels_exact + charging_panels_exact
    target_panels = math.ceil(total_panels_raw)
    
    # حساب الحد الأدنى للسلاسل لمنع أن تتجاوز السلسلة 9 ألواح
    min_strings = math.ceil(target_panels / PANEL_SPECS["max_string_size"])
    
    # البحث من الحد الأدنى المقبول حركياً
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


def calculate_battery_bank(night_amp, night_hours):
    required_kwh = night_amp * 0.285 * night_hours
    
    best_option = None
    min_diff = float('inf')
    
    # توسيع مدى الفحص حتى 10 بطاريات للأحمال العالية جداً
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
                
    # خيار حماية احتياطي في حال تجاوز السعة المتاحة
    if best_option is None:
        max_bat = BATTERIES[-1]
        qty = math.ceil(required_kwh / max_bat["capacity_kwh"])
        best_option = {
            "model": max_bat["name"],
            "unit_cap": max_bat["capacity_kwh"],
            "total_cap": max_bat["capacity_kwh"] * qty,
            "qty": qty,
            "price": max_bat["price"]
        }
        
    return required_kwh, best_option
