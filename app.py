
from pathlib import Path
from datetime import datetime

import streamlit as st
import pandas as pd
import numpy as np
import cv2
from PIL import Image


# =========================================================
# 1. PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="URONEX | Smart Kidney Screening",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="expanded"
)

BASE_DIR = Path(__file__).resolve().parent


# =========================================================
# 2. IMAGE PATHS
# =========================================================

def find_image(filename):
    for path in BASE_DIR.rglob("*"):
        if path.is_file() and path.name.lower() == filename.lower():
            return path
    return None


KIDNEY = find_image("kidney.png")
LOGO = find_image("logo.png")
STRIP = find_image("strip.png")


def show_image(path, caption=None, width="stretch"):
    if path and path.exists():
        st.image(str(path), caption=caption, width=width)
    else:
        st.info(f"{path.name if path else 'Image'} not found.")


# =========================================================
# 3. SESSION STATE
# =========================================================

if "history" not in st.session_state:
    st.session_state.history = []

if "uronex_latest_result" not in st.session_state:
    st.session_state.uronex_latest_result = None



# =========================================================
# 4. CUSTOM DESIGN - CLEAR AND VISIBLE OUTPUT
# =========================================================

st.markdown("""
<style>

/* Main background */
.stApp {
    background: linear-gradient(135deg, #061421, #092b3a, #061421);
    color: #FFFFFF !important;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background-color: #071b29;
}

/* Headings */
h1, h2, h3, h4 {
    color: #55e6d0 !important;
    font-weight: 700 !important;
}

/* Normal text */
p, label, li {
    color: #F0F7FA !important;
}

/* METRIC CARDS */
[data-testid="stMetric"] {
    background-color: #123B4D !important;
    border: 1px solid #35C5C5 !important;
    border-radius: 14px !important;
    padding: 18px !important;
}

/* Metric labels */
[data-testid="stMetricLabel"],
[data-testid="stMetricLabel"] *,
[data-testid="stMetricLabel"] p {
    color: #FFFFFF !important;
    -webkit-text-fill-color: #FFFFFF !important;
    font-size: 17px !important;
    font-weight: 700 !important;
}

/* IMPORTANT: Metric numbers */
[data-testid="stMetricValue"],
[data-testid="stMetricValue"] *,
[data-testid="stMetricValue"] div,
[data-testid="stMetricValue"] p {
    color: #FFFFFF !important;
    -webkit-text-fill-color: #FFFFFF !important;
    font-size: 34px !important;
    font-weight: 800 !important;
    opacity: 1 !important;
}

/* Metric additional text */
[data-testid="stMetricDelta"] {
    color: #FFFFFF !important;
}

/* Result messages */
[data-testid="stAlert"] {
    border-radius: 12px !important;
}

[data-testid="stAlert"] p,
[data-testid="stAlert"] div {
    color: #FFFFFF !important;
    -webkit-text-fill-color: #FFFFFF !important;
    font-weight: 700 !important;
}

/* Buttons */
.stButton > button {
    background-color: #21b6a5 !important;
    color: #061421 !important;
    border-radius: 8px !important;
    font-weight: bold !important;
}

/* Tables */
[data-testid="stDataFrame"] {
    color: #FFFFFF !important;
}

</style>
""", unsafe_allow_html=True)


# =========================================================
# 5. SIDEBAR NAVIGATION
# =========================================================

with st.sidebar:

    if LOGO:
        show_image(LOGO, width=180)
    else:
        st.title("🧬 URONEX")

    st.caption("SMART KIDNEY SCREENING")
    st.markdown("---")
    st.subheader("NAVIGATION")

    page = st.radio(
        "Select Page",
        [
            "Home",
            "About URONEX",
            "How It Works",
            "New Screening",
            "Screening History",
            "Team"
        ],
        label_visibility="collapsed"
    )

    st.markdown("---")
    st.caption("BIOMEDICAL ENGINEERING PROJECT")
    st.caption("Experimental Prototype | Version 1.0")


# =========================================================
# 6. HOME PAGE
# =========================================================

if page == "Home":

    st.title("Welcome to URONEX")
    st.subheader("Smart Preliminary Kidney Health Screening")

    st.write(
        "Microfluidics • Colorimetric Detection • "
        "Smartphone Image Processing"
    )

    st.markdown("---")

    col1, col2 = st.columns(2)

    with col1:
        st.header("About Our Innovation")
        st.write("""
        URONEX is an experimental paper-based microfluidic
        screening prototype designed for preliminary assessment
        of urinary biomarkers.

        It combines a disposable microfluidic strip with a
        reusable 3D-printed reader housing.

        Images are processed using Python and OpenCV.
        """)

    with col2:
        show_image(KIDNEY, "Kidney Health Screening")

    st.markdown("---")
    st.header("Our Technology")

    c1, c2, c3 = st.columns(3)

    c1.subheader("🧪 Microfluidics")
    c1.write("Paper-based capillary flow.")

    c2.subheader("📷 Smart Imaging")
    c2.write("Smartphone-assisted image acquisition.")

    c3.subheader("📊 Image Analysis")
    c3.write("Automatic colour-index analysis.")

    st.markdown("---")
    st.header("URONEX Microfluidic Strip")
    show_image(STRIP, "URONEX Reaction Strip")


# =========================================================
# 7. ABOUT URONEX
# =========================================================

elif page == "About URONEX":

    st.title("About URONEX")

    st.subheader(
        "Design and Development of a Smartphone-Assisted "
        "Microfluidic Cartridge for Multiparametric Urine Analysis"
    )

    st.write("""
    URONEX is an experimental paper-based microfluidic
    screening prototype.

    The disposable strip contains multiple reaction regions.
    A reusable 3D-printed housing supports image acquisition.
    Python and OpenCV are used for image processing.
    """)

    st.header("Project Components")

    components = [
        "Disposable paper-based microfluidic strip",
        "Sample inlet and capillary channels",
        "Albumin detection region",
        "Creatinine detection region",
        "pH detection region",
        "Blood detection region",
        "Reusable 3D-printed reader housing",
        "Smartphone-assisted image acquisition"
    ]

    for item in components:
        st.markdown(f"- {item}")

    st.markdown("---")
    show_image(STRIP, "URONEX Detection Strip")

    st.warning(
        "URONEX is an experimental prototype, not a "
        "clinically validated diagnostic device."
    )


# =========================================================
# 8. HOW IT WORKS
# =========================================================

elif page == "How It Works":

    st.title("How URONEX Works")

    workflow = [
        ("01", "Sample Introduction", "Urine sample enters the inlet."),
        ("02", "Capillary Flow", "Sample moves through paper channels."),
        ("03", "Colour Reaction", "Sample interacts with reagent regions."),
        ("04", "Image Acquisition", "Camera captures the developed strip."),
        ("05", "Image Processing", "OpenCV analyses the reaction regions."),
        ("06", "Result Display", "Visual indices and screening information are displayed.")
    ]

    for number, title, description in workflow:
        with st.container(border=True):
            st.subheader(f"{number} | {title}")
            st.write(description)

    st.markdown("---")
    st.header("Reaction Zones")

    zones_df = pd.DataFrame({
        "Zone": ["CREA", "ALB", "pH", "BLOOD"],
        "Purpose": [
            "Creatinine-related reaction",
            "Albumin-related reaction",
            "Urine pH reaction",
            "Blood-related reaction"
        ]
    })

    st.dataframe(
        zones_df,
        hide_index=True,
        width="stretch"
    )




# =========================================================
# 9. NEW SCREENING - URONEX
# =========================================================

elif page == "New Screening":

    st.title("🧪 URONEX - New Urine Screening")

    st.write(
        "Experimental smartphone-assisted urine strip "
        "colour screening."
    )

    # -----------------------------------------------------
    # 9.1 PATIENT DETAILS
    # -----------------------------------------------------

    st.markdown("---")
    st.subheader("👤 Patient Details")

    col1, col2 = st.columns(2)

    with col1:

        patient_name = st.text_input("Patient Name")
        patient_id = st.text_input("Patient ID")

        patient_age = st.number_input(
            "Age",
            min_value=0,
            max_value=120,
            value=18
        )

    with col2:

        patient_gender = st.selectbox(
            "Gender",
            ["Select", "Male", "Female", "Other"]
        )

        sample_id = st.text_input(
            "Sample ID",
            value="URN-001"
        )

    # -----------------------------------------------------
    # 9.2 IMAGE UPLOAD / CAMERA
    # -----------------------------------------------------

    st.markdown("---")
    st.subheader("📷 Upload or Capture Strip")

    input_method = st.radio(
        "Select image method",
        ["Upload Image", "Use Camera"],
        horizontal=True
    )

    if input_method == "Upload Image":

        uploaded_file = st.file_uploader(
            "Choose urine strip image",
            type=["jpg", "jpeg", "png"],
            key="uronex_image_upload"
        )

    else:

        uploaded_file = st.camera_input(
            "Capture urine strip",
            key="uronex_camera"
        )

    # -----------------------------------------------------
    # 9.3 IMAGE PROCESSING
    # -----------------------------------------------------

    if uploaded_file is not None:

        try:

            image = Image.open(uploaded_file).convert("RGB")
            image_np = np.array(image)

            st.image(
                image,
                caption="Uploaded URONEX Strip",
                width="stretch"
            )

            height, width = image_np.shape[:2]

            # Crop side borders of strip
            x1 = int(width * 0.20)
            x2 = int(width * 0.89)

            y1 = int(height * 0.08)
            y2 = int(height * 0.96)

            strip = image_np[y1:y2, x1:x2]

            if strip.size == 0:

                st.error("Unable to crop strip image.")

            else:

                hsv = cv2.cvtColor(
                    strip,
                    cv2.COLOR_RGB2HSV
                )

                # TOP TO BOTTOM:
                # BLOOD -> pH -> ALBUMIN -> CREATININE
                #
                # These are approximate starting regions.
                # Verify them using the preview images.

                zones = {
                    "BLOOD": (0.03, 0.25),
                    "pH": (0.25, 0.47),
                    "ALB": (0.53, 0.75),
                    "CREA": (0.75, 0.98)
                }

                readings = {}
                zone_images = {}

                # -------------------------------------------------
                # AUTOMATIC COLOUR ANALYSIS
                # -------------------------------------------------

                for zone, (start, end) in zones.items():

                    ya = int(hsv.shape[0] * start)
                    yb = int(hsv.shape[0] * end)

                    pad = hsv[ya:yb, :]

                    if pad.size == 0:

                        readings[zone] = None
                        continue

                    # Remove outer margins
                    py1 = int(pad.shape[0] * 0.15)
                    py2 = max(
                        py1 + 1,
                        int(pad.shape[0] * 0.85)
                    )

                    px1 = int(pad.shape[1] * 0.05)
                    px2 = int(pad.shape[1] * 0.95)

                    pad = pad[py1:py2, px1:px2]

                    if pad.size == 0:

                        readings[zone] = None
                        continue

                    # HSV measurements
                    hue = float(np.mean(pad[:, :, 0]))
                    saturation = float(np.mean(pad[:, :, 1]))
                    brightness = float(np.mean(pad[:, :, 2]))

                    # Experimental visual colour index
                    visual_index = round(
                        saturation * 100.0 / 255.0,
                        2
                    )

                    readings[zone] = {
                        "Visual Index": visual_index,
                        "Hue": round(hue, 2),
                        "Saturation": round(saturation, 2),
                        "Brightness": round(brightness, 2)
                    }

                    zone_images[zone] = cv2.cvtColor(
                        pad,
                        cv2.COLOR_HSV2RGB
                    )

                # -------------------------------------------------
                # 9.4 REACTION REGION PREVIEW
                # -------------------------------------------------

                st.markdown("---")
                st.header("🔬 Reaction Region Preview")

                preview_columns = st.columns(4)

                for column, zone in zip(
                    preview_columns,
                    ["BLOOD", "pH", "ALB", "CREA"]
                ):

                    with column:

                        if zone in zone_images:

                            st.image(
                                zone_images[zone],
                                caption=zone,
                                width="stretch"
                            )

                        else:

                            st.warning(
                                f"{zone} region unavailable"
                            )

                # -------------------------------------------------
                # 9.5 CHECK AVAILABLE PARAMETERS
                # -------------------------------------------------

                available_zones = ["pH", "ALB", "CREA"]

                if any(
                    readings.get(zone) is None
                    for zone in available_zones
                ):

                    st.error(
                        "Unable to analyse one or more available "
                        "reaction regions. Please check the image "
                        "and region previews."
                    )

                else:

                    # BLOOD component is not available
                    blood_index = 0.00

                    # Extract available readings
                    ph_index = readings["pH"]["Visual Index"]
                    alb_index = readings["ALB"]["Visual Index"]
                    crea_index = readings["CREA"]["Visual Index"]

                    # -------------------------------------------------
                    # 9.6 DEMONSTRATION LEVEL CLASSIFICATION
                    # -------------------------------------------------

                    def classify_level(value):

                        if value < 20:
                            return "Low"

                        elif value < 50:
                            return "Moderate"

                        else:
                            return "High"

                    individual_levels = {

                        "pH": classify_level(ph_index),

                        "ALB": classify_level(alb_index),

                        "CREA": classify_level(crea_index)
                    }

                    # -------------------------------------------------
                    # 9.7 INDIVIDUAL PARAMETER RESULTS
                    # -------------------------------------------------

                    st.markdown("---")
                    st.header("📊 Automatic Analysis Results")

                    st.subheader(
                        "Individual Parameter Results"
                    )

                    display_results = [

                        ("BLOOD", blood_index, "Not Configured"),

                        (
                            "pH",
                            ph_index,
                            individual_levels["pH"]
                        ),

                        (
                            "ALBUMIN",
                            alb_index,
                            individual_levels["ALB"]
                        ),

                        (
                            "CREATININE",
                            crea_index,
                            individual_levels["CREA"]
                        )
                    ]

                    result_columns = st.columns(4)

                    for column, (name, value, level) in zip(
                        result_columns,
                        display_results
                    ):

                        with column:

                            st.metric(
                                label=f"{name} Visual Index",
                                value=f"{value:.2f}/100"
                            )

                            if level == "Low":

                                st.success("LOW")

                            elif level == "Moderate":

                                st.warning("MODERATE")

                            elif level == "High":

                                st.error("HIGH")

                            else:

                                st.info("NOT CONFIGURED")

                    # -------------------------------------------------
                    # 9.8 OVERALL PROTOTYPE RESULT
                    # -------------------------------------------------

                    st.markdown("---")
                    st.header("🔎 Overall Prototype Result")

                    # BLOOD is excluded because no component is available
                    overall_index = round(
                        np.mean([
                            ph_index,
                            alb_index,
                            crea_index
                        ]),
                        2
                    )

                    overall_level = classify_level(
                        overall_index
                    )

                    col1, col2 = st.columns(2)

                    with col1:

                        st.metric(
                            "Overall Visual Index",
                            f"{overall_index:.2f}/100"
                        )

                    with col2:

                        if overall_level == "Low":

                            st.success(
                                "OVERALL LEVEL: LOW"
                            )

                        elif overall_level == "Moderate":

                            st.warning(
                                "OVERALL LEVEL: MODERATE"
                            )

                        else:

                            st.error(
                                "OVERALL LEVEL: HIGH"
                            )

                    st.info(
                        "Overall demonstration category is calculated "
                        "using pH, Albumin and Creatinine visual indices. "
                        "BLOOD is excluded because its reaction component "
                        "is unavailable."
                    )

                    # -------------------------------------------------
                    # 9.9 COMPLETE PARAMETER TABLE
                    # -------------------------------------------------

                    st.markdown("---")
                    st.header("📋 Complete Parameter Details")

                    detail_data = [

                        {
                            "Parameter": "BLOOD",
                            "Visual Index": 0.00,
                            "Prototype Level": "Not Configured",
                            "Hue": "N/A",
                            "Saturation": "N/A",
                            "Brightness": "N/A"
                        },

                        {
                            "Parameter": "pH",
                            "Visual Index": ph_index,
                            "Prototype Level": individual_levels["pH"],
                            "Hue": readings["pH"]["Hue"],
                            "Saturation": readings["pH"]["Saturation"],
                            "Brightness": readings["pH"]["Brightness"]
                        },

                        {
                            "Parameter": "ALBUMIN",
                            "Visual Index": alb_index,
                            "Prototype Level": individual_levels["ALB"],
                            "Hue": readings["ALB"]["Hue"],
                            "Saturation": readings["ALB"]["Saturation"],
                            "Brightness": readings["ALB"]["Brightness"]
                        },

                        {
                            "Parameter": "CREATININE",
                            "Visual Index": crea_index,
                            "Prototype Level": individual_levels["CREA"],
                            "Hue": readings["CREA"]["Hue"],
                            "Saturation": readings["CREA"]["Saturation"],
                            "Brightness": readings["CREA"]["Brightness"]
                        }
                    ]

                    detail_df = pd.DataFrame(detail_data)

                    st.dataframe(
                        detail_df,
                        use_container_width=True,
                        hide_index=True
                    )

                    # -------------------------------------------------
                    # 9.10 CREATE PATIENT RESULT
                    # -------------------------------------------------

                    result = {

                        "Patient Name": patient_name,
                        "Patient ID": patient_id,
                        "Age": patient_age,
                        "Gender": patient_gender,
                        "Sample ID": sample_id,

                        "Date": datetime.now().strftime(
                            "%d-%m-%Y %H:%M"
                        ),

                        "BLOOD Visual Index": 0.00,
                        "BLOOD Level": "Not Configured",

                        "pH Visual Index": ph_index,
                        "pH Level": individual_levels["pH"],

                        "ALB Visual Index": alb_index,
                        "ALB Level": individual_levels["ALB"],

                        "CREA Visual Index": crea_index,
                        "CREA Level": individual_levels["CREA"],

                        "Overall Visual Index": overall_index,
                        "Prototype Screening Level": overall_level
                    }

                    st.session_state.uronex_latest_result = result

                    # -------------------------------------------------
                    # 9.11 SAVE RESULT
                    # -------------------------------------------------

                    st.markdown("---")

                    if st.button(
                        "💾 Save Screening Result",
                        key="save_uronex_result"
                    ):

                        st.session_state.history.append(
                            result.copy()
                        )

                        st.success(
                            "Screening result saved successfully!"
                        )

                    # -------------------------------------------------
                    # 9.12 DOWNLOAD REPORT
                    # -------------------------------------------------

                    report_df = pd.DataFrame([result])

                    csv_data = report_df.to_csv(
                        index=False
                    ).encode("utf-8")

                    safe_sample_id = "".join(
                        char for char in sample_id
                        if char.isalnum() or char in ("-", "_")
                    )

                    if not safe_sample_id:
                        safe_sample_id = "URONEX"

                    st.download_button(
                        "⬇️ Download Complete Screening Report",
                        data=csv_data,
                        file_name=f"{safe_sample_id}_Report.csv",
                        mime="text/csv",
                        key="download_uronex_report"
                    )

                    # -------------------------------------------------
                    # 9.13 DISCLAIMER
                    # -------------------------------------------------

                    st.markdown("---")

                    st.warning(
                        "URONEX is an experimental academic prototype. "
                        "Low, Moderate and High are demonstration "
                        "categories based on image colour indices. "
                        "They are not measured biomarker concentrations "
                        "or validated CKD risk levels. BLOOD is shown "
                        "as Not Configured because its reaction component "
                        "is unavailable."
                    )

        except Exception as e:

            st.error(
                f"Image processing error: {e}"
            )

    else:

        st.info(
            "Upload or capture a urine strip image to display "
            "the screening results."
        )



# =========================================================
# 10. SCREENING HISTORY
# =========================================================

elif page == "Screening History":

    st.title("Screening History")

    records = st.session_state.history

    if records:

        df = pd.DataFrame(records)

        st.metric(
            "Total Screening Records",
            len(df)
        )

        st.dataframe(
            df,
            hide_index=True,
            width="stretch"
        )

        csv_data = df.to_csv(
            index=False
        ).encode("utf-8")

        st.download_button(
            "Download Screening History",
            data=csv_data,
            file_name="URONEX_History.csv",
            mime="text/csv",
            key="uronex_history_download"
        )

        if st.button(
            "Clear Screening History",
            key="uronex_clear_history"
        ):

            st.session_state.history = []
            st.rerun()

    else:

        st.info("No screening records available.")


# =========================================================
# 11. TEAM
# =========================================================

elif page == "Team":

    st.title("URONEX Project Team")

    st.subheader(
        "Final-Year Biomedical Engineering Project"
    )

    members = [
        "Kamali P",
        "Jinisha Derlin C V",
        "Divya Sri R"
    ]

    columns = st.columns(3)

    for col, member in zip(columns, members):

        with col:

            with st.container(border=True):

                st.title("👩‍🔬")
                st.subheader(member)
                st.write("Biomedical Engineering")

    st.markdown("---")
    st.header("Project Department")

    st.write("""
    Department of Biomedical Engineering

    Vel Tech Multi Tech Dr. Rangarajan
    Dr. Sakunthala Engineering College
    """)


# =========================================================
# 12. FOOTER
# =========================================================

st.markdown("---")

st.caption(
    "🧬 URONEX | Smart Preliminary Kidney Health Screening"
)

st.caption(
    "Biomedical Engineering Final-Year Project | Version 1.0"
)
