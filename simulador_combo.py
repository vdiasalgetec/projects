import numpy as np

def calcular_custo(produto, tipo, n_alunos, params):
    if tipo == 'cliente':
        if produto == 'conteudo':
            # Cliente pode ter cf ou cv+taxa dependendo do modelo
            if 'cf' in params:
                return params['cf']
            else:
                return n_alunos * params['cv'] + (params['taxa'] if n_alunos > 0 else 0)
        elif produto == 'labs':
            return n_alunos * params['cv'] + (params['taxa'] if n_alunos > 0 else 0)
        elif produto == 'avaliacao':
            if params.get('modelo') == 'interno':
                return params['cf'] + params['custo_questao'] * params['qtd_questoes']
            else:
                return n_alunos * params['cv'] + (params['taxa'] if n_alunos > 0 else 0)
        elif produto == 'lms':
            return n_alunos * params['cv'] + (params['taxa'] if n_alunos > 0 else 0)
    elif tipo == 'proposta':
        return n_alunos * params['cv'] + (params['taxa'] if n_alunos > 0 else 0)
    return 0

def simular_intervalo_alunos(config_cliente, config_proposta, intervalo=(100, 10000, 100)):
    resultados = []
    for n in range(intervalo[0], intervalo[1]+1, intervalo[2]):
        total_cliente = sum(
            calcular_custo(p, 'cliente', n, config_cliente[p]) for p in config_cliente
        )
        total_proposta = sum(
            calcular_custo(p, 'proposta', n, config_proposta[p]) for p in config_proposta
        )
        resultados.append({
            'alunos': n,
            'cliente': total_cliente,
            'proposta': total_proposta
        })
    return resultados
