"""
GPL-3.0 License

Copyright (C) 2020-2022 Monirul Shawon

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

import getpass
import json
import logging
import os
import platform
import sys
import time

import requests
from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *
from models.connection_type import ConnectionType
from models.response_variable import (
    ResponseVariableDisplacement,
    ResponseVariableInternalForce,
    ResponseVariableType,
)

# from supports import *
from plotter import plot_plain_static_system, plot_static_system
from static_system import StaticSystem
from static_system_solution import StaticSystemSolution
from static_system_solver import StaticSystemSolver
from ui_main import Ui_MainWindow


import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from numpy.linalg import norm
from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *
from models.design_parameter import DesignParameterElement
from models.element import Element
from models.node import Node
from models.support import Support
from models.settings import Settings
from new_utilities import (
    set_lim,
)
from utilities import (
    get_bending_moment_curve,
    get_derived_bending_moment_curve,
    get_derived_normal_force_curve,
    get_derived_shear_force_curve,
    get_dofs_of_element,
    get_normal_force_curve,
    get_shear_force_curve,
    plot_bending_moment,
    plot_derived_bending_moment,
    plot_derived_normal_force,
    plot_derived_shear_force,
    plot_normal_force,
    plot_phi_displacement,
    plot_shear_force,
    plot_u_displacement,
    plot_w_displacement,
)
from vector import vector
from matplotlib.backend_bases import MouseButton


def create_plot_widget(layout):
    widget = QWidget()
    widget.figure = plt.figure()
    widget.canvas = FigureCanvas(widget.figure)
    layout.addWidget(widget.canvas)
    return widget


def set_table_item(table, row, column, value):
    table.setItem(
        row,
        column,
        QTableWidgetItem(
            str(value if value is not None else ""),
        ),
    )


def get_table_item_as_int(table, row, column):
    return int(table.item(row, column).text())


def get_table_item_as_float(table, row, column):
    return float(table.item(row, column).text())


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        "Graph widget 1"
        self.graph_widget = QWidget()
        self.graph_widget.figure = plt.figure()
        self.graph_widget.canvas = FigureCanvas(self.graph_widget.figure)
        self.graph_widget.toolbar1 = NavigationToolbar(
            self.graph_widget.canvas, self.graph_widget
        )
        self.ui.graphLayout_geometry.addWidget(self.graph_widget.toolbar1)
        self.ui.graphLayout_geometry.addWidget(self.graph_widget.canvas)
        ax = self.graph_widget.figure.add_subplot(111)
        ax.spines["right"].set_visible(False)
        ax.spines["top"].set_visible(False)
        ax.grid(True)

        ax = self.graph_widget.figure.add_subplot(111)
        ax.spines["right"].set_visible(False)
        ax.spines["top"].set_visible(False)
        ax.grid(True)

        self.nodes = {}
        self.elements = {}

        """
        page changing by clicking pushButton and connecting them to stackedWidget
        """
        self.ui.pushbutton_nodes.clicked.connect(
            lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.page_geometry)
        )
        self.ui.pushbutton_nodes.clicked.connect(
            lambda: self.ui.stackedWidget_2.setCurrentWidget(self.ui.page_node)
        )

        self.ui.pushbutton_members.clicked.connect(
            lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.page_geometry)
        )
        self.ui.pushbutton_members.clicked.connect(
            lambda: self.ui.stackedWidget_2.setCurrentWidget(self.ui.page_element)
        )

        self.ui.pushbutton_displacements.clicked.connect(
            lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.page_geometry)
        )
        self.ui.pushbutton_displacements.clicked.connect(
            lambda: self.ui.stackedWidget_2.setCurrentWidget(self.ui.page_displacements)
        )

        self.ui.pushbutton_internal_forces.clicked.connect(
            lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.page_geometry)
        )
        self.ui.pushbutton_internal_forces.clicked.connect(
            lambda: self.ui.stackedWidget_2.setCurrentWidget(
                self.ui.page_internal_forces
            )
        )

        self.ui.pushbutton_direct_sensa.clicked.connect(
            lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.page_geometry)
        )
        self.ui.pushbutton_direct_sensa.clicked.connect(
            lambda: self.ui.stackedWidget_2.setCurrentWidget(
                self.ui.page_direct_sensitivity_analysis
            )
        )

        self.ui.pushbutton_adjoint_sensa.clicked.connect(
            lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.page_geometry)
        )
        self.ui.pushbutton_adjoint_sensa.clicked.connect(
            lambda: self.ui.stackedWidget_2.setCurrentWidget(
                self.ui.page_adjoint_sensitivity_analysis
            )
        )

        """
        connecting desired functions by clicking pushButtons
        """

        """
        Node page
        """
        for i in range(2):
            supports_cb = QComboBox()
            supports_cb.addItems([support.value for support in Support])
            supports_cb.currentIndexChanged.connect(self.init_static_system)

            self.ui.tableWidget_nodes.setCellWidget(i, 2, supports_cb)

        self.ui.update_nodes.clicked.connect(self.init_node_table)
        self.ui.tableWidget_nodes.cellChanged.connect(self.init_static_system)

        """
        Element page
        """
        self.set_element_row(
            row=0,
            EA=1,
            EI=1,
            q_x=0,
            q_z=0,
            f_x_i=0,
            f_z_i=0,
            m_y_i=0,
            f_x_k=0,
            f_z_k=0,
            m_y_k=0,
        )

        self.ui.update_elements.clicked.connect(self.init_element_table)
        self.ui.tableWidget_elements.cellChanged.connect(self.init_static_system)

        """
        Displacements page
        """
        self.u_displacement_widget = create_plot_widget(self.ui.graphLayout_u)
        self.w_displacement_widget = create_plot_widget(self.ui.graphLayout_w)
        self.phi_displacement_widget = create_plot_widget(self.ui.graphLayout_phi)

        self.ui.displacements_comboBox.addItem("1")

        self.ui.displacements_comboBox.currentTextChanged.connect(
            self.plot_displacements
        )

        """
        Internal Forces page
        """
        self.normal_force_widget = create_plot_widget(self.ui.graphLayout_normal)
        self.shear_force_widget = create_plot_widget(self.ui.graphLayout_shear)
        self.bending_moment_widget = create_plot_widget(self.ui.graphLayout_moment)

        self.ui.internal_forces_comboBox.addItem("1")

        self.ui.internal_forces_comboBox.currentTextChanged.connect(
            self.plot_internal_forces
        )

        """
        Direct sensitivity analysis page
        """
        self.normal_force_derived_widget = create_plot_widget(
            self.ui.graphLayout_normal_derived
        )
        self.shear_force_derived_widget = create_plot_widget(
            self.ui.graphLayout_shear_derived
        )
        self.bending_moment_derived_widget = create_plot_widget(
            self.ui.graphLayout_moment_derived
        )
        """"""
        self.ui.direct_sensitivity_analysis_element_0_selection.currentTextChanged.connect(
            self.plot_direct_sensitivity_analysis
        )
        self.ui.direct_sensitivity_analysis_parameter_selection.currentTextChanged.connect(
            self.plot_direct_sensitivity_analysis
        )
        self.ui.direct_sensitivity_analysis_element_1_selection.currentTextChanged.connect(
            self.plot_direct_sensitivity_analysis
        )

        self.ui.direct_sensitivity_analysis_element_0_selection.addItem("1")

        self.ui.direct_sensitivity_analysis_parameter_selection.addItems(
            [p.value for p in DesignParameterElement]
        )

        self.ui.direct_sensitivity_analysis_element_1_selection.addItem("1")

        """
        adjoint sensitivity analysis page
        """

        self.ui.adjoint_sensitivity_analysis_element_0_selection.currentTextChanged.connect(
            self.plot_adjoint_sensitivity_analysis
        )
        self.ui.adjoint_sensitivity_analysis_response_variable_selection.currentTextChanged.connect(
            self.plot_adjoint_sensitivity_analysis
        )

        self.ui.adjoint_sensitivity_analysis_element_0_selection.addItem("1")

        self.ui.adjoint_sensitivity_analysis_response_variable_selection.addItems(
            [
                p.value
                for p in list(ResponseVariableInternalForce)
                + list(ResponseVariableDisplacement)
            ]
        )

        """
        Header
        """
        self.ui.spinBox_scale_factor.valueChanged.connect(self.update_scaling_factor)

        self.ui.min_x.editingFinished.connect(self.draw_graph)
        self.ui.max_x.editingFinished.connect(self.draw_graph)

        self.ui.min_z.editingFinished.connect(self.draw_graph)
        self.ui.max_z.editingFinished.connect(self.draw_graph)

        self.ui.show_loads.clicked.connect(self.draw_graph)
        self.ui.show_reaction_forces.clicked.connect(self.draw_graph)
        self.ui.show_element_ids.clicked.connect(self.draw_graph)
        self.ui.show_joints_and_supports.clicked.connect(self.draw_graph)

        self.ui.element_line_width.valueChanged.connect(self.draw_graph)

        self.color_quantity = None
        self.color_functions = None

        # self.load_static_system_from_file()

    def get_coords_of_node(self, id):
        x = float(self.ui.tableWidget_nodes.item(id - 1, 0).text())
        y = float(self.ui.tableWidget_nodes.item(id - 1, 1).text())

        return vector(x, y)

    def get_type_of_node(self, id):

        support_type = self.ui.tableWidget_nodes.cellWidget(id - 1, 2).currentIndex()

        support = [support for support in Support][support_type]

        if support == Support.PINNED:
            return (True, True, False)
        if support == Support.CLAMPED:
            return (True, True, True)
        if support == Support.HORIZONTAL_ROLLER:
            return (True, False, False)
        if support == Support.VERTICAL_ROLLER:
            return (False, True, False)

        return (False, False, False)

    def set_node_row(self, row, x=None, z=None, type=None):
        t = self.ui.tableWidget_nodes
        set_table_item(t, row, column=0, value=x)
        set_table_item(t, row, column=1, value=z)

        supports_cb = QComboBox()
        supports_cb.addItems([support.value for support in Support])

        t.setCellWidget(row, 2, supports_cb)
        if type:
            supports_cb.setCurrentIndex(
                [support.value for support in Support].index(type)
            )
        supports_cb.currentIndexChanged.connect(self.init_static_system)

    def set_element_row(
        self,
        row,
        node_i=None,
        node_k=None,
        type_i=None,
        type_k=None,
        EA=None,
        EI=None,
        q_x=None,
        q_z=None,
        f_x_i=None,
        f_z_i=None,
        m_y_i=None,
        f_x_k=None,
        f_z_k=None,
        m_y_k=None,
    ):
        t = self.ui.tableWidget_elements
        set_table_item(t, row, column=0, value=node_i)
        set_table_item(t, row, column=1, value=node_k)

        # set_table_item(t, row, column=2, value=type_i)
        # set_table_item(t, row, column=3, value=type_k)
        supports_cb_i = QComboBox()
        supports_cb_i.addItems([connection.value for connection in ConnectionType])

        t.setCellWidget(row, 2, supports_cb_i)

        if type_i:
            supports_cb_i.setCurrentIndex(
                [connection.value for connection in ConnectionType].index(type_i)
            )
        supports_cb_i.currentIndexChanged.connect(self.init_static_system)

        supports_cb_k = QComboBox()
        supports_cb_k.addItems([connection.value for connection in ConnectionType])

        t.setCellWidget(row, 3, supports_cb_k)
        if type_k:
            supports_cb_k.setCurrentIndex(
                [connection.value for connection in ConnectionType].index(type_k)
            )
        supports_cb_k.currentIndexChanged.connect(self.init_static_system)

        set_table_item(t, row, column=4, value=EA)
        set_table_item(t, row, column=5, value=EI)
        set_table_item(t, row, column=6, value=q_x)
        set_table_item(t, row, column=7, value=q_z)
        set_table_item(t, row, column=8, value=f_x_i)
        set_table_item(t, row, column=9, value=f_z_i)
        set_table_item(t, row, column=10, value=m_y_i)
        set_table_item(t, row, column=11, value=f_x_k)
        set_table_item(t, row, column=12, value=f_z_k)
        set_table_item(t, row, column=13, value=m_y_k)

    def get_element_row(self, row):
        t = self.ui.tableWidget_elements
        node_i_id = get_table_item_as_int(t, row=row, column=0)
        node_k_id = get_table_item_as_int(t, row=row, column=1)

        # q_x = get_table_item_as_float(t, row=row, column=2)
        # q_x = get_table_item_as_float(t, row=row, column=3)
        connections = [c for c in ConnectionType]
        type_i = connections[t.cellWidget(row, 2).currentIndex()]
        type_k = connections[t.cellWidget(row, 3).currentIndex()]

        EA = get_table_item_as_float(t, row=row, column=4)
        EI = get_table_item_as_float(t, row=row, column=5)

        q_x = get_table_item_as_float(t, row=row, column=6)
        q_z = get_table_item_as_float(t, row=row, column=7)

        f_x_i = get_table_item_as_float(t, row=row, column=8)
        f_z_i = get_table_item_as_float(t, row=row, column=9)
        m_y_i = get_table_item_as_float(t, row=row, column=10)
        f_x_k = get_table_item_as_float(t, row=row, column=11)
        f_z_k = get_table_item_as_float(t, row=row, column=12)
        m_y_k = get_table_item_as_float(t, row=row, column=13)

        return (
            node_i_id,
            node_k_id,
            type_i,
            type_k,
            EA,
            EI,
            q_x,
            q_z,
            f_x_i,
            f_z_i,
            m_y_i,
            f_x_k,
            f_z_k,
            m_y_k,
        )

    def load_static_system_from_file(self):
        # file_name = "rhein_bruecke.json"
        # file_name = "kragarm_mit_pendelstab.json"
        file_name = "bruecke.json"

        with open("example_static_systems/" + file_name, "r") as file:
            data = json.load(file)

        display = data["display"]
        nodes = data["nodes"]
        elements = data["elements"]

        self.ui.spinBox_nodes.setValue(len(nodes))
        self.ui.tableWidget_nodes.setRowCount(len(nodes))

        self.ui.spinBox_elements.setValue(len(elements))
        self.ui.tableWidget_elements.setRowCount(len(elements))

        for i, e in enumerate(elements):
            self.set_element_row(
                i,
                node_i=e["node_i"],
                node_k=e["node_k"],
                type_i=e["connection_type_i"],
                type_k=e["connection_type_k"],
                EA=e["EA"],
                EI=e["EI"],
                q_x=e["q_x"],
                q_z=e["q_z"],
                f_x_i=e["f_x_i"],
                f_z_i=e["f_z_i"],
                m_y_i=e["m_y_i"],
                f_x_k=e["f_x_k"],
                f_z_k=e["f_z_k"],
                m_y_k=e["m_y_k"],
            )

        for i, n in enumerate(nodes):

            if n["restrained_x"] and n["restrained_z"] and n["restrained_phi"]:
                support = Support.CLAMPED
            elif n["restrained_x"] and n["restrained_z"] and not n["restrained_phi"]:
                support = Support.PINNED
            elif (
                n["restrained_x"] and not n["restrained_z"] and not n["restrained_phi"]
            ):
                support = Support.HORIZONTAL_ROLLER
            elif (
                not n["restrained_x"] and n["restrained_z"] and not n["restrained_phi"]
            ):
                support = Support.VERTICAL_ROLLER
            else:
                support = Support.NONE
            self.set_node_row(i, x=n["x"], z=n["z"], type=support.value)

        self.ui.displacements_comboBox.clear()
        self.ui.displacements_comboBox.addItems(
            [str(i) for i in range(1, len(elements) + 1)]
        )

        self.ui.internal_forces_comboBox.clear()
        self.ui.internal_forces_comboBox.addItems(
            [str(i) for i in range(1, len(elements) + 1)]
        )

        self.ui.direct_sensitivity_analysis_element_0_selection.clear()
        self.ui.direct_sensitivity_analysis_element_0_selection.addItems(
            [str(i) for i in range(1, len(elements) + 1)]
        )

        self.ui.direct_sensitivity_analysis_element_1_selection.clear()
        self.ui.direct_sensitivity_analysis_element_1_selection.addItems(
            [str(i) for i in range(1, len(elements) + 1)]
        )

        self.ui.adjoint_sensitivity_analysis_element_0_selection.clear()
        self.ui.adjoint_sensitivity_analysis_element_0_selection.addItems(
            [str(i) for i in range(1, len(elements) + 1)]
        )

        if "min_x" in display:
            self.ui.min_x.setText(str(display["min_x"]))
        if "max_x" in display:
            self.ui.max_x.setText(str(display["max_x"]))

        if "min_z" in display:
            self.ui.min_z.setText(str(display["min_z"]))
        if "max_z" in display:
            self.ui.max_z.setText(str(display["max_z"]))

        self.init_static_system()

    def solve(self):
        solver = StaticSystemSolver(self.static_system)
        det = np.linalg.det(solver.get_non_restrained_k())
        if np.isclose(det, 0):
            self.solution = None
            self.draw_plain_static_system()
            ax = self.graph_widget.figure.gca()

            ax.text(
                0.85,
                0.95,
                "System is kinematic",
                transform=ax.transAxes,
                fontsize=12,
                verticalalignment="center",
                horizontalalignment="center",
                bbox=dict(facecolor="red", alpha=0.5),
            )

            self.graph_widget.figure.canvas.draw()
            return
        self.solution = StaticSystemSolution(
            displacements=solver.get_displacements(),
            external_forces=solver.get_external_forces(),
            internal_forces=[
                solver.get_internal_forces_of_element(i + 1)
                for i in range(len(self.static_system.get_elements()))
            ],
        )

        self.plot_displacements()
        self.plot_internal_forces()
        self.draw_graph()

    def init_static_system(self):
        static_system = StaticSystem()

        node_connections = {}

        for row in range(self.ui.tableWidget_elements.rowCount()):
            try:
                (
                    node_i_id,
                    node_k_id,
                    connection_type_i,
                    connection_type_k,
                    EA,
                    EI,
                    q_x,
                    q_z,
                    f_x_i,
                    f_z_i,
                    m_y_i,
                    f_x_k,
                    f_z_k,
                    m_y_k,
                ) = self.get_element_row(row)

                type_i = self.get_type_of_node(node_i_id)

                type_k = self.get_type_of_node(node_k_id)

                if node_i_id not in node_connections:
                    node_connections[node_i_id] = {
                        "elements": [],
                        "restrained_x": type_i[0],
                        "restrained_z": type_i[1],
                        "restrained_phi": type_i[2],
                    }

                if node_k_id not in node_connections:
                    node_connections[node_k_id] = {
                        "elements": [],
                        "restrained_x": type_k[0],
                        "restrained_z": type_k[1],
                        "restrained_phi": type_k[2],
                    }

                node_connections[node_i_id]["elements"].append(
                    {
                        "type": "i",
                        "id": row + 1,
                        "connection": connection_type_i,
                    }
                )

                node_connections[node_k_id]["elements"].append(
                    {
                        "type": "k",
                        "id": row + 1,
                        "connection": connection_type_k,
                    }
                )

                static_system.create_element(
                    self.get_coords_of_node(node_i_id),
                    self.get_coords_of_node(node_k_id),
                    EA=EA,
                    EI=EI,
                    q_x=q_x,
                    q_z=q_z,
                    f_x_i=f_x_i,
                    f_z_i=f_z_i,
                    m_y_i=m_y_i,
                    f_x_k=f_x_k,
                    f_z_k=f_z_k,
                    m_y_k=m_y_k,
                )
            except Exception as e:
                print(e)
                return

        for node_connection in node_connections.values():
            node_dof_x = None
            node_dof_z = None
            node_dof_phi = None

            for v in node_connection["elements"]:
                if v["type"] == "i":
                    dofs = get_dofs_of_element(id=v["id"])[:3]
                else:
                    dofs = get_dofs_of_element(id=v["id"])[3:]

                dof_x, dof_z, dof_phi = dofs

                if not node_dof_x:
                    node_dof_x = dof_x
                else:
                    static_system.set_boundary_condition(
                        dof=dof_x, times=1, is_equal_to_dof=node_dof_x
                    )
                if not node_dof_z:
                    node_dof_z = dof_z

                else:
                    static_system.set_boundary_condition(
                        dof=dof_z, times=1, is_equal_to_dof=node_dof_z
                    )

                if v["connection"] == ConnectionType.STIFF:
                    if not node_dof_phi:
                        node_dof_phi = dof_phi
                    else:
                        static_system.set_boundary_condition(
                            dof=dof_phi, times=1, is_equal_to_dof=node_dof_phi
                        )

            if node_connection["restrained_x"]:
                static_system.set_restrained_dof(dof=node_dof_x)
            if node_connection["restrained_z"]:
                static_system.set_restrained_dof(dof=node_dof_z)
            if node_connection["restrained_phi"]:
                static_system.set_restrained_dof(dof=node_dof_phi)

        self.static_system = static_system

        self.solve()

    def init_node_table(self):
        new_node_count = self.ui.spinBox_nodes.value()
        current_node_count = self.ui.tableWidget_nodes.rowCount()

        self.ui.tableWidget_nodes.setRowCount(new_node_count)

        if new_node_count > current_node_count:
            for i in range(current_node_count, new_node_count):
                supports_cb = QComboBox()
                supports_cb.addItems([support.value for support in Support])
                supports_cb.currentIndexChanged.connect(self.init_static_system)

                self.ui.tableWidget_nodes.setCellWidget(i, 2, supports_cb)

    def init_element_table(self):
        new_element_count = self.ui.spinBox_elements.value()
        current_element_count = self.ui.tableWidget_elements.rowCount()

        self.ui.tableWidget_elements.setRowCount(new_element_count)

        if new_element_count > current_element_count:
            for i in range(current_element_count, new_element_count):
                self.set_element_row(
                    row=i,
                    EA=1,
                    EI=1,
                    q_x=0,
                    q_z=0,
                    f_x_i=0,
                    f_z_i=0,
                    m_y_i=0,
                    f_x_k=0,
                    f_z_k=0,
                    m_y_k=0,
                )

        self.ui.displacements_comboBox.clear()
        self.ui.displacements_comboBox.addItems(
            [str(i) for i in range(1, new_element_count + 1)]
        )

        self.ui.internal_forces_comboBox.clear()
        self.ui.internal_forces_comboBox.addItems(
            [str(i) for i in range(1, new_element_count + 1)]
        )

        self.ui.direct_sensitivity_analysis_element_0_selection.clear()
        self.ui.direct_sensitivity_analysis_element_0_selection.addItems(
            [str(i) for i in range(1, new_element_count + 1)]
        )

        self.ui.direct_sensitivity_analysis_element_1_selection.clear()
        self.ui.direct_sensitivity_analysis_element_1_selection.addItems(
            [str(i) for i in range(1, new_element_count + 1)]
        )

        self.ui.adjoint_sensitivity_analysis_element_0_selection.clear()
        self.ui.adjoint_sensitivity_analysis_element_0_selection.addItems(
            [str(i) for i in range(1, new_element_count + 1)]
        )

    def draw_plain_static_system(self):
        self.graph_widget.figure.clear()
        ax = self.graph_widget.figure.add_subplot(111)
        ax.set_aspect("equal")
        ax.grid(True)

        x_values = []
        z_values = []

        for e in self.static_system.get_elements():
            x, z = e.p_i
            x_values.append(x)
            z_values.append(z)

            x, z = e.p_k
            x_values.append(x)
            z_values.append(z)

        plot_plain_static_system(
            ax=ax,
            static_system=self.static_system,
            show_loads=self.ui.show_loads.isChecked(),
            show_element_id=self.ui.show_element_ids.isChecked(),
            show_joints_and_supports=self.ui.show_joints_and_supports.isChecked(),
            element_line_width=self.ui.element_line_width.value(),
        )

        min_x = float(self.ui.min_x.text())
        max_x = float(self.ui.max_x.text())

        min_z = float(self.ui.min_z.text())
        max_z = float(self.ui.max_z.text())

        ax.set_xlim(min_x, max_x)
        ax.set_ylim(min_z, max_z)

        self.graph_widget.canvas.draw()

    def draw_graph(self):
        self.graph_widget.figure.clear()
        ax = self.graph_widget.figure.add_subplot(111)
        ax.set_aspect("equal")
        ax.grid(True)

        x_values = []
        z_values = []

        for e in self.static_system.get_elements():
            x, z = e.p_i
            x_values.append(x)
            z_values.append(z)

            x, z = e.p_k
            x_values.append(x)
            z_values.append(z)

        max_x = max(x_values)
        min_x = min(x_values)

        max_z = max(z_values)
        min_z = min(z_values)

        plot_static_system(
            ax=ax,
            static_system=self.static_system,
            static_system_solution=self.solution,
            show_reaction_forces=self.ui.show_reaction_forces.isChecked(),
            show_loads=self.ui.show_loads.isChecked(),
            show_element_id=self.ui.show_element_ids.isChecked(),
            color_quantity=self.color_quantity,
            show_joints_and_supports=self.ui.show_joints_and_supports.isChecked(),
            element_line_width=self.ui.element_line_width.value(),
            color_functions=self.color_functions,
        )

        min_x = float(self.ui.min_x.text())
        max_x = float(self.ui.max_x.text())

        min_z = float(self.ui.min_z.text())
        max_z = float(self.ui.max_z.text())

        ax.set_xlim(min_x, max_x)
        ax.set_ylim(min_z, max_z)

        self.graph_widget.canvas.draw()

    def update_scaling_factor(self, new_scaling_factor):
        Settings.scalingFactor = new_scaling_factor

        self.draw_graph()

    def on_normal_force_plot_clicked(self, event):
        self.color_functions = []

        for i, e in enumerate(self.static_system.elements):
            element_id = i + 1

            n_i, v_i, m_y_i, n_k, v_k, m_y_k = StaticSystemSolver(
                self.static_system
            ).get_internal_forces_of_element(element_id)
            self.color_functions.append(get_normal_force_curve(n_i=n_i, n_k=n_k))

        self.draw_graph()

    def on_shear_force_plot_clicked(self, event):
        self.color_functions = []

        for i, e in enumerate(self.static_system.elements):
            element_id = i + 1

            n_i, v_i, m_y_i, n_k, v_k, m_y_k = StaticSystemSolver(
                self.static_system
            ).get_internal_forces_of_element(element_id)
            self.color_functions.append(get_shear_force_curve(v_i=v_i, v_k=v_k))

        self.draw_graph()

    def on_bending_moment_plot_clicked(self, event):
        self.color_functions = []

        for i, e in enumerate(self.static_system.elements):
            element_id = i + 1
            _, q_z = e.get_local_area_loads()
            l = e.get_length()

            n_i, v_i, m_y_i, n_k, v_k, m_y_k = StaticSystemSolver(
                self.static_system
            ).get_internal_forces_of_element(element_id)
            self.color_functions.append(
                get_bending_moment_curve(m_y_i=m_y_i, m_y_k=m_y_k, q_z=q_z, l=l)
            )

        self.draw_graph()

    def on_derived_normal_force_plot_clicked(self, event):
        self.color_functions = []

        design_parameter = DesignParameterElement(
            value=self.ui.direct_sensitivity_analysis_parameter_selection.currentText()
        )

        param_element_id = int(
            self.ui.direct_sensitivity_analysis_element_0_selection.currentText()
        )

        for i, e in enumerate(self.static_system.elements):
            element_id = i + 1

            n_i, v_i, m_y_i, n_k, v_k, m_y_k = StaticSystemSolver(
                self.static_system
            ).get_derived_internal_forces_of_element(
                element_id, param_element_id, dx=design_parameter.value
            )
            self.color_functions.append(
                get_derived_normal_force_curve(derived_n_i=n_i, derived_n_k=n_k)
            )

        self.draw_graph()

    def on_derived_shear_force_plot_clicked(self, event):
        self.color_functions = []

        design_parameter = DesignParameterElement(
            value=self.ui.direct_sensitivity_analysis_parameter_selection.currentText()
        )

        param_element_id = int(
            self.ui.direct_sensitivity_analysis_element_0_selection.currentText()
        )

        for i, e in enumerate(self.static_system.elements):
            element_id = i + 1

            n_i, v_i, m_y_i, n_k, v_k, m_y_k = StaticSystemSolver(
                self.static_system
            ).get_derived_internal_forces_of_element(
                element_id, param_element_id, dx=design_parameter.value
            )
            self.color_functions.append(
                get_derived_shear_force_curve(derived_v_i=v_i, derived_v_k=v_k)
            )

        self.draw_graph()

    def on_derived_bending_moment_plot_clicked(self, event):
        self.color_functions = []

        design_parameter = DesignParameterElement(
            value=self.ui.direct_sensitivity_analysis_parameter_selection.currentText()
        )
        dx = design_parameter.value
        param_element_id = int(
            self.ui.direct_sensitivity_analysis_element_0_selection.currentText()
        )

        for i, e in enumerate(self.static_system.elements):
            element_id = i + 1

            n_i, v_i, m_y_i, n_k, v_k, m_y_k = StaticSystemSolver(
                self.static_system
            ).get_derived_internal_forces_of_element(
                element_id, param_element_id, dx=dx
            )
            self.color_functions.append(
                get_derived_bending_moment_curve(
                    d_m_y_i=m_y_i,
                    d_m_y_k=m_y_k,
                    q_z=e.q_z,
                    l=e.get_length(),
                    dx=dx if element_id == param_element_id else "",
                )
            )

        self.draw_graph()

    def plot_displacements(self):
        self.u_displacement_widget.figure.clear()
        self.w_displacement_widget.figure.clear()
        self.phi_displacement_widget.figure.clear()

        try:
            element_id = int(self.ui.displacements_comboBox.currentText())
            e = self.static_system.get_element(element_id)

            solver = StaticSystemSolver(self.static_system)

            u_i, w_i, phi_i, u_k, w_k, phi_k = (
                solver.get_local_displacements_of_element(element_id)
            )
            n_i, v_i, m_y_i, n_k, v_k, m_y_k = solver.get_internal_forces_of_element(
                element_id
            )

            q_x, q_z = e.get_local_area_loads()
            EA = e.EA
            EI = e.EI
            l = e.get_length()
        except:
            self.u_displacement_widget.canvas.draw()
            self.w_displacement_widget.canvas.draw()
            self.phi_displacement_widget.canvas.draw()
            return

        ax = self.u_displacement_widget.figure.add_subplot(111)
        plot_u_displacement(ax=ax, n_i=n_i, n_k=n_k, u_i=u_i, EA=EA)
        ax.set_title(
            f"Verschiebung entlang der Stabachse für Element {element_id}", fontsize=10
        )

        ax = self.w_displacement_widget.figure.add_subplot(111)
        plot_w_displacement(
            ax=ax,
            w_i=w_i,
            w_k=w_k,
            m_y_i=m_y_i,
            m_y_k=m_y_k,
            q_z=q_z,
            l=l,
            EI=EI,
        )
        ax.set_title(
            f"Verschiebung senkrecht zur Stabachse für Element {element_id}",
            fontsize=10,
        )

        ax = self.phi_displacement_widget.figure.add_subplot(111)
        plot_phi_displacement(
            ax=ax,
            w_i=w_i,
            w_k=w_k,
            m_y_i=m_y_i,
            m_y_k=m_y_k,
            q_z=q_z,
            l=l,
            EI=EI,
        )
        ax.set_title(f"Verdrehung für Element {element_id}", fontsize=10)

        self.u_displacement_widget.canvas.draw()
        self.w_displacement_widget.canvas.draw()
        self.phi_displacement_widget.canvas.draw()

    def plot_internal_forces(self):
        self.normal_force_widget.figure.clear()
        self.shear_force_widget.figure.clear()
        self.bending_moment_widget.figure.clear()

        try:
            element_id = int(self.ui.internal_forces_comboBox.currentText())
            e = self.static_system.get_element(element_id)
            n_i, v_i, m_y_i, n_k, v_k, m_y_k = StaticSystemSolver(
                self.static_system
            ).get_internal_forces_of_element(element_id)

            _, q_z = e.get_local_area_loads()

        except:
            self.normal_force_widget.canvas.draw()
            self.shear_force_widget.canvas.draw()
            self.bending_moment_widget.canvas.draw()
            return

        ax = self.normal_force_widget.figure.add_subplot(111)
        plot_normal_force(ax=ax, n_i=n_i, n_k=n_k)
        self.normal_force_widget.canvas.mpl_connect(
            "button_press_event",
            lambda event: self.on_normal_force_plot_clicked(event),
        )
        ax.set_title(f"Normalkraftverlauf für Element {element_id}", fontsize=10)

        ax = self.shear_force_widget.figure.add_subplot(111)
        plot_shear_force(ax=ax, v_i=v_i, v_k=v_k)
        self.shear_force_widget.canvas.mpl_connect(
            "button_press_event",
            lambda event: self.on_shear_force_plot_clicked(event),
        )
        ax.set_title(f"Querkraftverlauf für Element {element_id}", fontsize=10)

        ax = self.bending_moment_widget.figure.add_subplot(111)
        plot_bending_moment(ax=ax, m_y_i=m_y_i, m_y_k=m_y_k, q_z=q_z, l=e.get_length())
        self.bending_moment_widget.canvas.mpl_connect(
            "button_press_event",
            lambda event: self.on_bending_moment_plot_clicked(event),
        )
        ax.set_title(f"Momentenverlauf für Element {element_id}", fontsize=10)

        self.normal_force_widget.canvas.draw()
        self.shear_force_widget.canvas.draw()
        self.bending_moment_widget.canvas.draw()

    def plot_direct_sensitivity_analysis(self):
        self.normal_force_derived_widget.figure.clear()
        self.shear_force_derived_widget.figure.clear()
        self.bending_moment_derived_widget.figure.clear()

        try:
            element_id = int(
                self.ui.direct_sensitivity_analysis_element_1_selection.currentText()
            )
            e = self.static_system.get_element(element_id)

            design_parameter = DesignParameterElement(
                value=self.ui.direct_sensitivity_analysis_parameter_selection.currentText()
            )

            param_element_id = int(
                self.ui.direct_sensitivity_analysis_element_0_selection.currentText()
            )

            solver = StaticSystemSolver(self.static_system)

            sensa = solver.get_direct_sensa(
                id=param_element_id, design_parameter=design_parameter
            )
            n_i, v_i, m_y_i, n_k, v_k, m_y_k = sensa[element_id]

        except:
            self.normal_force_derived_widget.canvas.draw()
            self.shear_force_derived_widget.canvas.draw()
            self.bending_moment_derived_widget.canvas.draw()
            return

        ax = self.normal_force_derived_widget.figure.add_subplot(111)
        plot_derived_normal_force(ax=ax, derived_n_i=n_i, derived_n_k=n_k)
        self.normal_force_derived_widget.canvas.mpl_connect(
            "button_press_event",
            lambda event: self.on_derived_normal_force_plot_clicked(event),
        )
        ax.set_title(
            f"N/{design_parameter.value} für Element {element_id}", fontsize=10
        )

        ax = self.shear_force_derived_widget.figure.add_subplot(111)
        plot_derived_shear_force(ax=ax, derived_v_i=v_i, derived_v_k=v_k)
        self.shear_force_derived_widget.canvas.mpl_connect(
            "button_press_event",
            lambda event: self.on_derived_shear_force_plot_clicked(event),
        )
        ax.set_title(
            f"V/{design_parameter.value} für Element {element_id}", fontsize=10
        )

        ax = self.bending_moment_derived_widget.figure.add_subplot(111)
        plot_derived_bending_moment(
            ax=ax,
            d_m_y_i=m_y_i,
            d_m_y_k=m_y_k,
            q_z=e.q_z,
            l=e.get_length(),
            dx=design_parameter.value,
        )
        self.bending_moment_derived_widget.canvas.mpl_connect(
            "button_press_event",
            lambda event: self.on_derived_bending_moment_plot_clicked(event),
        )
        ax.set_title(
            f"M/{design_parameter.value} für Element {element_id}", fontsize=10
        )

        self.normal_force_derived_widget.canvas.draw()
        self.shear_force_derived_widget.canvas.draw()
        self.bending_moment_derived_widget.canvas.draw()

    def plot_adjoint_sensitivity_analysis(self):
        self.ui.adjoint_sensitivity_analysis_result_table.setRowCount(0)

        try:
            # Select the element from which the response variable should be selected
            response_element_id = int(
                self.ui.adjoint_sensitivity_analysis_element_0_selection.currentText()
            )

            try:
                response_variable = ResponseVariableInternalForce(
                    value=self.ui.adjoint_sensitivity_analysis_response_variable_selection.currentText()
                )
            except:
                response_variable = ResponseVariableDisplacement(
                    value=self.ui.adjoint_sensitivity_analysis_response_variable_selection.currentText()
                )
        except:
            return

        solver = StaticSystemSolver(self.static_system)

        sensa = solver.get_adjoint_sensa(
            id=response_element_id, response_parameter=response_variable
        )

        for e_id in sensa.keys():
            for p, s in sensa[e_id].items():
                self.append_row_to_adjoint_sensitivity_analysis_table(
                    element_id=e_id,
                    parameter=p,
                    value=s,
                )

    def append_row_to_adjoint_sensitivity_analysis_table(
        self,
        element_id,
        parameter,
        value,
    ):
        t = self.ui.adjoint_sensitivity_analysis_result_table
        row_position = t.rowCount()
        t.setRowCount(row_position + 1)

        t.setItem(row_position, 0, QTableWidgetItem(str(element_id)))
        t.setItem(row_position, 1, QTableWidgetItem(str(parameter)))
        t.setItem(row_position, 2, QTableWidgetItem(str(round(value, 6))))


if __name__ == "__main__":
    start_time = time.time()
    app = QApplication(sys.argv)
    app.setStyle("Oxygen")

    window = MainWindow()
    window.show()

    sys.exit(app.exec())
