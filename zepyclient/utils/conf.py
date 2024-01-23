import os
from dotenv import load_dotenv
    
# Load environment variables from .env file
load_dotenv() 

def get_from_dapr_state_store(key):
    # This is a placeholder function. You'll need to implement the logic to fetch data from DAPR state store.
    # For now, it always returns None.
    return None


def normalize_bool(value):
    if value:
        if value in ["True", "true"]:
            return True
        elif value in ["False", "false"]:
            return False
        else:
            return value
    else:
        return None

def get_config(variable_name, source=None):

    # Normalize the source value to handle case-insensitivity
    if source:
        source = source.lower()
        value = get_from_dapr_state_store(variable_name)
        
        return normalize_bool(value)
    elif source == "dpar":
        return get_from_dapr_state_store(variable_name)
    else:
        value = os.environ.get(variable_name)
        return normalize_bool(value)
