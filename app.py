import streamlit as st
from unified_agri_system import recommend_crop, detect_disease
from region_map import STATE_TO_ZONE

st.set_page_config(page_title="Smart Agriculture System", layout="wide")

# ---------------------------------------------------
# Custom UI Styling
# ---------------------------------------------------

st.markdown("""
<style>

/* Page Background */

/* Card Style */
.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
}

/* Section Headers */
h2 {
    color: #1b5e20;
    font-weight: 700;
}

h3 {
    color: #0d47a1;
}

/* Success box */
.stSuccess {
    border-radius: 12px;
}

/* Warning box */
.stWarning {
    border-radius: 12px;
}

/* Info box */
.stInfo {
    border-radius: 12px;
}



/* Buttons */
button {
    border-radius: 10px !important;
    font-weight: 600 !important;
}

</style>
""", unsafe_allow_html=True)


# ---------------------------------
# Initialize Session State
# ---------------------------------

if "soil_results" not in st.session_state:
    st.session_state.soil_results = None

if "image_results" not in st.session_state:
    st.session_state.image_results = None

st.title("🌾 Smart Precision Agriculture Digital Twin")
st.markdown("Independent Soil & Plant Health Analysis System")

st.markdown("<hr style='border:1px solid #ddd;'>", unsafe_allow_html=True)


# ---------------------------------------------------
# State-Specific Advisory (Covers All States)
# ---------------------------------------------------

STATE_ADVISORY = {

    "Andhra Pradesh": "Andhra Pradesh has diverse agro-climatic zones ranging from coastal humid regions to semi-arid Rayalaseema. Paddy dominates in irrigated coastal belts, while maize, cotton, and chilli perform well in interior regions. Farmers should plan according to monsoon variability and ensure efficient irrigation scheduling, especially during dry spells.",

    "Arunachal Pradesh": "Arunachal Pradesh experiences high rainfall and supports rice, maize, and horticultural crops in terraced landscapes. The hilly terrain requires soil conservation practices and proper drainage management to prevent erosion. Seasonal crop planning must consider heavy monsoon patterns and altitude variations.",

    "Assam": "Assam’s humid subtropical climate is ideal for rice, tea, jute, and mustard cultivation. Flood management plays a critical role in maintaining yield stability. Farmers should adopt resilient crop varieties and focus on drainage systems to manage excess water during peak monsoon months.",

    "Bihar": "Bihar supports a rice–wheat cropping system along with maize and pulses. Fertility management and crop rotation are important to maintain soil health. Irrigation planning during Rabi season significantly improves productivity and reduces climate-related risks.",

    "Chhattisgarh": "Known as the rice bowl of India, Chhattisgarh heavily depends on paddy cultivation. Upland areas also support maize and pulses. Adoption of improved seed varieties and balanced fertilization can enhance yield while maintaining soil sustainability.",

    "Goa": "Goa’s tropical coastal climate supports coconut, rice, and cashew cultivation. Farmers should focus on managing soil salinity and ensuring effective drainage during heavy monsoon rainfall. Plantation crops benefit from integrated pest management strategies.",

    "Gujarat": "Gujarat’s semi-arid conditions favor cotton, groundnut, and millet production. Water scarcity makes drip irrigation and moisture conservation practices highly important. Seasonal rainfall forecasting helps in optimizing sowing decisions.",

    "Haryana": "Haryana follows a wheat–rice dominant cropping system supported by extensive irrigation. Sustainable groundwater usage and diversification into pulses and oilseeds are increasingly encouraged. Soil testing and balanced nutrient management are essential for long-term productivity.",

    "Himachal Pradesh": "The temperate climate of Himachal Pradesh supports apple orchards, maize, and barley cultivation. Horticulture plays a major economic role in the region. Farmers should focus on orchard management, frost protection, and soil erosion control in hilly terrain.",

    "Jharkhand": "Jharkhand relies largely on rainfed agriculture, with rice, pulses, and oilseeds being common crops. Soil moisture conservation and timely sowing are critical under variable rainfall conditions. Adoption of climate-resilient practices can enhance productivity.",

    "Karnataka": "Karnataka’s diverse climate supports ragi, maize, coffee, and pulses. Semi-arid regions require drought-resistant crop varieties and efficient water use. Integrated nutrient management improves both soil fertility and crop performance.",

    "Kerala": "Kerala’s humid tropical climate is ideal for coconut, banana, rubber, and spice cultivation. Plantation crops dominate the landscape. Proper drainage, disease monitoring, and organic soil management practices are highly beneficial in this region.",

    "Madhya Pradesh": "Madhya Pradesh supports soybean, wheat, gram, and maize cultivation. The state’s central location offers balanced agro-climatic conditions. Crop diversification and soil nutrient optimization significantly enhance farm productivity.",

    "Maharashtra": "Maharashtra’s agro-climatic zones range from coastal humid to semi-arid interiors. Cotton, soybean, sugarcane, and jowar are widely cultivated. Efficient irrigation planning and drought-resistant crop selection are important due to rainfall variability.",

    "Manipur": "Manipur supports rice, maize, and horticultural crops under high rainfall conditions. Terrace farming and soil erosion control are important in hilly regions. Seasonal crop planning should align with monsoon timing.",

    "Meghalaya": "Meghalaya’s heavy rainfall supports rice, maize, and spice crops. Soil drainage and erosion management are critical due to sloping terrain. Organic farming practices are widely encouraged in this region.",

    "Mizoram": "Mizoram traditionally practices shifting cultivation, though modern farming methods are expanding. Rice, maize, and horticulture perform well under proper soil conservation. Water management and crop rotation improve sustainability.",

    "Nagaland": "Nagaland supports rice, maize, and millet cultivation in hilly landscapes. Terrace farming reduces soil erosion and improves water retention. Farmers should align crop cycles with seasonal rainfall patterns.",

    "Odisha": "Odisha’s coastal and inland zones favor rice, pulses, and oilseeds. Cyclone-prone areas require resilient crop varieties and disaster preparedness planning. Balanced nutrient management enhances soil productivity.",

    "Punjab": "Punjab’s irrigated agriculture heavily focuses on wheat and rice. Sustainable water use and crop diversification into maize and pulses are increasingly important. Soil health monitoring improves long-term productivity.",

    "Rajasthan": "Rajasthan’s arid and semi-arid climate favors millet, guar, and pulses. Efficient water management and drought-tolerant crop varieties are essential. Rainwater harvesting enhances agricultural stability.",

    "Sikkim": "Sikkim promotes organic agriculture and supports maize, cardamom, and horticulture. Temperate conditions require careful nutrient management. Sustainable farming practices are widely encouraged.",

    "Tamil Nadu": "Tamil Nadu supports rice, sugarcane, cotton, and groundnut cultivation. Tank irrigation systems are historically significant. Seasonal crop planning aligned with monsoon cycles improves yield stability.",

    "Telangana": "Telangana supports cotton, maize, and paddy under semi-arid conditions. Rainwater harvesting and micro-irrigation systems improve water efficiency. Balanced fertilization enhances crop outcomes.",

    "Tripura": "Tripura supports rice, rubber, and horticulture under high rainfall conditions. Proper drainage management and crop diversification increase productivity. Soil conservation measures are beneficial.",

    "Uttar Pradesh": "Uttar Pradesh supports wheat, rice, sugarcane, and pulses. Balanced nutrient management and irrigation scheduling significantly impact yields. Crop rotation practices maintain soil health.",

    "Uttarakhand": "Uttarakhand’s hilly terrain supports millets, maize, and horticulture crops. Soil erosion control and terrace farming are essential. Climate-sensitive planning enhances sustainability.",

    "West Bengal": "West Bengal supports rice, jute, and potato cultivation. High humidity favors paddy, but proper drainage is necessary. Seasonal rainfall monitoring helps optimize crop planning.",

    "Andaman and Nicobar Islands": "The tropical island climate supports coconut, arecanut, and spices. Salinity management and drainage planning are important due to coastal influence. Plantation crops dominate agriculture.",

    "Chandigarh": "Chandigarh follows cropping patterns similar to Punjab and Haryana. Wheat and rice are dominant under irrigation-based systems. Sustainable groundwater management is recommended.",

    "Dadra and Nagar Haveli and Daman and Diu": "This coastal region supports rice and horticultural crops. Irrigation planning and soil salinity management are important for consistent productivity.",

    "Delhi": "Delhi supports wheat, mustard, and vegetable cultivation in peri-urban areas. Efficient irrigation and soil testing improve productivity. Urban farming initiatives are increasing.",

    "Jammu and Kashmir": "Temperate conditions support apple orchards, saffron, and maize cultivation. Orchard management practices and frost protection are critical. Seasonal climate variation influences crop planning.",

    "Ladakh": "Ladakh’s cold desert climate supports barley and limited horticulture. Controlled irrigation systems and greenhouse farming improve crop success. Short growing seasons require careful planning.",

    "Lakshadweep": "Lakshadweep supports coconut and limited horticulture due to tropical island conditions. Proper drainage and soil fertility management are essential for plantation crops.",

    "Puducherry": "Puducherry supports rice and sugarcane cultivation under coastal tropical conditions. Irrigation planning and soil nutrient management significantly impact yields."
}



def explain_top_crop(top_crop, state, top_crops, N, P, K):

    top_confidence = top_crops[0]["confidence"]
    second_confidence = top_crops[1]["confidence"]

    confidence_percent = round(top_confidence * 100, 2)
    confidence_gap = round((top_confidence - second_confidence) * 100, 2)

    zone = STATE_TO_ZONE.get(state, "Agro-climatic region")

    if N > P and N > K:
        soil_comment = "nitrogen-rich soil conditions"
    elif P > N and P > K:
        soil_comment = "phosphorus-dominant nutrient balance"
    elif K > N and K > P:
        soil_comment = "potassium-influenced soil composition"
    else:
        soil_comment = "balanced macronutrient levels"

    if confidence_gap > 20:
        decision_strength = "a strong suitability margin over alternative crops"
    elif confidence_gap > 10:
        decision_strength = "a moderate suitability advantage compared to alternatives"
    else:
        decision_strength = "a competitive ranking among closely matched crop options"

    if confidence_percent > 70:
        risk_level = "High Suitability"
    elif confidence_percent > 50:
        risk_level = "Moderate Suitability"
    else:
        risk_level = "Conditional Suitability"

    explanation = (
        f"The crop '{top_crop.capitalize()}' achieved the highest modeled suitability score "
        f"of {confidence_percent}%, indicating {decision_strength}. "
        f"The system detected {soil_comment}, which aligns well with the crop’s nutrient requirements. "
        f"Additionally, agro-climatic conditions typical to {state} ({zone}) further reinforce this selection. "
        f"Overall classification: {risk_level} under the current parameters."
    )

    return explanation


def generate_plant_advice(health_status, confidence):

    confidence_percent = round(confidence * 100, 2)

    if health_status == "Healthy":
        return (
            f"The plant appears healthy with a confidence of {confidence_percent}%. "
            "Continue regular irrigation scheduling, maintain balanced fertilization, "
            "and monitor foliage weekly for early stress indicators. "
            "Preventive fungicide application during humid conditions can reduce disease risk."
        )
    else:
        if confidence_percent > 90:
            severity = "a high probability of infection"
        elif confidence_percent > 70:
            severity = "a moderate probability of infection"
        else:
            severity = "possible early-stage symptoms"

        return (
            f"The system detected {severity} ({confidence_percent}% confidence). "
            "Immediate intervention is recommended: remove affected leaves, "
            "avoid overhead irrigation to reduce moisture accumulation, "
            "and apply a suitable fungicide or bactericide as per agricultural guidelines. "
            "Improving air circulation between plants can help prevent further spread."
        )


# ---------------------------------------------------
# Layout Columns
# ---------------------------------------------------

col1, col2 = st.columns(2)

# ===================================================
# 🌱 LEFT COLUMN — SOIL ANALYSIS
# ===================================================

with col1:
    st.markdown("## 🌱 Soil Intelligence Module")
    st.markdown("---")


    N = st.number_input("Nitrogen (N)", min_value=0.0, value=90.0)
    P = st.number_input("Phosphorus (P)", min_value=0.0, value=42.0)
    K = st.number_input("Potassium (K)", min_value=0.0, value=43.0)

    available_states = sorted(
        [state for state in STATE_TO_ZONE.keys() if state != "DEFAULT"]
    )

    state = st.selectbox("Select State", available_states)

    if st.button("Analyze Soil", key="soil_btn"):

        with st.spinner("Analyzing soil conditions..."):
            top_crops = recommend_crop(N, P, K, state)

        st.session_state.soil_results = {
            "top_crops": top_crops,
            "state": state,
            "N": N,
            "P": P,
            "K": K
        }

    # Persistent Soil Results Display
    if st.session_state.soil_results is not None:
        

        results = st.session_state.soil_results
        top_crops = results["top_crops"]

        st.success("🌾 Top 3 Recommended Crops")

        for idx, crop_info in enumerate(top_crops, start=1):
            percentage = crop_info["confidence"] * 100
            st.markdown(
                f"""
                <div style='
                   padding:10px;
                   border-radius:10px;
                   margin-bottom:8px;
                   box-shadow:0px 2px 6px rgba(0,0,0,0.08);
                '>
                   <b>{idx}. {crop_info['crop'].capitalize()}</b> — {percentage:.2f}%
                </div>
                """,
                unsafe_allow_html=True
            )

            st.progress(crop_info["confidence"])

        st.divider()
        st.subheader("📘 Why this crop?")

        st.info(
            explain_top_crop(
                top_crops[0]["crop"],
                results["state"],
                top_crops,
                results["N"],
                results["P"],
                results["K"]
            )
        )

        st.divider()
        st.subheader("🌍 Regional Advisory")

        st.warning(
           STATE_ADVISORY.get(
               results["state"],
               "Regional advisory unavailable."
            )
        )



# ===================================================
# 🌿 RIGHT COLUMN — IMAGE ANALYSIS
# ===================================================

with col2:
    st.markdown("## 🌿 Plant Vision Module")
    st.markdown("---")


    uploaded_file = st.file_uploader(
        "Upload a leaf image",
        type=["jpg", "jpeg", "png"],
        key="leaf_upload"
    )

    if uploaded_file is not None:
        st.image(uploaded_file, use_container_width=True)

        if st.button("Analyze Image", key="leaf_btn"):

            with st.spinner("Analyzing image..."):

                image_path = "temp_uploaded_image.jpg"
                with open(image_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())

                health_status, confidence = detect_disease(image_path)

            st.session_state.image_results = {
                "health_status": health_status,
                "confidence": confidence
            }

    # Persistent Image Results Display
    if st.session_state.image_results is not None:

        result = st.session_state.image_results

        st.divider()

        if result["health_status"] == "Healthy":
            st.success("🌿 Plant Status: Healthy")
        else:
            st.error("⚠️ Plant Status: Diseased")

        st.write(f"Confidence: {result['confidence'] * 100:.2f}%")

        st.divider()
        st.subheader("🩺 Plant Care Recommendation")

        st.info(
            generate_plant_advice(
                result["health_status"],
                result["confidence"]
            )
        )


st.markdown("---")
st.markdown(
    "<center style='color:gray;'>Smart Precision Agriculture Digital Twin • AI-powered Advisory System</center>",
    unsafe_allow_html=True
)

