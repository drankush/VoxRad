```markdown
# BIRADS Guidelines for Breast Ultrasound (USG) - Structured Recommendations for LLMs

## 1. **BIRADS Categories & Definitions (USG-Specific)**
| BIRADS | Definition | Management |
|--------|------------|------------|
| **0**  | Incomplete: Need additional imaging (e.g., mammogram, MRI) | Recommend further imaging. |
| **1**  | Negative: No findings (rarely used in USG; use BIRADS 2 instead). | Routine screening. |
| **2**  | Benign: Simple cyst, intramammary node, stable solid mass. | Routine follow-up. |
| **3**  | Probably Benign: ≤2% malignancy risk. Solid mass with benign features. | Short-term follow-up (6 months). |
| **4**  | Suspicious: 3–94% malignancy risk. Subdivided as 4A (low), 4B (moderate), 4C (high). | Biopsy recommended. |
| **5**  | Highly Suggestive of Malignancy: ≥95% risk. | Biopsy and treatment planning. |
| **6**  | Known Biopsy-Proven Malignancy. | Treatment ongoing. |

---

## 2. **Sonographic Feature Analysis**
Guide the LLM to assess these features from the report and map to BIRADS:

### A. **Shape**
- **Oval/Round**: Favors BIRADS 3/2 (if cystic).
- **Irregular**: Raises suspicion (BIRADS 4/5).

### B. **Orientation**
- **Parallel** (wider than tall): Benign (BIRADS 2/3).
- **Non-Parallel** (taller than wide): Suspicious (BIRADS 4/5).

### C. **Margin**
- **Circumscribed**: Smooth, well-defined (BIRADS 2/3).
- **Indistinct**, **Angular**, **Microlobulated**, or **Spiculated**: Suspicious (BIRADS 4/5).

### D. **Lesion Boundary**
- **Abrupt Interface**: Benign (BIRADS 2/3).
- **Echogenic Halo**: Suspicious (BIRADS 4/5).

### E. **Echo Pattern**
- **Anechoic (Cyst)**: BIRADS 2.
- **Hyperechoic (Lipoma)**: BIRADS 2.
- **Hypoechoic (Solid)**: Requires further analysis (check margins/orientation).
- **Complex Cystic/Solid**: BIRADS 4.

### F. **Posterior Features**
- **Enhancement**: Benign (BIRADS 2/3).
- **Shadowing**: Suspicious (BIRADS 4/5).
- **Mixed Pattern**: Assess other features.

### G. **Calcifications**
- **Macrocalcifications (in cysts)**: BIRADS 2.
- **Microcalcifications (in solid mass)**: BIRADS 4/5.

### H. **Vascularity**
- **Absent/Peripheral**: BIRADS 2/3.
- **Internal Vascularity**: BIRADS 4/5.

### I. **Associated Features**
- **Duct Extension**, **Skin Thickening**, or **Architectural Distortion**: BIRADS 4/5.

---

## 3. **Decision Logic for LLMs**
Use this flowchart to assign BIRADS based on findings:
1. **Cystic Lesion** (anechoic, circumscribed, posterior enhancement) → **BIRADS 2**.
2. **Solid Mass**:
   - **All Benign Features** (oval, parallel, circumscribed, no vascularity) → **BIRADS 3**.
   - **1 Suspicious Feature** (e.g., angular margin) → **BIRADS 4A**.
   - **≥2 Suspicious Features** (irregular, non-parallel, spiculated) → **BIRADS 4B/4C**.
   - **Highly Suspicious** (spiculated + shadowing + internal vascularity) → **BIRADS 5**.
3. **Multiple Bilateral Masses** with benign features → **BIRADS 2**.
4. **Intraductal Mass** or **Calcifications in Solid Mass** → **BIRADS 4**.

---

## 4. **Examples for LLM Training**
### Case 1:
- **Findings**: 8mm oval, parallel, circumscribed, hypoechoic mass with posterior enhancement.
- **LLM Interpretation**: BIRADS 3 (probably benign; short-term follow-up).

### Case 2:
- **Findings**: 15mm irregular, non-parallel mass with spiculated margins and shadowing.
- **LLM Interpretation**: BIRADS 5 (highly suggestive of malignancy; biopsy urgently).

---

## 5. **Recommendations Structure**
Instruct the LLM to format recommendations to present in one sentence for each lesion. Do not mention headings presented in {}:
1. {Lesion location} e.g. Right upper outer quadrant at 11 o'clock position.{**BIRADS Category**}(e.g., **BIRADS 4A**,  Clarify uncertainty as BIRADS 0 if required) due to presence of {**Rationale** Concise feature summary} e.g., irregular shape, non-parallel orientation. {**Action**: Follow BIRADS management table} (e.g., "Biopsy recommended").

---
**Key LLM Directive**: You have to always provide BIRADS Category to each lesion. Always prioritize the most suspicious feature to assign the highest possible BIRADS category. If conflicting features exist, default to higher suspicion (e.g., circumscribed but irregular → BIRADS 4).
```