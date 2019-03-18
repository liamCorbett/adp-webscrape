from datetime import datetime
import os.path
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as conditions
from selenium.webdriver.support.ui import WebDriverWait


class ADPResource:
    RESOURCE_LOGIN_URL = 'https://online.adp.com/resource/login.html'
    EZLABORMANAGER_URL = 'https://ezlmportaldc1f.adp.com/ezLaborManagerNetRedirect/MAPortalStart.aspx?ISIClientID='

    def __init__(self, username, password, download_path=None, isi_client_id=None):
        self.username = username
        self.password = password
        self.download_path = download_path
        self.isi_client_id = isi_client_id

        self.driver = self.driver_init()

        self.log_in()

    def driver_init(self):
        # Sets Firefox options; browser will run 'headless' (disabled GUI).
        options = webdriver.FirefoxOptions()
        options.headless = False

        # Sets Firefox profile; sets DL path, disables "Open or Save as" menu.
        fp = webdriver.FirefoxProfile()

        if self.download_path:
            fp.set_preference('browser.download.dir', self.download_path)
            fp.set_preference('browser.download.folderList', 2)
        else:
            fp.set_preference('browser.download.folderList', 1)

        fp.set_preference('browser.download.manager.showWhenStarting', False)
        fp.set_preference('browser.helperApps.neverAsk.saveToDisk',
                          'text/html;'
                          'text/csv;'
                          'text/comma-separated-values;'
                          'application/octet-stream;'
                          'application/csv;'
                          'application/excel;'
                          'application/vnd.ms-excel;'
                          'application/vnd.msexcel')

        # Launches Firefox window controlled by "driver"
        driver = webdriver.Firefox(options=options, firefox_profile=fp)

        return driver

    def log_in(self):

        # Opens ADP login page
        self.driver.get(self.RESOURCE_LOGIN_URL)

        # Searches login page for form elements (username/password/submit),
        # but only after waiting (up to 20 seconds) for elements to load.
        username_field = WebDriverWait(self.driver, 20).until(
            conditions.presence_of_element_located((By.ID, 'user_id'))
        )
        password_field = self.driver.find_element_by_id('password')
        login_submit = self.driver.find_element_by_id('subBtn')

        # Types username & password from credentials.py
        username_field.clear()
        password_field.clear()
        username_field.send_keys(self.username)
        password_field.send_keys(self.password)

        # Submits login info
        login_submit.click()

    def download_timecard_csv(self, isi_client_id=None):

        isi_client_id = isi_client_id or self.isi_client_id

        assert isi_client_id, "No ISI Client ID found."

        # Loads URL for ezLaborManager
        self.driver.get(self.EZLABORMANAGER_URL + isi_client_id)

        # Clicks over to reports page (can only open in new tab)
        reports_button = WebDriverWait(self.driver, 20).until(
            conditions.presence_of_element_located(
                (By.ID, 'UI4_Banner1__ctl0_btnReports')
            )
        )

        reports_button.click()

        # Focuses second tab after waiting for up to 20 seconds for it to load.
        WebDriverWait(self.driver, 20).until(conditions.new_window_is_opened)
        self.driver.switch_to.window(self.driver.window_handles[1])

        # Clicks download button for timecard report.
        timecard_button = WebDriverWait(self.driver, 20).until(
            conditions.presence_of_element_located(
                (By.NAME, 'UI4:ctBody:grdMyReports:_ctl3:btnDownloadReport')
            )
        )
        timecard_button.click()

        # Focuses third tab after waiting for up to 20 seconds for it to load.
        WebDriverWait(self.driver, 20).until(conditions.new_window_is_opened)
        self.driver.switch_to.window(self.driver.window_handles[2])

        # Locates filename field and enters current datetime for download.
        filename_field = WebDriverWait(self.driver, 20).until(
            conditions.presence_of_element_located((By.ID, 'txt_fldFileName'))
        )
        filename_submit = self.driver.find_element_by_id('btnSubmit')

        timestamp = datetime.today().strftime('%Y-%m-%d-%H%M%S')

        filename_field.send_keys(timestamp)
        filename_submit.click()

        # ".part" files indicate that a file hasn't finished downloading.
        # This loop checks the download directory every second for the presence
        # of a .part file and will break if it disappears. Though it times out
        # if the download takes longer than 60 seconds.
        timeout = time.time() + 60
        file_path = self.download_path + '\\' + timestamp + '.csv'
        file_part_path = self.download_path + '\\' + timestamp + '.csv.part'

        while time.time() < timeout:
            if os.path.isfile(file_part_path):
                time.sleep(1)
                pass
            elif not os.path.isfile(file_path):
                time.sleep(1)
                pass
            else:
                break
        else:
            self.quit()
            assert False, "Download of file timed out."

        return file_path

    def close_all(self):
        for window in self.driver.window_handles:
            self.driver.switch_to.window(window)
            self.driver.close()

    def quit(self):
        self.driver.quit()
