#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>

#define MAX_HISTORY 100
#define MAX_INPUT 100

// Estrutura para armazenar uma operação realizada
typedef struct {
    char expression[MAX_INPUT];
    double result;
} HistoryEntry;

// Vetor para armazenar histórico e contador
HistoryEntry history[MAX_HISTORY];
int history_count = 0;

// Função para adicionar entrada no histórico
void add_history(const char* expr, double res) {
    if (history_count < MAX_HISTORY) {
        strncpy(history[history_count].expression, expr, MAX_INPUT-1);
        history[history_count].expression[MAX_INPUT-1] = '\0';
        history[history_count].result = res;
        history_count++;
    } else {
        // Se cheio, remove o mais antigo e insere o novo no fim
        for (int i=1; i < MAX_HISTORY; i++) {
            history[i-1] = history[i];
        }
        strncpy(history[MAX_HISTORY-1].expression, expr, MAX_INPUT-1);
        history[MAX_HISTORY-1].expression[MAX_INPUT-1] = '\0';
        history[MAX_HISTORY-1].result = res;
    }
}

// Funções matemáticas suportadas

double calc_add(double a, double b) {
    return a + b;
}

double calc_subtract(double a, double b) {
    return a - b;
}

double calc_multiply(double a, double b) {
    return a * b;
}

double calc_divide(double a, double b) {
    if (b == 0) {
        printf("Erro: divisão por zero.\n");
        return NAN;
    }
    return a / b;
}

double calc_power(double base, double exponent) {
    return pow(base, exponent);
}

double calc_sqrt(double x) {
    if (x < 0) {
        printf("Erro: raiz quadrada de número negativo.\n");
        return NAN;
    }
    return sqrt(x);
}

double calc_log(double x) {
    if (x <= 0) {
        printf("Erro: logaritmo de número não positivo.\n");
        return NAN;
    }
    return log10(x);
}

double calc_ln(double x) {
    if (x <= 0) {
        printf("Erro: logaritmo natural de número não positivo.\n");
        return NAN;
    }
    return log(x);
}

double calc_sin(double x) {
    return sin(x);
}

double calc_cos(double x) {
    return cos(x);
}

double calc_tan(double x) {
    return tan(x);
}

// Mostra histórico
void print_history() {
    printf("\n--- Histórico ---\n");
    for(int i=0; i<history_count; i++) {
        printf("%d: %s = %.10g\n", i+1, history[i].expression, history[i].result);
    }
    printf("----------------\n");
}

// Interface textual: mostra opções para usuário
void print_menu() {
    printf("\nCalculadora Científica\n");
    printf("1. Adição (+)\n");
    printf("2. Subtração (-)\n");
    printf("3. Multiplicação (*)\n");
    printf("4. Divisão (/)\n");
    printf("5. Potência (^)\n");
    printf("6. Raiz Quadrada (sqrt)\n");
    printf("7. Logaritmo base 10 (log)\n");
    printf("8. Logaritmo natural (ln)\n");
    printf("9. Seno (sin)\n");
    printf("10. Cosseno (cos)\n");
    printf("11. Tangente (tan)\n");
    printf("12. Mostrar Histórico\n");
    printf("13. Sair\n");
    printf("Escolha a operação: ");
}

// Função para ler um número com tratamento simples de erro
int read_double(const char* prompt, double *val) {
    printf("%s", prompt);
    if (scanf("%lf", val) != 1) {
        while(getchar() != '\n'); // limpar buffer
        printf("Entrada inválida.\n");
        return 0;
    }
    while(getchar() != '\n');
    return 1;
}

int main() {
    int option;
    double a, b, res;
    char expr[128];

    while (1) {
        print_menu();
        if(scanf("%d", &option) != 1) {
            printf("Entrada inválida.\n");
            while(getchar() != '\n');
            continue;
        }
        while(getchar() != '\n');

        switch (option) {
            case 1:
                if (!read_double("Digite o primeiro número: ", &a)) break;
                if (!read_double("Digite o segundo número: ", &b)) break;
                res = calc_add(a,b);
                snprintf(expr, sizeof(expr), "%.10g + %.10g", a, b);
                printf("Resultado: %.10g\n", res);
                add_history(expr, res);
                break;
            case 2:
                if (!read_double("Digite o primeiro número: ", &a)) break;
                if (!read_double("Digite o segundo número: ", &b)) break;
                res = calc_subtract(a,b);
                snprintf(expr, sizeof(expr), "%.10g - %.10g", a, b);
                printf("Resultado: %.10g\n", res);
                add_history(expr, res);
                break;
            case 3:
                if (!read_double("Digite o primeiro número: ", &a)) break;
                if (!read_double("Digite o segundo número: ", &b)) break;
                res = calc_multiply(a,b);
                snprintf(expr, sizeof(expr), "%.10g * %.10g", a, b);
                printf("Resultado: %.10g\n", res);
                add_history(expr, res);
                break;
            case 4:
                if (!read_double("Digite o dividendo: ", &a)) break;
                if (!read_double("Digite o divisor: ", &b)) break;
                res = calc_divide(a,b);
                snprintf(expr, sizeof(expr), "%.10g / %.10g", a, b);
                if (!isnan(res)) {
                    printf("Resultado: %.10g\n", res);
                    add_history(expr, res);
                }
                break;
            case 5:
                if (!read_double("Digite a base: ", &a)) break;
                if (!read_double("Digite o expoente: ", &b)) break;
                res = calc_power(a,b);
                snprintf(expr, sizeof(expr), "%.10g ^ %.10g", a, b);
                printf("Resultado: %.10g\n", res);
                add_history(expr, res);
                break;
            case 6:
                if (!read_double("Digite o número: ", &a)) break;
                res = calc_sqrt(a);
                snprintf(expr, sizeof(expr), "sqrt(%.10g)", a);
                if (!isnan(res)) {
                    printf("Resultado: %.10g\n", res);
                    add_history(expr, res);
                }
                break;
            case 7:
                if (!read_double("Digite o número: ", &a)) break;
                res = calc_log(a);
                snprintf(expr, sizeof(expr), "log(%.10g)", a);
                if (!isnan(res)) {
                    printf("Resultado: %.10g\n", res);
                    add_history(expr, res);
                }
                break;
            case 8:
                if (!read_double("Digite o número: ", &a)) break;
                res = calc_ln(a);
                snprintf(expr, sizeof(expr), "ln(%.10g)", a);
                if (!isnan(res)) {
                    printf("Resultado: %.10g\n", res);
                    add_history(expr, res);
                }
                break;
            case 9:
                if (!read_double("Digite o ângulo em radianos: ", &a)) break;
                res = calc_sin(a);
                snprintf(expr, sizeof(expr), "sin(%.10g)", a);
                printf("Resultado: %.10g\n", res);
                add_history(expr, res);
                break;
            case 10:
                if (!read_double("Digite o ângulo em radianos: ", &a)) break;
                res = calc_cos(a);
                snprintf(expr, sizeof(expr), "cos(%.10g)", a);
                printf("Resultado: %.10g\n", res);
                add_history(expr, res);
                break;
            case 11:
                if (!read_double("Digite o ângulo em radianos: ", &a)) break;
                res = calc_tan(a);
                snprintf(expr, sizeof(expr), "tan(%.10g)", a);
                printf("Resultado: %.10g\n", res);
                add_history(expr, res);
                break;
            case 12:
                print_history();
                break;
            case 13:
                printf("Encerrando calculadora.\n");
                return 0;
            default:
                printf("Opção inválida.\n");
        }
    }

    return 0;
}
