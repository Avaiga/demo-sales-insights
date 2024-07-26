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

import taipy as tp
from taipy.gui import Gui, notify

from configuration import scenario_cfg

from configuration.auth import *

from taipy import Core
from pages import *

def on_navigate(state, page):
    if page not in ["login", "TaiPy_root_page"]:
        state.current_page = page
    if page in ['Admin']:
        new_page = admin_page.get_traits(state.credentials)
        if page != new_page:
            notify(state, "error", f"You must be logged in to access {page}")
        return new_page
    else:
        return page

if __name__ == "__main__":
    pages = {
        "/": root_page,
        "login": login_page,
        "Overview": Overview,
        "Analysis": Analysis,
        "Predictions": Predictions,
        "Admin": Admin,
    }

    current_page = "Overview"

    core = Core()
    core.run()
    # #############################################################################
    # PLACEHOLDER: Create and submit your scenario here                           #
    #                                                                             #
    # Example:                                                                    #
    # from configuration import scenario_config                                   #
    # scenario = tp.create_scenario(scenario_config)                              #
    # scenario.submit()                                                           #
    # Comment, remove or replace the previous lines with your own use case        #
    # #############################################################################

    gui = Gui(pages=pages)
    gui.run(title="Sales Enterprise", port=2853, dark_mode=False)
    