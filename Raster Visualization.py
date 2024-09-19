from utils.imports import *
from lib.uploader import *
from lib.visualization import *
from streamlit import config_option
from lib.callbacks import *
from utils.variables import VARIABLES_LIST
from lib.logo_style import increase_logo

# Logo customization
st.logo("logo/Logo_G8.png")
increase_logo()

# Title and uploader
st.title("Raster Visualizer")
uploaded_files = upload_files_raster_viz()
if uploaded_files:
    print(uploaded_files)
    
    # Create a Leafmap map
    map = leafmap.Map()
    for uploaded_file in uploaded_files:
      # Save the raster file temporarily
      if uploaded_file.type=="image/tiff":
          
          # If rasters are uploaded, need to add 
          add_raster_to_map(uploaded_file=uploaded_file, map=map)

      elif uploaded_file.type=="application/vnd.ms-excel":
          
          # Create the dataframe from the uploaded file
          df = manage_csv(uploaded_file=uploaded_file)

          selected_variable = st.selectbox(label="Chose a variable to observe",options=VARIABLES_LIST)
          if selected_variable:
              variable, grid_values, transform, complete_path = create_rasters_needs(df,uploaded_file.name)
              save_and_add_raster_to_map(variable, grid_values, transform, complete_path, map)

        
    map.to_streamlit()
    

