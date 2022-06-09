from pysand_web.functions import getListOfTuples

transportModelsDict = {
                    'stokes':           {'name': 'Stokes', 'comment': ''},
                    'hydro':            {'name': 'Hydro', 'comment': 'Equinor sand transport model for horizontal pipelines. Based on T. Søntvedt (1995) and R. Schulkes (2002) work in Hydro'}
}

transport_models_tuples =   getListOfTuples(transportModelsDict, 'name')