#!/usr/bin/env python3

from falconpy import HostGroup,Hosts
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import requests
import time
import sys

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

class Window(QWidget):

    def __init__(self,parent=None):

        super(Window,self).__init__(parent)

        QWidget.__init__(self)
        QLabel.__init__(self)

        # Start Main Window Configuration #

        self.setWindowFlags(Qt.Window)
        self.setWindowTitle('CrowdStrike Containment Tool')
        self.setGeometry(400,100,400,800)
        self.setStyleSheet("border: 5px solid #e80229; border-radius: 5px; background-color: black;")
        self.setAttribute(Qt.WA_StyledBackground)

        # End Main Window Configuration #

        # Logo #

        self.img_label = QLabel(self)
        self.img_label.setStyleSheet("height: 100px; width: 100px; border: none;")
        self.img_label.setAlignment(Qt.AlignCenter)
        self.pixmap    = QPixmap("logo.png")
        self.img_label.setPixmap(self.pixmap)

        # End Logo Configuration #

        # Define Widgets #
    
        self.client_id_field = QLineEdit()                                          
        self.client_id_field.setPlaceholderText("(CrowdStrike API Account Client ID)")
        self.client_id_field.setStyleSheet("height: 35px; margin-top: 25px; background-color: grey; color: black; border: 2px solid #e80229; border-radius: 10px; font-style: bold; font-size: 16px; font-family: Arial")
        self.client_id_field.setAlignment(Qt.AlignCenter)

        self.client_secret_field = QLineEdit()                                          
        self.client_secret_field.setPlaceholderText("(CrowdStrike API Account Client Secret Key)")
        self.client_secret_field.setStyleSheet("height: 35px; margin-top: 5px; background-color: grey; color: black; border: 2px solid #e80229; border-radius: 10px; font-style: bold; font-size: 16px; font-family: Arial")
        self.client_secret_field.setAlignment(Qt.AlignCenter)

        self.initialize_button = QPushButton("Initialize", self)
        self.initialize_button.setGeometry(100,100,600,400)
        self.initialize_button.setStyleSheet("margin-top: 5px; height: 35px; background-color: grey; color: black; border: 2px solid #e80229; border-radius: 10px; font-style: bold; font-size: 18px; font-family: Arial")

        self.sensor_combo_box  = QComboBox()
        self.sensor_combo_box.setStyleSheet("margin-top: 10px; height: 35px; width: 35px; background-color: grey; color: black; border: 2px solid #e80229; border-radius: 5px; font-style: bold; font-size: 18px; font-family: Arial")
        self.sensor_combo_box.setCurrentIndex(0)

        self.host_group_combo_box = QComboBox()
        self.host_group_combo_box.setStyleSheet("margin-top: 10px; height: 35px; background-color: grey; color: ; border: 2px solid #e80229; border-radius: 5px; font-style: bold; text-align: center; font-size: 18px; font-family: Arial")
        self.host_group_combo_box.setCurrentIndex(0)

        self.isolate_host_button = QPushButton("Contain Host", self)
        self.isolate_host_button.setGeometry(100,100,600,400)
        self.isolate_host_button.setStyleSheet("margin-top: 5px; height: 35px; background-color: grey; color: black; border: 2px solid #e80229; border-radius: 10px; font-style: bold; font-size: 18px; font-family: Arial")

        self.isolate_host_group = QPushButton("Contain Host Group", self)
        self.isolate_host_group.setGeometry(100,100,600,400)
        self.isolate_host_group.setStyleSheet("margin-top: 5px; height: 35px; background-color: grey; color: black; border: 2px solid #e80229; border-radius: 10px; font-style: bold; font-size: 18px; font-family: Arial")

        self.lift_host_ctn = QPushButton("Lift Host Containment", self)
        self.lift_host_ctn.setGeometry(100,100,600,400)
        self.lift_host_ctn.setStyleSheet("margin-top: 5px; height: 35px; background-color: grey; color: black; border: 2px solid #e80229; border-radius: 10px; font-style: bold; font-size: 18px; font-family: Arial")

        self.lift_host_group_ctn = QPushButton("Lift Group Containment", self)
        self.lift_host_group_ctn.setGeometry(100,100,600,400)
        self.lift_host_group_ctn.setStyleSheet("margin-top: 5px; height: 35px; background-color: grey; color: black; border: 2px solid #e80229; border-radius: 10px; font-style: bold; font-size: 18px; font-family: Arial")

        self.output_window = QPlainTextEdit("")
        self.output_window.setStyleSheet("background-color: grey; color: black; border: 2px solid black; border-radius: 10px; font-style: bold; font-size: 16px; font-family: Arial")
        self.output_window.resize(100,100)
        self.output_window.ensureCursorVisible()
        self.output_window.insertPlainText("Enter your API account authentication data and press the initialize button. \n")

        # End Widget Definition #

        # Add Form Components #

        main_layout                       = QFormLayout()
        self.vert_logo_box                = QVBoxLayout()
        self.vert_params_box              = QVBoxLayout()
        self.vert_cbox_box                = QVBoxLayout()
        self.horiz_contain_button_box     = QHBoxLayout()
        self.horiz_lift_ctn_button_box    = QHBoxLayout()
        self.vert_text_box                = QVBoxLayout()

        # End Form Component Addition #

        # Connect buttons to methods #

        self.initialize_button.clicked.connect(self.Initialize)
        self.isolate_host_button.clicked.connect(self.ContainHost)
        self.isolate_host_group.clicked.connect(self.ContainHostGroup)
        self.lift_host_ctn.clicked.connect(self.LiftHostContainment)
        self.lift_host_group_ctn.clicked.connect(self.LiftHostGroupContainment)

        # End button method connections #

        # Add widgets to form fields #

        self.vert_logo_box.addWidget(self.img_label)

        self.vert_params_box.addWidget(self.client_id_field)
        self.vert_params_box.addWidget(self.client_secret_field)
        self.vert_params_box.addWidget(self.initialize_button)

        self.vert_cbox_box.addWidget(self.sensor_combo_box)
        self.vert_cbox_box.addWidget(self.host_group_combo_box)

        self.horiz_contain_button_box.addWidget(self.isolate_host_button)
        self.horiz_contain_button_box.addWidget(self.isolate_host_group)

        self.horiz_lift_ctn_button_box.addWidget(self.lift_host_ctn)
        self.horiz_lift_ctn_button_box.addWidget(self.lift_host_group_ctn)

        self.vert_text_box.addWidget(self.output_window)

        main_layout.addRow(self.vert_logo_box)
        main_layout.addRow(self.vert_params_box)
        main_layout.addRow(self.vert_cbox_box)
        main_layout.addRow(self.horiz_contain_button_box)
        main_layout.addRow(self.horiz_lift_ctn_button_box)
        main_layout.addRow(self.vert_text_box)

        self.setLayout(main_layout)
        self.setFocus()

    def QueryHostGroups(self):
        response = self.falcon_host_group.query_host_groups()
        host_group_ids = response['body']['resources']
        return host_group_ids
    
    def QueryHostIDs(self):
        response = self.falcon_hosts.query_devices_by_filter(limit=5000)
        host_ids = response['body']['resources']
        return host_ids

    def GetHostGroups(self):
        host_group_ids = self.QueryHostGroups()
        response    = self.falcon_host_group.get_host_groups(ids=host_group_ids)
        host_groups = response['body']['resources']
        return host_groups
    
    def GetHostGroupMembers(self,host_group_id):
        response      = self.falcon_host_group.query_combined_group_members(id=host_group_id)
        group_memebrs = response['body']['resources']
        return group_memebrs

    def GetHosts(self,hosts):
        response = self.falcon_hosts.get_device_details(ids=hosts)
        devices  = response['body']['resources']
        return devices
    
    def ContainHost(self):
        current_host    = self.sensor_combo_box.currentText()
        current_index   = self.sensor_combo_box.currentIndex()
        current_host    = self.all_hosts[current_index]
        current_host_id = current_host['device_id']
        contain_host = self.falcon_hosts.PerformActionV2(action_name="contain",ids=current_host_id)
        status_code  = contain_host['status_code']
        if(status_code == 202):
            self.output_window.insertPlainText("Successfully contained: {0} \n".format(current_host['hostname']))
        else:
            self.output_window.insertPlainText("Failed to contain: {0} \n".format(current_host['hostname']))
    
    def ContainHostGroup(self):
        current_host_group_index = self.host_group_combo_box.currentIndex()
        current_host_group       = self.host_groups[current_host_group_index]
        host_group_members       = self.GetHostGroupMembers(current_host_group['id'])
        self.output_window.insertPlainText("Containing the members of host group: {0} \n".format(current_host_group['name']))
        for host in host_group_members:
            contain_host = self.falcon_hosts.PerformActionV2(action_name="contain",ids=host['device_id'])
            status_code  = contain_host['status_code']
            if(status_code == 202):
                self.output_window.insertPlainText("Successfully isolated {0} \n".format(host['hostname']))
            else:
                self.output_window.insertPlainText("Failed to isolate {0} \n".format(host['hostname']))

    def LiftHostContainment(self):
        current_host    = self.sensor_combo_box.currentText()
        current_index   = self.sensor_combo_box.currentIndex()
        current_host    = self.all_hosts[current_index]
        current_host_id = current_host['device_id']
        lift_host_containment = self.falcon_hosts.PerformActionV2(action_name="lift_containment",ids=current_host_id)
        status_code           = lift_host_containment['status_code']
        if(status_code == 202):
            self.output_window.insertPlainText("Lifted containment on: {0} \n".format(current_host['hostname']))
        else:
            self.output_window.insertPlainText("Failed to lift containment on: {0} \n".format(current_host['hostname']))
    
    def LiftHostGroupContainment(self):
        current_host_group_index = self.host_group_combo_box.currentIndex()
        current_host_group       = self.host_groups[current_host_group_index]
        host_group_members       = self.GetHostGroupMembers(current_host_group['id'])
        self.output_window.insertPlainText("Lifting containment for the members of host group: {0} \n".format(current_host_group['name']))
        for host in host_group_members:
            lift_host_containment = self.falcon_hosts.PerformActionV2(action_name="lift_containment",ids=host['device_id'])
            status_code           = lift_host_containment['status_code']
            if(status_code == 202):
                self.output_window.insertPlainText("Lifted containment on: {0} \n".format(host['hostname']))
            else:
                self.output_window.insertPlainText("Failed to lift containment on: {0} \n".format(host['hostname']))
        
    def Initialize(self):

        self.client_id         = self.client_id_field.text()
        self.client_secret_id  = self.client_secret_field.text()

        self.output_window.insertPlainText("Initializing...\n")

        self.falcon_host_group = HostGroup(
                                            client_id     = self.client_id,
                                            client_secret = self.client_secret_id
                                          )
        self.falcon_hosts      = Hosts(
                                        client_id     = self.client_id,
                                        client_secret = self.client_secret_id
                                      )
        try:
            self.host_ids          = self.QueryHostIDs()
            self.all_hosts         = self.GetHosts(self.host_ids)
            self.host_groups       = self.GetHostGroups()
            for host in self.all_hosts:
                self.sensor_combo_box.addItem(host['hostname'])
            for group in self.host_groups:
                self.host_group_combo_box.addItem(group['name'])
            self.output_window.insertPlainText("Finished collecting host and host group data \n")
            time.sleep(3)
            self.output_window.clear()
        except Exception as e:
            self.output_window.insertPlainText("Failed to collect hosts and host groups: {0}\n".format(e))
            time.sleep(3)
            sys.exit()        

if(__name__ == '__main__'):
    app    = QApplication(sys.argv)
    screen = Window()
    screen.show()
    sys.exit(app.exec_())