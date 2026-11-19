/*
 * Sprint 1 e 2 - Sistema de Confiabilidade de Equipamentos
 * Data Structures and Algorithms - Prof. Daniel Gatti - FIAP 1CCPR
 * Desafio Inovacao Aberta Motiva Rodovias & FIAP
 *
 * Integrantes:
 *   Gustavo Fidelis de Souza e Silva - RM 574666
 *   Luan Mantovani Ferreira Neres    - RM 574563
 *   Pedro Henrique de Sa             - RM 576731
 *   Fernando Azevedo Costa           - RM 575676
 *   Rafael Meirelles                 - RM 574897
 *   Anna Luisa Lima                  - RM 575081
 *
 * Modelo exponencial de confiabilidade: R(t) = e^(-lambda * t)
 * Unidades usadas: lambda em falhas por dia e tempo em dias.
 */

#include <iostream>
#include <iomanip>
#include <string>
#include <cmath>
#include <limits>
#include <cstdlib>

using namespace std;

const int QTD = 10;  // quantidade de equipamentos

// ---------- Funcoes de calculo ----------

// Calcula a confiabilidade pelo modelo exponencial
double calcularConfiabilidade(double lambda, double tempo) {
    return exp(-lambda * tempo);
}

// Classifica o equipamento pela faixa de confiabilidade
string classificarEquipamento(double confiabilidade) {
    if (confiabilidade >= 0.90) {
        return "Excelente";
    } else if (confiabilidade >= 0.80) {
        return "Boa";
    } else if (confiabilidade >= 0.60) {
        return "Atencao";
    } else {
        return "Critica";
    }
}

// ---------- Funcoes recursivas ----------

// Opcao A: conta quantos equipamentos sao "Critica" (recursiva)
int contarCriticos(const double conf[], int n) {
    if (n == 0) {
        return 0;                                   // caso base: nenhum equipamento
    }
    int ehCritico = (classificarEquipamento(conf[n - 1]) == "Critica") ? 1 : 0;
    return ehCritico + contarCriticos(conf, n - 1); // chama a si mesma com n - 1
}

// Opcao B: soma as confiabilidades (recursiva), usada para a media
double somarConfiabilidades(const double conf[], int n) {
    if (n == 0) {
        return 0.0;                                 // caso base
    }
    return conf[n - 1] + somarConfiabilidades(conf, n - 1);
}

// Acha o equipamento de maior risco (menor confiabilidade)
int indiceMaiorRisco(const double conf[], int n) {
    int pior = 0;
    for (int i = 1; i < n; i++) {
        if (conf[i] < conf[pior]) {
            pior = i;
        }
    }
    return pior;
}

// ---------- Funcoes de entrada ----------

// Le um numero maior que zero; repete ate o usuario digitar certo
double lerPositivo(const string& pergunta) {
    double valor;
    while (true) {
        cout << pergunta;
        if (cin >> valor && valor > 0) {
            return valor;
        }
        if (cin.eof()) {                       // entrada acabou: encerra sem travar
            cout << "\nEntrada encerrada.\n";
            exit(0);
        }
        cout << "  Valor invalido. Digite um numero maior que zero (use ponto: 0.001).\n";
        cin.clear();
        cin.ignore(numeric_limits<streamsize>::max(), '\n');
    }
}

// Cadastro manual dos 10 equipamentos
void cadastrarManual(string nomes[], double lambdas[], double tempos[]) {
    for (int i = 0; i < QTD; i++) {
        cout << "\n--- Equipamento " << (i + 1) << " de " << QTD << " ---\n";
        cout << "Equipamento (sem espacos, ex.: Camera_01): ";
        if (!(cin >> nomes[i])) {
            cout << "\nEntrada encerrada.\n";
            exit(0);
        }
        lambdas[i] = lerPositivo("Taxa de Falha (falhas por dia, ex.: 0.001): ");
        tempos[i]  = lerPositivo("Tempo de Operacao (dias, ex.: 100): ");
    }
}

// Dados de exemplo: equipamentos de um trecho de rodovia (valores simulados)
void carregarExemplo(string nomes[], double lambdas[], double tempos[]) {
    string n[QTD]  = {"Camera_km412", "Camera_km415", "Camera_km418", "PMV_km410", "PMV_km420",
                      "Callbox_km413", "SAT_km416", "SCA_km410", "Laco_Pista03", "FreeFlow_km421"};
    double l[QTD]  = {0.0010, 0.0020, 0.0008, 0.0005, 0.0030, 0.0004, 0.0012, 0.0006, 0.0050, 0.0007};
    double t[QTD]  = {100, 120, 90, 150, 100, 200, 180, 60, 110, 300};
    for (int i = 0; i < QTD; i++) {
        nomes[i] = n[i];
        lambdas[i] = l[i];
        tempos[i] = t[i];
    }
}

// ---------- Saidas ----------

void exibirRelatorio(const string nomes[], const double lambdas[], const double tempos[],
                     const double conf[], int n) {
    cout << "\n-----------------------------------------\n";
    cout << "RELATORIO DE CONFIABILIDADE\n";
    cout << "-----------------------------------------\n";
    for (int i = 0; i < n; i++) {
        cout << "Equipamento: " << nomes[i] << "\n";
        cout << "Taxa de falha: " << lambdas[i] << " falhas/dia\n";
        cout << "Tempo de operacao: " << tempos[i] << " dias\n";
        cout << "Confiabilidade: " << fixed << setprecision(3) << conf[i] << "\n";
        cout.unsetf(ios::fixed);
        cout << setprecision(6);
        cout << "Classificacao: " << classificarEquipamento(conf[i]) << "\n\n";
    }

    double media = somarConfiabilidades(conf, n) / n;
    int criticos = contarCriticos(conf, n);
    int pior = indiceMaiorRisco(conf, n);

    cout << "-----------------------------------------\n";
    cout << "RESUMO\n";
    cout << "Media das confiabilidades (recursiva): " << fixed << setprecision(3) << media << "\n";
    cout << "Equipamentos criticos (recursiva): " << criticos << " de " << n << "\n";
    cout << "Maior risco de falha: " << nomes[pior] << " (R = " << conf[pior] << ")\n";
    cout.unsetf(ios::fixed);
    cout << setprecision(6);
}

// Bonus: confiabilidade em 30, 60, 90, 180 e 365 dias
void simularPeriodos(const string nomes[], const double lambdas[], int n) {
    int periodos[5] = {30, 60, 90, 180, 365};
    cout << "\n-----------------------------------------\n";
    cout << "SIMULACAO POR PERIODO (BONUS)\n";
    cout << "-----------------------------------------\n";
    for (int i = 0; i < n; i++) {
        cout << nomes[i] << "\n";
        for (int p = 0; p < 5; p++) {
            double r = calcularConfiabilidade(lambdas[i], periodos[p]);
            cout << "  " << setw(3) << periodos[p] << " dias -> " << fixed << setprecision(2) << r
                 << "  (" << classificarEquipamento(r) << ")\n";
            cout.unsetf(ios::fixed);
        }
    }
    cout << setprecision(6);
}

// ---------- Programa principal ----------

int main() {
    string nomes[QTD];
    double lambdas[QTD], tempos[QTD], conf[QTD];

    cout << "SISTEMA DE CONFIABILIDADE DE EQUIPAMENTOS - Motiva x FIAP\n";
    cout << "Modelo: R(t) = e^(-lambda * t)   (lambda em falhas/dia, t em dias)\n\n";

    int opcao = 0;
    while (opcao != 1 && opcao != 2) {
        cout << "1 - Cadastrar os 10 equipamentos\n";
        cout << "2 - Usar dados de exemplo\n";
        cout << "Escolha: ";
        if (!(cin >> opcao) && cin.eof()) {
            cout << "\nEntrada encerrada.\n";
            return 0;
        }
        if (opcao != 1 && opcao != 2) {
            cout << "  Opcao invalida. Digite 1 ou 2.\n\n";
            cin.clear();
            cin.ignore(numeric_limits<streamsize>::max(), '\n');
            opcao = 0;
        }
    }

    if (opcao == 1) {
        cadastrarManual(nomes, lambdas, tempos);
    } else {
        carregarExemplo(nomes, lambdas, tempos);
    }

    for (int i = 0; i < QTD; i++) {
        conf[i] = calcularConfiabilidade(lambdas[i], tempos[i]);
    }

    exibirRelatorio(nomes, lambdas, tempos, conf, QTD);
    simularPeriodos(nomes, lambdas, QTD);

    cout << "\nFim do relatorio.\n";
    return 0;
}
