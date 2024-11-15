# Copyright 2021-2024 Avaiga Private Limited
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with
# the License. You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on
# an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the
# specific language governing permissions and limitations under the License.

"""
Contain the application's configuration including the scenario configurations.

The configuration is run by the Core service.
"""

from algorithms import *

from taipy import Config

from taipy.config import Config, Scope
import datetime as dt
import os



job_execution_mode = os.environ.get("JOB_EXECUTION_MODE", "standalone")
repository_type = "filesystem" # os.environ.get("REPOSITORY_TYPE", "filesystem")
mongo_host = os.environ.get("MONGO_HOST", "localhost")
mongo_port = int(os.environ.get("MONGO_PORT", 27017))
mongo_user = os.environ.get("MONGO_USER", "taipy")
mongo_password = os.environ.get("MONGO_PASSWORD", "taipy")
mongo_app_db = os.environ.get("MONGO_APP_DB", "demo-cluster-mode-dev")

Config.configure_job_executions(mode=job_execution_mode)
Config.configure_core(
       storage_folder=".user_data",
       repository_type=repository_type,
       repository_properties={
       "mongodb_hostname": mongo_host,
       "mongodb_user": mongo_user,
       "mongodb_password": mongo_password,
       "mongodb_port": mongo_port,
       "application_db": mongo_app_db,
       },
)

def _connect_mongodb(
    db_host: str, db_port: int, db_username: str, db_password: str, db_extra_args: frozenset, db_driver: str
):
    """Create a connection to a Mongo database.
    The `"mongodb_extra_args"` passed by the user is originally a dictionary, but since `@lru_cache` wrapper only
    accepts hashable parameters, the `"mongodb_extra_args"` should be converted into a frozenset beforehand.

    Parameters:
        db_host (str): the database host.
        db_port (int): the database port.
        db_username (str): the database username.
        db_password (str): the database password.
        db_extra_args (frozenset): A frozenset converted from a dictionary of additional arguments to be passed into
            database connection string.
    Returns:
        pymongo.MongoClient
    """
    auth_str = ""
    if db_username and db_password:
        auth_str = f"{db_username}:{db_password}@"


    driver = "mongodb"
    if db_driver:
        driver = f"{driver}+{db_driver}"

    connection_string = f"{driver}://{auth_str}{db_host}"
    connection_string = connection_string if db_driver else f"{connection_string}:{db_port}"

    return connection_string

conn_str = _connect_mongodb(mongo_host, mongo_port, mongo_user, mongo_password, None, mongo_app_db)

#Config.configure_job_executions(mode="standalone", nb_of_workers=2)

path_to_data = "data/modified_supermarkt_sales_plus.csv"

initial_data_cfg = Config.configure_data_node(id="initial_data",
                                              storage_type="csv",
                                              path=path_to_data,
                                              scope=Scope.GLOBAL)

holiday_cfg = Config.configure_data_node(id="holiday", storage_type="csv")
level_cfg = Config.configure_data_node(id="level", default_data=1)
date_cfg = Config.configure_data_node(id="date")

final_data_cfg =  Config.configure_data_node(id="final_data")

model_arima_cfg = Config.configure_data_node(id="model_arima")
model_xgboost_cfg = Config.configure_data_node(id="model_xgboost")

predictions_arima_cfg = Config.configure_data_node(id="predictions_arima")
predictions_xgboost_cfg = Config.configure_data_node(id="predictions_xgboost")

result_cfg = Config.configure_data_node(id="result")


task_preprocess_cfg = Config.configure_task(id="task_preprocess_data",
                                            function=preprocess,
                                            input=[initial_data_cfg, holiday_cfg, level_cfg],
                                            output=[final_data_cfg, date_cfg])


task_train_arima_cfg = Config.configure_task(id="task_train",
                                             function=train_arima,
                                             input=final_data_cfg,
                                             output=model_arima_cfg) 

task_forecast_arima_cfg = Config.configure_task(id="task_forecast",
                                                function=forecast,
                                                input=model_arima_cfg,
                                                output=predictions_arima_cfg)


task_train_xgboost_cfg = Config.configure_task(id="task_train_xgboost",
                                               function=train_xgboost,
                                               input=final_data_cfg,
                                               output=model_xgboost_cfg)

task_forecast_xgboost_cfg = Config.configure_task(id="task_forecast_xgboost",
                                                  function=forecast_xgboost,
                                                  input=[model_xgboost_cfg, date_cfg],
                                                  output=predictions_xgboost_cfg)

task_result_cfg = Config.configure_task(id="task_result",
                                        function=concat,
                                        input=[final_data_cfg, 
                                               predictions_arima_cfg, 
                                               predictions_xgboost_cfg],
                                        output=result_cfg)


scenario_cfg = Config.configure_scenario(id='scenario', task_configs=[task_preprocess_cfg,
                                                                      task_train_arima_cfg,
                                                                      task_forecast_arima_cfg,
                                                                      task_train_xgboost_cfg,
                                                                      task_forecast_xgboost_cfg,
                                                                      task_result_cfg])

Config.export('configuration/config.toml')