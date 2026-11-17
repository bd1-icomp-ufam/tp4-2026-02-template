Universidade Federal do Amazonas
Instituto de Computação
Introdução a Bancos de Dados — ICC205 — 2026/02
Docente: Altigran Soares da Silva <alti@icomp.ufam.edu.br>

# Trabalho Prático IV — 20/11/2026
# Data da entrega: 10/12/2026 até 23:59

## 1. Apresentação

Este trabalho consiste na execução de um ciclo completo de projeto de banco de dados, tal como estudado na Unidade IV: levantamento de requisitos, projeto conceitual no modelo entidade-relacionamento estendido (EER), projeto lógico (esquema relacional), projeto físico (índices), povoamento e consultas em SQL sobre o PostgreSQL. O trabalho é dividido em quatro partes:

- **Parte I — projeto conceitual.** Entidades, relacionamentos, restrições e diagrama EER, na notação de Elmasri e Navathe.
- **Parte II — projeto lógico.** Mapeamento do EER para um esquema relacional, com o DDL em SQL e as restrições que as cláusulas nativas do DDL não expressam.
- **Parte III — projeto físico.** Índices justificados pelas consultas, com `EXPLAIN` antes e depois.
- **Parte IV — povoamento e consultas.** Dados sintéticos gerados por script, as consultas típicas do domínio e cinco consultas propostas pelo estudante.

O que se avalia é o **raciocínio de modelagem**: por que cada tipo de entidade, cada especialização e cada relacionamento existe, e por que cada tabela do esquema relacional tem a forma que tem. Um diagrama correto sem justificativa tem pouco valor; uma decisão de modelagem diferente da esperada, mas justificada e consistente com os requisitos, é aceita.

O trabalho pode ser feito **individualmente ou em dupla** (no máximo duas pessoas). Não há arguição; a autoria é verificada pela consistência entre o relatório, o histórico de commits e o material entregue.

## 2. Domínios

Cada estudante ou dupla escolhe **um** dos seis domínios abaixo e comunica a escolha no canal do trabalho até **27/11/2026**, informando os nomes. O mesmo domínio pode ser escolhido por mais de uma equipe: os trabalhos diferem pelas decisões de modelagem.

Os requisitos de cada domínio são **mínimos**. Onde o texto é omisso, a equipe faz suposições razoáveis e as registra na seção 1 do relatório. Os requisitos não esgotam o que pode ser modelado. Nenhuma consulta típica depende da data em que é executada: referências de tempo são relativas aos próprios dados.

### 2.1. Corrida por aplicativo

Plataforma que conecta passageiros e motoristas. Uma pessoa cadastrada pode atuar como passageiro, como motorista ou como ambos. Motoristas têm documentos (CNH, com validade) e conduzem veículos de tipos distintos (carro, moto, van), cada tipo com atributos próprios; um veículo pode ser conduzido por vários motoristas ao longo do tempo. Corridas pertencem a uma categoria, têm origem, destino e paradas intermediárias ordenadas, são pagas por um ou mais meios (cartão, Pix, dinheiro, crédito da plataforma), podem usar promoções e geram avaliações do passageiro sobre o motorista e do motorista sobre o passageiro. A cidade é dividida em regiões, com tarifa dinâmica por faixa de horário. Passageiros podem indicar outros passageiros.

Consultas típicas:

1. As 10 regiões de origem com mais corridas concluídas em cada mês.
2. Faturamento total e valor médio por corrida, por categoria de corrida e por tipo de veículo.
3. Motoristas com nota média acima da média geral e com mais corridas que a mediana, com o tipo de veículo que mais usaram.
4. Taxa de cancelamento por faixa de horário e por região.
5. Pessoas que atuam como passageiro e como motorista, com o número de corridas em cada papel.
6. Promoções com maior desconto total concedido e número de passageiros distintos alcançados.
7. Passageiros que indicaram ao menos três outros, com o total de corridas dos indicados.
8. Motoristas que fizeram corridas depois do vencimento da CNH, com o número dessas corridas.
9. Corridas com mais de duas paradas, com a diferença entre a duração de cada uma e a duração média das corridas da mesma categoria sem paradas.

### 2.2. Entrega de comida

Plataforma que conecta clientes, estabelecimentos e entregadores. Os estabelecimentos são de tipos distintos (restaurante, mercado, farmácia), cada tipo com atributos próprios (por exemplo, alvará sanitário ou responsável técnico). Cada estabelecimento mantém um cardápio organizado em categorias; os itens podem ter adicionais opcionais. Uma pessoa cadastrada pode ser cliente, entregador ou ambos. Clientes têm vários endereços. Pedidos reúnem itens, com adicionais escolhidos para cada item, são pagos, podem usar cupons e são entregues por entregadores que usam moto, bicicleta ou vão a pé e atuam em regiões. A taxa de entrega depende da distância. Clientes avaliam o estabelecimento e o entregador.

Consultas típicas:

1. Os 10 estabelecimentos de maior faturamento em cada tipo de estabelecimento e em cada mês.
2. Itens mais pedidos por categoria de cardápio, com os adicionais mais escolhidos para cada um.
3. Tempo médio entre o pedido e a entrega, por tipo de entregador e por região.
4. Clientes com pedidos em mais de um tipo de estabelecimento, com o gasto em cada tipo.
5. Cupons com maior desconto total concedido, com a proporção do total de pedidos que usaram cada cupom.
6. Os 10 entregadores com a menor nota média, entre os que fizeram mais entregas que a média dos entregadores.
7. Estabelecimentos cuja nota média do mês ficou abaixo da do mês anterior.
8. Itens com o mesmo nome vendidos por estabelecimentos diferentes, com o menor e o maior preço praticados em cada região.
9. Taxa de entrega média e número de entregas, por faixa de distância e por tipo de entregador.

### 2.3. Hospedagem entre pessoas

Plataforma de aluguel de imóveis por temporada. Uma pessoa cadastrada pode ser anfitrião, hóspede ou ambos. Imóveis são de tipos distintos (casa, apartamento, quarto), cada tipo com atributos próprios, e oferecem comodidades. Cada imóvel tem um calendário de disponibilidade com preço por data. Reservas têm um hóspede responsável e hóspedes adicionais, geram pagamentos com taxas (limpeza, serviço), seguem uma política de cancelamento (flexível, moderada, rígida) e geram avaliações do hóspede sobre o imóvel e do anfitrião sobre o hóspede. Hóspedes e anfitriões trocam mensagens. Os imóveis estão em bairros, que pertencem a cidades.

Consultas típicas:

1. Taxa de ocupação (noites reservadas ÷ noites disponíveis no calendário) por cidade e por tipo de imóvel, por mês.
2. Os 10 anfitriões com maior receita, com a distribuição da receita por tipo de imóvel.
3. Comodidades mais frequentes entre os imóveis com nota média acima da média geral.
4. Pessoas que são hóspedes e anfitriões, com o número de reservas em cada papel.
5. Preço médio por noite por cidade, separando alta temporada (dezembro, janeiro e julho) e baixa temporada (demais meses).
6. Reservas canceladas por política de cancelamento, com o valor reembolsado.
7. Imóveis que nunca receberam reserva, com a data do cadastro e o número de noites disponíveis no calendário.
8. Pares hóspede–anfitrião com reservas repetidas, com a nota média dada entre eles.
9. Tempo médio entre a primeira mensagem do hóspede e a primeira resposta do anfitrião, por anfitrião, com a nota média de cada anfitrião.

### 2.4. Plataforma de freelancers

Plataforma que conecta contratantes e profissionais. Uma pessoa física cadastrada pode atuar como contratante, como profissional ou como ambos. Contratantes são pessoas físicas ou empresas; profissionais são autônomos ou agências, e uma agência tem membros. Profissionais declaram habilidades, cada uma com um nível. Contratantes publicam projetos com orçamento e habilidades exigidas, cada uma com um nível mínimo; profissionais enviam propostas. Uma proposta aceita gera um contrato, de preço fixo ou por hora, dividido em marcos com prazo e valor. Um contrato com uma agência designa um ou mais membros para executá-lo. Os pagamentos ficam em custódia até a aprovação de cada marco, e a plataforma cobra uma comissão percentual sobre cada pagamento. Ao fim, contratante e profissional se avaliam. Contratos podem entrar em disputa, conduzida por um mediador.

Consultas típicas:

1. As 10 habilidades mais exigidas em cada mês, com a mediana dos orçamentos dos projetos que as exigem.
2. Os 10 profissionais com maior taxa de propostas aceitas (aceitas ÷ enviadas) em cada habilidade, entre os que enviaram ao menos 5.
3. Receita da plataforma por tipo de contrato e por tipo de contratante.
4. Projetos com mais de uma proposta, com a diferença entre a menor e a maior proposta.
5. Tempo médio entre a publicação do projeto e a assinatura do contrato, por faixa de orçamento.
6. Contratos com ao menos um marco entregue após o prazo, com o valor desses marcos e o atraso médio.
7. As 10 agências com maior valor total contratado, com o número de membros designados e o valor por membro.
8. Disputas por mediador e por resultado (a favor do contratante, a favor do profissional, acordo), com o valor envolvido.
9. Contratos fechados com profissionais cujo nível em alguma habilidade exigida estava abaixo do mínimo do projeto, por habilidade.

### 2.5. Carregadores de carros elétricos

Operadoras mantêm redes de estações de recarga, cada estação com localização e horário de funcionamento. Cada estação tem carregadores, de corrente alternada (CA) ou contínua (CC), cada tipo com atributos próprios, com potência e tipo de conector (por exemplo, Tipo 2, CCS, CHAdeMO). Veículos elétricos têm marca, modelo e capacidade de bateria, e aceitam um ou mais tipos de conector. Usuários possuem veículos e podem assinar planos de uma rede, com franquia mensal de energia; a energia acima da franquia é cobrada por kWh. Sessões de recarga registram início, fim, energia entregue e a tarifa vigente. Carregadores podem ser reservados. Manutenções, com prazo, data de início e data de conclusão, e ocorrências em carregadores são atendidas por técnicos. Uma pessoa cadastrada pode ser usuário, técnico ou ambos. Redes diferentes mantêm acordos de roaming, que permitem a um usuário carregar na rede de outra operadora.

Consultas típicas:

1. Energia total entregue e receita por rede e por tipo de conector, por mês.
2. As 5 estações com maior energia entregue em cada faixa de horário (madrugada, manhã, tarde, noite), pelo horário de início da sessão.
3. Modelos de veículo mais frequentes por tipo de conector, com a duração média da sessão.
4. Usuários de plano com consumo mensal acima da franquia, com o excedente cobrado.
5. Carregadores com maior tempo parado por manutenção, com o número de ocorrências por tipo.
6. Reservas sem sessão associada, por estação e por usuário.
7. Sessões feitas em rede diferente da rede do plano do usuário (roaming), com a tarifa média comparada à das sessões na rede própria.
8. Técnicos com o maior número de manutenções concluídas no prazo.
9. Energia entregue e duração média da sessão por tipo de carregador (CA ou CC).

### 2.6. Frete e logística de última milha

Empresa de entregas com remetentes (pessoas ou empresas) e destinatários. Uma pessoa física cadastrada pode ser remetente, destinatário, entregador ou mais de um desses papéis. Destinatários têm endereços, que pertencem a bairros de cidades. Pacotes são de tipos distintos (comum, frágil, refrigerado, perigoso), cada tipo com atributos próprios. A operação usa centros de distribuição de dois tipos (hub e ponto de coleta). Pacotes passam por centros de distribuição até a entrega, em rotas com paradas ordenadas, duração planejada e duração realizada, executadas por entregadores com veículos (moto, van, caminhão). Cada tentativa de entrega é registrada com o resultado e o motivo, quando malsucedida. O rastreamento é feito por eventos com data, hora e local. Ocorrências (extravio, avaria) têm responsável e valor de ressarcimento. O frete é cobrado por faixa de peso e tipo de pacote.

Consultas típicas:

1. Taxa de entrega na primeira tentativa por centro de distribuição de origem da rota e por tipo de veículo.
2. Tempo médio entre a coleta e a entrega, por tipo de pacote e por cidade de destino.
3. Rotas com mais paradas, com a diferença entre a duração planejada e a realizada.
4. Remetentes com maior volume de pacotes, com a proporção de pacotes com ocorrência.
5. Ocorrências por tipo de pacote, com o valor total ressarcido.
6. Os 10 entregadores com mais tentativas malsucedidas em cada motivo.
7. Pacotes que passaram por mais de três centros de distribuição até a entrega.
8. Receita de frete por faixa de peso e por tipo de pacote.
9. Pacotes com intervalo superior a 24 horas entre dois eventos consecutivos de rastreamento, com o local e o maior intervalo.

## 3. Ferramentas

O diagrama EER deve ser feito em **uma das duas ferramentas abaixo. Nenhuma outra é aceita.**

1. **DBV EER Studio**, aplicação web que roda no navegador, sem instalação: <https://davidbuenov.github.io/dbv-eer-studio/>. Código e licença (MIT): <https://github.com/davidbuenov/dbv-eer-studio>. O arquivo-fonte do diagrama tem extensão `.eer`. A ferramenta gera também um esquema relacional e um DDL a partir do diagrama. Na interface, a aba correspondente tem o rótulo "Modelo Relacional"; o termo correto, usado neste enunciado e no relatório, é **esquema relacional**.
2. **TerraER 3.14**, aplicação em Java (JAR único, requer Java instalado). Obter **somente** da página de lançamentos do projeto no GitHub: <https://github.com/rterrabh/TerraER/releases/tag/TerraER3.14>. O site `terraer.com.br` não deve ser usado, pois a página de tutoriais continha links alheios ao projeto na data de redação deste enunciado. A ferramenta não gera esquema relacional.

Em ambas, o diagrama segue a notação de Elmasri e Navathe. O DDL gerado pelo DBV EER Studio é **rascunho**: deve ser revisado (tipos de dados, ordem de criação das tabelas, restrições) e o que se entrega e avalia é o DDL revisado, que precisa executar sem erro no PostgreSQL 16 do repositório-template.

## 4. Parte I — projeto conceitual

O projeto conceitual contém:

**4.1. Entidades.** Lista dos tipos de entidade com atributos (simples, chave, derivados, multivalorados), semântica de cada um e, para subclasses, as superclasses, e para superclasses, as especializações que delas se originam.

**4.2. Relacionamentos.** Lista dos tipos de relacionamento com atributos, entidades participantes, cardinalidade, restrições de participação (total ou parcial) e semântica.

**4.3. Diagrama EER**, na notação de Elmasri e Navathe, produzido em uma das ferramentas da seção 3. O diagrama deve refletir fielmente as listas dos itens 4.1 e 4.2.

**4.4. Justificativas.** Para cada hierarquia de especialização, a razão de ter sido modelada assim (e não como um atributo de tipo na superclasse); para cada entidade fraca e cada relacionamento de grau maior que dois presentes no diagrama, a razão de terem sido modelados assim.

## 5. Parte II — projeto lógico

**5.1. Esquema relacional.** Lista de todas as tabelas, com atributos, chaves primárias, chaves estrangeiras e restrições, e a **justificativa de cada tabela** a partir do diagrama, indicando o passo do mapeamento EER para relacional aplicado (entidade regular, entidade fraca, relacionamento 1:1, 1:N ou N:M, atributo multivalorado, relacionamento n-ário, especialização, categoria).

**5.2. Mapeamento das hierarquias.** Para cada especialização, a opção de mapeamento escolhida (tabela por subclasse, tabela única com atributo de tipo, tabela por subclasse com atributos herdados, ou outra) e a razão da escolha, em função das restrições de disjunção e participação e das consultas do domínio.

**5.3. DDL.** Arquivo `sql/01_esquema.sql`, em SQL para o PostgreSQL 16, com as restrições nativas (`PRIMARY KEY`, `FOREIGN KEY`, `UNIQUE`, `NOT NULL`, `CHECK`) e tipos de dados adequados aos atributos. As tabelas devem ser criadas em ordem que não viole dependências de chave estrangeira, ou as chaves estrangeiras devem ser adicionadas com `ALTER TABLE` ao final.

**5.4. Restrições semânticas.** Identificar e listar **ao menos duas** restrições do projeto conceitual que as cláusulas nativas do DDL não expressam (por exemplo, a restrição de disjunção entre subclasses, ou uma participação total que atravessa tabelas) e implementá-las com gatilhos (`TRIGGER`) e funções, no mesmo arquivo ou em `sql/01b_restricoes.sql`. O PostgreSQL não implementa `CREATE ASSERTION`. Para cada restrição, um teste em `sql/03_testes_restricoes.sql` com um comando aceito e um comando rejeitado; o relatório traz a saída de cada um (a confirmação da inserção e a mensagem de erro). O verificador não executa esse arquivo.

## 6. Parte III — projeto físico

**6.1. Índices.** Arquivo `sql/02_indices.sql` com os índices criados, cada um justificado no relatório pela consulta (da seção 2 ou do item 7.3) que o motiva.

**6.2. Comparação.** Para **duas** consultas escolhidas pelo estudante, o plano de execução (`EXPLAIN (ANALYZE, BUFFERS)`) **antes e depois** da criação do índice, com a explicação da diferença observada. Se um índice criado não for usado pelo otimizador, o relatório deve dizer isso e explicar por quê.

## 7. Parte IV — povoamento e consultas

**7.1. Povoamento.** Script `src/gerar_dados.py`, em Python 3.12, que popula o banco com **dados sintéticos** e é **reprodutível** (semente fixa registrada no script). A biblioteca `Faker` pode ser usada. Volume mínimo: a maior tabela do esquema deve ter pelo menos **100.000 linhas** (em geral a de corridas, pedidos, reservas, contratos, sessões de recarga ou pacotes), nenhuma tabela pode ficar vazia e pelo menos 5 tabelas devem ter **1.000 linhas ou mais**. O script deve gerar e carregar os dados em **até 10 minutos** nas máquinas da turma. Os dados devem respeitar todas as restrições do esquema e ter distribuição suficiente para que as consultas retornem resultados não triviais. Em entrega de comida, itens de estabelecimentos diferentes devem repetir nomes (consulta 8 do domínio). Em hospedagem, os preços por data devem variar conforme a temporada (consulta 5 do domínio). Em recarga de veículos, parte das reservas não deve ter sessão associada (consulta 6 do domínio).

**7.2. Consultas típicas.** Cada uma das consultas típicas do domínio escolhido (seção 2), em SQL, uma consulta por arquivo, `sql/consultas/q01.sql`, `q02.sql` e assim por diante, com uma única instrução `SELECT` por consulta, e o resultado (primeiras 20 linhas) em `resultados/`.

**7.3. Consultas próprias.** Cinco consultas analíticas **diferentes** das consultas típicas, propostas pela equipe, cada uma com o enunciado em linguagem natural e o SQL (`sql/consultas/p01.sql` a `p05.sql`). Ao menos duas devem usar a hierarquia de especialização, quando o diagrama tiver uma.

## 8. Verificador automático

O repositório-template traz um verificador, executado por `make test`, que confere o que é mecânico:

- `sql/01_esquema.sql` executa sem erro em um banco PostgreSQL 16 vazio;
- o povoamento executa e atende ao volume mínimo da seção 7.1;
- cada arquivo de consulta executa e retorna ao menos uma linha;
- os arquivos obrigatórios existem (diagrama exportado, arquivo-fonte do diagrama, relatório em PDF, `dominio.txt`).

O verificador **não avalia** o diagrama EER, as justificativas nem a adequação do esquema ao domínio. Passar no verificador é condição para a nota dos itens correspondentes, mas não a determina.

## 9. Relatório

O relatório é um arquivo PDF, `docs/relatorio.pdf`, com as seções:

**9.1. Domínio e suposições.** O domínio escolhido, os nomes dos integrantes e as suposições feitas onde os requisitos eram omissos.

**9.2. Projeto conceitual.** Os itens 4.1 a 4.4: listas de entidades e relacionamentos, o diagrama EER e as justificativas.

**9.3. Projeto lógico.** Os itens 5.1, 5.2 e 5.4: o esquema relacional com a justificativa de cada tabela, as opções de mapeamento das hierarquias e as restrições semânticas com seus testes.

**9.4. Projeto físico.** Os índices e a comparação dos dois planos de execução (itens 6.1 e 6.2).

**9.5. Consultas.** Para cada consulta típica e própria, o resultado e um comentário curto sobre a plausibilidade do resultado em relação aos dados gerados.

**9.6. Divisão do trabalho (somente duplas).** Quem fez o quê. A contribuição de cada integrante deve ser visível no histórico de commits.

**9.7. Declaração de uso de ferramentas de IA.** Seção obrigatória. Deve informar quais ferramentas foram usadas, em que partes do trabalho, o que foi solicitado a elas e o que foi modificado posteriormente. **O uso declarado não implica desconto de nota.** O que se avalia é a consistência entre a declaração e o material entregue.

## 10. Estrutura do repositório

```
/
├── docs/
│   ├── eer/            diagrama (PNG ou SVG) e arquivo-fonte
│   └── relatorio.pdf
├── sql/
│   ├── 01_esquema.sql
│   ├── 01b_restricoes.sql   (se separado)
│   ├── 02_indices.sql
│   ├── 03_testes_restricoes.sql
│   └── consultas/      q01.sql, q02.sql, ... e p01.sql a p05.sql
├── src/                gerar_dados.py e utilitários
├── resultados/         saídas das consultas e planos de execução
├── tests/              check.py (verificador)
├── dominio.txt         domínio escolhido e nomes dos integrantes
├── Dockerfile
├── docker-compose.yml
├── Makefile
└── README.md
```

O repositório deve funcionar do zero com a sequência `make up`, `make esquema`, `make dados`, `make indices`, `make consultas` e `make test`, sem depender de caminho absoluto, de configuração manual não documentada ou de pacote instalado fora dos contêineres.

## 11. Entrega

A entrega é feita por **repositório GitHub privado**, um por estudante ou por dupla, criado a partir do template `tp4-2026-02-template` na organização `bd1-icomp-ufam`. Cada estudante ou dupla deve:

1. criar o repositório a partir do template (em dupla, um dos integrantes cria e adiciona o outro como colaborador);
2. adicionar o docente como colaborador;
3. marcar a versão final com a tag **`v1.0`**, exatamente com esse nome;
4. enviar a tag ao GitHub: `git push origin v1.0`.

Será corrigido o commit apontado pela tag `v1.0` no repositório remoto no encerramento do prazo. Antes do prazo, confirmar que a tag aparece no remoto:

```
git ls-remote --tags origin
```

Tags com outro nome, branches chamados `v1.0` e repositórios sem o docente como colaborador não caracterizam entrega.

**Entrega intermediária, sem nota.** Até **03/12/2026, 23:59**, a equipe pode marcar com a tag **`cp1`** uma versão com a Parte I (itens 4.1 a 4.4 no relatório e o diagrama exportado). O docente comenta os requisitos, o diagrama e as justificativas. A entrega intermediária é opcional e não vale nota.

## 12. Calendário

- **20/11/2026:** publicação do enunciado e do template.
- **27/11/2026:** prazo para comunicar domínio e integrantes no canal do trabalho.
- **03/12/2026:** limite para dúvidas e para a entrega intermediária opcional (`cp1`). Nesta data é a aula de mapeamento ER-relacional.
- **10/12/2026, 23:59:** entrega final (tag `v1.0`).

## 13. Avaliação

Nota de 0 a 10:

- Projeto conceitual (requisitos, diagrama e justificativas): **3,0**
- Projeto lógico (esquema relacional, justificativa de cada tabela, DDL e restrições semânticas): **2,5**
- Projeto físico (índices e comparação dos planos): **1,0**
- Consultas típicas em SQL, com resultados: **2,0**
- Cinco consultas próprias: **1,0**
- Organização do repositório e do relatório, rito de entrega e reprodutibilidade: **0,5**

Divergência entre o diagrama e o esquema relacional (tabela sem origem no diagrama, ou elemento do diagrama sem tabela e sem justificativa) e divergência entre o relatório e o que o repositório produz ao ser executado são os itens de maior peso negativo do trabalho.

## 14. Comentários gerais

As Partes I e II dependem do conteúdo de EER e de mapeamento ER-relacional, tratado nas aulas de 26/11, 01/12 e 03/12. A Parte I pode ser iniciada a partir da publicação, com o conteúdo de ER já estudado, e a entrega intermediária opcional serve a esse fim.

O uso de ferramentas de IA é permitido e deve ser declarado. O trabalho não avalia a produção do diagrama ou do código, e sim a capacidade de justificar cada decisão de modelagem e de relacionar o diagrama, o esquema relacional e os resultados obtidos.

## 15. Referências

1. ELMASRI, R.; NAVATHE, S. B. *Sistemas de Banco de Dados*, 7ª ed. Pearson, 2018. Capítulos sobre o modelo EER e sobre o projeto de banco de dados relacional por mapeamento ER e EER.
2. SILBERSCHATZ, A.; KORTH, H. F.; SUDARSHAN, S. *Sistema de Banco de Dados*, 6ª ed. Elsevier, 2012.
3. The PostgreSQL Global Development Group. *PostgreSQL 16 Documentation*: CREATE TABLE; CREATE INDEX; CREATE TRIGGER; Using EXPLAIN. <https://www.postgresql.org/docs/16/>
4. DBV EER Studio. <https://github.com/davidbuenov/dbv-eer-studio>
5. TerraER. <https://github.com/rterrabh/TerraER>
