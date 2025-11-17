import java.util.*;

class Cliente {
    private String nome;
    private String cpf;
    private String senha;
    private List<Conta> contas = new ArrayList<>();

    public Cliente(String nome, String cpf, String senha) {
        this.nome = nome;
        this.cpf = cpf;
        this.senha = senha;
    }

    public String getNome() { return nome; }
    public String getCpf() { return cpf; }

    public boolean autenticar(String senha) {
        return Objects.equals(this.senha, senha);
    }

    public void adicionarConta(Conta conta) {
        contas.add(conta);
    }

    public List<Conta> getContas() { return contas; }
}

abstract class Conta {
    protected int numero;
    protected double saldo;
    protected Cliente titular;
    protected List<Transacao> transacoes = new ArrayList<>();

    public Conta(int numero, Cliente titular) {
        this.numero = numero;
        this.titular = titular;
        this.saldo = 0.0;
    }

    public int getNumero() { return numero; }
    public double getSaldo() { return saldo; }
    public Cliente getTitular() { return titular; }

    public void depositar(double valor) {
        saldo += valor;
        transacoes.add(new Transacao("Depósito", valor, new Date()));
    }

    public boolean sacar(double valor) {
        if (saldo >= valor) {
            saldo -= valor;
            transacoes.add(new Transacao("Saque", -valor, new Date()));
            return true;
        }
        return false;
    }

    public void transferir(Conta destino, double valor) {
        if (sacar(valor)) {
            destino.depositar(valor);
            transacoes.add(new Transacao("Transferência para conta " + destino.getNumero(), -valor, new Date()));
        }
    }

    public List<Transacao> getTransacoes() { return transacoes; }

    public abstract void aplicarRendimento();
}

class ContaCorrente extends Conta {
    private double limiteChequeEspecial = 500.0;

    public ContaCorrente(int numero, Cliente titular) { super(numero, titular); }

    @Override
    public boolean sacar(double valor) {
        if (saldo + limiteChequeEspecial >= valor) {
            saldo -= valor;
            transacoes.add(new Transacao("Saque", -valor, new Date()));
            return true;
        }
        return false;
    }

    @Override
    public void aplicarRendimento() {
        // Conta corrente não possui rendimento
    }
}

class ContaPoupanca extends Conta {
    public ContaPoupanca(int numero, Cliente titular) { super(numero, titular); }

    @Override
    public void aplicarRendimento() {
        double rendimento = saldo * 0.005; // 0,5% ao mês
        saldo += rendimento;
        transacoes.add(new Transacao("Rendimento Poupança", rendimento, new Date()));
    }
}

class Transacao {
    private String descricao;
    private double valor;
    private Date data;

    public Transacao(String descricao, double valor, Date data) {
        this.descricao = descricao;
        this.valor = valor;
        this.data = data;
    }

    @Override
    public String toString() {
        return "[" + data + "] " + descricao + ": " + String.format("R$ %.2f", valor);
    }
}

class Banco {
    private Map<String, Cliente> clientes = new HashMap<>();
    private Map<Integer, Conta> contas = new HashMap<>();
    private static int proximoNumeroConta = 1001;

    public Cliente cadastrarCliente(String nome, String cpf, String senha) {
        Cliente cliente = new Cliente(nome, cpf, senha);
        clientes.put(cpf, cliente);
        return cliente;
    }

    public Cliente autenticarCliente(String cpf, String senha) {
        Cliente cliente = clientes.get(cpf);
        if (cliente != null && cliente.autenticar(senha)) {
            return cliente;
        }
        return null;
    }

    public ContaCorrente criarContaCorrente(Cliente cliente) {
        ContaCorrente cc = new ContaCorrente(proximoNumeroConta++, cliente);
        contas.put(cc.getNumero(), cc);
        cliente.adicionarConta(cc);
        return cc;
    }

    public ContaPoupanca criarContaPoupanca(Cliente cliente) {
        ContaPoupanca cp = new ContaPoupanca(proximoNumeroConta++, cliente);
        contas.put(cp.getNumero(), cp);
        cliente.adicionarConta(cp);
        return cp;
    }

    public Conta buscarConta(int numero) {
        return contas.get(numero);
    }

    public void aplicarRendimentos() {
        for (Conta conta : contas.values()) {
            conta.aplicarRendimento();
        }
    }

    public List<Cliente> getClientes() { return new ArrayList<>(clientes.values()); }
}

public class SistemaBancarioApp {
    private static Banco banco = new Banco();
    private static Scanner sc = new Scanner(System.in);

    public static void main(String[] args) {
        System.out.println("=== Sistema Bancário OOP ===");

        boolean rodando = true;
        Cliente clienteAtual = null;

        while (rodando) {
            if (clienteAtual == null) {
                System.out.println("1. Cadastrar cliente");
                System.out.println("2. Entrar");
                System.out.println("0. Sair");
                int op = sc.nextInt(); sc.nextLine();

                switch (op) {
                    case 1:
                        System.out.print("Nome: ");
                        String nome = sc.nextLine();
                        System.out.print("CPF: ");
                        String cpf = sc.nextLine();
                        System.out.print("Senha: ");
                        String senha = sc.nextLine();
                        Cliente novoCliente = banco.cadastrarCliente(nome, cpf, senha);
                        System.out.println("Cliente cadastrado!");
                        break;
                    case 2:
                        System.out.print("CPF: ");
                        String cpfLogin = sc.nextLine();
                        System.out.print("Senha: ");
                        String senhaLogin = sc.nextLine();
                        clienteAtual = banco.autenticarCliente(cpfLogin, senhaLogin);
                        if (clienteAtual != null) {
                            System.out.println("Bem-vindo, " + clienteAtual.getNome());
                        } else {
                            System.out.println("Credenciais inválidas.");
                        }
                        break;
                    case 0:
                        rodando = false;
                        System.out.println("Saindo...");
                        break;
                    default:
                        System.out.println("Opção inválida.");
                        break;
                }
            } else {
                System.out.println("1. Criar conta corrente");
                System.out.println("2. Criar conta poupança");
                System.out.println("3. Listar contas");
                System.out.println("4. Acessar conta");
                System.out.println("5. Deslogar");
                int op = sc.nextInt(); sc.nextLine();

                switch (op) {
                    case 1:
                        banco.criarContaCorrente(clienteAtual);
                        System.out.println("Conta corrente criada!");
                        break;
                    case 2:
                        banco.criarContaPoupanca(clienteAtual);
                        System.out.println("Conta poupança criada!");
                        break;
                    case 3:
                        for (Conta c : clienteAtual.getContas()) {
                            System.out.println("Conta #" + c.getNumero() + " - Saldo: R$ " + c.getSaldo());
                        }
                        break;
                    case 4:
                        System.out.print("Número da conta: ");
                        int numeroConta = sc.nextInt(); sc.nextLine();
                        Conta conta = banco.buscarConta(numeroConta);
                        if (conta != null && conta.getTitular() == clienteAtual) {
                            acessarConta(conta);
                        } else {
                            System.out.println("Conta não encontrada ou não pertence ao usuário.");
                        }
                        break;
                    case 5:
                        clienteAtual = null;
                        break;
                    default:
                        System.out.println("Opção inválida.");
                }
            }
        }
    }

    private static void acessarConta(Conta conta) {
        boolean gerenciando = true;
        while (gerenciando) {
            System.out.println("Conta #" + conta.getNumero() + " | Saldo: R$ " + conta.getSaldo());
            System.out.println("1. Depositar");
            System.out.println("2. Sacar");
            System.out.println("3. Transferir");
            System.out.println("4. Mostrar extrato");
            System.out.println("5. Voltar");

            int op = sc.nextInt(); sc.nextLine();
            switch (op) {
                case 1:
                    System.out.print("Valor do depósito: ");
                    double valorDep = sc.nextDouble(); sc.nextLine();
                    conta.depositar(valorDep);
                    System.out.println("Depósito realizado.");
                    break;
                case 2:
                    System.out.print("Valor do saque: ");
                    double valorSaq = sc.nextDouble(); sc.nextLine();
                    if (conta.sacar(valorSaq)) {
                        System.out.println("Saque realizado.");
                    } else {
                        System.out.println("Saldo insuficiente.");
                    }
                    break;
                case 3:
                    System.out.print("Número da conta destino: ");
                    int destino = sc.nextInt(); sc.nextLine();
                    Conta contaDestino = banco.buscarConta(destino);
                    if (contaDestino == null) {
                        System.out.println("Conta destino não encontrada.");
                        break;
                    }
                    System.out.print("Valor da transferência: ");
                    double valorTransf = sc.nextDouble(); sc.nextLine();
                    conta.transferir(contaDestino, valorTransf);
                    System.out.println("Transferência efetuada.");
                    break;
                case 4:
                    for (Transacao t : conta.getTransacoes()) {
                        System.out.println(t);
                    }
                    break;
                case 5:
                    gerenciando = false;
                    break;
                default:
                    System.out.println("Opção inválida.");
            }
        }
    }
}
