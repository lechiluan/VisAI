import streamlit as st
import requests
from PIL import Image
from io import BytesIO
from model_ai import generate_prompt


def is_valid_image_url(url):
    """Check if URL contains a valid image."""
    try:
        response = requests.get(url, timeout=5)
        if response.status_code != 200:
            return False
        content_type = response.headers.get('content-type', '')
        if not content_type.startswith('image/'):
            return False
        Image.open(BytesIO(response.content))
        return True
    except Exception:
        return False


def load_image_from_url(url):
    try:
        if not is_valid_image_url(url):
            return None
        response = requests.get(url)
        img = Image.open(BytesIO(response.content))
        return img
    except Exception:
        return None


def main():
    st.set_page_config(
        page_title="VisAI - DELIVERY PACKAGE DAMAGE DETECTION", layout="wide")

    st.markdown("""
        <style>
        .stButton > button {
            border-radius: 6px;
            font-weight: 500;
        }
        .stTextArea > div > div > textarea {
            border-radius: 6px;
        }
        .css-1629p8f h1 {
            font-weight: 600;
        }
        </style>
    """, unsafe_allow_html=True)

    st.title(":mag_right: VisAI - DELIVERY PACKAGE DAMAGE DETECTION")

    with st.sidebar:
        st.header("Instructions")
        st.markdown(
            """
            ### How to Use:
            
            **1. Input Images**
            - Enter a list of image URLs
            - Separate URLs with commas
            
            **2. Analysis**
            - Click "Analyze Responsibility"
            - Wait for processing
            
            **3. Results**
            - Review image validation
            - Check responsibility assessment
            - Read detailed analysis
            
            ⚠️ **Note:** Ensure all URLs are accessible and contain valid images
            """
        )

    if 'urls_input' not in st.session_state:
        st.session_state['urls_input'] = ""

    if 'analysis_results' not in st.session_state:
        st.session_state['analysis_results'] = None

    st.markdown("### 📸 Input Image URLs")
    urls_input = st.text_area(
        "List of Image URLs:",
        value=st.session_state['urls_input'],
        placeholder="Paste URLs separated by commas",
        height=150,
        help="Each URL should point to a valid image file",
    )

    st.session_state['urls_input'] = urls_input

    button_cols = st.columns([5, 3, 5])

    with button_cols[0]:
        analyze_button = st.button(
            "🔍 Analyze Responsibility", type="primary", use_container_width=True)

    with button_cols[1]:
        clear_button = st.button("❌Clear", use_container_width=True)

    if clear_button:
        st.session_state['urls_input'] = ""
        st.session_state['analysis_results'] = None

    if analyze_button:
        if urls_input:
            urls = [url.strip()
                    for url in urls_input.split(',') if url.strip()]

            if urls:
                with st.expander("📊 Analysis Details", expanded=True):
                    st.write(f"**Total images to analyze:** {len(urls)}")

                    valid_urls = []
                    invalid_urls = []

                    progress_bar = st.progress(0)
                    status_text = st.empty()

                    for idx, url in enumerate(urls):
                        status_text.text(
                            f"Processing image {idx + 1}/{len(urls)}...")
                        progress_bar.progress((idx + 1) / len(urls))

                        image = load_image_from_url(url)
                        if image:
                            valid_urls.append(url)
                        else:
                            invalid_urls.append(url)

                    status_text.empty()
                    progress_bar.empty()

                # Display valid images in a grid
                if valid_urls:
                    st.markdown("### 🖼️ Valid Images")
                    cols = 3
                    for i in range(0, len(valid_urls), cols):
                        columns = st.columns(cols)
                        for col_index, url in enumerate(valid_urls[i:i+cols]):
                            with columns[col_index]:
                                st.image(url, use_container_width=True)
                                st.caption(f"Image {i + col_index + 1}")

                # Show invalid URLs in an expander
                if invalid_urls:
                    with st.expander("⚠️ Invalid URLs", expanded=False):
                        st.error(
                            "The following URLs were invalid or inaccessible:")
                        for url in invalid_urls:
                            st.code(url, language="text")

                # Process valid images and store results in session state
                if valid_urls:
                    with st.spinner("Analyzing images..."):
                        result = generate_prompt(valid_urls)
                        # Store results in session state for potential future use or display.
                        st.session_state['analysis_results'] = result

                    # Display analysis results only after processing is complete.
                    display_analysis_results(valid_urls, invalid_urls)

                else:
                    st.error(
                        "No valid images found for analysis. Please check your URLs and try again.")
            else:
                st.error(
                    "No valid image URLs provided. Please enter at least one URL.")
        else:
            st.error("Please provide image URLs to analyze.")


def display_analysis_results(valid_urls, invalid_urls):
    """Display the analysis results."""
    result = st.session_state['analysis_results']

    if result is not None:
        st.markdown("### 📋 VisAI Analysis Results")

        # Create a card-like container for results
        results_container = st.container()

        with results_container:
            col1, col2 = st.columns([1, 2])

            with col1:
                st.markdown("**This product is damaged by:**")
                case = result.get('case', 'No response')
                if case == "Vendors":
                    st.error(case)
                elif case == "Carriers":
                    st.warning(case)
                else:
                    st.info(case)

            with col2:
                st.markdown("**Analysis:**")
                st.write(result.get('reason', 'No response'))

            # Add metrics
            st.markdown("---")
            metric_cols = st.columns(3)
            temp = result.get('total_token', 0)
            cal = temp*1.25/1000000
            metric_cols[0].metric("Valid Images", len(valid_urls))
            metric_cols[1].metric("Total Tokens", temp)
            metric_cols[2].metric("Total Cost", f"${cal:.6f}")


if __name__ == "__main__":
    main()
