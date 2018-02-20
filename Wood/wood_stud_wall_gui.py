# -*- coding: utf-8 -*-
import Tkinter as tk
import ttk
import tkFont
import wood_classes as wood
import matplotlib
matplotlib.use('TKAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import tkFileDialog
import os

class Master_window:

    def __init__(self, master):
        
        self.master = master
        self.f_size = 8
        helv = tkFont.Font(family='Helvetica',size=self.f_size, weight='bold')
        self.menubar = tk.Menu(self.master)
        self.menu = tk.Menu(self.menubar, tearoff=0)
        self.menu_props = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label = "File", menu=self.menu)
        self.menu.add_command(label="Open", command=self.file_open)
        self.menu.add_separator()
        self.menu.add_command(label="Quit", command=self.quit_app)
        try:
            self.master.config(menu=self.menubar)
        except AttributeError:
            self.master.tk.call(master, "config", "-menu", self.menubar)

        #Main Frames
        self.main_frame = tk.Frame(master, bd=2, relief='sunken', padx=1,pady=1)
        self.main_frame.pack(anchor='c', padx= 1, pady= 1, fill=tk.BOTH, expand=1)
        self.base_frame = tk.Frame(master, bd=2, relief='sunken', padx=1,pady=1)
        self.base_frame.pack(side=tk.BOTTOM, padx= 1, pady= 1, fill=tk.X, expand=1)
        
        self.nb = ttk.Notebook(self.main_frame)
        self.nb.pack(fill=tk.BOTH)
        
        #Tab 1
        self.page1 = ttk.Frame(self.nb)
        self.nb.add(self.page1, text='Wall and Stud Information and Inputs - Find Axial Capacity Per Stud')
        
        self.pg1_frame = tk.Frame(self.page1, bd=2, relief='sunken', padx=1,pady=1)
        self.pg1_frame.pack(fill=tk.BOTH, padx=5, pady=5)
        
        #user input frame
        self.input_frame = tk.LabelFrame(self.pg1_frame, text="Inputs", bd=2, relief='sunken', padx=5, pady=5)
        
        #Wall Geometry Frame
        self.geo_frame = tk.LabelFrame(self.input_frame, text="Wall Stud Geometry: ", bd=2, relief='sunken', padx=5, pady=5)

        #stud dimensions - nominal
        tk.Label(self.geo_frame, text='Nominal Stud Size:').grid(row=1,column=1)
        self.b_nom = tk.StringVar()
        self.b_nom.set('2')
        self.b_nom_selection = tk.OptionMenu(self.geo_frame, self.b_nom, '2','3','4', command=self.actual_stud_size)
        self.b_nom_selection.grid(row=2,column=1)
        tk.Label(self.geo_frame, text='x').grid(row=2,column=2)
        self.d_nom = tk.StringVar()
        self.d_nom.set('6')
        self.d_nom_selection = tk.OptionMenu(self.geo_frame, self.d_nom, '3','4','5','6','8','10','12','14','16', command=self.actual_stud_size)
        self.d_nom_selection.grid(row=2,column=3)
        
        #stud dimensions - actual
        tk.Label(self.geo_frame, text='Actual Stud Size:').grid(row=1,column=4)
        self.b_actual_label = tk.Label(self.geo_frame, text='1.5')
        self.b_actual_label.grid(row=2,column=4)
        tk.Label(self.geo_frame, text='x').grid(row=2,column=5)
        self.d_actual_label = tk.Label(self.geo_frame, text='5.5')
        self.d_actual_label.grid(row=2,column=6)
        
        #stud Spacing
        self.spacing_label = tk.Label(self.geo_frame, text='Stud Spacing: ')
        self.spacing_label.grid(row=3,column=1)
        self.stud_spacing = tk.StringVar()
        self.spacing_entry = tk.Entry(self.geo_frame, textvariable=self.stud_spacing, width=10)
        self.spacing_entry.grid(row=3,column=2)
        tk.Label(self.geo_frame, text='in').grid(row=3,column=3)
        
        #Wall Height
        self.height_label = tk.Label(self.geo_frame, text='Wall Height: ')
        self.height_label.grid(row=4,column=1)
        self.wall_height = tk.StringVar()
        self.height_entry = tk.Entry(self.geo_frame, textvariable=self.wall_height, width=10)
        self.height_entry.grid(row=4,column=2)
        tk.Label(self.geo_frame, text='ft').grid(row=4,column=3)
        
        #subtract wall plates from height
        self.sub_plates = tk.IntVar()
        tk.Checkbutton(self.geo_frame, text=': Subtract Wall Plates from Height (y/n)', variable=self.sub_plates).grid(row=3, column=4)
        self.plates_label = tk.Label(self.geo_frame, text='# of 1.5" Plates to subtract: ')
        self.plates_label.grid(row=4,column=4)        
        self.num_plates = tk.StringVar()
        self.num_plates.set(0)
        self.num_plates_entry = tk.Entry(self.geo_frame, textvariable=self.num_plates, width=5)
        self.num_plates_entry.grid(row=4,column=5)
        
        self.geo_frame.pack(fill=tk.X, padx=5, pady=5)
        
        #Reference Stud Design Values - Frame
        self.ref_stud_properties_frame = tk.LabelFrame(self.input_frame, text="Reference Stud Design Values : ", bd=2, relief='sunken', padx=5, pady=5)
        
        #Wall Stud Grade
        self.grade_label = tk.Label(self.ref_stud_properties_frame,text = 'Grade :')
        self.grade_label.grid(row=1, column=1)
        self.grade = tk.StringVar()
        self.grade.set('No.1/No.2')
        grades = ['Select Structural','No.1 & Better','No.1/No.2','No.1','No.2','No.3','Stud','Construction','Utility']
        self.grade_selection = tk.OptionMenu(self.ref_stud_properties_frame, self.grade, *grades)
        self.grade_selection.grid(row=1,column=2)        
        
        #Fb
        self.fb_label = tk.Label(self.ref_stud_properties_frame,text = 'Fb :')
        self.fb_label.grid(row=2, column=1)
        self.fb_psi = tk.StringVar()
        self.fb_psi.set(875)
        self.fb_entry = tk.Entry(self.ref_stud_properties_frame, textvariable=self.fb_psi, width=10)
        self.fb_entry.grid(row=2, column=2)
        tk.Label(self.ref_stud_properties_frame, text='psi').grid(row=2,column=3)
        
        #Fv
        self.fv_label = tk.Label(self.ref_stud_properties_frame,text = 'Fv :')
        self.fv_label.grid(row=3, column=1)
        self.fv_psi = tk.StringVar()
        self.fv_psi.set(135)
        self.fv_entry = tk.Entry(self.ref_stud_properties_frame, textvariable=self.fv_psi, width=10)
        self.fv_entry.grid(row=3, column=2)
        tk.Label(self.ref_stud_properties_frame, text='psi').grid(row=3,column=3)

        #Fc
        self.fc_label = tk.Label(self.ref_stud_properties_frame,text = 'Fc :')
        self.fc_label.grid(row=4, column=1)
        self.fc_psi = tk.StringVar()
        self.fc_psi.set(1150)
        self.fc_entry = tk.Entry(self.ref_stud_properties_frame, textvariable=self.fc_psi, width=10)
        self.fc_entry.grid(row=4, column=2)
        tk.Label(self.ref_stud_properties_frame, text='psi').grid(row=4,column=3) 

        #E
        self.E_label = tk.Label(self.ref_stud_properties_frame,text = 'E :')
        self.E_label.grid(row=5, column=1)
        self.E_psi = tk.StringVar()
        self.E_psi.set(1400000)
        self.E_entry = tk.Entry(self.ref_stud_properties_frame, textvariable=self.E_psi, width=15)
        self.E_entry.grid(row=5, column=2)
        tk.Label(self.ref_stud_properties_frame, text='psi').grid(row=5,column=3)

        #Emin
        self.Emin_label = tk.Label(self.ref_stud_properties_frame,text = 'Emin :')
        self.Emin_label.grid(row=6, column=1)
        self.Emin_psi = tk.StringVar()
        self.Emin_psi.set(510000)
        self.Emin_entry = tk.Entry(self.ref_stud_properties_frame, textvariable=self.Emin_psi, width=15)
        self.Emin_entry.grid(row=6, column=2)
        tk.Label(self.ref_stud_properties_frame, text='psi').grid(row=6,column=3)
        
        #Fc_perp_pl
        self.fc_perp_label = tk.Label(self.ref_stud_properties_frame,text = 'Fc_perp,bottom pl :')
        self.fc_perp_label.grid(row=7, column=1)
        self.fc_perp_psi = tk.StringVar()
        self.fc_perp_psi.set(425)
        self.fc_perp_entry = tk.Entry(self.ref_stud_properties_frame, textvariable=self.fc_perp_psi, width=10)
        self.fc_perp_entry.grid(row=7, column=2)
        tk.Label(self.ref_stud_properties_frame, text='psi').grid(row=7,column=3)
        
        #FRT?
        self.frt_yn = tk.IntVar()
        tk.Checkbutton(self.ref_stud_properties_frame, text=': FRT (y/n)', variable=self.frt_yn).grid(row=1, column=4)
        self.frt_fb_label = tk.Label(self.ref_stud_properties_frame,text = 'Cfrt,fb :')
        self.frt_fb_label.grid(row=2,column=4)
        self.frt_fb = tk.StringVar()
        self.frt_fb.set(1.0)
        self.frt_fb_entry = tk.Entry(self.ref_stud_properties_frame, textvariable=self.frt_fb, width=10)
        self.frt_fb_entry.grid(row=2,column=5)
        self.frt_fv_label = tk.Label(self.ref_stud_properties_frame,text = 'Cfrt,fv :')
        self.frt_fv_label.grid(row=3,column=4)
        self.frt_fv = tk.StringVar()
        self.frt_fv.set(1.0)
        self.frt_fv_entry = tk.Entry(self.ref_stud_properties_frame, textvariable=self.frt_fv, width=10)
        self.frt_fv_entry.grid(row=3,column=5)
        self.frt_fc_label = tk.Label(self.ref_stud_properties_frame,text = 'Cfrt,fc :')
        self.frt_fc_label.grid(row=4,column=4)
        self.frt_fc = tk.StringVar()
        self.frt_fc.set(1.0)
        self.frt_fc_entry = tk.Entry(self.ref_stud_properties_frame, textvariable=self.frt_fc, width=10)
        self.frt_fc_entry.grid(row=4,column=5)
        self.frt_fc_perp_label = tk.Label(self.ref_stud_properties_frame,text = 'Cfrt,fc_perp :')
        self.frt_fc_perp_label.grid(row=5,column=4)
        self.frt_fc_perp = tk.StringVar()
        self.frt_fc_perp.set(1.0)
        self.frt_fc_perp_entry = tk.Entry(self.ref_stud_properties_frame, textvariable=self.frt_fc_perp, width=10)
        self.frt_fc_perp_entry.grid(row=5,column=5)
        self.frt_E_label = tk.Label(self.ref_stud_properties_frame,text = 'Cfrt,E :')
        self.frt_E_label.grid(row=6,column=4)
        self.frt_E = tk.StringVar()
        self.frt_E.set(1.0)
        self.frt_E_entry = tk.Entry(self.ref_stud_properties_frame, textvariable=self.frt_E, width=10)
        self.frt_E_entry.grid(row=6,column=5)
        self.frt_Emin_label = tk.Label(self.ref_stud_properties_frame,text = 'Cfrt,Emin :')
        self.frt_Emin_label.grid(row=7,column=4)
        self.frt_Emin = tk.StringVar()
        self.frt_Emin.set(1.0)
        self.frt_Emin_entry = tk.Entry(self.ref_stud_properties_frame, textvariable=self.frt_Emin, width=10)
        self.frt_Emin_entry.grid(row=7,column=5)         
        
        self.species_label = tk.Label(self.ref_stud_properties_frame,text = 'Species :')
        self.species_label.grid(row=8,column=1)
        self.species = tk.StringVar()
        self.species.set('Spruce-Pine-Fur')
        self.species_entry = tk.Entry(self.ref_stud_properties_frame, textvariable=self.species, width=50)
        self.species_entry.grid(row=8,column=2,columnspan=3)
        
        self.ref_stud_properties_frame.pack(fill=tk.X, padx=5, pady=5)
        
        self.enviro_treatment_frame = tk.LabelFrame(self.input_frame, text="Enviroment and Treatment : ", bd=2, relief='sunken', padx=5, pady=5)
        
        #Moisture %
        self.moisture_label = tk.Label(self.enviro_treatment_frame,text = 'Moisture % :')
        self.moisture_label.grid(row=1,column=1)
        self.moisture = tk.StringVar()
        self.moisture.set(19.0)
        self.moisture_entry = tk.Entry(self.enviro_treatment_frame, textvariable=self.moisture, width=10)
        self.moisture_entry.grid(row=1,column=2)   
        
        #Temp F
        self.temp_label = tk.Label(self.enviro_treatment_frame,text = 'Temperature (F) - <= 150 :')
        self.temp_label.grid(row=2,column=1)
        self.temp = tk.StringVar()
        self.temp.set(90.0)
        self.temp_entry = tk.Entry(self.enviro_treatment_frame, textvariable=self.temp, width=10)
        self.temp_entry.grid(row=2,column=2)
        
        #Incised?
        self.incised_yn = tk.IntVar()
        tk.Checkbutton(self.enviro_treatment_frame, text=': Incised (y/n)', variable=self.incised_yn).grid(row=3, column=1)       
        
        self.enviro_treatment_frame.pack(fill=tk.X, padx=5, pady=5)

        self.lateral_frame = tk.LabelFrame(self.input_frame, text="Lateral Pressure : ", bd=2, relief='sunken', padx=5, pady=5) 
        
        #Pressure
        self.pressure_label = tk.Label(self.lateral_frame,text = 'Pressure (psf) :')
        self.pressure_label.grid(row=1,column=1)
        self.pressure = tk.StringVar()
        self.pressure_entry = tk.Entry(self.lateral_frame, textvariable=self.pressure, width=10)
        self.pressure_entry.grid(row=1,column=2)
        
        #Cd
        self.cd_label = tk.Label(self.lateral_frame,text = 'Cd :')
        self.cd_label.grid(row=2,column=1)
        self.cd = tk.StringVar()
        self.cd.set('0.9')
        cds = ['0.9','1.0','1.15','1.25','1.6','2.0']
        self.cd_selection = tk.OptionMenu(self.lateral_frame, self.cd, *cds)
        self.cd_selection.grid(row=2, column=2)
        
        #Min Eccentricity?
        self.min_ecc_yn = tk.IntVar()
        tk.Checkbutton(self.lateral_frame, text=': Min. Eccentricty of d/6 (y/n)', variable=self.min_ecc_yn).grid(row=3, column=1) 
        self.lateral_frame.pack(fill=tk.X, padx=5, pady=5)
        
        self.b_run = tk.Button(self.input_frame,text="Calc", command=self.run, font=helv)
        self.b_run.pack(side=tk.RIGHT)
        self.b_build_chart = tk.Button(self.input_frame,text="Build P-Lateral Pressure Chart", command=self.generate_interaction_graph, font=helv, state = tk.DISABLED)
        self.b_build_chart.pack(side=tk.RIGHT)
        self.b_build_pm = tk.Button(self.input_frame,text="Build P-M Chart", command=self.generate_pm_graph, font=helv, state = tk.DISABLED)
        self.b_build_pm.pack(side=tk.RIGHT) 
        
        self.input_frame.pack(side=tk.LEFT, padx=5, pady=5)
                
        #results frame
        self.results_frame = tk.LabelFrame(self.pg1_frame, text="Results", bd=2, relief='sunken', padx=5, pady=5)
        self.nds_table_frame = tk.LabelFrame(self.results_frame, text="NDS 2005 - Table 4.3.1", bd=2, relief='sunken', padx=5, pady=5)
        self.res_labels = []
        self.res_nds_table_output = []
        for y in range(0,7):
            for i in range(0,16):
                label = tk.Label(self.nds_table_frame, text='--')
                label.grid(row=y+1,column=i+1)
                self.res_labels.append(label)
                self.res_nds_table_output.append('-')
        self.res_labels[0].configure(text='')
        self.res_nds_table_output[0] = ''
        self.res_labels[1].configure(text='')
        self.res_nds_table_output[1] = ','
        self.res_labels[14].configure(text='')
        self.res_nds_table_output[14] = ','
        self.res_labels[15].configure(text='')
        self.res_nds_table_output[15] = '\n'
        factors = ['Cd','Cm','Ct','CL','Cf','Cfu','Ci','Cr','Cp','CT','Cb','Cfrt']
        i=2
        for c in factors:
            self.res_labels[i].configure(text=c)
            self.res_nds_table_output[i] = c
            i+=1
        row_headers = ["Fb' = Fb ","Fv' = Fv ","Fc' = Fc ","Fc_perp' = Fc_perp ","E' = E ","Emin' = Emin "]
        i=16
        for header in row_headers:
            self.res_labels[i].configure(text=header)
            self.res_nds_table_output[i] = header
            i+=16
        
        i=31
        for y in range(1,7):
            self.res_labels[i].configure(text='psi')
            self.res_nds_table_output[i] = 'psi\n'
            i+=16
        self.nds_table_frame.pack(side=tk.TOP, padx=5, pady=5)
        
        ## Text Results Frame
        self.text_results_frame = tk.LabelFrame(self.results_frame, text="Calculation Results: ", bd=2, relief='sunken', padx=2, pady=2, font=helv)

        self.results_text_box = tk.Text(self.text_results_frame, height = 10, width = 10, bg= "grey90", font= tkFont.Font(family='Helvetica',size=8, weight='normal'), wrap=tk.WORD)
        self.results_text_box.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.text_results_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        self.b_output_res= tk.Button(self.results_frame,text="Export Results", command=self.write_text_results_to_file, font=helv, state = tk.DISABLED)
        self.b_output_res.pack(side=tk.RIGHT)
        self.b_output_pp= tk.Button(self.results_frame,text="Export P-Pressure Curves", command=self.print_pp_graph_common, font=helv, state = tk.DISABLED)
        self.b_output_pp.pack(side=tk.RIGHT)
        self.b_output_pm= tk.Button(self.results_frame,text="Export P-M Curves", command=self.print_pm_graph_common, font=helv, state = tk.DISABLED)
        self.b_output_pm.pack(side=tk.RIGHT)
        self.results_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        #Tab 2 -P vs Pressure Curve
        self.page2 = ttk.Frame(self.nb)
        self.nb.add(self.page2, text='P-Lateral Pressure Diagram', state = tk.DISABLED)
        
        self.pg2_frame = tk.Frame(self.page2, bd=2, relief='sunken', padx=1,pady=1)
        self.pg2_frame.pack(fill=tk.BOTH, padx=5, pady=5)
        
        self.chart_frame = tk.Frame(self.pg2_frame, padx=5, pady=5)

        self.Fig = matplotlib.figure.Figure(figsize=(12,6),dpi=96)
        self.ax1 = self.Fig.add_subplot(111)
        self.ax1.minorticks_on()
        self.ax1.grid(b=True, which='major', color='k', linestyle='-', alpha=0.3)
        self.ax1.grid(b=True, which='minor', color='g', linestyle='-', alpha=0.1)
        self.ax2=self.ax1.twinx()
        #Prebuild chart lines so data can be refreshed to cut down on render time
        #['0.9','1.0','1.15','1.25','1.6','2.0']
        self.line_cd009, = self.ax1.plot([0,10],[10,0], label='Cd = 0.9')
        self.line_cd100, = self.ax1.plot([0,15],[15,0], label='Cd = 1.0')
        self.line_cd115, = self.ax1.plot([0,25],[25,0], label='Cd = 1.15')
        self.line_cd125, = self.ax1.plot([0,35],[35,0], label='Cd = 1.25')
        self.line_cd160, = self.ax1.plot([0,50],[50,0], label='Cd = 1.6')
        self.line_cd200, = self.ax1.plot([0,75],[75,0], label='Cd = 2.0')
        self.line_pl_cb, = self.ax1.plot([0,10],[3,3], label='PL Crushing')
        self.line_pl_wo_cb, = self.ax1.plot([0,10],[1.5,1.5], label='PL Crushing w/o Cb')
        self.line_delta_cd009, = self.ax2.plot([0,10],[0,13], label='D - Cd = 0.9')
        self.line_delta_cd100, = self.ax2.plot([0,15],[15,0], label='D - Cd = 1.0')
        self.line_delta_cd115, = self.ax2.plot([0,25],[25,0], label='D - Cd = 1.15')
        self.line_delta_cd125, = self.ax2.plot([0,35],[35,0], label='D - Cd = 1.25')
        self.line_delta_cd160, = self.ax2.plot([0,50],[50,0], label='D - Cd = 1.6')
        self.line_delta_cd200, = self.ax2.plot([0,75],[75,0], label='D - Cd = 2.0')
        self.line_delta_180, = self.ax2.plot([6,6],[0,13], label='H/180', linestyle=':')
        self.line_delta_240, = self.ax2.plot([4,4],[0,13], label='H/240', linestyle=':')
        self.line_delta_360, = self.ax2.plot([1,1],[0,13], label='H/360', linestyle=':')
        self.line_delta_600, = self.ax2.plot([1,1],[0,13], label='H/600', linestyle=':')
        
        self.legend_ax1 = self.ax1.legend(loc=1, fontsize='x-small')
        self.legend_ax2 = self.ax2.legend(loc=4, fontsize='x-small')        
        
        self.ax1.set_ylabel('Axial (lbs)')
        self.ax1.set_xlabel('Lateral Pressure (psf)')
        self.ax2.set_ylabel('Mid Height Deflection (in)')
        
        self.canvas = matplotlib.backends.backend_tkagg.FigureCanvasTkAgg(self.Fig, master=self.chart_frame)
        self.canvas.show()
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        self.toolbar = NavigationToolbar2TkAgg(self.canvas, self.chart_frame)
        self.toolbar.update()
        self.canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        self.chart_frame.pack(side=tk.TOP, fill=tk.BOTH)
        
        #Tab 3 -P vs M Curve
        self.page3 = ttk.Frame(self.nb)
        self.nb.add(self.page3, text='P-M Diagram', state = tk.DISABLED)
        
        self.pg3_frame = tk.Frame(self.page3, bd=2, relief='sunken', padx=1,pady=1)
        self.pg3_frame.pack(fill=tk.BOTH, padx=5, pady=5)
        
        self.chart_frameB = tk.Frame(self.pg3_frame, padx=5, pady=5)

        self.FigB = matplotlib.figure.Figure(figsize=(12,6),dpi=96)
        self.ax1B = self.FigB.add_subplot(111)
        self.ax1B.minorticks_on()
        self.ax1B.grid(b=True, which='major', color='k', linestyle='-', alpha=0.3)
        self.ax1B.grid(b=True, which='minor', color='g', linestyle='-', alpha=0.1)
        self.ax2B=self.ax1B.twinx()
        #Prebuild chart lines so data can be refreshed to cut down on render time
        #['0.9','1.0','1.15','1.25','1.6','2.0']
        self.line_cd009B, = self.ax1B.plot([0,10],[10,0], label='Cd = 0.9')
        self.line_cd100B, = self.ax1B.plot([0,15],[15,0], label='Cd = 1.0')
        self.line_cd115B, = self.ax1B.plot([0,25],[25,0], label='Cd = 1.15')
        self.line_cd125B, = self.ax1B.plot([0,35],[35,0], label='Cd = 1.25')
        self.line_cd160B, = self.ax1B.plot([0,50],[50,0], label='Cd = 1.6')
        self.line_cd200B, = self.ax1B.plot([0,75],[75,0], label='Cd = 2.0')
        self.line_pl_cbB, = self.ax1B.plot([0,10],[3,3], label='PL Crushing')
        self.line_pl_wo_cbB, = self.ax1B.plot([0,10],[1.5,1.5], label='PL Crushing w/o Cb')
        self.line_delta_cd009B, = self.ax2B.plot([0,10],[0,13], label='D - Cd = 0.9')
        self.line_delta_cd100B, = self.ax2B.plot([0,15],[15,0], label='D - Cd = 1.0')
        self.line_delta_cd115B, = self.ax2B.plot([0,25],[25,0], label='D - Cd = 1.15')
        self.line_delta_cd125B, = self.ax2B.plot([0,35],[35,0], label='D - Cd = 1.25')
        self.line_delta_cd160B, = self.ax2B.plot([0,50],[50,0], label='D - Cd = 1.6')
        self.line_delta_cd200B, = self.ax2B.plot([0,75],[75,0], label='D - Cd = 2.0')
        self.line_delta_180B, = self.ax2B.plot([6,6],[0,13], label='H/180', linestyle=':')
        self.line_delta_240B, = self.ax2B.plot([4,4],[0,13], label='H/240', linestyle=':')
        self.line_delta_360B, = self.ax2B.plot([1,1],[0,13], label='H/360', linestyle=':')
        self.line_delta_600B, = self.ax2B.plot([1,1],[0,13], label='H/600', linestyle=':')

        
        self.legend_ax1B = self.ax1B.legend(loc=1, fontsize='x-small')
        self.legend_ax2B = self.ax2B.legend(loc=4, fontsize='x-small')        
        
        self.ax1B.set_ylabel('Axial (lbs)')
        self.ax1B.set_xlabel('Moment (in-lbs)')
        self.ax2B.set_ylabel('Mid Height Deflection (in)')
        
        self.canvasB = matplotlib.backends.backend_tkagg.FigureCanvasTkAgg(self.FigB, master=self.chart_frameB)
        self.canvasB.show()
        self.canvasB.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        self.toolbarB = NavigationToolbar2TkAgg(self.canvasB, self.chart_frameB)
        self.toolbarB.update()
        self.canvasB._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        self.chart_frameB.pack(side=tk.TOP, fill=tk.BOTH)
        
        self.b_quit = tk.Button(self.base_frame,text="Quit", command=self.quit_app, font=helv)
        self.b_quit.pack(side=tk.RIGHT)
        self.b_save = tk.Button(self.base_frame,text="Save Inputs", command=self.save_inputs, font=helv, state = tk.DISABLED)
        self.b_save.pack(side=tk.RIGHT)
            
    def quit_app(self):
        self.master.destroy()
        self.master.quit()
        
    def enable_tab2(self):
        self.nb.tab(1,state=tk.NORMAL)
        self.nb.tab(2,state=tk.NORMAL)
    
    def actual_stud_size(self, *event):
        b = float(self.b_nom.get())
        d = float(self.d_nom.get())
        
        self.b_actual = b - 0.5
        if d > 6.0:
            self.d_actual = d - 0.75
        else:
            self.d_actual = d - 0.5
        
        self.b_actual_label.configure(text=self.b_actual)
        self.d_actual_label.configure(text=self.d_actual)
    
    def run(self, *event):
        self.results_text_box.delete(1.0,tk.END)
        self.actual_stud_size()
        self.enable_tab2()
        # (self,b_in=1.5,d_in=3.5,height_ft=10, spacing_in=12, grade="No.2", fb_psi=875, fv_psi= 150, fc_psi=1150, E_psi=1400000, Emin_psi=510000, fc_perp_pl_psi=565, moisture_percent = 19, temp = 90, incised = 0,  num_plates = 0, c_frt=[1,1,1,1,1,1]):
        b = self.b_actual
        d = self.d_actual
        height = float(self.wall_height.get())
        spacing = float(self.stud_spacing.get())
        grade = self.grade.get()
        self.title = '{0}x{1} ({2:.2f}x{3:.2f})- Height:{4} ft - Species: {7} - Grade: {5} - Spacing: {6} in'.format(self.b_nom.get(),self.d_nom.get(),b,d,height,grade,spacing, self.species.get())
        self.results_text_box.insert(tk.END, self.title)
        
        fb = float(self.fb_psi.get())
        fv = float(self.fv_psi.get())
        fc = float(self.fc_psi.get())
        E = float(self.E_psi.get())
        Emin = float(self.Emin_psi.get())
        fc_perp = float(self.fc_perp_psi.get())
        moisture = float(self.moisture.get())
        temp = float(self.temp.get())
        incise = self.incised_yn.get()
        
        sub_plates = self.sub_plates.get()
        if sub_plates == 1:
            num_pl = float(self.num_plates.get())
        else:
            num_pl = 0
            
        frt = self.frt_yn.get()
        if frt ==1:
            cfrt = [float(self.frt_fb.get()),float(self.frt_fv.get()),float(self.frt_fc.get()),float(self.frt_fc_perp.get()),float(self.frt_E.get()),float(self.frt_Emin.get())]
        else:
            cfrt =[1,1,1,1,1,1]
        
        min_ecc = self.min_ecc_yn.get()
        if min_ecc == 1:
            self.e_in = d/6.0
            e_string = ' at min d/6 = {0:.3f} in eccentricity '.format(self.e_in)
        else:
            self.e_in = 0
            e_string =''
        
        self.wall = wood.wood_stud_wall(b,d,height,spacing,grade,fb,fv,fc,E,Emin,fc_perp,moisture,temp,incise,num_pl, cfrt)
        
        pressure_psf = float(self.pressure.get())
        
        self.pressure_moment_inlbs = (((pressure_psf*(self.wall.spacing_in/12.0))*(self.wall.height_in/12.0)**2)/8.0) * 12.0
        self.pressure_shear_lbs = (((pressure_psf*(self.wall.spacing_in/12.0))*(self.wall.height_in/12.0))/2.0)
        
        ##Solve for maximum axial capacity
        cd = float(self.cd.get())
        p_lbs = self.wall.axial_capacity_w_moment(cd,self.pressure_moment_inlbs,self.e_in)
        
        ##Create Text String and write Axial result to text box        
        axial_string = '\n\n-- Pmax,allow = {0:.2f} lbs ({2:.2f} plf) {1} --'.format(p_lbs,e_string, p_lbs/(self.wall.spacing_in/12.0))
        axial_string = axial_string + '\n-- PL Crushing (Cb): {0:.2f} lbs ({2:.2f} plf) --\n-- PL Crushing (w/o Cb): {1:.2f} lbs ({3:.2f} plf) --'.format(self.wall.crushing_limit_lbs,self.wall.crushing_limit_lbs_no_cb,self.wall.crushing_limit_lbs/(self.wall.spacing_in/12.0),self.wall.crushing_limit_lbs_no_cb/(self.wall.spacing_in/12.0))
        common_capacities = self.wall.cap_at_common_spacing(cd,pressure_psf,self.e_in)
        axial_string = axial_string + '\n\n--Common Spacing Capacities--\n' + common_capacities
        self.results_text_box.insert(tk.END, axial_string)
        
        ##Pull Section properties from wall class and write out to results text box
        section_props_string = '\n\n--Section Properties--\nA = {0:.3f} in^2 -- s = {1:.3f} in^3 -- I = {2:.3f} in^4'.format(self.wall.area_in2,self.wall.s_in3,self.wall.I_in4)
        self.results_text_box.insert(tk.END, section_props_string)
        
        #Applied Loads - Axial
        self.loads_string = '\n\n--Applied Loads--\nPressure: {0:.2f} psf x Spacing x 1 ft / 12 in = {1:.2f} plf'.format(pressure_psf,pressure_psf * (spacing/12.0))
        w_plf = pressure_psf * (spacing/12.0)            
        deflection_lat = (5 * (w_plf) * (self.wall.height_in/12)**4)/(384*self.wall.E_prime_psi*self.wall.I_in4)*1728        
        if min_ecc == 1:
            self.ecc_moment_inlbs = p_lbs * self.e_in
            self.ecc_shear_lbs = self.ecc_moment_inlbs / self.wall.height_in
            deflection_axial = (((self.ecc_moment_inlbs)*self.wall.height_in**2)/(16.0*self.wall.E_prime_psi*self.wall.I_in4))
            deflection = deflection_lat + deflection_axial
            applied_shear_string = '\nLateral Shear: {0:.2f} lbs + Gravity Shear: {1:.2f} lbs = Total Shear: {2:.2f} lbs'.format(self.pressure_shear_lbs, self.ecc_shear_lbs,self.pressure_shear_lbs+self.ecc_shear_lbs)
            applied_moment_string = '\nLateral Moment: {0:.2f} in-lbs + Gravity Moment: {1:.2f} in-lbs = Total Moment: {2:.2f} in-lbs'.format(self.pressure_moment_inlbs, self.ecc_moment_inlbs,self.pressure_moment_inlbs+self.ecc_moment_inlbs)
            deflection_string = '\nLateral Delta: {0:.3f} in + Gravity Delta: {1:.3f} in = Delta: {2:.3f} in - H / {3:.1f}'.format(deflection_lat, deflection_axial, deflection, self.wall.height_in/deflection)
        else:
            self.ecc_moment_inlbs = 0.0
            self.ecc_shear_lbs = 0.0
            applied_shear_string = '\nLateral Shear: {0:.2f} lbs'.format(self.pressure_shear_lbs)
            applied_moment_string = '\nLateral Moment: {0:.2f} in-lbs'.format(self.pressure_moment_inlbs)
            deflection_string = '\nLateral Delta: {0:.3f} - H / {1:.1f}'.format(deflection_lat, self.wall.height_in/deflection_lat)
        self.loads_string = self.loads_string + applied_shear_string + applied_moment_string + deflection_string
        self.results_text_box.insert(tk.END, self.loads_string)
        
        ##Stresses
        self.stress_string = '\n\n--Stresses--'
        axial_stress = p_lbs/self.wall.area_in2
        self.stress_string = self.stress_string+'\nfc = P/A = {0:.3f} psi'.format(axial_stress)
        shear = self.pressure_shear_lbs + self.ecc_shear_lbs
        shear_stress = (3.0*shear)/(2.0*b*d)
        self.stress_string = self.stress_string+'\nfv = VQ/Ib = 3V/2bd = {0:.3f} psi'.format(shear_stress)
        moment = self.pressure_moment_inlbs + self.ecc_moment_inlbs
        bending_stress = moment/self.wall.s_in3
        self.stress_string = self.stress_string+'\nfb = Mc/I = M/s = 6M/bd^2 = {0:.3f} psi'.format(bending_stress)
        #Combine ratio per NDS 2005 equation (3.9-3)
        #[fc/Fc]'^2 + fb / Fb' [ 1- (fc / FcE)] <= 1.0
        ratio = (axial_stress/self.wall.fc_prime_psi)**2 + (bending_stress / (self.wall.fb_prime_calc(cd)*(1-(axial_stress/self.wall.fcE_psi))))
        self.stress_string = self.stress_string+"\nCombined Axial+Bending:\n[fc/Fc]'^2 + fb / Fb' [ 1- (fc / FcE)] = {0:.3f} <= 1.0".format(ratio)        
        self.results_text_box.insert(tk.END, self.stress_string)
        
        ##Calculation of Cp
        self.cp_string = '\n\n--Calculation of Cp--'
        self.cp_string=self.cp_string + '\nFc* = reference compression design value parallel to grain multiplied by all applicable adjusment factors except Cp\nFc* = {0:.2f} psi\nc = 0.8 - NDS 2005 3.7.1'.format(self.wall.fc_star_psi)
        self.cp_string=self.cp_string + self.wall.assumptions_ke + self.wall.assumptions_leb
        self.cp_string = self.cp_string + 'Ke * le,d / d = {0:.3f} in < 50'.format(self.wall.height_in/d)
        self.cp_string = self.cp_string + "\nFcE = 0.822 * Emin' / (Le/d)^2 - NDS 2005 Section 3.7.1\nFcE = {0:.3f} psi".format(self.wall.fcE_psi)
        self.cp_string = self.cp_string + "\nCp = ([1 + (FcE / Fc*)] / 2c ) - sqrt[ [1 + (FcE / Fc*) / 2c]^2 - (FcE / Fc*) / c] = {0:.3f} - NDS 2005 Section 3.7.1".format(self.wall.cp)
        self.results_text_box.insert(tk.END, self.cp_string)
        
        ##write out assumption from wall creation - see wood_classes.py
        assumptions_string = self.wall.assumptions + self.wall.assumptions_c+self.wall.assumptions_cp
        self.results_text_box.insert(tk.END, assumptions_string)
        
        ##Fill in reduction factor table
        #Fb
        self.res_labels[17].configure(text='{0:.2f}'.format(fb))
        self.res_nds_table_output[17] = '{0:.2f}'.format(fb)
        self.res_labels[18].configure(text='{0:.2f}'.format(cd))
        self.res_nds_table_output[18] = '{0:.2f}'.format(cd)
        self.res_labels[19].configure(text='{0:.2f}'.format(self.wall.cm_fb))
        self.res_nds_table_output[19] = '{0:.2f}'.format(self.wall.cm_fb)
        self.res_labels[20].configure(text='{0:.2f}'.format(self.wall.ct_fb))
        self.res_nds_table_output[20] = '{0:.2f}'.format(self.wall.ct_fb)
        self.res_labels[21].configure(text='{0:.2f}'.format(self.wall.cl))
        self.res_nds_table_output[21] = '{0:.2f}'.format(self.wall.cl)        
        self.res_labels[22].configure(text='{0:.2f}'.format(self.wall.cf_fb))
        self.res_nds_table_output[22] = '{0:.2f}'.format(self.wall.cf_fb)
        self.res_labels[23].configure(text='{0:.2f}'.format(self.wall.cfu))
        self.res_nds_table_output[23] = '{0:.2f}'.format(self.wall.cfu)
        self.res_labels[24].configure(text='{0:.2f}'.format(self.wall.ci_fb))
        self.res_nds_table_output[24] = '{0:.2f}'.format(self.wall.ci_fb)
        self.res_labels[25].configure(text='{0:.2f}'.format(self.wall.cr))
        self.res_nds_table_output[25] = '{0:.2f}'.format(self.wall.cr)
        self.res_labels[29].configure(text='{0:.2f}'.format(cfrt[0]))
        self.res_nds_table_output[29] = '{0:.2f}'.format(cfrt[0])
        self.res_labels[30].configure(text='{0:.2f}'.format(self.wall.fb_prime_calc(cd)))
        self.res_nds_table_output[30] = '{0:.2f}'.format(self.wall.fb_prime_calc(cd))
        
        #Fv
        self.res_labels[33].configure(text='{0:.2f}'.format(fv))
        self.res_nds_table_output[33] = '{0:.2f}'.format(fv)
        self.res_labels[34].configure(text='{0:.2f}'.format(cd))
        self.res_nds_table_output[34] = '{0:.2f}'.format(cd)
        self.res_labels[35].configure(text='{0:.2f}'.format(self.wall.cm_fv))
        self.res_nds_table_output[35] = '{0:.2f}'.format(self.wall.cm_fv)
        self.res_labels[36].configure(text='{0:.2f}'.format(self.wall.ct_fv))
        self.res_nds_table_output[36] = '{0:.2f}'.format(self.wall.ct_fv)
        self.res_labels[40].configure(text='{0:.2f}'.format(self.wall.ci_fv))
        self.res_nds_table_output[40] = '{0:.2f}'.format(self.wall.ci_fv)
        self.res_labels[45].configure(text='{0:.2f}'.format(cfrt[1]))
        self.res_nds_table_output[45] = '{0:.2f}'.format(cfrt[1])
        self.res_labels[46].configure(text='{0:.2f}'.format(self.wall.fv_prime_psi_cd))
        self.res_nds_table_output[46] = '{0:.2f}'.format(self.wall.fv_prime_psi_cd)
        
        #Fc
        self.res_labels[49].configure(text='{0:.2f}'.format(fc))
        self.res_nds_table_output[49] = '{0:.2f}'.format(fc)
        self.res_labels[50].configure(text='{0:.2f}'.format(cd))
        self.res_nds_table_output[50] = '{0:.2f}'.format(cd)
        self.res_labels[51].configure(text='{0:.2f}'.format(self.wall.cm_fc))
        self.res_nds_table_output[51] = '{0:.2f}'.format(self.wall.cm_fc)
        self.res_labels[52].configure(text='{0:.2f}'.format(self.wall.ct_fc))
        self.res_nds_table_output[52] = '{0:.2f}'.format(self.wall.ct_fc)
        self.res_labels[54].configure(text='{0:.2f}'.format(self.wall.cf_fc))
        self.res_nds_table_output[54] = '{0:.2f}'.format(self.wall.cf_fc)
        self.res_labels[56].configure(text='{0:.2f}'.format(self.wall.ci_fc))
        self.res_nds_table_output[56] = '{0:.2f}'.format(self.wall.ci_fc)
        self.res_labels[58].configure(text='{0:.3f}'.format(self.wall.cp))
        self.res_nds_table_output[58] = '{0:.3f}'.format(self.wall.cp)
        self.res_labels[61].configure(text='{0:.2f}'.format(cfrt[2]))
        self.res_nds_table_output[61] = '{0:.2f}'.format(cfrt[2])
        self.res_labels[62].configure(text='{0:.2f}'.format(self.wall.fc_prime_psi))
        self.res_nds_table_output[62] = '{0:.2f}'.format(self.wall.fc_prime_psi)
        
        #fc_perp
        self.res_labels[65].configure(text='{0:.2f}'.format(fc_perp))
        self.res_nds_table_output[65] = '{0:.2f}'.format(fc_perp)
        self.res_labels[67].configure(text='{0:.2f}'.format(self.wall.cm_fc_perp))
        self.res_nds_table_output[67] = '{0:.2f}'.format(self.wall.cm_fc_perp)
        self.res_labels[68].configure(text='{0:.2f}'.format(self.wall.ct_fc_perp))
        self.res_nds_table_output[68] = '{0:.2f}'.format(self.wall.ct_fc_perp)
        self.res_labels[72].configure(text='{0:.2f}'.format(self.wall.ci_fc_perp))
        self.res_nds_table_output[72] = '{0:.2f}'.format(self.wall.ci_fc_perp)
        self.res_labels[76].configure(text='{0:.2f}'.format(self.wall.cb_fc_perp))
        self.res_nds_table_output[76] = '{0:.2f}'.format(self.wall.cb_fc_perp)
        self.res_labels[77].configure(text='{0:.2f}'.format(cfrt[3]))
        self.res_nds_table_output[77] = '{0:.2f}'.format(cfrt[3])
        self.res_labels[78].configure(text='{0:.2f}'.format(self.wall.fc_perp_pl_prime_psi))
        self.res_nds_table_output[78] = '{0:.2f}'.format(self.wall.fc_perp_pl_prime_psi)
        
        #E
        self.res_labels[81].configure(text='{0:.2f}'.format(E))
        self.res_nds_table_output[81] = '{0:.2f}'.format(E)
        self.res_labels[83].configure(text='{0:.2f}'.format(self.wall.cm_E))
        self.res_nds_table_output[83] = '{0:.2f}'.format(self.wall.cm_E)
        self.res_labels[84].configure(text='{0:.2f}'.format(self.wall.ct_E))
        self.res_nds_table_output[84] = '{0:.2f}'.format(self.wall.ct_E)
        self.res_labels[88].configure(text='{0:.2f}'.format(self.wall.ci_E))
        self.res_nds_table_output[88] = '{0:.2f}'.format(self.wall.ci_E)
        self.res_labels[93].configure(text='{0:.2f}'.format(cfrt[4]))
        self.res_nds_table_output[93] = '{0:.2f}'.format(cfrt[4])
        self.res_labels[94].configure(text='{0:.2f}'.format(self.wall.E_prime_psi))
        self.res_nds_table_output[94] = '{0:.2f}'.format(self.wall.E_prime_psi)
        
        #Emin
        self.res_labels[97].configure(text='{0:.2f}'.format(Emin))
        self.res_nds_table_output[97] = '{0:.2f}'.format(Emin)
        self.res_labels[99].configure(text='{0:.2f}'.format(self.wall.cm_E))
        self.res_nds_table_output[99] = '{0:.2f}'.format(self.wall.cm_E)
        self.res_labels[100].configure(text='{0:.2f}'.format(self.wall.ct_E))
        self.res_nds_table_output[100] = '{0:.2f}'.format(self.wall.ct_E)
        self.res_labels[104].configure(text='{0:.2f}'.format(self.wall.ci_E))
        self.res_nds_table_output[104] = '{0:.2f}'.format(self.wall.ci_E)
        self.res_labels[107].configure(text='{0:.2f}'.format(self.wall.cT))
        self.res_nds_table_output[107] = '{0:.2f}'.format(self.wall.cT)
        self.res_labels[109].configure(text='{0:.2f}'.format(cfrt[5]))
        self.res_nds_table_output[109] = '{0:.2f}'.format(cfrt[5])
        self.res_labels[110].configure(text='{0:.2f}'.format(self.wall.Emin_prime_psi))
        self.res_nds_table_output[110] = '{0:.2f}'.format(self.wall.Emin_prime_psi)
        
        self.b_build_chart.configure(state=tk.NORMAL)
        self.b_build_pm.configure(state=tk.NORMAL)
        self.b_output_res.configure(state=tk.NORMAL)
        self.b_output_pm.configure(state=tk.NORMAL)
        self.b_output_pp.configure(state=tk.NORMAL)
        self.b_save.configure(state=tk.NORMAL)
        
    def generate_interaction_graph(self,*event):        
        e_in = self.e_in
        #Refresh chart data for each Cd
        #Cd - NDS 2005 Table 2.3.2
        #cd = [0.9,1.0,1.15,1.25,1.6,2.0]
        w,p,d = self.wall.wall_interaction_diagram_cd(0.9,e_in,0)
        self.line_cd009.set_data(w,p)
        self.line_delta_cd009.set_data(w,d)
        
        w,p,d = self.wall.wall_interaction_diagram_cd(1.0,e_in,0)
        self.line_cd100.set_data(w,p)
        self.line_delta_cd100.set_data(w,d)
        
        w,p,d = self.wall.wall_interaction_diagram_cd(1.15,e_in,0)
        self.line_cd115.set_data(w,p)
        self.line_delta_cd115.set_data(w,d)
        
        w,p,d = self.wall.wall_interaction_diagram_cd(1.25,e_in,0)
        self.line_cd125.set_data(w,p)
        self.line_delta_cd125.set_data(w,d)
        
        w,p,d = self.wall.wall_interaction_diagram_cd(1.6,e_in,0)
        self.line_cd160.set_data(w,p)
        self.line_delta_cd160.set_data(w,d)
        
        w,p,d = self.wall.wall_interaction_diagram_cd(2.0,e_in,0)
        self.line_cd200.set_data(w,p)
        self.line_delta_cd200.set_data(w,d)
        
        if (self.wall.crushing_limit_lbs/(self.wall.spacing_in/12.0)) > 1.2*max(p):
            self.line_pl_cb.set_data([0,0],[0,0])
            self.line_pl_wo_cb.set_data([0,0],[0,0])        
        else:
            self.line_pl_cb.set_data([0,max(w)],[self.wall.crushing_limit_lbs/(self.wall.spacing_in/12.0),self.wall.crushing_limit_lbs/(self.wall.spacing_in/12.0)])
            self.line_pl_wo_cb.set_data([0,max(w)],[self.wall.crushing_limit_lbs_no_cb/(self.wall.spacing_in/12.0),self.wall.crushing_limit_lbs_no_cb/(self.wall.spacing_in/12.0)])
        
        self.line_delta_180.set_data([0,max(w)],[self.wall.height_in/180.0,self.wall.height_in/180.0])
        self.line_delta_240.set_data([0,max(w)],[self.wall.height_in/240.0,self.wall.height_in/240.0])
        self.line_delta_360.set_data([0,max(w)],[self.wall.height_in/360.0,self.wall.height_in/360.0])
        self.line_delta_600.set_data([0,max(w)],[self.wall.height_in/600.0,self.wall.height_in/600.0])
        
        self.ax1.set_xlim(0, max(w)+20)
        self.ax1.set_ylim(0, max(p)+200)
        self.ax2.set_ylim(0, max(d)+0.75)
        
        min_ecc = self.min_ecc_yn.get()
        if min_ecc == 1:
            e_string = ' at min d/6 = {0:.3f} in eccentricity '.format(self.e_in)
        else:
            e_string =''        
        
        self.ax1.set_ylabel('Axial (plf)'+e_string)
        
        self.ax1.set_title(self.title)
        self.canvas.draw()
        
    def generate_pm_graph(self,*event):        
        e_in = self.e_in
        #Refresh chart data for each Cd
        #Cd - NDS 2005 Table 2.3.2
        #cd = [0.9,1.0,1.15,1.25,1.6,2.0]
        w,p,d = self.wall.wall_pm_diagram_cd(0.9,e_in,0)
        self.line_cd009B.set_data(w,p)
        self.line_delta_cd009B.set_data(w,d)
        
        w,p,d = self.wall.wall_pm_diagram_cd(1.0,e_in,0)
        self.line_cd100B.set_data(w,p)
        self.line_delta_cd100B.set_data(w,d)
        
        w,p,d = self.wall.wall_pm_diagram_cd(1.15,e_in,0)
        self.line_cd115B.set_data(w,p)
        self.line_delta_cd115B.set_data(w,d)
        
        w,p,d = self.wall.wall_pm_diagram_cd(1.25,e_in,0)
        self.line_cd125B.set_data(w,p)
        self.line_delta_cd125B.set_data(w,d)
        
        w,p,d = self.wall.wall_pm_diagram_cd(1.6,e_in,0)
        self.line_cd160B.set_data(w,p)
        self.line_delta_cd160B.set_data(w,d)
        
        w,p,d = self.wall.wall_pm_diagram_cd(2.0,e_in,0)
        self.line_cd200B.set_data(w,p)
        self.line_delta_cd200B.set_data(w,d)
        
        if (self.wall.crushing_limit_lbs/(self.wall.spacing_in/12.0)) > 1.2*max(p):
            self.line_pl_cbB.set_data([0,0],[0,0])
            self.line_pl_wo_cbB.set_data([0,0],[0,0])        
        else:
            self.line_pl_cbB.set_data([0,max(w)],[self.wall.crushing_limit_lbs/(self.wall.spacing_in/12.0),self.wall.crushing_limit_lbs/(self.wall.spacing_in/12.0)])
            self.line_pl_wo_cbB.set_data([0,max(w)],[self.wall.crushing_limit_lbs_no_cb/(self.wall.spacing_in/12.0),self.wall.crushing_limit_lbs_no_cb/(self.wall.spacing_in/12.0)])
        
        self.line_delta_180B.set_data([0,max(w)],[self.wall.height_in/180.0,self.wall.height_in/180.0])
        self.line_delta_240B.set_data([0,max(w)],[self.wall.height_in/240.0,self.wall.height_in/240.0])
        self.line_delta_360B.set_data([0,max(w)],[self.wall.height_in/360.0,self.wall.height_in/360.0])
        self.line_delta_600B.set_data([0,max(w)],[self.wall.height_in/600.0,self.wall.height_in/600.0])
        
        self.ax1B.set_xlim(0, max(w)+500)
        self.ax1B.set_ylim(0, max(p)+200)
        self.ax2B.set_ylim(0, max(d)+0.75)
        
        min_ecc = self.min_ecc_yn.get()
        if min_ecc == 1:
            e_string = ' at min d/6 = {0:.3f} in eccentricity '.format(self.e_in)
        else:
            e_string =''        
        
        self.ax1B.set_ylabel('Axial (plf)'+e_string)
        
        self.ax1B.set_title(self.title)
        self.canvasB.draw()
    
    def path_exists(self,path):
        res_folder_exist = os.path.isdir(path)

        if res_folder_exist is False:

            os.makedirs(path)

        else:
            pass

        return 'Directory created'
        
    def save_inputs(self,*event):
        self.run()        
        ##Create a file containing user inputs to be read back in
        #all inputs are single values so write a single input per line
        string = ''
        #Gather inputs
        #geometry
        b = self.b_nom.get()
        string = string + '{0}\n'.format(b)
        d = self.d_nom.get()
        string = string + '{0}\n'.format(d)
        spacing = self.stud_spacing.get()
        string = string + '{0}\n'.format(spacing)
        h = self.wall_height.get()
        string = string + '{0}\n'.format(h)
        sub_pl = self.sub_plates.get()
        string = string + '{0}\n'.format(sub_pl)
        plates = self.num_plates.get()
        string = string + '{0}\n'.format(plates)
        
        #Reference Stud Values
        grade = self.grade.get()
        string = string + '{0}\n'.format(grade)

        #Fb
        fb = self.fb_psi.get()
        string = string + '{0}\n'.format(fb)
        #Fv
        fv = self.fv_psi.get()
        string = string + '{0}\n'.format(fv)
        #Fc
        fc = self.fc_psi.get()
        string = string + '{0}\n'.format(fc)
        #E
        E = self.E_psi.get()
        string = string + '{0}\n'.format(E)
        #Emin
        Emin = self.Emin_psi.get()
        string = string + '{0}\n'.format(Emin)        
        #Fc_perp_pl
        fcperp = self.fc_perp_psi.get()
        string = string + '{0}\n'.format(fcperp)       
        #FRT?
        frtyn = self.frt_yn.get()
        string = string + '{0}\n'.format(frtyn)
        frtfb = self.frt_fb.get()
        string = string + '{0}\n'.format(frtfb)
        frtfv = self.frt_fv.get()
        string = string + '{0}\n'.format(frtfv)
        frtfc = self.frt_fc.get()
        string = string + '{0}\n'.format(frtfc)
        frtfperp = self.frt_fc_perp.get()
        string = string + '{0}\n'.format(frtfperp)
        frtE = self.frt_E.get()
        string = string + '{0}\n'.format(frtE)
        frtEmin = self.frt_Emin.get()
        string = string + '{0}\n'.format(frtEmin)
        species = self.species .get()
        string = string + '{0}\n'.format(species)
        #Moisture %
        moist = self.moisture.get()   
        string = string + '{0}\n'.format(moist)       
        #Temp F
        temp= self.temp.get()
        string = string + '{0}\n'.format(temp)        
        #Incised?
        inc = self.incised_yn.get()
        string = string + '{0}\n'.format(inc)
        
        p = self.pressure.get()
        string = string + '{0}\n'.format(p)
        cd = self.cd.get()
        string = string + '{0}\n'.format(cd)
        e = self.min_ecc_yn.get()
        string = string + '{0}\n'.format(e)
        
        label = '{0}x{1}_height-{2}_ft_pressure-{3}_psf_Cd-{4}'.format(b,d,h,p,cd)
        path = os.path.join(os.path.expanduser('~'),'Desktop','RESULTS','Wood_Walls', label)
        self.path_exists(path)
        
        name = label+'_inputs.wdwall'
        
        file = open(os.path.join(path,name),'w')
        file.write(string)
        file.close()
        
    def file_open(self):
        filename = tkFileDialog.askopenfilename()
        in_file = open(filename,'r')
        in_data = in_file.readlines()
        in_file.close()
        
        b = in_data[0].rstrip('\n')
        self.b_nom.set(b)
        d = in_data[1].rstrip('\n')
        self.d_nom.set(d)
        spacing = in_data[2].rstrip('\n')
        self.stud_spacing.set(spacing)
        h = in_data[3].rstrip('\n')
        self.wall_height.set(h)
        sub_pl = in_data[4].rstrip('\n')
        self.sub_plates.set(sub_pl)
        plates = in_data[5].rstrip('\n')
        self.num_plates.set(plates)
        
        #Reference Stud Values
        grade = in_data[6].rstrip('\n')
        self.grade.set(grade)

        #Fb
        fb = in_data[7].rstrip('\n')
        self.fb_psi.set(fb)
        #Fv
        fv = in_data[8].rstrip('\n')
        self.fv_psi.set(fv)
        #Fc
        fc = in_data[9].rstrip('\n')
        self.fc_psi.set(fc)
        #E
        E = in_data[10].rstrip('\n')
        self.E_psi.set(E)

        #Emin
        Emin = in_data[11].rstrip('\n')
        self.Emin_psi.set(Emin)        
        #Fc_perp_pl
        fcperp = in_data[12].rstrip('\n')
        self.fc_perp_psi.set(fcperp)
       
        #FRT?
        frtyn = in_data[13].rstrip('\n')
        self.frt_yn.set(frtyn)

        frtfb = in_data[14].rstrip('\n')
        self.frt_fb.set(frtfb)

        frtfv = in_data[15].rstrip('\n')
        self.frt_fv.set(frtfv)

        frtfc = in_data[16].rstrip('\n')
        self.frt_fc.set(frtfc)

        frtfperp = in_data[17].rstrip('\n')
        self.frt_fc_perp.set(frtfperp)

        frtE = in_data[18].rstrip('\n')
        self.frt_E.set(frtE)

        frtEmin = in_data[19].rstrip('\n')
        self.frt_Emin.set(frtEmin)

        species = in_data[20].rstrip('\n')
        self.species.set(species)

        #Moisture %
        moist = in_data[21].rstrip('\n')
        self.moisture.set(moist)   
       
        #Temp F
        temp= in_data[22].rstrip('\n')
        self.temp.set(temp)
       
        #Incised?
        inc = in_data[23].rstrip('\n')
        self.incised_yn.set(inc)

        
        p = in_data[24].rstrip('\n')
        self.pressure.set(p)

        cd = in_data[25].rstrip('\n')
        self.cd.set(cd)

        e = in_data[26].rstrip('\n')
        self.min_ecc_yn.set(e)
        
        self.run()
        
    def write_text_results_to_file(self,*event):
        #generate file name and confirm path exists if not create it
        b = self.b_nom.get()
        d = self.d_nom.get()
        h = self.wall_height.get()
        p = self.pressure.get()
        cd = self.cd.get()
        min_ecc = self.min_ecc_yn.get()
        if min_ecc == 1:
            e_string_file = '-Axial_Ecc_Included'
        else:
            e_string_file =''
            
        label = '{0}x{1}_height-{2}_ft_pressure-{3}_psf_Cd-{4}'.format(b,d,h,p,cd)
        path = os.path.join(os.path.expanduser('~'),'Desktop','RESULTS','Wood_Walls', label)
        self.path_exists(path)
        
        name = label+e_string_file+'_results.txt'
        output = self.results_text_box.get(1.0,tk.END)
        file = open(os.path.join(path,name),'w')
        file.write(output)
        file.close()
        
        name_nds_table = label+e_string_file+'_nds_load_factor_table.csv'
        string = ''
        for i in range(len(self.res_nds_table_output)):
            string = string + '{0},'.format(self.res_nds_table_output[i])
        file = open(os.path.join(path,name_nds_table),'w')
        file.write(string)
        file.close()
    
    def print_pm_graph_common(self,*event):
        b = self.b_actual
        d = self.d_actual
        h = self.wall_height.get()
        p = self.pressure.get()
        cd = self.cd.get()
        grade = self.grade.get()
        label = '{0}x{1}_height-{2}_ft_pressure-{3}_psf_Cd-{4}'.format(self.b_nom.get(),self.d_nom.get(),h,p,cd)
        path = os.path.join(os.path.expanduser('~'),'Desktop','RESULTS','Wood_Walls', label,'PvM_Charts')
        self.path_exists(path)
        
        #initialize plot
        pmfig, ax1C = plt.subplots(figsize=(17,11), dpi=600)
        ax1C.minorticks_on()
        ax1C.grid(b=True, which='major', color='k', linestyle='-', alpha=0.3)
        ax1C.grid(b=True, which='minor', color='g', linestyle='-', alpha=0.1)
        ax2C=ax1C.twinx()
        #Prebuild chart lines so data can be refreshed to cut down on render time
        #['0.9','1.0','1.15','1.25','1.6','2.0']
        line_cd009C, = ax1C.plot([0,10],[10,0], label='Cd = 0.9')
        line_cd100C, = ax1C.plot([0,15],[15,0], label='Cd = 1.0')
        line_cd115C, = ax1C.plot([0,25],[25,0], label='Cd = 1.15')
        line_cd125C, = ax1C.plot([0,35],[35,0], label='Cd = 1.25')
        line_cd160C, = ax1C.plot([0,50],[50,0], label='Cd = 1.6')
        line_cd200C, = ax1C.plot([0,75],[75,0], label='Cd = 2.0')
        line_pl_cbC, = ax1C.plot([0,10],[3,3], label='PL Crushing')
        line_pl_wo_cbC, = ax1C.plot([0,10],[1.5,1.5], label='PL Crushing w/o Cb')
        line_delta_cd009C, = ax2C.plot([0,10],[0,13], label='D - Cd = 0.9')
        line_delta_cd100C, = ax2C.plot([0,15],[15,0], label='D - Cd = 1.0')
        line_delta_cd115C, = ax2C.plot([0,25],[25,0], label='D - Cd = 1.15')
        line_delta_cd125C, = ax2C.plot([0,35],[35,0], label='D - Cd = 1.25')
        line_delta_cd160C, = ax2C.plot([0,50],[50,0], label='D - Cd = 1.6')
        line_delta_cd200C, = ax2C.plot([0,75],[75,0], label='D - Cd = 2.0')
        self.line_delta_180C, = ax2C.plot([6,6],[0,13], label='H/180', linestyle=':')
        self.line_delta_240C, = ax2C.plot([4,4],[0,13], label='H/240', linestyle=':')
        self.line_delta_360C, = ax2C.plot([1,1],[0,13], label='H/360', linestyle=':')
        self.line_delta_600C, = ax2C.plot([1,1],[0,13], label='H/600', linestyle=':')

        legend_ax1C = ax1C.legend(loc=1, fontsize='x-small')
        legend_ax2C = ax2C.legend(loc=4, fontsize='x-small')
        
        min_ecc = self.min_ecc_yn.get()
        if min_ecc == 1:
            e_string = ' at min d/6 = {0:.3f} in eccentricity '.format(self.e_in)
            e_string_file = '-Axial_Ecc_Included'
        else:
            e_string =''
            e_string_file =''
            
        ax1C.set_ylabel('Axial (plf)'+e_string)
        ax1C.set_xlabel('Moment (in-lbs)')
        ax2C.set_ylabel('Mid Height Deflection (in)')
        
        
        spacings = [4,6,8,12,16,24]
        for s in spacings:
            file = '{0}x{1}_height-{2}_ft_Spacing_{3}_in-PvM_chart_11x17{4}.pdf'.format(self.b_nom.get(),self.d_nom.get(),h,s,e_string_file)
            title = '{0}x{1} ({2:.2f}x{3:.2f})- Height:{4} ft - Species: {7} - Grade: {5} - Spacing: {6} in'.format(self.b_nom.get(),self.d_nom.get(),self.b_actual,self.d_actual,h,grade,s, self.species.get())
            e_in = self.e_in
            #Refresh chart data for each Cd
            #Cd - NDS 2005 Table 2.3.2
            #cd = [0.9,1.0,1.15,1.25,1.6,2.0]
            w,p,d = self.wall.wall_pm_diagram_cd(0.9,e_in,s)
            line_cd009C.set_data(w,p)
            line_delta_cd009C.set_data(w,d)
            
            w,p,d = self.wall.wall_pm_diagram_cd(1.0,e_in,s)
            line_cd100C.set_data(w,p)
            line_delta_cd100C.set_data(w,d)
            
            w,p,d = self.wall.wall_pm_diagram_cd(1.15,e_in,s)
            line_cd115C.set_data(w,p)
            line_delta_cd115C.set_data(w,d)
            
            w,p,d = self.wall.wall_pm_diagram_cd(1.25,e_in,s)
            line_cd125C.set_data(w,p)
            line_delta_cd125C.set_data(w,d)
            
            w,p,d = self.wall.wall_pm_diagram_cd(1.6,e_in,s)
            line_cd160C.set_data(w,p)
            line_delta_cd160C.set_data(w,d)
            
            w,p,d = self.wall.wall_pm_diagram_cd(2.0,e_in,s)
            line_cd200C.set_data(w,p)
            line_delta_cd200C.set_data(w,d)
            
            if (self.wall.crushing_limit_lbs/(s/12.0)) > 1.2*max(p):
                line_pl_cbC.set_data([0,0],[0,0])
                line_pl_wo_cbC.set_data([0,0],[0,0])        
            else:
                line_pl_cbC.set_data([0,max(w)],[self.wall.crushing_limit_lbs/(s/12.0),self.wall.crushing_limit_lbs/(s/12.0)])
                line_pl_wo_cbC.set_data([0,max(w)],[self.wall.crushing_limit_lbs_no_cb/(s/12.0),self.wall.crushing_limit_lbs_no_cb/(s/12.0)])
            
            self.line_delta_180C.set_data([0,max(w)],[self.wall.height_in/180.0,self.wall.height_in/180.0])
            self.line_delta_240C.set_data([0,max(w)],[self.wall.height_in/240.0,self.wall.height_in/240.0])
            self.line_delta_360C.set_data([0,max(w)],[self.wall.height_in/360.0,self.wall.height_in/360.0])
            self.line_delta_600C.set_data([0,max(w)],[self.wall.height_in/600.0,self.wall.height_in/600.0])
            
            ax1C.set_xlim(0, max(w)+500)
            ax1C.set_ylim(0, max(p)+200)
            ax2C.set_ylim(0, max(d)+0.75)
            
            ax1C.set_title(title)
            
            pmfig.savefig(os.path.join(path,file))
        
        plt.close('all')
        
    def print_pp_graph_common(self,*event):
        b = self.b_actual
        d = self.d_actual
        h = self.wall_height.get()
        p = self.pressure.get()
        cd = self.cd.get()
        grade = self.grade.get()
        label = '{0}x{1}_height-{2}_ft_pressure-{3}_psf_Cd-{4}'.format(self.b_nom.get(),self.d_nom.get(),h,p,cd)
        path = os.path.join(os.path.expanduser('~'),'Desktop','RESULTS','Wood_Walls', label,'PvPressure_Charts')
        self.path_exists(path)
        
        #initialize plot
        pmfig, ax1C = plt.subplots(figsize=(17,11), dpi=600)
        ax1C.minorticks_on()
        ax1C.grid(b=True, which='major', color='k', linestyle='-', alpha=0.3)
        ax1C.grid(b=True, which='minor', color='g', linestyle='-', alpha=0.1)
        ax2C=ax1C.twinx()
        #Prebuild chart lines so data can be refreshed to cut down on render time
        #['0.9','1.0','1.15','1.25','1.6','2.0']
        line_cd009C, = ax1C.plot([0,10],[10,0], label='Cd = 0.9')
        line_cd100C, = ax1C.plot([0,15],[15,0], label='Cd = 1.0')
        line_cd115C, = ax1C.plot([0,25],[25,0], label='Cd = 1.15')
        line_cd125C, = ax1C.plot([0,35],[35,0], label='Cd = 1.25')
        line_cd160C, = ax1C.plot([0,50],[50,0], label='Cd = 1.6')
        line_cd200C, = ax1C.plot([0,75],[75,0], label='Cd = 2.0')
        line_pl_cbC, = ax1C.plot([0,10],[3,3], label='PL Crushing')
        line_pl_wo_cbC, = ax1C.plot([0,10],[1.5,1.5], label='PL Crushing w/o Cb')
        line_delta_cd009C, = ax2C.plot([0,10],[0,13], label='D - Cd = 0.9')
        line_delta_cd100C, = ax2C.plot([0,15],[15,0], label='D - Cd = 1.0')
        line_delta_cd115C, = ax2C.plot([0,25],[25,0], label='D - Cd = 1.15')
        line_delta_cd125C, = ax2C.plot([0,35],[35,0], label='D - Cd = 1.25')
        line_delta_cd160C, = ax2C.plot([0,50],[50,0], label='D - Cd = 1.6')
        line_delta_cd200C, = ax2C.plot([0,75],[75,0], label='D - Cd = 2.0')
        self.line_delta_180C, = ax2C.plot([6,6],[0,13], label='H/180', linestyle=':')
        self.line_delta_240C, = ax2C.plot([4,4],[0,13], label='H/240', linestyle=':')
        self.line_delta_360C, = ax2C.plot([1,1],[0,13], label='H/360', linestyle=':')
        self.line_delta_600C, = ax2C.plot([1,1],[0,13], label='H/600', linestyle=':')

        legend_ax1C = ax1C.legend(loc=1, fontsize='x-small')
        legend_ax2C = ax2C.legend(loc=4, fontsize='x-small')
        
        min_ecc = self.min_ecc_yn.get()
        if min_ecc == 1:
            e_string = ' at min d/6 = {0:.3f} in eccentricity '.format(self.e_in)
            e_string_file = '-Axial_Ecc_Included'
        else:
            e_string =''
            e_string_file =''
            
        ax1C.set_ylabel('Axial (plf)'+e_string)
        ax1C.set_xlabel('Pressure (psf)')
        ax2C.set_ylabel('Mid Height Deflection (in)')
        
        
        spacings = [4,6,8,12,16,24]
        for s in spacings:
            file = '{0}x{1}_height-{2}_ft_Spacing_{3}_in-PvP_chart_11x17{4}.pdf'.format(self.b_nom.get(),self.d_nom.get(),h,s,e_string_file)
            title = '{0}x{1} ({2:.2f}x{3:.2f})- Height:{4} ft - Species: {7} - Grade: {5} - Spacing: {6} in'.format(self.b_nom.get(),self.d_nom.get(),self.b_actual,self.d_actual,h,grade,s, self.species.get())
            e_in = self.e_in
            #Refresh chart data for each Cd
            #Cd - NDS 2005 Table 2.3.2
            #cd = [0.9,1.0,1.15,1.25,1.6,2.0]
            w,p,d = self.wall.wall_interaction_diagram_cd(0.9,e_in,s)
            line_cd009C.set_data(w,p)
            line_delta_cd009C.set_data(w,d)
            
            w,p,d = self.wall.wall_interaction_diagram_cd(1.0,e_in,s)
            line_cd100C.set_data(w,p)
            line_delta_cd100C.set_data(w,d)
            
            w,p,d = self.wall.wall_interaction_diagram_cd(1.15,e_in,s)
            line_cd115C.set_data(w,p)
            line_delta_cd115C.set_data(w,d)
            
            w,p,d = self.wall.wall_interaction_diagram_cd(1.25,e_in,s)
            line_cd125C.set_data(w,p)
            line_delta_cd125C.set_data(w,d)
            
            w,p,d = self.wall.wall_interaction_diagram_cd(1.6,e_in,s)
            line_cd160C.set_data(w,p)
            line_delta_cd160C.set_data(w,d)
            
            w,p,d = self.wall.wall_interaction_diagram_cd(2.0,e_in,s)
            line_cd200C.set_data(w,p)
            line_delta_cd200C.set_data(w,d)
            
            if (self.wall.crushing_limit_lbs/(s/12.0)) > 1.2*max(p):
                line_pl_cbC.set_data([0,0],[0,0])
                line_pl_wo_cbC.set_data([0,0],[0,0])        
            else:
                line_pl_cbC.set_data([0,max(w)],[self.wall.crushing_limit_lbs/(s/12.0),self.wall.crushing_limit_lbs/(s/12.0)])
                line_pl_wo_cbC.set_data([0,max(w)],[self.wall.crushing_limit_lbs_no_cb/(s/12.0),self.wall.crushing_limit_lbs_no_cb/(s/12.0)])
                
            self.line_delta_180C.set_data([0,max(w)],[self.wall.height_in/180.0,self.wall.height_in/180.0])
            self.line_delta_240C.set_data([0,max(w)],[self.wall.height_in/240.0,self.wall.height_in/240.0])
            self.line_delta_360C.set_data([0,max(w)],[self.wall.height_in/360.0,self.wall.height_in/360.0])
            self.line_delta_600C.set_data([0,max(w)],[self.wall.height_in/600.0,self.wall.height_in/600.0])
            
            ax1C.set_xlim(0, max(w)+20)
            ax1C.set_ylim(0, max(p)+200)
            ax2C.set_ylim(0, max(d)+0.75)
            
            ax1C.set_title(title)
            
            pmfig.savefig(os.path.join(path,file))
        
        plt.close('all')
        
def main():            
    root = tk.Tk()
    root.title("Wood Stud Wall - 2-4x Studs - North American Species (Not Southern Pine)")
    Master_window(root)
    root.minsize(1024,768)
    root.mainloop()

if __name__ == '__main__':
    main()   

            
