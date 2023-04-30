<h1>Comentários sobre código de automação em Python</h1>

<h2> Princípios Gerais </h2>

<ol>
<li> <h4>Usar formatador</h4> 
Formatadores garantem que a formatação do seu código é consistente. Uma formatação consistente significa código mais legível, porque é mais fácil de ler/entender algo quando existem padrões.

Nessa palestra um engenheiro da Netflix fala sobre a importância de formatadores: https://www.youtube.com/watch?v=srXzADSGR04

O Python tem uma formatação oficial recomendada, o Pep 8: https://peps.python.org/pep-0008/

Aqui explica como sugiro configurar um formatador em Python no Visual Studio Code: https://code.visualstudio.com/docs/python/editing#_formatting
</li>

<li><h4>Ajustar/Remover comentários não esclarecedores</h4>
Minha impressão é que o código foi escrito por outra pessoa (só porque não imagino você escrevendo do jeito que tá escrito) e tem alguns comentários que confundem um pouco e poderiam ser ajustados/removidos. Acho que vale muito à pena criar o hábito de reescrever código copiado (se não for um código grande ou que não vai ser alterado), porque, mesmo sem entender tão bem o que tá rolando, é a melhor fonte de aprendizado que você pode ter e te permite remover/ajustar partes (como comentários) que não fazem sentido (e acabam te atrapalhando no futuro).
</li>

<li><h4>Pensar no usuário do código </h4>
O usuário do código é sempre ao menos uma pessoa (você mesmo), frequentemente várias pessoas (os desenvolvedores com você no projeto) e infelizmente quase sempre pessoas que vão consumir o valor que seu código gera. No caso desse código, esse último grupo, penso eu, são funcionários da empresa que ao menos a priori vão ter que ajustar e rodar o código nos próprios computadores.

Sob esse prisma, é importante pensar nessas pessoas. Elas por exemplo vão ter que configurar variáveis como o Path dos cenários, quais cenários vão ser pulados (acho que essa funcionalidade pode ser útil pra eles) e coisas assim. Criar algumas variáveis de configuração no início do arquivo na minha visão é uma maneira clara e explicíta de ajudar esses usuários. O uso de letras maiúsculas em uma variável é uma convenção que indica que aquela variável é imutável (mais tecnicamente, a referência a aquela variável é imutável), o que é particularmente importante em linguagens que nativamente não te dão tanto controle sobre a mutabilidade das variáveis (como Python);
</li>

<li> <h4>Explicitar tipos</h4>
Cara, hoje eu sou defensor ferrenho de linguagens tipadas. É absolutamente inevitável: sempre que você for ler código, você vai na sua cabeça estar memorizando quais as variáveis do programa e quais são seus valores (e portanto tipos). Você declarar explicitamente quais tipos você tá utilizando (por exemplo pelo uso de simples classes que servem só pra instanciar objetos de um tipo específico) e usando type hints (https://docs.python.org/3/library/typing.html) te ajuda infinitamente a esclarecer na sua cabeça o que tá rolando. E, bem importante, melhora a "code completion" (as "dicas" que seu editor, por exemplo VS Code, te dá enquanto você tá escrevendo o código) e te permite identificar erros antes mesmo de rodar o programa (por exemplo se a variável "scenario_num" é uma string, seu editor pode avisar que scenario_num == 0 não faz sentido, porque sempre vai dar false)
</li>

<li><h4>DRY - Don't Repeat Yourself NEM SEMPRE É BOM</h4>
DRY é um princípio famoso de arquitetura de software que diz que sempre que você vê código repetido, você tem que abstrair ele (por exemplo criando uma função) pra manter ele em um só lugar. Eu já me ferrei muito por tomar esse princípio como verdade absoluta e tentar ficar abstraindo tudo o tempo todo (e ficar incomodado sempre que eu via código repetido). 

Existem alguns problemas em seguir cegamente esse princípio:
<ul>
<li>
Se você tentar abstrair algo e seu código não ficar bem escrito, você não só vai criar código confuso como vai propagar as problemáticas desse código pra todos os lugares que ele tá sendo usado. E aí no futuro refatorar vai ser uma dor de cabeça bizarra, porque você vai ter várias partes do seu código que dependem de maneiras específicas da sua abstração ruim. 
</li>

<li>
Meu princípio geral, que acho que é mais fundamental do que o DRY, é que em termos de arquitetura, o software tem que ser otimizado para a <b>mudança</b>. Isto é, você tem que ser capaz de com o mínimo de tempo possível alterar ou adicionar coisas no código para habilitar uma nova funcionalidade/comportamento - pra alcançar isso às vezes você tem que investir em código mais legível, às vezes em princípios como DRY, às vezes outras coisas. Depende do caso. E reconhecer que otimizar código é um trade-off: existe um ponto ótimo para o tempo que você gasta otimizando pra facilitar mudanças no futuro versus o tempo que é perdido otimizando para mudanças ao invés de efetivamente implementar as mudanças. 

Concretamente: vamos supor que você vê uma parte do código que se repete:

<pre>
<code>
command_window_pos = get_command_window_position()
pyautogui.click(convert_resolution(command_window_pos))
pyautogui.write("escrevendo algo")
pyautogui.press("enter")
</code>
</pre>

Você cria uma função pra melhorar seu código:

<pre>
<code>
def write_on_command_window(text: str):
    command_window_pos = get_command_window_position()
    pyautogui.click(convert_resolution(command_window_pos))
    pyautogui.write(text)
    pyautogui.press("enter")
</code>
</pre>

Mais aí você descobre que, vamos supor, a maneira com que você tem que clicar na janela de comando é diferente do contexto (to inventando qualquer coisa). Você poderia fazer: 

<pre>
<code>
def write_on_command_window(text: str, context):
    command_window_pos = get_command_window_position()

    if context == "something":
      pyautogui.click(convert_resolution(command_window_pos))
    else:
      # click differently

    pyautogui.write(text)
    pyautogui.press("enter")
</code>
</pre>

Em breve o código da função write_on_command_window vai ter milhares de if/elses que parecem nem fazer sentido algum. Pois é, você criou uma abstração ruim. E aí sempre que você quiser chamar essa função que escreve algo na janela de comando, você vai querer chamar essa função - e vai ter que ler e entender seu código ruim. Seu código não tá otimizado pra mudança: você perde mais tempo entendo e refatorarando a abstração do que se não tivesse criado abstração nenhuma e simplesmente tivesse escrevido código repetido (ou muito parecido) em diferentes contextos.

O que eu quis chamar atenção nesse ponto é que eu criei uma abstração "UI" que é útil pra lidar com coisas repetidas e acho que simplifica e melhora o código. Mas não precisa ser DRY a qualquer custo - não precisa criar uma função nova em "UI" pra cada caso diferente. Depende de quão confiante você tá em criar uma abstração nova - e em geral é melhor errar pra repetir código do que criar uma abstração ruim.
</li>
</ul>
</li>


</ol>

<h2> Dicas Específicas </h2>

<ol>

<li> <h4>Utilizar "imports" mais específicos</h4>
A não ser que seja uma biblioteca gigantesca que você vai importar várias funções (ou vai muito frequentemente o que e o nome das funções que você importa), eu prefiro usar:

<pre>
<code>
from arquivo/biblioteca import ...
</code>
</pre>

Do que:
<pre>
<code>
import arquivo/biblioteca
</code>
</pre>

Isso ajuda a esclarecer a relação entre o arquivo importador e importado pra quem tá lendo o código pelas primeiras vezes (por exemplo "ah, beleza, ele tá o arquivo "scenarios_fun" exporta só uma função "get_scenarios_list") e permite (ou ao menos comunica) a possibilidade de encapsulamento de partes do módulo importado (com import scenarios_fun, você pode utilizar todas as funções do scenarios_fun, o que frequentemente é indesejável).


</li>

<li><h4>Mais sobre encapsulamento</h4>
Como no Python você não pode especificar em um arquivo exatamente o que você quer que seja importado (ao menos não que eu saiba), é importante ajudar a esclarcer o encapsulamento utilização a convenção de colocar um "_" antes de variáveis/funções privadas (que não devem ser alteradas fora de um arquivo/contexto específico). Por exemplo "_get_scenario_number" deixa bem claro que essa função não deve ser invocada fora do arquivo em que foi criada - e isso diminui o risco de alguém chamar ela inadequadamente (o que poderia causar bugs ou só criar código confuso).
</li>

<li><h4>Minimizar o nível de aninhamento (do inglês "nesting")</h4>
Não é uma regra escrita na pedra, mas em geral quanto mais aninhando seu código tá, tipo:

<pre>
<code>
  for i in range(10):
    if x:
      if z:
        if j
          # ...código
</code>
</pre>

Pior. Porque quando você tá lendo o código, você começa a ter que entender/memorizar a condição que você tá lidando (no exemplo de cima, if x and z and j) em vários lugares separados, geralmente um longe do outro no código. Nem sempre faz sentido, mas uma técnica muito utilizada pra reduzir o aninhamento é lidar com a negação da condição. Explicando com o exemplo acima:

<pre>
<code>
for i in range(10):
  if not x or not z or not j:
    continue

  # ...código
</code>
</pre>

Claro que você poderia fazer: 

<pre>
<code>
for i in range(10):
  if x and z and j:
    # ...código
</code>
</pre>

Mas você teria um nível a mais de aninhamento!
</li>

<li><h4>Código simples é melhor</h4></li>
Posso ter interpretado algo meio errado, mas achei o módulo/arquivos scenarios_fun "overengineered"/excessivamente complexo. Na função principal do programa, o que você tá fazendo é um loop não por scenarios, mas por casos específicos de scenarios (scenario 1 com FAHTS ou USFOS, na FirstRun ou With PFP, etc...). Você chamar várias funções diferentes no meio do loop cria uma complexidade absurda, porque em cada iteração torna necessário estudar três funções diferentes que fazem coisas diferentes pra entender qual é o tipo do scenario/caso que você tá lidando. 

A principal razão pela qual eu prefiro Javascript sobre o Python é porque sinto que Javascript é uma linguagem orientada a objetos (não confundir com orientada a classes, to falando de objeto como o tipo objeto em JS), enquanto Python é mais focada em listas. Objetos/dicionários são uma estrutura de dados superior pra organizar e utilizar o código, porque te dão mais flexibilidade e criam código mais legível. 

Isto é:

<pre>
<code>
# Obtendo o tema de preferência do usuário no site com dicionário
user["preferences"]["theme"]
</code>
</pre>

É bem mais legível do que:

<pre>
<code>
# Obtendo o tema de preferência do usuário no site com lista
user[0][3]
</code>
</pre>

Então sou a favor de criar dicionários pra ser uma estrutura de dados mais intuitiva de dados no seu programa. Mas acho que no caso desse programa específico, um array com objetos (instâncias de classes em Python) com tipos bem claros é a estrutura mais simples pra lidar com o problema. E simples é bom.
</ol>