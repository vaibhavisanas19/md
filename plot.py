import streamlit as st
import subprocess
import os
import platform

# ====== CONFIGURATION ======
# Set the EXACT path to your vina.exe
VINA_PATH = r"C:\Program Files (x86)\The Scripps Research Institute\Vina\vina.exe"


# ====== DOCKING FUNCTION ======
def run_vina(receptor, ligand, center_x, center_y, center_z, size_x, size_y, size_z):
    # Verify Vina exists
    if not os.path.exists(VINA_PATH):
        st.error(f"❌ AutoDock Vina NOT FOUND at:\n{VINA_PATH}")
        st.error("Please install Vina or check the path!")
        return None

    try:
        command = [
            f'"{VINA_PATH}"',  # Quotes handle spaces in path
            "--receptor", receptor,
            "--ligand", ligand,
            "--center_x", str(center_x),
            "--center_y", str(center_y),
            "--center_z", str(center_z),
            "--size_x", str(size_x),
            "--size_y", str(size_y),
            "--size_z", str(size_z),
            "--out", "docked_output.pdbqt"
        ]

        # Run Vina
        result = subprocess.run(
            " ".join(command),  # Combine with spaces
            shell=True,  # Required for Windows paths with spaces
            capture_output=True,
            text=True
        )

        return result.stdout if result.returncode == 0 else result.stderr

    except Exception as e:
        return f"🚨 Docking failed: {str(e)}"


# ====== STREAMLIT UI ======
st.title("AutoDock Vina Docking App")
st.markdown(f"**Vina Path:** `{VINA_PATH}`")
st.markdown(f"**Path exists:** `{os.path.exists(VINA_PATH)}`")

# File Upload
receptor_file = st.file_uploader("Upload Receptor (PDBQT)", type="pdbqt")
ligand_file = st.file_uploader("Upload Ligand (PDBQT)", type="pdbqt")

# Docking Box Parameters
st.subheader("Docking Box Settings")
col1, col2 = st.columns(2)
with col1:
    center_x = st.number_input("Center X", value=0.0)
    center_y = st.number_input("Center Y", value=0.0)
    center_z = st.number_input("Center Z", value=0.0)
with col2:
    size_x = st.number_input("Size X (Å)", value=20.0)
    size_y = st.number_input("Size Y (Å)", value=20.0)
    size_z = st.number_input("Size Z (Å)", value=20.0)

# Run Docking
if st.button("Run Docking", type="primary"):
    if receptor_file and ligand_file:
        # Save files
        with open("receptor.pdbqt", "wb") as f:
            f.write(receptor_file.getbuffer())
        with open("ligand.pdbqt", "wb") as f:
            f.write(ligand_file.getbuffer())

        # Run Vina
        with st.spinner("Running docking..."):
            output = run_vina(
                "receptor.pdbqt", "ligand.pdbqt",
                center_x, center_y, center_z,
                size_x, size_y, size_z
            )

        # Show results
        st.subheader("Results")
        if output:
            st.text_area("Vina Output", output, height=300)

            # Download results
            if os.path.exists("docked_output.pdbqt"):
                with open("docked_output.pdbqt", "rb") as f:
                    st.download_button(
                        "Download Results",
                        f,
                        file_name="docked_results.pdbqt"
                    )
    else:
        st.error("Please upload both receptor and ligand files!")