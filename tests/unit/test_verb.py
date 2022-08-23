from boaviztapi.service.verbose import verbose_component, verbose_device


def test_verbose_component_cpu_1(complete_cpu_model):
    assert verbose_component(complete_cpu_model) == {
        'core_units': {'source': None, 'status': 'INPUT', 'unit': 'none', 'value': 24},
        'die_size_per_core': {'source': None,
                              'status': 'INPUT',
                              'unit': 'mm2',
                              'value': 0.245},
        'impacts': {'adp': {'unit': 'kgSbeq', 'value': 0.04},
                    'gwp': {'unit': 'kgCO2eq', 'value': 43.4},
                    'pe': {'unit': 'MJ', 'value': 650.0}},
        'units': 2}


def test_verbose_component_cpu_2(incomplete_cpu_model):
    assert verbose_component(incomplete_cpu_model) == {
        'core_units': {'source': None, 'status': 'INPUT', 'unit': 'none', 'value': 12},
        'die_size_per_core': {'source': None,
                              'status': 'COMPLETED',
                              'unit': 'mm2',
                              'value': 0.404},
        'family': {'source': None,
                   'status': 'INPUT',
                   'unit': 'none',
                   'value': 'Skylake'},
        'impacts': {'adp': {'unit': 'kgSbeq', 'value': 0.02},
                    'gwp': {'unit': 'kgCO2eq', 'value': 19.7},
                    'pe': {'unit': 'MJ', 'value': 297.0}},
        'units': 1}


def test_verbose_component_ram(complete_ram_model):
    assert verbose_component(complete_ram_model) == {
        'capacity': {'source': None, 'status': 'INPUT', 'unit': 'GB', 'value': 32},
        'density': {'source': None,
                    'status': 'INPUT',
                    'unit': 'GB/cm2',
                    'value': 1.79},
        'impacts': {'adp': {'unit': 'kgSbeq', 'value': 0.0336},
                    'gwp': {'unit': 'kgCO2eq', 'value': 540.0},
                    'pe': {'unit': 'MJ', 'value': 6720.0}},
        'units': 12}


def test_verbose_component_ssd(empty_ssd_model):
    assert verbose_component(empty_ssd_model) == {
        'capacity': {'source': None, 'status': 'DEFAULT', 'unit': 'GB', 'value': 1000},
        'density': {'source': None,
                    'status': 'DEFAULT',
                    'unit': 'GB/cm2',
                    'value': 48.5},
        'impacts': {'adp': {'unit': 'kgSbeq', 'value': 0.0019},
                    'gwp': {'unit': 'kgCO2eq', 'value': 52.0},
                    'pe': {'unit': 'MJ', 'value': 640.0}},
        'units': 1}


def test_verbose_component_power_supply(empty_power_supply_model):
    assert verbose_component(empty_power_supply_model) == {
        'impacts': {'adp': {'unit': 'kgSbeq', 'value': 0.025},
                    'gwp': {'unit': 'kgCO2eq', 'value': 72.7},
                    'pe': {'unit': 'MJ', 'value': 1050.0}},
        'unit_weight': {'source': None,
                        'status': 'DEFAULT',
                        'unit': 'kg',
                        'value': 2.99},
        'units': 1}


def test_verbose_component_case(blade_case_model):
    assert verbose_component(blade_case_model) == {
        'case_type': {'source': None,
                      'status': 'INPUT',
                      'unit': 'none',
                      'value': 'blade'},
        'impacts': {'adp': {'unit': 'kgSbeq', 'value': 0.0277},
                    'gwp': {'unit': 'kgCO2eq', 'value': 85.9},
                    'pe': {'unit': 'MJ', 'value': 1230.0}},
        'units': 1}


def test_verbose_device_server_1(incomplete_server_model):
    assert verbose_device(incomplete_server_model) == {
        'ASSEMBLY-1': {
                       'impacts': {'adp': {'unit': 'kgSbeq', 'value': 1.41e-06},
                                   'gwp': {'unit': 'kgCO2eq', 'value': 6.68},
                                   'pe': {'unit': 'MJ', 'value': 68.6}},
                       'units': 1},
        'CASE-1': {
                   'impacts': {'adp': {'unit': 'kgSbeq', 'value': 0.0202},
                               'gwp': {'unit': 'kgCO2eq', 'value': 150.0},
                               'pe': {'unit': 'MJ', 'value': 2200.0}},
                   'units': 1},
        'CPU-1': {
                  'core_units': {'source': None,
                                 'status': 'DEFAULT',
                                 'unit': 'none',
                                 'value': 24},
                  'die_size_per_core': {'source': None,
                                        'status': 'DEFAULT',
                                        'unit': 'mm2',
                                        'value': 0.245},
                  'impacts': {'adp': {'unit': 'kgSbeq', 'value': 0.04},
                              'gwp': {'unit': 'kgCO2eq', 'value': 43.4},
                              'pe': {'unit': 'MJ', 'value': 650.0}},
                  'units': 2},
        'MOTHERBOARD-1': {
                          'impacts': {'adp': {'unit': 'kgSbeq', 'value': 0.00369},
                                      'gwp': {'unit': 'kgCO2eq', 'value': 66.1},
                                      'pe': {'unit': 'MJ', 'value': 836.0}},
                          'units': 1},
        'POWER_SUPPLY-1': {
                           'impacts': {'adp': {'unit': 'kgSbeq', 'value': 0.05},
                                       'gwp': {'unit': 'kgCO2eq', 'value': 145.4},
                                       'pe': {'unit': 'MJ', 'value': 2100.0}},
                           'unit_weight': {'source': None,
                                           'status': 'DEFAULT',
                                           'unit': 'kg',
                                           'value': 2.99},
                           'units': 2},
        'RAM-1': {
                  'capacity': {'source': None,
                               'status': 'INPUT',
                               'unit': 'GB',
                               'value': 32},
                  'density': {'source': None,
                              'status': 'INPUT',
                              'unit': 'GB/cm2',
                              'value': 1.79},
                  'impacts': {'adp': {'unit': 'kgSbeq', 'value': 0.0672},
                              'gwp': {'unit': 'kgCO2eq', 'value': 1080.0},
                              'pe': {'unit': 'MJ', 'value': 13440.0}},
                  'units': 24},
        'SSD-1': {
                  'capacity': {'source': None,
                               'status': 'INPUT',
                               'unit': 'GB',
                               'value': 400},
                  'density': {'source': None,
                              'status': 'INPUT',
                              'unit': 'GB/cm2',
                              'value': 50.6},
                  'impacts': {'adp': {'unit': 'kgSbeq', 'value': 0.0011},
                              'gwp': {'unit': 'kgCO2eq', 'value': 24.0},
                              'pe': {'unit': 'MJ', 'value': 293.0}},
                  'units': 1},
        'USAGE': {'impacts': {'adp': {'unit': 'kgSbeq', 'value': 0.000169},
                              'gwp': {'unit': 'kgCO2eq', 'value': 1000.0},
                              'pe': {'unit': 'MJ', 'value': 33800.0}}}}


def test_verbose_device_server_2(dell_r740_model):
    assert verbose_device(dell_r740_model) == {
        'ASSEMBLY-1': {
                       'impacts': {'adp': {'unit': 'kgSbeq', 'value': 1.41e-06},
                                   'gwp': {'unit': 'kgCO2eq', 'value': 6.68},
                                   'pe': {'unit': 'MJ', 'value': 68.6}},
                       'units': 1},
        'CASE-1': {
                   'impacts': {'adp': {'unit': 'kgSbeq', 'value': 0.0202},
                               'gwp': {'unit': 'kgCO2eq', 'value': 150.0},
                               'pe': {'unit': 'MJ', 'value': 2200.0}},
                   'units': 1},
        'CPU-1': {
                  'core_units': {'source': None,
                                 'status': 'INPUT',
                                 'unit': 'none',
                                 'value': 24},
                  'die_size_per_core': {'source': None,
                                        'status': 'INPUT',
                                        'unit': 'mm2',
                                        'value': 0.245},
                  'impacts': {'adp': {'unit': 'kgSbeq', 'value': 0.04},
                              'gwp': {'unit': 'kgCO2eq', 'value': 43.4},
                              'pe': {'unit': 'MJ', 'value': 650.0}},
                  'units': 2},
        'MOTHERBOARD-1': {
                          'impacts': {'adp': {'unit': 'kgSbeq', 'value': 0.00369},
                                      'gwp': {'unit': 'kgCO2eq', 'value': 66.1},
                                      'pe': {'unit': 'MJ', 'value': 836.0}},
                          'units': 1},
        'POWER_SUPPLY-1': {
                           'impacts': {'adp': {'unit': 'kgSbeq', 'value': 0.05},
                                       'gwp': {'unit': 'kgCO2eq', 'value': 145.4},
                                       'pe': {'unit': 'MJ', 'value': 2100.0}},
                           'unit_weight': {'source': None,
                                           'status': 'INPUT',
                                           'unit': 'kg',
                                           'value': 2.99},
                           'units': 2},
        'RAM-1': {
                  'capacity': {'source': None,
                               'status': 'INPUT',
                               'unit': 'GB',
                               'value': 32},
                  'density': {'source': None,
                              'status': 'INPUT',
                              'unit': 'GB/cm2',
                              'value': 1.79},
                  'impacts': {'adp': {'unit': 'kgSbeq', 'value': 0.0336},
                              'gwp': {'unit': 'kgCO2eq', 'value': 540.0},
                              'pe': {'unit': 'MJ', 'value': 6720.0}},
                  'units': 12},
        'SSD-1': {
                  'capacity': {'source': None,
                               'status': 'INPUT',
                               'unit': 'GB',
                               'value': 400},
                  'density': {'source': None,
                              'status': 'INPUT',
                              'unit': 'GB/cm2',
                              'value': 50.6},
                  'impacts': {'adp': {'unit': 'kgSbeq', 'value': 0.0011},
                              'gwp': {'unit': 'kgCO2eq', 'value': 24.0},
                              'pe': {'unit': 'MJ', 'value': 293.0}},
                  'units': 1},
        'USAGE': {'impacts': {'adp': {'unit': 'kgSbeq', 'value': 0.000169},
                              'gwp': {'unit': 'kgCO2eq', 'value': 1000.0},
                              'pe': {'unit': 'MJ', 'value': 33800.0}}}}
