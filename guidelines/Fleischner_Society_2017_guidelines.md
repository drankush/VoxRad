# Fleischner Society 2017 Guidelines for Management of Incidental Pulmonary Nodules

The Fleischner Society's 2017 guidelines provide recommendations for the management of incidental pulmonary nodules detected on CT scans. These guidelines are based on nodule size, type (solid or subsolid), and patient risk factors. Below is a structured approach to assist a Large Language Model (LLM) in generating appropriate recommendations from radiology findings.

## Nodule Classification

1. **Solid Nodules**: Completely solid with no ground-glass opacity.
2. **Subsolid Nodules**:
   - **Pure Ground-Glass Nodules (GGNs)**: Appear as hazy areas without solid components.
   - **Part-Solid Nodules**: Contain both ground-glass and solid components.

## Patient Risk Assessment

- **Low Risk**: Minimal or absent history of smoking and no other known risk factors.
- **High Risk**: History of smoking or other risk factors for lung cancer.

## Management Recommendations

### Solid Nodules

**Single Solid Nodule:**

- **<6 mm**:
  - *Low Risk*: No routine follow-up required.
  - *High Risk*: Optional CT at 12 months.

- **6–8 mm**:
  - *Low Risk*: Initial follow-up CT at 6–12 months; if unchanged, consider CT at 18–24 months.
  - *High Risk*: Initial follow-up CT at 6–12 months; if unchanged, repeat CT at 18–24 months.

- **>8 mm**:
  - Consider options including CT at 3 months, PET/CT, or tissue sampling, based on the probability of malignancy.

**Multiple Solid Nodules:**

- **<6 mm**:
  - *Low Risk*: No routine follow-up required.
  - *High Risk*: Optional CT at 12 months.

- **>6 mm**:
  - Initial follow-up CT at 3–6 months; if stable, consider CT at 18–24 months.

### Subsolid Nodules

**Single Subsolid Nodule:**

- **<6 mm**:
  - No routine follow-up required.

- **≥6 mm**:
  - Initial follow-up CT at 6–12 months to confirm persistence:
    - *If unchanged*:
      - **Pure GGN**: Consider CT at 2 and 4 years.
      - **Part-Solid Nodule with Solid Component <6 mm**: Annual CT for 5 years.
    - *If the solid component is ≥6 mm*: Consider PET/CT or tissue sampling.

**Multiple Subsolid Nodules:**

- **<6 mm**:
  - Follow-up CT at 3–6 months; if stable, consider CT at 2 and 4 years.

- **≥6 mm**:
  - Manage based on the most suspicious nodule.

## Application to Radiology Findings

When interpreting radiology findings, the LLM should:

1. **Identify Nodule Characteristics**:
   - Determine the size, type (solid or subsolid), and specific features (e.g., spiculation, enhancement patterns) of each nodule.

2. **Assess Patient Risk Factors**:
   - Evaluate the patient's smoking history and other relevant risk factors to classify them as low or high risk.

3. **Apply Fleischner Guidelines**:
   - Use the nodule characteristics and patient risk assessment to provide management recommendations as outlined above.

**Example Application:**

*Findings Mentioned in the report*:
- **Right Upper Lobe**: Solid nodule, 8 mm, spiculated margins.
- **Left Lower Lobe**: Ground-glass nodule, 6 mm.
- **Right Lower Lobe**: Part-solid nodule, 12 mm, peripheral enhancement with a central non-enhancing component.

Your OUTPUT should only be structured like this:
*Recommendations*:
- **Right Upper Lobe Nodule**:
  - *Low Risk*: Follow-up CT at 6–12 months; if unchanged, consider CT at 18–24 months.
  - *High Risk*: Follow-up CT at 6–12 months; if unchanged, repeat CT at 18–24 months.

- **Left Lower Lobe Nodule**:
  - Follow-up CT at 6–12 months to confirm persistence; if unchanged, consider CT at 2 and 4 years.

- **Right Lower Lobe Nodule**:
  - Given the size and part-solid nature with a solid component ≥6 mm, consider PET/CT or tissue sampling.

By following this structured approach, the LLM can generate appropriate management recommendations based on the Fleischner Society's 2017 guidelines. 