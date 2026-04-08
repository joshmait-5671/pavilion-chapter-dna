# Meteorologist Profiling Framework

A structured system for mapping a forecaster's tendencies, strengths, biases, and style across 10 dimensions.

---

## Dimension 1: Model Reliance Spectrum

**Where does the forecaster fall between raw model output and subjective judgment?**

| End | Description |
|-----|-------------|
| **Model Purist** | Trusts numerical model output with minimal human adjustment. |
| **Model-Informed Synthesizer** | Uses models as primary input but adjusts based on known biases, local knowledge, and pattern recognition. |
| **Gut-Feel Forecaster** | Relies heavily on personal experience, sky reading, and intuition. Models are one input among many. |

---

## Dimension 2: Model Allegiance

**Which models does the forecaster default to?**

| Model | Characteristics | What Preference Suggests |
|-------|----------------|--------------------------|
| **ECMWF (Euro)** | 9km res, 2x daily, best medium-range (days 3-10). Gold standard. | Methodical, accuracy-first. |
| **GFS** | 25km res, 4x daily, free. Tends to overamplify storms. | Accessible, update-hungry, may lean dramatic. |
| **NAM** | 3km nested, strong for mesoscale (lake-effect, cold air damming), 60-hour range. | Regional specialist, detail-oriented. |
| **HRRR** | Hourly updates, 3km, 18-hour range. Best for real-time convective forecasting. | Nowcasting focus, storm chaser mentality. |
| **Ensemble/Blend** | Multi-model consensus. | Probabilistic thinker, avoids anchoring. |

*Key bias:* Forecasters often over-trust whichever model they check first ("anchoring").

---

## Dimension 3: Probabilistic Sophistication

| Level | Description |
|-------|-------------|
| **Binary** | "It will snow" / "It won't snow." |
| **Coarse Probabilistic** | "Good chance of snow." Uses buckets, not numbers. |
| **Calibrated Probabilistic** | "60% chance of 4+ inches, 20% chance of 8+." Gives ranges with confidence levels. |
| **Ensemble-Informed** | References model spread, percentile ranges. Communicates the full distribution. |

*This is the single biggest differentiator between average and excellent forecasters.*

---

## Dimension 4: Bias Profile

| Bias | Description |
|------|-------------|
| **Wet Bias** | Overpredicts precipitation probability. |
| **Storm Hype** | Overpromises storm intensity. Every system is "one for the ages." |
| **Warm/Cold Bias** | Systematic temperature skew. |
| **Recency Bias** | Over-indexes on the last big event. |
| **Anchoring Bias** | Locks onto first model run, adjusts insufficiently. |
| **Conservative Bias** | Underforecasts extremes. Pulls toward climatology. |
| **Dramatic Bias** | Overforecasts extremes. Calls for tail-end scenarios. |

---

## Dimension 5: Temporal Focus

| Range | Window | Profile |
|-------|--------|---------|
| **Nowcasting** | 0-6 hours | Tactician. Real-time actionability. |
| **Short-Range** | 1-3 days | Operational. "What's happening this week." |
| **Medium-Range** | 4-10 days | Pattern thinker. Teleconnections (NAO, PNA, MJO). |
| **Extended/Seasonal** | 10+ days | Big-picture. Comfortable with deep uncertainty. |

---

## Dimension 6: Phenomenon Specialty

| Specialty | Description |
|-----------|-------------|
| **Winter Weather / Snow** | Obsesses over totals, ice storms, nor'easters, rain-snow line. |
| **Severe / Convective** | Tornado and supercell focused. Storm chaser energy. |
| **Tropical** | Hurricane tracking. NHC cones, spaghetti models. |
| **Daily Sensible Weather** | Temp, rain/no-rain, weekend forecasts. Practical, audience-oriented. |

---

## Dimension 7: Communication Style

| Style | Description |
|-------|-------------|
| **The Educator** | Explains the "why." Shows maps, discusses dynamics. |
| **The Alarm Raiser** | Leads with impact and urgency. Safety-focused. |
| **The Entertainer** | Makes weather fun. Heavy on personality. May sacrifice nuance. |
| **The Data Dumper** | Posts raw model output with minimal translation. |
| **The Hedger** | Covers all scenarios. Technically accurate, low utility. |
| **The Bold Caller** | Picks a number early and stands by it. High risk, high reward. |

---

## Dimension 8: Verification & Accountability

| Level | Description |
|-------|-------------|
| **None** | Makes forecasts, never revisits. |
| **Selective** | Highlights hits, quietly ignores busts. |
| **Honest but Informal** | Acknowledges misses publicly. No systematic tracking. |
| **Rigorous** | Tracks accuracy over time. Adjusts methods based on results. |

---

## Dimension 9: Local Knowledge Depth

| Level | Description |
|-------|-------------|
| **Generic** | Applies broad model output without local adjustment. |
| **Regional** | Knows general area tendencies. |
| **Hyperlocal** | Understands specific valley channeling, urban heat islands, elevation-dependent precip. Adjusts by miles, not counties. |

*This is where amateurs who've lived in one area for decades can outperform credentialed meteorologists.*

---

## Dimension 10: Update Discipline

| Pattern | Description |
|---------|-------------|
| **Stubborn** | Makes early call, sticks with it regardless. Identity tied to original forecast. |
| **Whipsaw** | Changes dramatically with every model run. Erodes trust. |
| **Bayesian Updater** | Adjusts incrementally as evidence arrives. Communicates what changed and why. *(Ideal)* |

---

## Scoring Card

| # | Dimension | Scale |
|---|-----------|-------|
| 1 | Model Reliance | Purist ←→ Gut Feel |
| 2 | Model Allegiance | Single-model ←→ Multi-model blend |
| 3 | Probabilistic Sophistication | Binary ←→ Ensemble-informed |
| 4 | Bias Profile | List dominant biases |
| 5 | Temporal Focus | Nowcast ←→ Extended range |
| 6 | Phenomenon Specialty | Primary weather type(s) |
| 7 | Communication Style | Primary archetype(s) |
| 8 | Verification & Accountability | None ←→ Rigorous |
| 9 | Local Knowledge | Generic ←→ Hyperlocal |
| 10 | Update Discipline | Stubborn ←→ Whipsaw (Bayesian center) |
