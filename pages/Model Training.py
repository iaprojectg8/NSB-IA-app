from utils.imports import *
from lib.session_variables import *
from lib.uploader import *
from lib.visualization import *
from lib.model import rdf_regressor, save_model
from streamlit import config_option
from lib.callbacks import *
from utils.variables import G8_LOGO_PATH, KERAN_LOGO_PATH
from lib.preprocessing import *
from lib.tools import put_logo_if_possible
from lib.logo_style import increase_logo
    
put_logo_if_possible()

st.logo(G8_LOGO_PATH)
increase_logo

st.title("Model trainer")
# Main execution
uploaded_files = upload_train_file_model()
if uploaded_files:
    print(uploaded_files)
    df, selected_variables = manage_uploaded_model(uploaded_files)
    df = df.sample(100000)
    st.session_state.selected_variables = selected_variables
    print(st.session_state.selected_variables)
    X,y = create_X_y(df,selected_variables)
    estimator = st.number_input(label="Amount of estimators (trees)", min_value=1, max_value=150, value=25)
    
    st.button("Train a model", on_click=callback_train)

    if st.session_state.train:
        
        model = rdf_regressor(X, y, estimator=estimator)

        st.session_state.model = model
        
        print(st.session_state.input_path)
        st.write("Your model is in memory you can go to the test page and try to predict on a new dataset containing the same variable as the ")
        save_model(model)
    if st.session_state.save:
         
      
        dump(st.session_state.model, st.session_state.input_path)
        st.session_state.save = 0



    