**Breast Imaging Reporting and Data System (BI-RADS) Guidelines for Mammography Interpretation**  

This structured guide outlines how to interpret mammographic findings and assign BI-RADS categories with corresponding clinical recommendations. The system standardizes reporting to ensure appropriate management based on lesion characteristics.  

---

## **BI-RADS Categories & Descriptors**  
### **Category 0: Incomplete Assessment**  
**Findings requiring additional imaging:**  
- Asymmetries without clear margins  
- One-view-only calcifications/masses  
- Technical limitations (e.g., poor compression, motion artifacts)  

**Recommendations:**  
- Additional diagnostic mammography views (spot compression, magnification)  
- Ultrasound correlation for focal asymmetries/masses [4][8]  

---

### **Category 1: Negative**  
**Findings:**  
- Symmetric fibroglandular tissue  
- Benign calcifications (e.g., vascular, secretory)  
- No masses, distortions, or suspicious features  

**Recommendations:**  
- Routine screening in 1–2 years (age-dependent) [3][6]  

---

### **Category 2: Benign**  
**Findings:**  
- Intramammary lymph nodes  
- Stable calcifications (e.g., popcorn-type in fibroadenomas)  
- Simple cysts confirmed on ultrasound  

**Recommendations:**  
- Routine follow-up with no additional action [2][4]  

---

### **Category 3: Probably Benign**  
**Findings (≤2% malignancy risk):**  
| Feature          | Descriptors                                  |  
|-------------------|---------------------------------------------|  
| **Masses**        | Oval/round, circumscribed margins           |  
| **Calcifications**| Punctate, diffuse distribution              |  
| **Focal Asymmetry**| Non-palpable, stable over time             |  

**Recommendations:**  
- Short-interval follow-up (6 months)  
- Consider vacuum-assisted excision (VAE) for atypia [1][4]  

---

### **Category 4: Suspicious**  
**Subcategories and features:**  
| Subtype | Malignancy Risk | Key Descriptors                          |  
|---------|-----------------|------------------------------------------|  
| 4A      | 2–10%           | Round mass with indistinct margins       |  
| 4B      | 10–50%          | Fine pleomorphic calcifications          |  
| 4C      | 50–95%          | Spiculated mass + associated calcifications |  

**Recommendations:**  
- Tissue diagnosis required (core needle biopsy preferred)  
- Surgical excision if atypia/DCIS confirmed [1][2][8]  

---

### **Category 5: Highly Suggestive of Malignancy**  
**Findings (≥95% malignancy risk):**  
- Spiculated high-density mass  
- Fine-linear/linear-branching calcifications  
- Architectural distortion with stromal reaction  

**Recommendations:**  
- Biopsy confirmation followed by surgical planning  
- Sentinel lymph node biopsy if invasive cancer suspected [2][4]  

---

### **Category 6: Known Biopsy-Proven Malignancy**  
**Findings:**  
- Lesion already confirmed as malignant  

**Recommendations:**  
- Definitive treatment (surgery, systemic therapy)  
- Preoperative staging if needed [2][6]  

---

## **Interpretation Logic for LLMs**  
1. **Prioritize worst features:** A mass with spiculated margins overrides benign calcifications.  
2. **Combine findings:** Architectural distortion + pleomorphic calcifications → Category 4C/5.  
3. **Stability matters:** New or enlarging lesions increase suspicion (e.g., upgrade Category 3 to 4 if interval growth).  
4. **Density considerations:** High-density masses in fatty breasts warrant closer scrutiny [4][8].  

---

## **Example Workflow**  
**Input Findings:**  
- "Cluster of fine-linear calcifications in the upper outer quadrant."  

**LLM Processing:**  
1. Calcification morphology: Fine-linear → high suspicion.  
2. Distribution: Cluster → localized.  
3. BI-RADS Assignment: Category 4B.  

**Recommendation Output:**  
- "Tissue sampling required (core biopsy). Correlate with ultrasound for targeted sampling [2][4]."  

This framework ensures systematic risk stratification and reduces variability in mammography reporting.

