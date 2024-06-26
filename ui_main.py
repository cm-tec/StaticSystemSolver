# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main.ui'
##
## Created by: Qt User Interface Compiler version 6.6.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QCheckBox, QComboBox,
    QDoubleSpinBox, QGridLayout, QGroupBox, QHBoxLayout,
    QHeaderView, QLineEdit, QMainWindow, QPushButton,
    QSizePolicy, QSpacerItem, QSpinBox, QStackedWidget,
    QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget)
import resource_rc

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1523, 939)
        palette = QPalette()
        brush = QBrush(QColor(0, 0, 0, 255))
        brush.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Active, QPalette.WindowText, brush)
        brush1 = QBrush(QColor(255, 255, 255, 255))
        brush1.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Active, QPalette.Button, brush1)
        palette.setBrush(QPalette.Active, QPalette.Light, brush1)
        palette.setBrush(QPalette.Active, QPalette.Midlight, brush1)
        brush2 = QBrush(QColor(127, 127, 127, 255))
        brush2.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Active, QPalette.Dark, brush2)
        brush3 = QBrush(QColor(170, 170, 170, 255))
        brush3.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Active, QPalette.Mid, brush3)
        palette.setBrush(QPalette.Active, QPalette.Text, brush)
        palette.setBrush(QPalette.Active, QPalette.BrightText, brush1)
        palette.setBrush(QPalette.Active, QPalette.ButtonText, brush)
        palette.setBrush(QPalette.Active, QPalette.Base, brush1)
        palette.setBrush(QPalette.Active, QPalette.Window, brush1)
        palette.setBrush(QPalette.Active, QPalette.Shadow, brush)
        palette.setBrush(QPalette.Active, QPalette.AlternateBase, brush1)
        brush4 = QBrush(QColor(255, 255, 220, 255))
        brush4.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Active, QPalette.ToolTipBase, brush4)
        palette.setBrush(QPalette.Active, QPalette.ToolTipText, brush)
        brush5 = QBrush(QColor(0, 0, 0, 128))
        brush5.setStyle(Qt.SolidPattern)
#if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        palette.setBrush(QPalette.Active, QPalette.PlaceholderText, brush5)
#endif
        palette.setBrush(QPalette.Inactive, QPalette.WindowText, brush)
        palette.setBrush(QPalette.Inactive, QPalette.Button, brush1)
        palette.setBrush(QPalette.Inactive, QPalette.Light, brush1)
        palette.setBrush(QPalette.Inactive, QPalette.Midlight, brush1)
        palette.setBrush(QPalette.Inactive, QPalette.Dark, brush2)
        palette.setBrush(QPalette.Inactive, QPalette.Mid, brush3)
        palette.setBrush(QPalette.Inactive, QPalette.Text, brush)
        palette.setBrush(QPalette.Inactive, QPalette.BrightText, brush1)
        palette.setBrush(QPalette.Inactive, QPalette.ButtonText, brush)
        palette.setBrush(QPalette.Inactive, QPalette.Base, brush1)
        palette.setBrush(QPalette.Inactive, QPalette.Window, brush1)
        palette.setBrush(QPalette.Inactive, QPalette.Shadow, brush)
        palette.setBrush(QPalette.Inactive, QPalette.AlternateBase, brush1)
        palette.setBrush(QPalette.Inactive, QPalette.ToolTipBase, brush4)
        palette.setBrush(QPalette.Inactive, QPalette.ToolTipText, brush)
#if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        palette.setBrush(QPalette.Inactive, QPalette.PlaceholderText, brush5)
#endif
        palette.setBrush(QPalette.Disabled, QPalette.WindowText, brush2)
        palette.setBrush(QPalette.Disabled, QPalette.Button, brush1)
        palette.setBrush(QPalette.Disabled, QPalette.Light, brush1)
        palette.setBrush(QPalette.Disabled, QPalette.Midlight, brush1)
        palette.setBrush(QPalette.Disabled, QPalette.Dark, brush2)
        palette.setBrush(QPalette.Disabled, QPalette.Mid, brush3)
        palette.setBrush(QPalette.Disabled, QPalette.Text, brush2)
        palette.setBrush(QPalette.Disabled, QPalette.BrightText, brush1)
        palette.setBrush(QPalette.Disabled, QPalette.ButtonText, brush2)
        palette.setBrush(QPalette.Disabled, QPalette.Base, brush1)
        palette.setBrush(QPalette.Disabled, QPalette.Window, brush1)
        palette.setBrush(QPalette.Disabled, QPalette.Shadow, brush)
        palette.setBrush(QPalette.Disabled, QPalette.AlternateBase, brush1)
        palette.setBrush(QPalette.Disabled, QPalette.ToolTipBase, brush4)
        palette.setBrush(QPalette.Disabled, QPalette.ToolTipText, brush)
#if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        palette.setBrush(QPalette.Disabled, QPalette.PlaceholderText, brush5)
#endif
        MainWindow.setPalette(palette)
        icon = QIcon()
        icon.addFile(u":/newPrefix/logo@2x.png", QSize(), QIcon.Normal, QIcon.Off)
        MainWindow.setWindowIcon(icon)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.horizontalLayout = QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.widget = QWidget(self.centralwidget)
        self.widget.setObjectName(u"widget")
        self.horizontalLayout_2 = QHBoxLayout(self.widget)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.groupBox = QGroupBox(self.widget)
        self.groupBox.setObjectName(u"groupBox")
        self.groupBox.setMaximumSize(QSize(16777215, 16777215))
        self.groupBox.setStyleSheet(u"")
        self.gridLayout_2 = QGridLayout(self.groupBox)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_2.setHorizontalSpacing(0)
        self.gridLayout_2.setVerticalSpacing(1)
        self.gridLayout_2.setContentsMargins(-1, 3, -1, 3)
        self.verticalSpacer_6 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.gridLayout_2.addItem(self.verticalSpacer_6, 7, 0, 1, 1)

        self.pushbutton_displacements = QPushButton(self.groupBox)
        self.pushbutton_displacements.setObjectName(u"pushbutton_displacements")
        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushbutton_displacements.sizePolicy().hasHeightForWidth())
        self.pushbutton_displacements.setSizePolicy(sizePolicy)
        font = QFont()
        font.setBold(True)
        font.setItalic(False)
        self.pushbutton_displacements.setFont(font)
        self.pushbutton_displacements.setCursor(QCursor(Qt.PointingHandCursor))
        self.pushbutton_displacements.setStyleSheet(u"QPushButton {\n"
"	background-color: rgb(255, 152, 93);\n"
"    border-style: outset;\n"
"    border-width: 2px;\n"
"    border-radius: 10px;\n"
"    border-color: beige;\n"
"    font: bold 14px;\n"
"    min-width: 10em;\n"
"}\n"
"QPushButton:hover {\n"
"	background-color: rgb(255, 135, 55);\n"
"    border-style: inset;\n"
"}")

        self.gridLayout_2.addWidget(self.pushbutton_displacements, 3, 0, 1, 1)

        self.verticalSpacer_7 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.gridLayout_2.addItem(self.verticalSpacer_7, 2, 0, 1, 1)

        self.pushbutton_internal_forces = QPushButton(self.groupBox)
        self.pushbutton_internal_forces.setObjectName(u"pushbutton_internal_forces")
        sizePolicy.setHeightForWidth(self.pushbutton_internal_forces.sizePolicy().hasHeightForWidth())
        self.pushbutton_internal_forces.setSizePolicy(sizePolicy)
        self.pushbutton_internal_forces.setFont(font)
        self.pushbutton_internal_forces.setCursor(QCursor(Qt.PointingHandCursor))
        self.pushbutton_internal_forces.setStyleSheet(u"QPushButton {\n"
"	background-color: rgb(255, 152, 93);\n"
"    border-style: outset;\n"
"    border-width: 2px;\n"
"    border-radius: 10px;\n"
"    border-color: beige;\n"
"    font: bold 14px;\n"
"    min-width: 10em;\n"
"}\n"
"QPushButton:hover {\n"
"	background-color: rgb(255, 135, 55);\n"
"    border-style: inset;\n"
"}")

        self.gridLayout_2.addWidget(self.pushbutton_internal_forces, 4, 0, 1, 1)

        self.pushbutton_direct_sensa = QPushButton(self.groupBox)
        self.pushbutton_direct_sensa.setObjectName(u"pushbutton_direct_sensa")
        sizePolicy.setHeightForWidth(self.pushbutton_direct_sensa.sizePolicy().hasHeightForWidth())
        self.pushbutton_direct_sensa.setSizePolicy(sizePolicy)
        self.pushbutton_direct_sensa.setFont(font)
        self.pushbutton_direct_sensa.setCursor(QCursor(Qt.PointingHandCursor))
        self.pushbutton_direct_sensa.setStyleSheet(u"QPushButton {\n"
"	background-color: rgb(255, 152, 93);\n"
"    border-style: outset;\n"
"    border-width: 2px;\n"
"    border-radius: 10px;\n"
"    border-color: beige;\n"
"    font: bold 14px;\n"
"    min-width: 10em;\n"
"}\n"
"QPushButton:hover {\n"
"	background-color: rgb(255, 135, 55);\n"
"    border-style: inset;\n"
"}")

        self.gridLayout_2.addWidget(self.pushbutton_direct_sensa, 5, 0, 1, 1)

        self.pushbutton_members = QPushButton(self.groupBox)
        self.pushbutton_members.setObjectName(u"pushbutton_members")
        sizePolicy.setHeightForWidth(self.pushbutton_members.sizePolicy().hasHeightForWidth())
        self.pushbutton_members.setSizePolicy(sizePolicy)
        self.pushbutton_members.setFont(font)
        self.pushbutton_members.setCursor(QCursor(Qt.PointingHandCursor))
        self.pushbutton_members.setStyleSheet(u"QPushButton {\n"
"	background-color: rgb(135, 177, 255);\n"
"    border-style: outset;\n"
"    border-width: 2px;\n"
"    border-radius: 10px;\n"
"    border-color: beige;\n"
"    font: bold 14px;\n"
"    min-width: 10em;\n"
"}\n"
"QPushButton:hover {\n"
"	background-color: rgb(55, 162, 255);\n"
"    border-style: inset;\n"
"}\n"
"")

        self.gridLayout_2.addWidget(self.pushbutton_members, 1, 0, 1, 1)

        self.pushbutton_adjoint_sensa = QPushButton(self.groupBox)
        self.pushbutton_adjoint_sensa.setObjectName(u"pushbutton_adjoint_sensa")
        sizePolicy.setHeightForWidth(self.pushbutton_adjoint_sensa.sizePolicy().hasHeightForWidth())
        self.pushbutton_adjoint_sensa.setSizePolicy(sizePolicy)
        self.pushbutton_adjoint_sensa.setFont(font)
        self.pushbutton_adjoint_sensa.setCursor(QCursor(Qt.PointingHandCursor))
        self.pushbutton_adjoint_sensa.setStyleSheet(u"QPushButton {\n"
"	background-color: rgb(255, 152, 93);\n"
"    border-style: outset;\n"
"    border-width: 2px;\n"
"    border-radius: 10px;\n"
"    border-color: beige;\n"
"    font: bold 14px;\n"
"    min-width: 10em;\n"
"}\n"
"QPushButton:hover {\n"
"	background-color: rgb(255, 135, 55);\n"
"    border-style: inset;\n"
"}")

        self.gridLayout_2.addWidget(self.pushbutton_adjoint_sensa, 6, 0, 1, 1)

        self.pushbutton_nodes = QPushButton(self.groupBox)
        self.pushbutton_nodes.setObjectName(u"pushbutton_nodes")
        sizePolicy.setHeightForWidth(self.pushbutton_nodes.sizePolicy().hasHeightForWidth())
        self.pushbutton_nodes.setSizePolicy(sizePolicy)
        self.pushbutton_nodes.setFont(font)
        self.pushbutton_nodes.setCursor(QCursor(Qt.PointingHandCursor))
        self.pushbutton_nodes.setStyleSheet(u"QPushButton {\n"
"	background-color: rgb(135, 177, 255);\n"
"    border-style: outset;\n"
"    border-width: 2px;\n"
"    border-radius: 10px;\n"
"    border-color: beige;\n"
"    font: bold 14px;\n"
"    min-width: 10em;\n"
"}\n"
"QPushButton:hover {\n"
"	background-color: rgb(55, 162, 255);\n"
"    border-style: inset;\n"
"}\n"
"")
        self.pushbutton_nodes.setAutoDefault(False)
        self.pushbutton_nodes.setFlat(False)

        self.gridLayout_2.addWidget(self.pushbutton_nodes, 0, 0, 1, 1)


        self.horizontalLayout_2.addWidget(self.groupBox)

        self.stackedWidget = QStackedWidget(self.widget)
        self.stackedWidget.setObjectName(u"stackedWidget")
        self.stackedWidget.setEnabled(True)
        self.stackedWidget.setStyleSheet(u"")
        self.page_geometry = QWidget()
        self.page_geometry.setObjectName(u"page_geometry")
        self.gridLayout_8 = QGridLayout(self.page_geometry)
        self.gridLayout_8.setObjectName(u"gridLayout_8")
        self.graphLayout_geometry = QVBoxLayout()
        self.graphLayout_geometry.setSpacing(0)
        self.graphLayout_geometry.setObjectName(u"graphLayout_geometry")
        self.graphLayout_geometry.setContentsMargins(-1, -1, -1, 0)

        self.gridLayout_8.addLayout(self.graphLayout_geometry, 1, 1, 1, 2)

        self.stackedWidget_2 = QStackedWidget(self.page_geometry)
        self.stackedWidget_2.setObjectName(u"stackedWidget_2")
        self.stackedWidget_2.setEnabled(True)
        sizePolicy1 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.stackedWidget_2.sizePolicy().hasHeightForWidth())
        self.stackedWidget_2.setSizePolicy(sizePolicy1)
        self.stackedWidget_2.setMaximumSize(QSize(16777215, 300))
        self.page_node = QWidget()
        self.page_node.setObjectName(u"page_node")
        self.gridLayout_1 = QGridLayout(self.page_node)
        self.gridLayout_1.setObjectName(u"gridLayout_1")
        self.gridLayout_1.setContentsMargins(0, 5, -1, -1)
        self.spinBox_nodes = QSpinBox(self.page_node)
        self.spinBox_nodes.setObjectName(u"spinBox_nodes")
        self.spinBox_nodes.setMinimumSize(QSize(55, 30))
        self.spinBox_nodes.setMaximumSize(QSize(50, 16777215))
        self.spinBox_nodes.setAlignment(Qt.AlignCenter)
        self.spinBox_nodes.setMinimum(2)
        self.spinBox_nodes.setMaximum(1000)
        self.spinBox_nodes.setValue(2)

        self.gridLayout_1.addWidget(self.spinBox_nodes, 0, 0, 1, 1)

        self.tableWidget_nodes = QTableWidget(self.page_node)
        if (self.tableWidget_nodes.columnCount() < 3):
            self.tableWidget_nodes.setColumnCount(3)
        __qtablewidgetitem = QTableWidgetItem()
        self.tableWidget_nodes.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.tableWidget_nodes.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.tableWidget_nodes.setHorizontalHeaderItem(2, __qtablewidgetitem2)
        if (self.tableWidget_nodes.rowCount() < 2):
            self.tableWidget_nodes.setRowCount(2)
        self.tableWidget_nodes.setObjectName(u"tableWidget_nodes")
        self.tableWidget_nodes.setAlternatingRowColors(True)
        self.tableWidget_nodes.setTextElideMode(Qt.ElideRight)

        self.gridLayout_1.addWidget(self.tableWidget_nodes, 1, 0, 1, 3)

        self.update_nodes = QPushButton(self.page_node)
        self.update_nodes.setObjectName(u"update_nodes")
        sizePolicy2 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.update_nodes.sizePolicy().hasHeightForWidth())
        self.update_nodes.setSizePolicy(sizePolicy2)
        self.update_nodes.setMinimumSize(QSize(23, 20))
        self.update_nodes.setMaximumSize(QSize(80, 16777215))
        self.update_nodes.setCursor(QCursor(Qt.PointingHandCursor))
        self.update_nodes.setStyleSheet(u"QPushButton {\n"
"	background-color: rgb(123, 193, 255);\n"
"    border-style: outset;\n"
"    border-width: 2px;\n"
"    border-radius: 10px;\n"
"    border-color: beige;\n"
"    font: bold 14px;\n"
"    min-width: 1em;\n"
"    padding: 1px;\n"
"}\n"
"QPushButton:hover {\n"
"	background-color: rgb(85, 162, 255);\n"
"    border-style: inset;\n"
"}\n"
"")

        self.gridLayout_1.addWidget(self.update_nodes, 0, 1, 1, 1)

        self.stackedWidget_2.addWidget(self.page_node)
        self.page_element = QWidget()
        self.page_element.setObjectName(u"page_element")
        self.gridLayout_3 = QGridLayout(self.page_element)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.gridLayout_3.setContentsMargins(0, 5, -1, -1)
        self.update_elements = QPushButton(self.page_element)
        self.update_elements.setObjectName(u"update_elements")
        sizePolicy2.setHeightForWidth(self.update_elements.sizePolicy().hasHeightForWidth())
        self.update_elements.setSizePolicy(sizePolicy2)
        self.update_elements.setMinimumSize(QSize(23, 20))
        self.update_elements.setMaximumSize(QSize(80, 16777215))
        self.update_elements.setCursor(QCursor(Qt.PointingHandCursor))
        self.update_elements.setStyleSheet(u"QPushButton {\n"
"	background-color: rgb(123, 193, 255);\n"
"    border-style: outset;\n"
"    border-width: 2px;\n"
"    border-radius: 10px;\n"
"    border-color: beige;\n"
"    font: bold 14px;\n"
"    min-width: 1em;\n"
"    padding: 1px;\n"
"}\n"
"QPushButton:hover {\n"
"	background-color: rgb(85, 162, 255);\n"
"    border-style: inset;\n"
"}\n"
"")

        self.gridLayout_3.addWidget(self.update_elements, 0, 1, 1, 1)

        self.spinBox_elements = QSpinBox(self.page_element)
        self.spinBox_elements.setObjectName(u"spinBox_elements")
        self.spinBox_elements.setMinimumSize(QSize(55, 30))
        self.spinBox_elements.setMaximumSize(QSize(50, 16777215))
        self.spinBox_elements.setAlignment(Qt.AlignCenter)
        self.spinBox_elements.setMinimum(1)
        self.spinBox_elements.setMaximum(1000)
        self.spinBox_elements.setValue(1)

        self.gridLayout_3.addWidget(self.spinBox_elements, 0, 0, 1, 1)

        self.tableWidget_elements = QTableWidget(self.page_element)
        if (self.tableWidget_elements.columnCount() < 14):
            self.tableWidget_elements.setColumnCount(14)
        __qtablewidgetitem3 = QTableWidgetItem()
        self.tableWidget_elements.setHorizontalHeaderItem(0, __qtablewidgetitem3)
        __qtablewidgetitem4 = QTableWidgetItem()
        self.tableWidget_elements.setHorizontalHeaderItem(1, __qtablewidgetitem4)
        __qtablewidgetitem5 = QTableWidgetItem()
        self.tableWidget_elements.setHorizontalHeaderItem(2, __qtablewidgetitem5)
        __qtablewidgetitem6 = QTableWidgetItem()
        self.tableWidget_elements.setHorizontalHeaderItem(3, __qtablewidgetitem6)
        __qtablewidgetitem7 = QTableWidgetItem()
        self.tableWidget_elements.setHorizontalHeaderItem(4, __qtablewidgetitem7)
        __qtablewidgetitem8 = QTableWidgetItem()
        self.tableWidget_elements.setHorizontalHeaderItem(5, __qtablewidgetitem8)
        __qtablewidgetitem9 = QTableWidgetItem()
        self.tableWidget_elements.setHorizontalHeaderItem(6, __qtablewidgetitem9)
        __qtablewidgetitem10 = QTableWidgetItem()
        self.tableWidget_elements.setHorizontalHeaderItem(7, __qtablewidgetitem10)
        __qtablewidgetitem11 = QTableWidgetItem()
        self.tableWidget_elements.setHorizontalHeaderItem(8, __qtablewidgetitem11)
        __qtablewidgetitem12 = QTableWidgetItem()
        self.tableWidget_elements.setHorizontalHeaderItem(9, __qtablewidgetitem12)
        __qtablewidgetitem13 = QTableWidgetItem()
        self.tableWidget_elements.setHorizontalHeaderItem(10, __qtablewidgetitem13)
        __qtablewidgetitem14 = QTableWidgetItem()
        self.tableWidget_elements.setHorizontalHeaderItem(11, __qtablewidgetitem14)
        __qtablewidgetitem15 = QTableWidgetItem()
        self.tableWidget_elements.setHorizontalHeaderItem(12, __qtablewidgetitem15)
        __qtablewidgetitem16 = QTableWidgetItem()
        self.tableWidget_elements.setHorizontalHeaderItem(13, __qtablewidgetitem16)
        if (self.tableWidget_elements.rowCount() < 1):
            self.tableWidget_elements.setRowCount(1)
        __qtablewidgetitem17 = QTableWidgetItem()
        self.tableWidget_elements.setItem(0, 0, __qtablewidgetitem17)
        self.tableWidget_elements.setObjectName(u"tableWidget_elements")
        self.tableWidget_elements.setAlternatingRowColors(True)
        self.tableWidget_elements.setTextElideMode(Qt.ElideRight)
        self.tableWidget_elements.setRowCount(1)

        self.gridLayout_3.addWidget(self.tableWidget_elements, 1, 0, 1, 5)

        self.stackedWidget_2.addWidget(self.page_element)
        self.page_displacements = QWidget()
        self.page_displacements.setObjectName(u"page_displacements")
        self.displacements_gridLayout_4 = QGridLayout(self.page_displacements)
        self.displacements_gridLayout_4.setObjectName(u"displacements_gridLayout_4")
        self.displacements_gridLayout_4.setContentsMargins(0, 5, -1, -1)
        self.displacements_comboBox = QComboBox(self.page_displacements)
        self.displacements_comboBox.setObjectName(u"displacements_comboBox")
        self.displacements_comboBox.setEditable(False)

        self.displacements_gridLayout_4.addWidget(self.displacements_comboBox, 0, 0, 1, 1)

        self.container_displacements = QHBoxLayout()
        self.container_displacements.setObjectName(u"container_displacements")
        self.graphLayout_u = QVBoxLayout()
        self.graphLayout_u.setObjectName(u"graphLayout_u")

        self.container_displacements.addLayout(self.graphLayout_u)

        self.graphLayout_w = QVBoxLayout()
        self.graphLayout_w.setObjectName(u"graphLayout_w")

        self.container_displacements.addLayout(self.graphLayout_w)

        self.graphLayout_phi = QVBoxLayout()
        self.graphLayout_phi.setObjectName(u"graphLayout_phi")

        self.container_displacements.addLayout(self.graphLayout_phi)


        self.displacements_gridLayout_4.addLayout(self.container_displacements, 1, 0, 1, 1)

        self.stackedWidget_2.addWidget(self.page_displacements)
        self.page_internal_forces = QWidget()
        self.page_internal_forces.setObjectName(u"page_internal_forces")
        self.gridLayout_4 = QGridLayout(self.page_internal_forces)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.gridLayout_4.setContentsMargins(0, 5, -1, -1)
        self.internal_forces_comboBox = QComboBox(self.page_internal_forces)
        self.internal_forces_comboBox.setObjectName(u"internal_forces_comboBox")
        self.internal_forces_comboBox.setEditable(False)

        self.gridLayout_4.addWidget(self.internal_forces_comboBox, 0, 0, 1, 1)

        self.container_internal_forces = QHBoxLayout()
        self.container_internal_forces.setObjectName(u"container_internal_forces")
        self.graphLayout_normal = QVBoxLayout()
        self.graphLayout_normal.setObjectName(u"graphLayout_normal")

        self.container_internal_forces.addLayout(self.graphLayout_normal)

        self.graphLayout_shear = QVBoxLayout()
        self.graphLayout_shear.setObjectName(u"graphLayout_shear")

        self.container_internal_forces.addLayout(self.graphLayout_shear)

        self.graphLayout_moment = QVBoxLayout()
        self.graphLayout_moment.setObjectName(u"graphLayout_moment")

        self.container_internal_forces.addLayout(self.graphLayout_moment)


        self.gridLayout_4.addLayout(self.container_internal_forces, 1, 0, 1, 1)

        self.stackedWidget_2.addWidget(self.page_internal_forces)
        self.page_direct_sensitivity_analysis = QWidget()
        self.page_direct_sensitivity_analysis.setObjectName(u"page_direct_sensitivity_analysis")
        self.gridLayout_5 = QGridLayout(self.page_direct_sensitivity_analysis)
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.gridLayout_5.setContentsMargins(0, 5, -1, -1)
        self.direct_sensitivity_analysis_element_0_selection = QComboBox(self.page_direct_sensitivity_analysis)
        self.direct_sensitivity_analysis_element_0_selection.setObjectName(u"direct_sensitivity_analysis_element_0_selection")
        self.direct_sensitivity_analysis_element_0_selection.setEditable(False)

        self.gridLayout_5.addWidget(self.direct_sensitivity_analysis_element_0_selection, 0, 0, 1, 1)

        self.direct_sensitivity_analysis_parameter_selection = QComboBox(self.page_direct_sensitivity_analysis)
        self.direct_sensitivity_analysis_parameter_selection.setObjectName(u"direct_sensitivity_analysis_parameter_selection")
        self.direct_sensitivity_analysis_parameter_selection.setEditable(False)

        self.gridLayout_5.addWidget(self.direct_sensitivity_analysis_parameter_selection, 0, 1, 1, 1)

        self.direct_sensitivity_analysis_element_1_selection = QComboBox(self.page_direct_sensitivity_analysis)
        self.direct_sensitivity_analysis_element_1_selection.setObjectName(u"direct_sensitivity_analysis_element_1_selection")
        self.direct_sensitivity_analysis_element_1_selection.setEditable(False)

        self.gridLayout_5.addWidget(self.direct_sensitivity_analysis_element_1_selection, 0, 2, 1, 1)

        self.container_internal_forces_derived = QHBoxLayout()
        self.container_internal_forces_derived.setObjectName(u"container_internal_forces_derived")
        self.graphLayout_normal_derived = QVBoxLayout()
        self.graphLayout_normal_derived.setObjectName(u"graphLayout_normal_derived")

        self.container_internal_forces_derived.addLayout(self.graphLayout_normal_derived)

        self.graphLayout_shear_derived = QVBoxLayout()
        self.graphLayout_shear_derived.setObjectName(u"graphLayout_shear_derived")

        self.container_internal_forces_derived.addLayout(self.graphLayout_shear_derived)

        self.graphLayout_moment_derived = QVBoxLayout()
        self.graphLayout_moment_derived.setObjectName(u"graphLayout_moment_derived")

        self.container_internal_forces_derived.addLayout(self.graphLayout_moment_derived)


        self.gridLayout_5.addLayout(self.container_internal_forces_derived, 1, 0, 1, 3)

        self.stackedWidget_2.addWidget(self.page_direct_sensitivity_analysis)
        self.page_adjoint_sensitivity_analysis = QWidget()
        self.page_adjoint_sensitivity_analysis.setObjectName(u"page_adjoint_sensitivity_analysis")
        self.gridLayout_6 = QGridLayout(self.page_adjoint_sensitivity_analysis)
        self.gridLayout_6.setObjectName(u"gridLayout_6")
        self.gridLayout_6.setContentsMargins(0, 5, -1, -1)
        self.adjoint_sensitivity_analysis_element_0_selection = QComboBox(self.page_adjoint_sensitivity_analysis)
        self.adjoint_sensitivity_analysis_element_0_selection.setObjectName(u"adjoint_sensitivity_analysis_element_0_selection")
        self.adjoint_sensitivity_analysis_element_0_selection.setEditable(False)

        self.gridLayout_6.addWidget(self.adjoint_sensitivity_analysis_element_0_selection, 0, 0, 1, 1)

        self.adjoint_sensitivity_analysis_response_variable_selection = QComboBox(self.page_adjoint_sensitivity_analysis)
        self.adjoint_sensitivity_analysis_response_variable_selection.setObjectName(u"adjoint_sensitivity_analysis_response_variable_selection")
        self.adjoint_sensitivity_analysis_response_variable_selection.setEditable(False)

        self.gridLayout_6.addWidget(self.adjoint_sensitivity_analysis_response_variable_selection, 0, 1, 1, 1)

        self.adjoint_sensitivity_analysis_result_table = QTableWidget(self.page_adjoint_sensitivity_analysis)
        if (self.adjoint_sensitivity_analysis_result_table.columnCount() < 3):
            self.adjoint_sensitivity_analysis_result_table.setColumnCount(3)
        __qtablewidgetitem18 = QTableWidgetItem()
        self.adjoint_sensitivity_analysis_result_table.setHorizontalHeaderItem(0, __qtablewidgetitem18)
        __qtablewidgetitem19 = QTableWidgetItem()
        self.adjoint_sensitivity_analysis_result_table.setHorizontalHeaderItem(1, __qtablewidgetitem19)
        __qtablewidgetitem20 = QTableWidgetItem()
        self.adjoint_sensitivity_analysis_result_table.setHorizontalHeaderItem(2, __qtablewidgetitem20)
        self.adjoint_sensitivity_analysis_result_table.setObjectName(u"adjoint_sensitivity_analysis_result_table")
        self.adjoint_sensitivity_analysis_result_table.setEnabled(True)
        self.adjoint_sensitivity_analysis_result_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.adjoint_sensitivity_analysis_result_table.setAlternatingRowColors(True)
        self.adjoint_sensitivity_analysis_result_table.setTextElideMode(Qt.ElideRight)
        self.adjoint_sensitivity_analysis_result_table.setRowCount(0)

        self.gridLayout_6.addWidget(self.adjoint_sensitivity_analysis_result_table, 1, 0, 1, 2)

        self.stackedWidget_2.addWidget(self.page_adjoint_sensitivity_analysis)

        self.gridLayout_8.addWidget(self.stackedWidget_2, 2, 1, 1, 2)

        self.horizontalLayoutHeader = QHBoxLayout()
        self.horizontalLayoutHeader.setObjectName(u"horizontalLayoutHeader")
        self.spinBox_scale_factor = QDoubleSpinBox(self.page_geometry)
        self.spinBox_scale_factor.setObjectName(u"spinBox_scale_factor")
        self.spinBox_scale_factor.setMaximumSize(QSize(50, 16777215))
        self.spinBox_scale_factor.setSingleStep(0.100000000000000)
        self.spinBox_scale_factor.setValue(1.000000000000000)

        self.horizontalLayoutHeader.addWidget(self.spinBox_scale_factor)

        self.min_x = QLineEdit(self.page_geometry)
        self.min_x.setObjectName(u"min_x")
        self.min_x.setMaximumSize(QSize(100, 16777215))
        self.min_x.setAlignment(Qt.AlignCenter)

        self.horizontalLayoutHeader.addWidget(self.min_x)

        self.max_x = QLineEdit(self.page_geometry)
        self.max_x.setObjectName(u"max_x")
        self.max_x.setMaximumSize(QSize(100, 16777215))
        self.max_x.setAlignment(Qt.AlignCenter)

        self.horizontalLayoutHeader.addWidget(self.max_x)

        self.min_z = QLineEdit(self.page_geometry)
        self.min_z.setObjectName(u"min_z")
        self.min_z.setMaximumSize(QSize(100, 16777215))
        self.min_z.setAlignment(Qt.AlignCenter)

        self.horizontalLayoutHeader.addWidget(self.min_z)

        self.max_z = QLineEdit(self.page_geometry)
        self.max_z.setObjectName(u"max_z")
        self.max_z.setMaximumSize(QSize(100, 16777215))
        self.max_z.setAlignment(Qt.AlignCenter)

        self.horizontalLayoutHeader.addWidget(self.max_z)

        self.show_joints_and_supports = QCheckBox(self.page_geometry)
        self.show_joints_and_supports.setObjectName(u"show_joints_and_supports")
        self.show_joints_and_supports.setChecked(True)

        self.horizontalLayoutHeader.addWidget(self.show_joints_and_supports)

        self.show_loads = QCheckBox(self.page_geometry)
        self.show_loads.setObjectName(u"show_loads")
        self.show_loads.setChecked(True)

        self.horizontalLayoutHeader.addWidget(self.show_loads)

        self.show_reaction_forces = QCheckBox(self.page_geometry)
        self.show_reaction_forces.setObjectName(u"show_reaction_forces")
        self.show_reaction_forces.setChecked(True)

        self.horizontalLayoutHeader.addWidget(self.show_reaction_forces)

        self.show_element_ids = QCheckBox(self.page_geometry)
        self.show_element_ids.setObjectName(u"show_element_ids")
        self.show_element_ids.setChecked(True)

        self.horizontalLayoutHeader.addWidget(self.show_element_ids)

        self.element_line_width = QDoubleSpinBox(self.page_geometry)
        self.element_line_width.setObjectName(u"element_line_width")
        self.element_line_width.setMaximumSize(QSize(50, 16777215))
        self.element_line_width.setSingleStep(1.000000000000000)
        self.element_line_width.setValue(1.000000000000000)

        self.horizontalLayoutHeader.addWidget(self.element_line_width)


        self.gridLayout_8.addLayout(self.horizontalLayoutHeader, 0, 1, 1, 1)

        self.stackedWidget.addWidget(self.page_geometry)

        self.horizontalLayout_2.addWidget(self.stackedWidget)


        self.horizontalLayout.addWidget(self.widget)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        self.pushbutton_nodes.setDefault(False)
        self.stackedWidget.setCurrentIndex(0)
        self.stackedWidget_2.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Truss 101", None))
        self.groupBox.setTitle("")
        self.pushbutton_displacements.setText(QCoreApplication.translate("MainWindow", u"\n"
" Displacements\n"
"", None))
        self.pushbutton_internal_forces.setText(QCoreApplication.translate("MainWindow", u"\n"
" Internal Forces\n"
"", None))
        self.pushbutton_direct_sensa.setText(QCoreApplication.translate("MainWindow", u"\n"
" Direct Sensa\n"
"", None))
        self.pushbutton_members.setText(QCoreApplication.translate("MainWindow", u"\n"
" Members\n"
"", None))
        self.pushbutton_adjoint_sensa.setText(QCoreApplication.translate("MainWindow", u"\n"
" Adjoint Sensa\n"
"", None))
        self.pushbutton_nodes.setText(QCoreApplication.translate("MainWindow", u"\n"
" Nodes\n"
"", None))
        ___qtablewidgetitem = self.tableWidget_nodes.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("MainWindow", u"X", None));
        ___qtablewidgetitem1 = self.tableWidget_nodes.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("MainWindow", u"Z", None));
        ___qtablewidgetitem2 = self.tableWidget_nodes.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("MainWindow", u"Type", None));
        self.update_nodes.setText(QCoreApplication.translate("MainWindow", u"Update", None))
        self.update_elements.setText(QCoreApplication.translate("MainWindow", u"Update", None))
        ___qtablewidgetitem3 = self.tableWidget_elements.horizontalHeaderItem(0)
        ___qtablewidgetitem3.setText(QCoreApplication.translate("MainWindow", u"Node i", None));
        ___qtablewidgetitem4 = self.tableWidget_elements.horizontalHeaderItem(1)
        ___qtablewidgetitem4.setText(QCoreApplication.translate("MainWindow", u"Node k", None));
        ___qtablewidgetitem5 = self.tableWidget_elements.horizontalHeaderItem(2)
        ___qtablewidgetitem5.setText(QCoreApplication.translate("MainWindow", u"connection_type_i", None));
        ___qtablewidgetitem6 = self.tableWidget_elements.horizontalHeaderItem(3)
        ___qtablewidgetitem6.setText(QCoreApplication.translate("MainWindow", u"connection_type_k", None));
        ___qtablewidgetitem7 = self.tableWidget_elements.horizontalHeaderItem(4)
        ___qtablewidgetitem7.setText(QCoreApplication.translate("MainWindow", u"EA", None));
        ___qtablewidgetitem8 = self.tableWidget_elements.horizontalHeaderItem(5)
        ___qtablewidgetitem8.setText(QCoreApplication.translate("MainWindow", u"EI", None));
        ___qtablewidgetitem9 = self.tableWidget_elements.horizontalHeaderItem(6)
        ___qtablewidgetitem9.setText(QCoreApplication.translate("MainWindow", u"q_x", None));
        ___qtablewidgetitem10 = self.tableWidget_elements.horizontalHeaderItem(7)
        ___qtablewidgetitem10.setText(QCoreApplication.translate("MainWindow", u"q_z", None));
        ___qtablewidgetitem11 = self.tableWidget_elements.horizontalHeaderItem(8)
        ___qtablewidgetitem11.setText(QCoreApplication.translate("MainWindow", u"f_x_i", None));
        ___qtablewidgetitem12 = self.tableWidget_elements.horizontalHeaderItem(9)
        ___qtablewidgetitem12.setText(QCoreApplication.translate("MainWindow", u"f_z_i", None));
        ___qtablewidgetitem13 = self.tableWidget_elements.horizontalHeaderItem(10)
        ___qtablewidgetitem13.setText(QCoreApplication.translate("MainWindow", u"m_y_i", None));
        ___qtablewidgetitem14 = self.tableWidget_elements.horizontalHeaderItem(11)
        ___qtablewidgetitem14.setText(QCoreApplication.translate("MainWindow", u"f_x_k", None));
        ___qtablewidgetitem15 = self.tableWidget_elements.horizontalHeaderItem(12)
        ___qtablewidgetitem15.setText(QCoreApplication.translate("MainWindow", u"f_z_k", None));
        ___qtablewidgetitem16 = self.tableWidget_elements.horizontalHeaderItem(13)
        ___qtablewidgetitem16.setText(QCoreApplication.translate("MainWindow", u"m_y_k", None));

        __sortingEnabled = self.tableWidget_elements.isSortingEnabled()
        self.tableWidget_elements.setSortingEnabled(False)
        self.tableWidget_elements.setSortingEnabled(__sortingEnabled)

        self.displacements_comboBox.setCurrentText("")
        self.displacements_comboBox.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Select a element", None))
        self.internal_forces_comboBox.setCurrentText("")
        self.internal_forces_comboBox.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Select a element", None))
        self.direct_sensitivity_analysis_element_0_selection.setCurrentText("")
        self.direct_sensitivity_analysis_element_0_selection.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Select the element from which the design parameter is to be selected", None))
        self.direct_sensitivity_analysis_parameter_selection.setCurrentText("")
        self.direct_sensitivity_analysis_parameter_selection.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Select the design parameter", None))
        self.direct_sensitivity_analysis_element_1_selection.setCurrentText("")
        self.direct_sensitivity_analysis_element_1_selection.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Select an element from which the response variables are to be displayed", None))
        self.adjoint_sensitivity_analysis_element_0_selection.setCurrentText("")
        self.adjoint_sensitivity_analysis_element_0_selection.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Select the element from which the response variable is to be selected", None))
        self.adjoint_sensitivity_analysis_response_variable_selection.setCurrentText("")
        self.adjoint_sensitivity_analysis_response_variable_selection.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Select the response variable", None))
        ___qtablewidgetitem17 = self.adjoint_sensitivity_analysis_result_table.horizontalHeaderItem(0)
        ___qtablewidgetitem17.setText(QCoreApplication.translate("MainWindow", u"Element", None));
        ___qtablewidgetitem18 = self.adjoint_sensitivity_analysis_result_table.horizontalHeaderItem(1)
        ___qtablewidgetitem18.setText(QCoreApplication.translate("MainWindow", u"Design Variable", None));
        ___qtablewidgetitem19 = self.adjoint_sensitivity_analysis_result_table.horizontalHeaderItem(2)
        ___qtablewidgetitem19.setText(QCoreApplication.translate("MainWindow", u"Sensitivity", None));
        self.min_x.setText(QCoreApplication.translate("MainWindow", u"-0.1", None))
        self.max_x.setText(QCoreApplication.translate("MainWindow", u"2.1", None))
        self.min_z.setText(QCoreApplication.translate("MainWindow", u"-0.5", None))
        self.max_z.setText(QCoreApplication.translate("MainWindow", u"0.5", None))
        self.show_joints_and_supports.setText(QCoreApplication.translate("MainWindow", u"Show joints and supports", None))
        self.show_loads.setText(QCoreApplication.translate("MainWindow", u"Show loads", None))
        self.show_reaction_forces.setText(QCoreApplication.translate("MainWindow", u"Show reaction forces", None))
        self.show_element_ids.setText(QCoreApplication.translate("MainWindow", u"Show elementIds", None))
    # retranslateUi

