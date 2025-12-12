# LISTA FEITA
from math import (comb, factorial, exp)


# Questão 1. Probabilidade de obter um número ímpar ao jogar um dado
def probabilidade_numero_impar():
    return 3 / 6  # 3 números ímpares em um dado de 6 faces

# Questão 2. Probabilidade de obter dois números iguais ao lançar dois dados
def probabilidade_dados_iguais():
    return 6 / 36  # 6 combinações iguais em 36 totais

# Questão 3. Probabilidade de retirar uma bola azul de um saco
def probabilidade_bola_azul():
    return 3 / 8  # 3 bolas azuis em 8 totais

# Questão 4. Probabilidade de tirar um ás de um baralho de 52 cartas
def probabilidade_tirar_as():
    return 4 / 52  # 4 ases em 52 cartas

# Questão 5. Probabilidade de sair "cara" 3 vezes ao lançar uma moeda 5 vezes
def probabilidade_cara_3_vezes():
    n = 5
    k = 3
    p = 0.5
    return comb(n, k) * (p**k) * ((1-p)**(n-k))

# Questão 6. Probabilidade de conseguir 5 no primeiro lançamento e 4 no segundo
def probabilidade_5_e_4():
    return (1/6) * (1/6)  # Probabilidade de 5 e 4

# Questão 7. Probabilidade de obter pelo menos um 5 em dois lançamentos
def probabilidade_pelo_menos_um_5():
    prob_sem_5 = (5/6) ** 2
    return 1 - prob_sem_5

# Questão 8. Probabilidade de sair 3 vezes o número 5 ao lançar um dado 7 vezes
def probabilidade_dado_3_vezes_5():
    n = 7
    k = 3
    p = 1/6
    return comb(n, k) * (p**k) * ((1-p)**(n-k))

# Questão 9. Probabilidade de ter 3 meninos e 2 meninas em 5 filhos
def probabilidade_meninos_e_meninas():
    n = 5
    k = 3
    p = 0.5
    return comb(n, k) * (p**k) * ((1-p)**(n-k))

# Questão 10. Número máximo de tentativas para abrir o cofre com 3 dígitos distintos
def tentativas_cofre():
    return factorial(10) // factorial(10 - 3)

# Questão 11. Número de anagramas da palavra MATEMATICA
def anagramas_palavra():
    letras = "MATEMATICA"
    total_letras = len(letras)
    count = {char: letras.count(char) for char in set(letras)}
    denominador = 1
    for v in count.values():
        denominador *= factorial(v)
    return factorial(total_letras) // denominador

# Questão 12. Comissões de 2 pessoas entre 5
def comissoes():
    return comb(5, 2)

# Questão 13. Probabilidade de ganhar na Mega-Sena em um jogo simples
def probabilidade_mega_sena():
    total_combinacoes = comb(60, 6)
    return 1 / total_combinacoes

# Questão 14. Probabilidade de escolher uma mulher com nível superior
def probabilidade_mulher_nivel_superior():
    homens = 20
    mulheres = 30
    homens_nivel_superior = homens / 2
    mulheres_nivel_superior = mulheres / 2
    total = homens + mulheres
    return mulheres_nivel_superior / total

# Questão 15. Probabilidade de acertar 2 pênaltis em 5 com 80% de aproveitamento
def probabilidade_penaltis():
    n = 5
    k = 2
    p = 0.8
    return comb(n, k) * (p**k) * ((1-p)**(n-k))

# Questão 16. Probabilidade de a sopa estar salgada
def probabilidade_sopa_salgada():
    prob_salgada = (0.4 * 0.1) + (0.4 * 0.05) + (0.2 * 0.2)
    return prob_salgada

# Questão 17. Probabilidade de a sopa estar salgada, dado que está salgada
def probabilidade_sopa_jose():
    prob_jose = 0.4 * 0.05
    prob_jose_total = (0.4 * 0.05) + (0.4 * 0.1) + (0.2 * 0.2)
    return prob_jose / prob_jose_total

# Questão 18. Diferença entre distribuições de Poisson e Binomial
def diferenca_poisson_binomial():
    return "A distribuição binomial é usada para um número fixo de tentativas, enquanto a Poisson é usada para eventos raros em um intervalo fixo."

# Questão 19. Probabilidade de receber 2 solicitações em média de 5 por hora (distribuição de Poisson)
def probabilidade_solicitacoes_poisson():
    lambda_ = 5
    k = 2
    return (lambda_**k * exp(-lambda_)) / factorial(k)

# Questão 20. Probabilidade de não mais que 2 tubos defeituosos em 10 com 20% de defeitos
def probabilidade_tubos_defeituosos():
    n = 10
    p = 0.2
    probabilidade = sum(comb(n, k) * (p**k) * ((1-p)**(n-k)) for k in range(3))
    return probabilidade

# Execução das funções e impressão dos resultados
if __name__ == "__main__":
    print(f"1. Probabilidade de obter um número ímpar: {probabilidade_numero_impar():.2f}")
    print(f"2. Probabilidade de dois números iguais: {probabilidade_dados_iguais():.2f}")
    print(f"3. Probabilidade de retirar uma bola azul: {probabilidade_bola_azul():.2f}")
    print(f"4. Probabilidade de tirar um ás: {probabilidade_tirar_as():.2f}")
    print(f"5. Probabilidade de sair 'cara' 3 vezes: {probabilidade_cara_3_vezes():.4f}")
    print(f"6. Probabilidade de 5 no primeiro e 4 no segundo: {probabilidade_5_e_4():.4f}")
    print(f"7. Probabilidade de obter pelo menos um 5: {probabilidade_pelo_menos_um_5():.4f}")
    print(f"8. Probabilidade de sair 3 vezes o número 5 em 7 lançamentos: {probabilidade_dado_3_vezes_5():.4f}")
    print(f"9. Probabilidade de ter 3 meninos e 2 meninas: {probabilidade_meninos_e_meninas():.4f}")
    print(f"10. Número máximo de tentativas para abrir o cofre: {tentativas_cofre()}")
    print(f"11. Número de anagramas da palavra MATEMATICA: {anagramas_palavra()}")
    print(f"12. Número de comissões de 2 pessoas: {comissoes()}")
    print(f"13. Probabilidade de ganhar na Mega-Sena: {probabilidade_mega_sena():.10f}")
    print(f"14. Probabilidade de escolher uma mulher com nível superior: {probabilidade_mulher_nivel_superior():.4f}")
    print(f"15. Probabilidade de acertar 2 pênaltis em 5: {probabilidade_penaltis():.4f}")
    print(f"16. Probabilidade de a sopa estar salgada: {probabilidade_sopa_salgada():.4f}")
    print(f"17. Probabilidade de a sopa estar salgada, dado que foi feita por José: {probabilidade_sopa_jose():.4f}")
    print(f"18. Diferença entre distribuições de Poisson e Binomial: {diferenca_poisson_binomial()}")
    print(f"19. Probabilidade de receber 2 solicitações: {probabilidade_solicitacoes_poisson():.4f}")
    print(f"20. Probabilidade de não mais que 2 tubos defeituosos: {probabilidade_tubos_defeituosos():.4f}")
