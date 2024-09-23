from utils.imports import *
from lib.session_variables import *
from lib.uploader import upload_csv_train_file, manage_csv
from lib.model_train import rdf_regressor, display_all_precedent_training_graphs, save_model
from streamlit import config_option
from lib.callbacks import callback_train
from utils.variables import G8_LOGO_PATH, TRAINING_LIST, DATAFRAME_HEIGHT
from lib.preprocessing import create_X_y
from lib.logo_style import increase_logo, put_logo_if_possible
from copy import copy
    
put_logo_if_possible()
st.logo(G8_LOGO_PATH)
increase_logo()

st.title("Model trainer")
st.session_state.csv_file = upload_csv_train_file()
if st.session_state.csv_file:
    
    df = manage_csv(uploaded_file=st.session_state.csv_file)
    st.session_state.df_train = df
    n_rows = len(df)

    # Select the variables
    st.session_state.selected_variables = st.multiselect("Chose the variable on which you want to train", options=TRAINING_LIST,default=st.session_state.selected_variables)
    

    # Select the amount of observation for 
    data_amount = st.selectbox("Choose the data size for training",[int(n_rows/10**(i/2)) if i%2==0 else int(n_rows/(10**((i-1)/2)*2),) for i in range(10)])
    df_sampled = copy(df).sample(data_amount,ignore_index=True)
    
    # Separate and display dataset
    X,y = create_X_y(df_sampled,copy(st.session_state.selected_variables))
    st.subheader("Training dataframe")
    st.dataframe(X, height=DATAFRAME_HEIGHT)

    # Hyperparamters selection
    estimator = st.number_input(label="Amount of estimators (trees)", min_value=1, max_value=150, value=25)
    test_size = st.slider(label="Chose the data proportion given to test",min_value=0.0, max_value=1.0, step=0.01, value=0.2)
    st.button("Train a model", on_click=callback_train)

    if st.session_state.train:
        
        model_scaler_dict = rdf_regressor(X,y, estimator, test_size)
        print(st.session_state.input_path)
        st.write("Your model is in memory you can go to the test page and try to predict on a new dataset containing the same variable as the ")
        save_model()
        st.session_state.training_done = 1
        st.session_state.tarin = 0

    # This is in case the training has been done but we want to display the results of it
    elif st.session_state.training_done:
        st.subheader("A model has already been trained, and here are the results")
        display_all_precedent_training_graphs()
        
    if st.session_state.save:
        
        # It saves the model
        dump(st.session_state.model_scaler_dict, st.session_state.input_path)
        st.session_state.save = 0

elif st.session_state.training_done:
    st.subheader("Here are the last model performances")
    display_all_precedent_training_graphs()