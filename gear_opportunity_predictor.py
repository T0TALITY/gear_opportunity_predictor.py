import csv
import statistics


class GearOpportunityPredictor:
    def __init__(self):
        # Simple generic ratio map for a 6-speed manual performance car
        self.gear_ratios = {
            1: 2.66,
            2: 1.78,
            3: 1.30,
            4: 1.00,
            5: 0.74,
            6: 0.50,
        }

    def load_csv(self, path):
        rows = []
        with open(path, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for r in reader:
                rows.append({
                    "elapsed_s": self._f(r.get("elapsed_s")),
                    "rpm": self._f(r.get("rpm")),
                    "speed_kph": self._f(r.get("speed_kph")),
                    "throttle_pct": self._f(r.get("throttle_pct")),
                    "engine_load_pct": self._f(r.get("engine_load_pct")),
                    "intake_c": self._f(r.get("intake_c")),
                    "coolant_c": self._f(r.get("coolant_c")),
                })
        return rows

    def infer_gear(self, rpm, speed_kph):
        """
        Very rough inferred gear estimator.
        We compare rpm/speed against expected proportional ratios.
        """
        if not rpm or not speed_kph or speed_kph <= 1:
            return None

        ratio_signal = rpm / speed_kph
        expected = {
            1: 95,
            2: 64,
            3: 47,
            4: 36,
            5: 27,
            6: 19,
        }

        best_gear = None
        best_error = None
        for gear, exp in expected.items():
            err = abs(ratio_signal - exp)
            if best_error is None or err < best_error:
                best_error = err
                best_gear = gear
        return best_gear

    def analyse(self, rows):
        analysed = []
        for r in rows:
            gear = self.infer_gear(r["rpm"], r["speed_kph"])
            traction_waste = self._traction_waste_score(
                gear, r["throttle_pct"], r["speed_kph"], r["engine_load_pct"]
            )
            heat_pressure = self._heat_pressure_score(r["intake_c"], r["coolant_c"])
            productive_load = self._productive_load_score(
                gear, r["rpm"], r["speed_kph"], r["engine_load_pct"], heat_pressure
            )

            analysed.append({
                "gear": gear,
                "traction_waste": traction_waste,
                "heat_pressure": heat_pressure,
                "productive_load": productive_load,
            })

        return self._summarise(analysed)

    def _traction_waste_score(self, gear, throttle, speed, load):
        if gear is None or throttle is None or speed is None or load is None:
            return None

        score = 0.0

        # Lower gears with high throttle at low speed are more likely waste-heavy
        if gear == 1:
            score += 0.45
        elif gear == 2:
            score += 0.25
        elif gear == 3:
            score += 0.10

        if throttle > 70:
            score += 0.25
        elif throttle > 40:
            score += 0.12

        if speed < 35:
            score += 0.25
        elif speed < 60:
            score += 0.10

        if load > 85:
            score += 0.10

        return round(min(score, 1.0), 3)

    def _heat_pressure_score(self, intake_c, coolant_c):
        if intake_c is None or coolant_c is None:
            return None

        combined = intake_c + coolant_c
        # Generic banding
        if combined >= 165:
            return 1.0
        if combined >= 150:
            return 0.8
        if combined >= 135:
            return 0.6
        if combined >= 120:
            return 0.4
        return 0.2

    def _productive_load_score(self, gear, rpm, speed, load, heat_pressure):
        if None in (gear, rpm, speed, load, heat_pressure):
            return None

        score = 0.0

        # Favor mid gears and usable rpm band
        if gear in (3, 4):
            score += 0.40
        elif gear in (5, 6):
            score += 0.20
        elif gear == 2:
            score += 0.15
        else:
            score += 0.05

        if 2500 <= rpm <= 4500:
            score += 0.30
        elif 1800 <= rpm < 2500 or 4500 < rpm <= 5500:
            score += 0.18
        else:
            score += 0.08

        if speed >= 60:
            score += 0.15
        if load >= 55:
            score += 0.15

        # Penalize heat pressure
        score -= heat_pressure * 0.25

        return round(max(0.0, min(score, 1.0)), 3)

    def _summarise(self, analysed):
        gears = [r["gear"] for r in analysed if r["gear"] is not None]
        traction = [r["traction_waste"] for r in analysed if r["traction_waste"] is not None]
        heat = [r["heat_pressure"] for r in analysed if r["heat_pressure"] is not None]
        productive = [r["productive_load"] for r in analysed if r["productive_load"] is not None]

        dominant_gears = {}
        for g in gears:
            dominant_gears[g] = dominant_gears.get(g, 0) + 1

        ranked_gears = sorted(dominant_gears.items(), key=lambda x: x[1], reverse=True)

        avg_traction = self._avg(traction)
        avg_heat = self._avg(heat)
        avg_productive = self._avg(productive)

        recommendations = []

        if avg_traction is not None and avg_traction > 0.45:
            recommendations.append(
                "High low-gear waste detected. Reduce early torque hit or delay full demand until traction is usable."
            )

        if avg_productive is not None and avg_productive < 0.45:
            recommendations.append(
                "Load appears poorly converted into useful motion. Concentrate strongest delivery in mid gears."
            )

        if avg_heat is not None and avg_heat > 0.65:
            recommendations.append(
                "Thermal pressure is limiting useful work. Prioritize cooldown and charge-temperature control."
            )

        if avg_productive is not None and avg_productive >= 0.55:
            recommendations.append(
                "Midrange delivery appears productive. Preserve 3rd/4th gear authority and avoid unnecessary low-gear shock."
            )

        if not recommendations:
            recommendations.append(
                "No major gearing inefficiency signal detected in this sample. Validate with a longer capture."
            )

        return {
            "dominant_gears": ranked_gears,
            "avg_traction_waste": round(avg_traction, 3) if avg_traction is not None else None,
            "avg_heat_pressure": round(avg_heat, 3) if avg_heat is not None else None,
            "avg_productive_load": round(avg_productive, 3) if avg_productive is not None else None,
            "recommendations": recommendations,
        }

    def _avg(self, values):
        return statistics.mean(values) if values else None

    def _f(self, value):
        try:
            return float(value)
        except Exception:
            return None


if __name__ == "__main__":
    predictor = GearOpportunityPredictor()
    data = predictor.load_csv("example_log.csv")
    report = predictor.analyse(data)

    print("=== Gear Opportunity Report ===")
    for k, v in report.items():
        print(f"{k}: {v}")
