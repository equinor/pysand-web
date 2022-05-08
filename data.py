def getListOfTuples(dictionary, nestedattribute):
    a = []
    for k, v in dictionary.items():
        pair = (k, v[nestedattribute])
        a.append(pair)
    return a

materialDict = {
                    'carbon_steel':             {'rho_t': 7800, 'K': 2e-9, 'n': 2.6, 'angle_dependency': 'ductile', 'name': 'Carbon Steel'},
                    'duplex':                   {'rho_t': 7850, 'K': 2e-9, 'n': 2.6, 'angle_dependency': 'ductile', 'name': 'Duplex'},
                    'ss316':                    {'rho_t': 8000, 'K': 2e-9, 'n': 2.6, 'angle_dependency': 'ductile', 'name': 'SS316'},
                    'inconel':                  {'rho_t': 8440, 'K': 2e-9, 'n': 2.6, 'angle_dependency': 'ductile', 'name': 'Inconel'},
                    'grp_epoxy':                {'rho_t': 1800, 'K': 3e-10, 'n': 3.6, 'angle_dependency': 'ductile', 'name': 'GRP Epoxy'},
                    'grp_vinyl_ester':          {'rho_t': 1800, 'K': 6e-10, 'n': 3.6, 'angle_dependency': 'ductile', 'name': 'GRP Vinyl Ester'},
                    'hdpe':                     {'rho_t': 1150, 'K': 3.5e-9, 'n': 2.9, 'angle_dependency': 'ductile', 'name': 'HDPE'},
                    'aluminium':                {'rho_t': 2700, 'K': 5.8e-9, 'n': 2.3, 'angle_dependency': 'ductile', 'name': 'Aluminium'},
                    'dc_05_tungsten':           {'rho_t': 15250, 'K': 1.1e-10, 'n': 2.3, 'angle_dependency': 'brittle', 'name': 'DC 05 Tungsten'},
                    'cs_10_tungsten':           {'rho_t': 14800, 'K': 3.2e-10, 'n': 2.2, 'angle_dependency': 'brittle', 'name': 'CS 10 Tungsten'},
                    'cr_37_tungsten':           {'rho_t': 14600, 'K': 8.8e-11, 'n': 2.5, 'angle_dependency': 'brittle', 'name': 'CR 37 Tungsten'},
                    '95_alu_oxide':             {'rho_t': 3700, 'K': 6.8e-8, 'n': 2, 'angle_dependency': 'brittle', 'name': '95 Alu Oxide'},
                    '99_alu_oxide':             {'rho_t': 3700, 'K': 9.5e-7, 'n': 1.2, 'angle_dependency': 'brittle', 'name': '99 Alu Oxide'},
                    'psz_ceramic_zirconia':     {'rho_t': 5700, 'K': 4.1e-9, 'n': 2.5, 'angle_dependency': 'brittle', 'name': 'PSZ Ceramic Zirconia'},
                    'ZrO2-Y3_ceramic_zirconia': {'rho_t': 6070, 'K': 4e-11, 'n': 2.7, 'angle_dependency': 'brittle', 'name': 'Zr02-Y3 Ceramic Zirconia'},
                    'SiC_silicon_carbide':      {'rho_t': 3100, 'K': 6.5e-9, 'n': 1.9, 'angle_dependency': 'brittle', 'name': 'Silicon Carbide'},
                    'Si3N4_silicon_nitride':    {'rho_t': 3200, 'K': 2e-10, 'n': 2, 'angle_dependency': 'brittle', 'name': 'Silicon Nitride'},
                    'TiB2_titanium_diboride':   {'rho_t': 4250, 'K': 9.3e-9, 'n': 1.9, 'angle_dependency': 'brittle', 'name': 'Titanium Diboride'},
                    'B4C_boron_carbide':        {'rho_t': 2500, 'K': 3e-8, 'n': .9, 'angle_dependency': 'brittle', 'name': 'Boron Carbide'},
                    'SiSiC_ceramic_carbide':    {'rho_t': 3100, 'K': 7.4e-11, 'n': 2.7, 'angle_dependency': 'brittle', 'name': 'Ceramic Carbide'}
    }

erosiveAgentDict = {
                    'quartz': {'rho_p': 2650, 'name': 'Quartz sand'}
}

erosionModelsDict = {
                    'bend':             {'name': 'Pipe bends', 'comment': ''},
                    'tee':              {'name': 'Blinded tee', 'comment': ''},
                    'straight_pipe':    {'name': 'Smooth and straight pipes', 'comment': ''},
                    'welded_joint':     {'name': 'Welded joint', 'comment': ''},
                    'manifold':         {'name': 'Manifold', 'comment': ''},
                    'reducer':          {'name': 'Reducer', 'comment': ''},
                    'probes':           {'name': 'Intrusive erosion probes', 'comment': ''},
                    'flexible':         {'name': 'Flexible pipes', 'comment': ''},
                    'choke_gallery':    {'name': 'Choke gallery', 'comment': ''},
                    'nozzlevalve_wall': {
                                        'name':     'Nozzlevalve wall',
                                        'comment':  'This is not an official DNV RP-O501 erosion model. General erosion equation tuned to match CFD results'
                                        },

}

materials_tuples = getListOfTuples(materialDict, 'name')
particles_tuples = getListOfTuples(erosiveAgentDict, 'name')
erosion_models_tuples = getListOfTuples(erosionModelsDict, 'name')