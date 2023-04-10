# %%
#Importing Librarires for notebook

#.. Snowflake Snowpark Session Library
from snowflake.snowpark import Session



# %%
# Constructing Dict for Snowflake Snowpark Connection Params

sf_conn_config = {
    "account": "vt67141.central-india.azure",
    "user": "divyansh",
    "password": "Divyansh@123",
    "role" : "SYSADMIN",
    "warehouse" : "COMPUTE_WH",
    "database" : "OPEN_AI_DB",
    "schema" : "EMOTION_RECOGNITION"
}

# %%
# Secret Key for OPEN_AI API Calls
OPENAI_API_KEY = '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'


