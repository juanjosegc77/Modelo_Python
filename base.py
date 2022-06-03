# -*- coding: utf-8 -*-
__author__ = 'I.B. Juan José Guzmán Cruz'


def getData():


    Bc = {
        'CT': [['recomendado', 0, 200, 1, 1], ['limitrofe', 200, 240, 1, 0], ['alto_riesgo', 240, 400, 0, 0],
               ['mg/dL']],
        'C-LDL': [['recomendado', 0, 130, 1, 1], ['limitrofe', 130, 160, 1, 0.5], ['alto_riesgo', 160, 190, 0.5, 0],
                  ['muy_alto_riesgo', 190, 400, 0, 0], ['mg/dL']],
        'TG': [['recomendado', 0, 150, 1, 1], ['limitrofe', 150, 200, 1, 0.5], ['alto_riesgo', 200, 1000, 0.5, 0],
               ['muy_alto_riesgo', 1000, 1100, 0, 0], ['mg/dL']],
        'C-HDL': [['alto_riesgo', 0, 35, 0, 1], ['recomendado', 35, 70, 1, 1], ['mg/dL']],
        'PCR': [['bajo_riesgo', 0, 1, 1, 1], ['riesgo_promedio', 1, 3, 1, 0.5], ['alto_riesgo', 3, 5, 0.5, 0],
                ['mg/dL']],
        'TSH': [['hipotiroidismo_secundario', 0, 1, 0, 1], ['normal', 1, 4.5, 1, 1],
                ['Hipotiroidismo subclínico', 4.5, 10, 1, 0.5], ['Hipotiroidismo primario', 10, 15.5, 0.5, 0],
                ['ulU/mL']],
        'Vitamina_D': [['deficiencia', 0, 20, 0, 1], ['normal', 20, 100, 1, 1], ['ng/dL']],
        'mcv': [['bajo', 40, 60, 0, 1], ['normal', 80, 95, 1, 1], ['alto', 95, 110, 1, 0], ['fL']],
        'alkphos': [['bajo', 0, 40, 0, 1], ['normal', 40, 129, 1, 1], ['alto', 129, 160, 1, 0], ['U/L']],
        'sgpt': [['bajo', 0, 7, 0, 1], ['normal', 7, 55, 1, 1], ['alto', 55, 200, 1, 0], ['U/L']],
        'sgot': [['bajo', 0, 8, 0, 1], ['normal', 8, 48, 1, 1], ['alto', 48, 100, 1, 0], ['U/L']],
        'gammagt': [['bajo', 0, 8, 0, 1], ['normal', 8, 61, 1, 1], ['alto', 61, 310, 1, 0], ['U/L']]
    }

    '''
    
    Bc = {
        'CT': [['recomendado', 0, 200, 1, 1], ['limitrofe', 200, 240, 1, 0], ['alto_riesgo', 240, 400, 0, 0], ['mg/dL']],
        'C-LDL': [['recomendado', 0, 130, 1, 1], ['limitrofe', 130, 160, 1, 0.5], ['alto_riesgo', 160, 190, 0.5, 0],
                  ['muy_alto_riesgo', 190, 400, 0, 0], ['mg/dL']],
        'TG': [['recomendado', 0, 150, 1, 1], ['limitrofe', 150, 200, 1, 0.5], ['alto_riesgo', 200, 1000, 0.5, 0],
               ['muy_alto_riesgo', 1000, 1100, 0, 0], ['mg/dL']],
        'C-HDL': [['alto_riesgo', 0, 35, 0, 1], ['recomendado', 35, 70, 1, 1], ['mg/dL']],
        'PCR': [['bajo_riesgo', 0, 1, 1, 1], ['riesgo_promedio', 1, 3, 1, 0.5], ['alto_riesgo', 3, 5, 0.5, 0], ['mg/dL']],
        'TSH': [['hipotiroidismo_secundario', 0, 1, 0, 1], ['normal', 1, 4.5, 1, 1],
                ['Hipotiroidismo subclínico', 4.5, 10, 1, 0.5], ['Hipotiroidismo primario', 10, 15.5, 0.5, 0], ['ulU/mL']],
        'Vitamina_D': [['deficiencia', 0, 20, 0, 1], ['normal', 20, 100, 1, 1], ['ng/dL']]
    }

    

    Bc = {
        'mcv': [['bajo', 40, 60, 0, 1], ['normal', 80, 95, 1, 1], ['alto', 95, 110, 1, 0], ['fL']],
        'alkphos': [['bajo', 0, 40, 0, 1], ['normal', 40, 129, 1, 1], ['alto', 129, 160, 1, 0], ['U/L']],
        'sgpt': [['bajo', 0, 7, 0, 1], ['normal', 7, 55, 1, 1], ['alto', 55, 200, 1, 0], ['U/L']],
        'sgot': [['bajo', 0, 8, 0, 1], ['normal', 8, 48, 1, 1], ['alto', 48, 100, 1, 0], ['U/L']],
        'gammagt': [['bajo', 0, 8, 0, 1], ['normal', 8, 61, 1, 1], ['alto', 61, 310, 1, 0], ['U/L']]
    }

    

    Bc = {

        'CT': [['recomendado', 0, 200, 1, 1], ['limitrofe', 200, 240, 1, 0], ['alto_riesgo', 240, 400, 0, 0], ['mg/dL']]
        # 'C-LDL': [['recomendado', 0, 130, 1, 1], ['limitrofe', 130, 160, 1, 0.5], ['alto_riesgo', 160, 190, 0.5, 0],
        #           ['muy_alto_riesgo', 190, 400, 0, 0], ['mg/dL']],
        # 'TG': [['recomendado', 0, 150, 1, 1], ['limitrofe', 150, 200, 1, 0.5], ['alto_riesgo', 200, 1000, 0.5, 0],
        #        ['muy_alto_riesgo', 1000, 1100, 0, 0], ['mg/dL']]
        # 'C-HDL': [['alto_riesgo', 0, 35, 0, 1], ['recomendado', 35, 70, 1, 1], ['mg/dL']]
        # 'PCR': [['bajo_riesgo', 0, 1, 1, 1], ['riesgo_promedio', 1, 3, 1, 0.5], ['alto_riesgo', 3, 5, 0.5, 0], ['mg/dL']]
        # 'TSH': [['hipotiroidismo_secundario', 0, 1, 0, 1], ['normal', 1, 4.5, 1, 1],
        #         ['Hipotiroidismo subclínico', 4.5, 10, 1, 0.5], ['Hipotiroidismo primario', 10, 15.5, 0.5, 0], ['ulU/mL']],
        # 'Vitamina_D': [['deficiencia', 0, 20, 0, 1], ['normal', 20, 100, 1, 1], ['ng/dL']],
        # 'mcv': [['bajo', 40, 60, 0, 1], ['normal', 80, 95, 1, 1], ['alto', 95, 110, 1, 0], ['fL']],
        # 'alkphos': [['bajo', 0, 40, 0, 1], ['normal', 40, 129, 1, 1], ['alto', 129, 160, 1, 0], ['U/L']],
        # 'sgpt': [['bajo', 0, 7, 0, 1], ['normal', 7, 55, 1, 1], ['alto', 55, 200, 1, 0], ['U/L']],
        # 'sgot': [['bajo', 0, 8, 0, 1], ['normal', 8, 48, 1, 1], ['alto', 48, 100, 1, 0], ['U/L']],
        # 'gammagt': [['bajo', 0, 8, 0, 1], ['normal', 8, 61, 1, 1], ['alto', 61, 310, 1, 0], ['U/L']]
    }

    '''

    return Bc