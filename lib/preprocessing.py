from utils.imports import *

def clean_csv(filename):
    """
    Function to clean CSV when the QGIS algo was not working as
    expected
    """
    df = pd.read_csv(filename,encoding='ISO-8859-1')
    print(df)
    df = df.drop(labels=["layer", "path"], axis=1)
    print(df)
    df.to_csv("Yaounde_Futur_Urb.csv",index=False)

clean_csv("yaounde_futur.csv")

def create_X_y(df,parameters_list):
    """Prepares feature matrix X and target vector y from the DataFrame by selecting the right parameters
    and cleaning the data.
    
    Parameters:
    df (DataFrame): The input DataFrame.
    parameters_list (list): List of parameters to include in the feature matrix.
    
    Returns:
    tuple: Feature matrix X and target vector y.
    """
    # y will always be the same because this is the variable we want to predict
    
    df = take_right_parameters(df,*parameters_list)
    y = df["LST"] 
    y = np.array(y,dtype=np.float16)     
    X = df.drop('LST', axis=1)  # If you want to take all the variables except the dependant one do this, even if it is hard to understand

    return X,y

def take_right_parameters(df,params_to_take=[],params_to_drop=[]):
    """
    Selects or drops specified parameters (columns) from the DataFrame.
    
    Parameters:
    df (DataFrame): The input DataFrame.
    params_to_take (list): List of parameters to include in the DataFrame.
    params_to_drop (list): List of parameters to drop from the DataFrame.
    
    Returns:
    DataFrame: The DataFrame with the specified parameters taken or dropped.
    """
    if params_to_take!=[]:
        if "LST" not in params_to_take:
            params_to_take.append("LST")
        df = df[params_to_take]
            
    elif params_to_drop!=[]:
        print(params_to_drop)
        print(df)
        df = df.drop(params_to_drop,axis=1)
        print(df)

    return df