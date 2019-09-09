import dominate
from dominate.tags import *
import datetime
import pdfkit


class Report(object):
    def __init__(self, report_uuid, app_name, logo, company=None,
                 contract=None):
        self.report_uuid = str(report_uuid).upper()
        self.app_name = str(app_name).upper()
        self.html = dominate.document()

        self.html += h2("", style=
                            "margin-left:auto;margin-right:auto;font-size:"
                            "50;text-align:center;"
                            "padding:4px; height:75px")

        # Top Padding
        self.html += h2("", style=
                            "margin-left:auto;margin-right:auto;font-size:"
                            "50;text-align:center;"
                            "padding:4px; height:25px")

        # First Title Labels and URL Tab Title
        self.html.title = '{} Automation Report'.format(self.app_name)
        self.html += h1('{} Automation Report'.format(self.app_name),
                        style=
                        "font-size:99;text-align:center;padding:0px;"
                        "line-height:1")
        # self.html += h1('Report UUID: {}'.format(self.report_uuid),
        #                 style=
        #                 "font-size:89;text-align:center;padding:0px;"
        #                 "line-height:1")

        # Date label
        self.html += h1(str(datetime.date.today()), style=
                            "margin-left:auto;margin-right:auto;font-size:"
                            "95;text-align:center;"
                            "padding:3px")

        # Company Name
        if company:
            self.html += h2(str(company), style=
                            "margin-left:auto;margin-right:auto;font-size:"
                            "50;text-align:center;"
                            "padding:0px;line-height:0")

        # Contract Number
        if contract:
            self.html += h2("Contract: W81XWH-15-F-0421", style=
                            "margin-left:auto;margin-right:auto;font-size:"
                            "50;text-align:center;"
                            "padding:0px; height:88px")

        # Company Logo
        if logo:
            self.html += td(div(img(src=logo), _class='photo',
                            ALIGN='Center', style ="height:540;width:142"))

        # Spacer
        self.html += h2("", style=
                            "margin-left:auto;margin-right:auto;font-size:"
                            "50;text-align:center;"
                            "padding:4px; height:850px")

        # Copyright Footer
        self.html += h3("Test Anatomy: The Lightweight Automation Engine",
                        style=
                            "margin-left:auto;margin-right:auto;font-size:"
                            "50;text-align:center;line-height:0"
                            "padding:0px")

        self.html += h3("Test Anatomy: Copyright 2019 Eric "
                        "github.com/eagleEggs", style=
                            "margin-left:auto;margin-right:auto;font-size:"
                            "50;text-align:center;"
                            "padding:0px;line-height:0")

        self.html += h2("", style=";page-break-after:always")

        # Test Results Table
        self.contents = table(border=1,
                              style=
                              "margin-left:auto;margin-right:auto;font-size:"
                              "large;text-align:center;"
                              "padding:4px;page-break-after:always")

        self.html += h3("Summary of Test Results", style=
                                "margin-left:auto;margin-right:auto;font-size:"
                                "95;text-align:center;"
                                "padding:3px")

        self.html += self.contents

    def add_script(self, name):  # TestCycle()
        self.name = name # this duplicates the script name on the page...
        self.html += h1('{}'.format(name), # TODO: remove this from TA
                        style =
                        "font-size:large;text-align:center;padding:4px;"
                                        "page-break-before:always")

    def add_screenshot(self, screenshot, functionality, status=None):
        remove_chars = "[']"
        for item in remove_chars:
            str(screenshot).replace(item, "")

        if status:
            self.html += h1('Screenshot of Functionality: {}'.format(functionality),
                            style=
                            "font-size:large;text-align:center;padding:4px;"
                            "page-break-after:always")
            self.html += div(img(src=screenshot), _class='photo', style=
                                                        "text-align:center")

        else:
            self.html += h1('{}'.format(functionality),
                            style =
                            "font-size:large;text-align:center;padding:4px")
            self.html += div(img(src=screenshot), _class='photo', style=
                                                        "text-align:center")

    def add_status(self, status, line=None):  # TestCycle()
        if line:
            self.html += h1(status, line,
                        style =
                        "font-size:large;text-align:center;"
                        "padding:4px;color:ff360b;page-break-after:always")
            with self.contents:
                row = tr()
                with row.add(td()):
                    p('{}_{}'.format(status, self.name),
                        style =
                        "font-size:large;text-align:left;"
                        "padding:4px;color:ff360b")

        else:
            self.html += h1(status,
                        style =
                        "font-size:large;text-align:center;"
                        "padding:4px;color:#008000;page-break-after:always")

            with self.contents:
                row = tr()
                with row.add(td()):
                    p('{}_{}'.format(status, self.name),
                        style =
                        "font-size:large;text-align:left;"
                        "padding:4px;color:#008000")

    def add_logo(self, logo1, logo2=False):
        self.html += td(div(img(src=logo1), _class='photo',
                            ALIGN='Center', style="height:540;width:142"))

    def finalize_html(self, driver):  # TestCycle()
        resultshtml= open('{}/Automation Report.html'.format(
                driver.report_folder), 'w')
        resultshtml.write(self.html.render())
        resultshtml.close()
        print("HTML Gen Complete")

        # the following errors out with successive tests:

        print(driver.report_folder)
        pdfkit.from_file('{}/Automation Report.html'.format(
                driver.report_folder),
                         '{}/Automation Report.pdf'.format(
                                 driver.report_folder))
        print("PDF Gen Complete")

    def finalize_pdf(self):
        pass
