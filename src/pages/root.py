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
The root page of the application.
Page content is imported from the root.md file.

Please refer to https://docs.taipy.io/en/latest/manuals/gui/pages for more details.
"""
import taipy.gui.builder as tgb


def creates_pages(pages):
    return [(f"/{page}", page.replace("_", " ").title()) for page in list(pages)[1:]]


with tgb.Page() as root_page:
    with tgb.part("header sticky"):
        with tgb.layout(
            "100px 12rem 1 8rem 150px",
            columns__mobile="100px 12rem 1 8rem 150px",
            class_name="header-content",
        ):
            tgb.image("favicon.png", width="50px")
            tgb.text("Sales **Dashboard**", mode="md")
            tgb.navbar(
                lov="{creates_pages(pages)}",
            )
            tgb.part()

            tgb.text(
                "Welcome **back**!",
                mode="md",
            )

    with tgb.part("content"):
        with tgb.layout(columns="1 1 1"):
            with tgb.part():
                tgb.text("# **Total** sales:", mode="md")
                tgb.text(lambda data: f"### US $ {int(data['Total'].sum())}", mode="md")

            with tgb.part():
                tgb.text("# Average **Rating**:", mode="md")
                tgb.text(
                    lambda data: f"### {round(data['Rating'].mean(), 1)}", mode="md"
                )

            with tgb.part():
                tgb.text("# Average **Sales**:", mode="md")
                tgb.text(
                    lambda data: f"### US $ {round(data['Total'].mean(), 2)}", mode="md"
                )

        with tgb.expandable(
            title="Data",
            expanded=False,
        ):
            tgb.table("{data}")

        tgb.html("br")

        tgb.content()

        tgb.toggle(theme=True)
