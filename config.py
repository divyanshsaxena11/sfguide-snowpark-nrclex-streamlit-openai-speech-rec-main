# %%
#Importing Librarires for notebook

#.. Snowflake Snowpark Session Library
from snowflake.snowpark import Session



# %%
# Constructing Dict for Snowflake Snowpark Connection Params

sf_conn_config = {
    "account": "xxxxxxxxx.xxxxxxxxx-xxxxxxxxx.xxxxxxxxx",
    "user": "xxxxxxxxx",
    "password": "xxxxxxxxxxxxxxxxxx",
    "role" : "SYSADMIN",
    "warehouse" : "COMPUTE_WH",
    "database" : "OPEN_AI_DB",
    "schema" : "EMOTION_RECOGNITION"
}

# %%
# Secret Key for OPEN_AI API Calls
OPENAI_API_KEY = [OPENAI KEY SECRET]