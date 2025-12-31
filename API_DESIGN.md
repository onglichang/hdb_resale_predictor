# User-Centric API Design for HDB Prediction

To serve actual Singaporeans effectively, we must minimize friction. Users should not be asked for information they cannot easily answer (e.g., "Lease Commence Date" or exact "Floor Area"). 

## 1. The "Singaporean" Context
*   **What they know**: Postal Code (6 digits), Unit # (e.g., #05-123), and generally "4-Room" or "5-Room".
*   **What they don't know**: Lease start year, exact floor area in sqm, or the official HDB town name (is it "Kallang/Whampoa" or just "Kallang"?).

## 2. Proposed API Schema

We propose a **Smart Enrichment** architecture. The API accepts minimal inputs and queries government APIs (OneMap/HDB) to fill in the blanks.

### Request Object (`POST /predict/smart`)

```json
{
  "postal_code": "560567",       // REQUIRED: Uniquely identifies Block/Street/Town
  "flat_type": "4 ROOM",         // REQUIRED: 3 ROOM, 4 ROOM, 5 ROOM, EXE...
  "floor_number": "08",          // REQUIRED: Derives 'storey_range' (e.g. "07 TO 09")
  "floor_area_sqm": 90           // OPTIONAL: If omitted, we fetch the average for this block/type.
}
```

### Response Object

```json
{
  "prediction": 650000.00,
  "confidence_interval": {
     "low": 630000,
     "high": 670000
  },
  "property_details": {
     "address": "BLK 567 ANG MO KIO AVE 3",
     "town": "ANG MO KIO",
     "remaining_lease": "55 years 3 months", // Auto-derived
     "lease_commence_date": 1980             // Auto-derived
  },
  "explanation": "Predicted based on recent transactions of 4 ROOM flats in Ang Mo Kio."
}
```

---

## 3. Enrichment Logic (Backend Strategy)

To make this simple schema work, the backend needs an **Enrichment Service**:

1.  **Resolve Postal Code**:
    *   Call **OneMap API** (`https://www.onemap.gov.sg/api/common/elastic/search?searchVal=560567...`)
    *   **Returns**: `BLK_NO` ("567"), `ROAD_NAME` ("ANG MO KIO AVE 3"), `LATITUDE`, `LONGITUDE`.
2.  **Derive HDB Attributes**:
    *   Map `ROAD_NAME` + `BLK_NO` against a cached HDB Property Dictionary (built from our training data).
    *   **Fills**: `TOWN` ("ANG MO KIO"), `LEASE_COMMENCE_DATE` (1980).
3.  **Handle Missing Floor Area**:
    *   If user doesn't provide `floor_area_sqm`, query our database for the *average* size of a "4 ROOM" flat in "Block 567".
4.  **Format Storey**:
    *   Bucket the user's "08" into the model's required bin `"07 TO 09"`.

## 4. Why this works
*   **Zero Ambiguity**: Postal codes handle the "Town" vs "Street" confusion.
*   **Zero Research**: User doesn't need to check their lease deed.
*   **High Accuracy**: We use exact location data (Lat/Long derived from Postal) for future distance-based features.
