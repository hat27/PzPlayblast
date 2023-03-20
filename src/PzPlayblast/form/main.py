#-*-coding: utf8-*-

import sys
import os
import pprint

task_directory = os.path.normpath(os.path.join(os.path.dirname(__file__), "../../../")) 
print(task_directory)

sys.path.append(task_directory)

from Qt import QtWidgets, QtCore
from puzzle2.Puzzle import Puzzle
from sticky.StickyProjectManager import StickyProjectManager
from sticky.Sticky import StickyConfig

class ProjectManager(StickyProjectManager):
    def __init__(self, *args, **kwargs):
        super(ProjectManager, self).__init__(*args, **kwargs)

        # fix to your location
        self.root_directory = "sample/env"

    # override this method to get your own config files
    def get_key_config_files(self):
        return super().get_key_config_files()

class PzPlayblast(QtWidgets.QMainWindow):
    TOOL_NAME = "PzPlayblast"
    VERSION = "0.0.1"
    def __init__(self, parent=None):
        super(PzPlayblast, self).__init__(parent)
        self.puzzle = Puzzle(name=self.TOOL_NAME, log_directory="sample/log", new=True)
        self.sticky = StickyConfig()

        layout = QtWidgets.QVBoxLayout()

        self.combo = QtWidgets.QComboBox()
        layout.addWidget(self.combo)

        for each in ["start", "end"]:
            setattr(self, "{}_spin".format(each), QtWidgets.QSpinBox())
            spin_box = getattr(self, "{}_spin".format(each))
            label = QtWidgets.QLabel(each)
            label.setMinimumWidth(50)
            label.setMaximumWidth(50)
            spin_box.setMinimum(-100000)
            spin_box.setMaximum(100000)
            spin_box.setAlignment(QtCore.Qt.AlignCenter)
            hlayout = QtWidgets.QHBoxLayout()
            hlayout.addWidget(label)
            hlayout.addWidget(spin_box)
            layout.addLayout(hlayout)

        btn = QtWidgets.QPushButton("playblast")
        layout.addWidget(btn)

        widget = QtWidgets.QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)
        
        btn.clicked.connect(self.btn_clicked)
        self.project = ProjectManager()
                            
        self.combo.addItems(self.get_projects())
        self.setWindowTitle("{} {}".format(self.TOOL_NAME, self.VERSION))
    
    def get_projects(self):
        projects = []
        for each in os.listdir(self.project.root_directory):
            path = os.path.join(self.project.root_directory, each)
            info, data = self.sticky.read(path)
            if info.get("type") == "project":
                projects.append(".".join(each.split(".")[:-2]))
        projects.sort()
        return projects

    def btn_clicked(self):
        project_name = self.combo.currentText()
        self.project.set(project_name, tool_name=self.TOOL_NAME)
        file_path = "somewhere/work/shots/ep01/s01/c01/ep01_s01_c01_anim.ma"
        playblast_template = self.project.config["shot"].get("template", {}).get("playblast")
        main_template = self.project.config["shot"]["template"]["main"]

        if playblast_template and main_template:
            fields = self.project.field_value_generator.get_field_value(main_template, file_path)
            output_path = self.project.field_value_generator.generate(playblast_template, fields)
        else:
            fields = {}
            output_path = False

        data = {
            "common": {
                     "width": self.project.config["general"]["resolution"]["width"], 
                     "height": self.project.config["general"]["resolution"]["height"], 
                     "fps": self.project.config["general"]["fps"], 
                     "file_path": file_path, 
                     "fields": fields, 
                     "project_name": project_name
                     }, 
            "main": {"start_frame": self.start_spin.value(), 
                     "end_frame": self.end_spin.value()}
        }
        if output_path:
            data["main"]["output_path"] = output_path

        print("")
        print("run process: {}".format(project_name))
        for config in self.project.config_files:
            print("depend file: {}".format(config))
        print("")
        pprint.pprint(self.project.config["puzzle"]["playblast"])
        print("")
        self.puzzle.play(self.project.config["puzzle"]["playblast"], data)
        message = []
        error = False
        for log in self.puzzle.logger.details.get_all():
            print(log)
            if "details" in log:
                message.extend(log["details"])
            else:
                message.append(log["header"])
            if log["return_code"] > 0:
                error = True
        if error:
            QtWidgets.QMessageBox.warning(self, "info", "\n".join(message), QtWidgets.QMessageBox.Ok)
        else:
            QtWidgets.QMessageBox.information(self, "info", "\n".join(message), QtWidgets.QMessageBox.Ok)
    
    def is_opened(self):
        return True

if __name__ == "__main__":
    try:
        app = QtWidgets.QApplication(sys.argv)
    except:
        pass
    main = PzPlayblast()
    main.show()
    try:
        sys.exit(app.exec_())
    except:
        pass

