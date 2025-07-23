const fs = require('fs');
const path = require('path');

// Configurações
const PASTA_DADOS = path.join(__dirname, '..', 'dados');
const PASTA_ESTATISTICAS = path.join(__dirname, '..', 'estatisticas');

// --- Funções utilitárias ---

// Parse de data no formato "dd/mm/yyyy"
function parseData(dataStr) {
  const partes = dataStr.split('/');
  if (partes.length !== 3) return new Date(0);
  const [dia, mes, ano] = partes.map(Number);
  return new Date(ano, mes - 1, dia);
}

// Garante que a pasta existe, cria se não existir
function garantirPasta(pasta) {
  if (!fs.existsSync(pasta)) fs.mkdirSync(pasta, { recursive: true });
}

// --- Leitura de dados ---

// Lista ficheiros de anos válidos
function listarFicheirosAnos() {
  return fs.readdirSync(PASTA_DADOS).filter(f => {
    const ano = f.replace('.json', '');
    return /^\d{4}$/.test(ano) && +ano >= 2011 && +ano <= 2025;
  });
}

// Lê um ficheiro de sorteios de um ano
function lerSorteiosAno(nomeFicheiro) {
  const caminho = path.join(PASTA_DADOS, nomeFicheiro);
  const conteudo = fs.readFileSync(caminho, 'utf-8');
  const dados = JSON.parse(conteudo);
  const ano = nomeFicheiro.replace('.json', '');
  return dados[ano] || [];
}

// Carrega todos os sorteios e ordena por data
function carregarTodosSorteios() {
  const ficheiros = listarFicheirosAnos();
  let todos = [];
  ficheiros.forEach(f => {
    try {
      todos = todos.concat(lerSorteiosAno(f));
    } catch (e) {
      console.warn(`Erro a ler ${f}: ${e.message}`);
    }
  });
  todos.sort((a, b) => parseData(a.data) - parseData(b.data));
  return todos;
}

// --- Estatísticas e heurísticas ---

function calcularEstatisticas(sorteios) {
  const total = sorteios.length;
  const estatisticas = {};

  for (let numero = 1; numero <= 49; numero++) {
    let num_saidas = 0;
    let ultimo_idx = -1;
    const indices = [];

    sorteios.forEach((sorteio, idx) => {
      if (sorteio.numeros?.includes(numero)) {
        num_saidas++;
        ultimo_idx = idx;
        indices.push(idx);
      }
    });

    // Gap médio entre saídas
    const gaps = [];
    for (let i = 1; i < indices.length; i++) {
      gaps.push(indices[i] - indices[i - 1]);
    }
    const gap_medio = gaps.length ? +(gaps.reduce((a, b) => a + b, 0) / gaps.length).toFixed(2) : null;

    estatisticas[numero] = {
      numero,
      num_saidas,
      percent_saidas: total ? +(num_saidas / total * 100).toFixed(2) : 0,
      ausencias: ultimo_idx >= 0 ? total - ultimo_idx - 1 : total,
      gap_medio,
      tendencia: indices.length >= 2 ? indices[indices.length - 1] - indices[indices.length - 2] : null
    };
  }

  return estatisticas;
}

function atribuirPontos(lista, peso) {
  const pontos = {};
  lista.slice(0, 10).forEach((e, idx) => {
    const score = (10 - idx) * peso;
    pontos[e.numero] = (pontos[e.numero] || 0) + score;
  });
  return pontos;
}

// Heurísticas básicas
function pontuarPorFrequencia(est) {
  const ordenado = Object.values(est).sort((a, b) => b.num_saidas - a.num_saidas);
  return atribuirPontos(ordenado, 3);
}

function pontuarPorAusencia(est) {
  const ordenado = Object.values(est).sort((a, b) => b.ausencias - a.ausencias);
  return atribuirPontos(ordenado, 2);
}

function pontuarPorTendencia(est) {
  const candidatos = Object.values(est).filter(e => e.tendencia !== null && e.tendencia <= 10);
  return atribuirPontos(candidatos, 2);
}

function pontuarPorGapMedio(est) {
  const ordenado = Object.values(est)
    .filter(e => e.gap_medio !== null)
    .map(e => ({ ...e, desvio: Math.abs(e.gap_medio - 40) }))
    .sort((a, b) => a.desvio - b.desvio);
  return atribuirPontos(ordenado, 1);
}

// Pares frequentes
function calcularParesFrequentes(sorteios) {
  const paresCount = {};
  sorteios.forEach(sorteio => {
    const nums = sorteio.numeros || [];
    for (let i = 0; i < nums.length; i++) {
      for (let j = i + 1; j < nums.length; j++) {
        const par = [nums[i], nums[j]].sort((a,b) => a-b).join('-');
        paresCount[par] = (paresCount[par] || 0) + 1;
      }
    }
  });
  return paresCount;
}

function pontuarPorPares(paresFreq) {
  const paresOrdenados = Object.entries(paresFreq).sort((a,b) => b[1] - a[1]).slice(0, 20);
  const pontos = {};
  paresOrdenados.forEach(([par, freq], idx) => {
    const [n1, n2] = par.split('-').map(Number);
    const score = 15 - idx;
    pontos[n1] = (pontos[n1] || 0) + score;
    pontos[n2] = (pontos[n2] || 0) + score;
  });
  return pontos;
}

// Trios frequentes
function calcularTriosFrequentes(sorteios) {
  const triosCount = {};
  sorteios.forEach(sorteio => {
    const nums = sorteio.numeros || [];
    for (let i = 0; i < nums.length; i++) {
      for (let j = i + 1; j < nums.length; j++) {
        for (let k = j + 1; k < nums.length; k++) {
          const trio = [nums[i], nums[j], nums[k]].sort((a,b) => a-b).join('-');
          triosCount[trio] = (triosCount[trio] || 0) + 1;
        }
      }
    }
  });
  return triosCount;
}

function pontuarPorTrios(triosFreq) {
  const triosOrdenados = Object.entries(triosFreq).sort((a,b) => b[1] - a[1]).slice(0, 10);
  const pontos = {};
  triosOrdenados.forEach(([trio, freq], idx) => {
    const nums = trio.split('-').map(Number);
    const score = 20 - idx * 2;
    nums.forEach(n => {
      pontos[n] = (pontos[n] || 0) + score;
    });
  });
  return pontos;
}

// Frequência por ano
function calcularFrequenciaPorAno(sorteios) {
  const freqAno = {};
  sorteios.forEach(sorteio => {
    const ano = parseData(sorteio.data).getFullYear();
    if (!freqAno[ano]) freqAno[ano] = {};
    (sorteio.numeros || []).forEach(num => {
      freqAno[ano][num] = (freqAno[ano][num] || 0) + 1;
    });
  });
  return freqAno;
}

// Crescimento anual de frequência
function pontuarCrescimentoAno(freqAno) {
  const anos = Object.keys(freqAno).map(a => +a).sort();
  const pontos = {};

  for (let num = 1; num <= 49; num++) {
    let crescimentos = 0;
    for (let i = 1; i < anos.length; i++) {
      const anoAtual = anos[i];
      const anoAnterior = anos[i-1];
      const freqAtual = freqAno[anoAtual][num] || 0;
      const freqAnterior = freqAno[anoAnterior][num] || 0;
      if (freqAtual > freqAnterior) crescimentos++;
    }
    if (crescimentos >= 2) {
      pontos[num] = crescimentos * 3;
    }
  }
  return pontos;
}

// Combina várias pontuações somando os scores
function combinarPontuacoes(...listas) {
  const combinadas = {};
  listas.forEach(lista => {
    for (const [num, score] of Object.entries(lista)) {
      combinadas[num] = (combinadas[num] || 0) + score;
    }
  });
  return combinadas;
}

// Normalização simples min-max
function normalizarPontuacoes(pontos) {
  const valores = Object.values(pontos);
  const min = Math.min(...valores);
  const max = Math.max(...valores);
  const normalizado = {};
  Object.entries(pontos).forEach(([num, score]) => {
    normalizado[num] = +((score - min) / (max - min || 1)).toFixed(4);
  });
  return normalizado;
}

// --- Avaliação da simulação ---

function compararPrevisao(reais, previstos) {
  const acertos = reais.filter(n => previstos.includes(n));
  return {
    reais,
    previstos,
    acertos,
    num_acertos: acertos.length
  };
}

// --- Função principal do programa (previsão para o próximo sorteio) ---

function mainPrevisao() {
  console.log("A carregar sorteios...");
  const sorteios = carregarTodosSorteios();
  const ultimos50 = sorteios.slice(-50);

  console.log("A calcular heurísticas...");

  const totalEst = calcularEstatisticas(sorteios);
  const recentEst = calcularEstatisticas(ultimos50);

  const pontosTotal = combinarPontuacoes(
    pontuarPorFrequencia(totalEst),
    pontuarPorAusencia(totalEst),
    pontuarPorTendencia(totalEst),
    pontuarPorGapMedio(totalEst)
  );

  const pontosRecentes = combinarPontuacoes(
    pontuarPorFrequencia(recentEst),
    pontuarPorTendencia(recentEst),
    pontuarPorGapMedio(recentEst)
  );

  const paresFreq = calcularParesFrequentes(sorteios);
  const triFreq = calcularTriosFrequentes(sorteios);
  const freqAno = calcularFrequenciaPorAno(sorteios);

  const pontosPares = pontuarPorPares(paresFreq);
  const pontosTrios = pontuarPorTrios(triFreq);
  const pontosCrescimentoAno = pontuarCrescimentoAno(freqAno);

  const pontosCombinados = combinarPontuacoes(
    pontosTotal,
    pontosRecentes,
    pontosPares,
    pontosTrios,
    pontosCrescimentoAno
  );

  const provaveis = Object.entries(pontosCombinados)
    .sort((a, b) => b[1] - a[1])
    .slice(0, 2)
    .map(([numero]) => Number(numero));

  console.log(`\n🔮 Números mais prováveis no próximo sorteio: ${provaveis.join(', ')}`);

  const resultado = {
    gerado_em: new Date().toISOString(),
    total_sorteios: sorteios.length,
    heuristicas: {
      total: pontosTotal,
      ultimos50: pontosRecentes,
      pares: pontosPares,
      trios: pontosTrios,
      crescimentoAno: pontosCrescimentoAno
    },
    combinadas: pontosCombinados,
    sugestao_final: provaveis
  };

  garantirPasta(PASTA_ESTATISTICAS);
  const destino = path.join(PASTA_ESTATISTICAS, 'estatisticas_teste.json');
  fs.writeFileSync(destino, JSON.stringify(resultado, null, 2), 'utf-8');
  console.log(`\n✅ Resultado guardado em ${destino}`);
}

// --- Função da simulação histórica ---

function mainSimulacao() {
  console.log("🔄 Simulação de sorteios de 2012 com base nos dados anteriores...");

  const dados2011 = lerSorteiosAno('2011.json');
  const dados2012 = lerSorteiosAno('2012.json');

  const resultadosSimulacao = [];
  let sorteiosDisponiveis = [...dados2011];

  dados2012.forEach((sorteio2012, index) => {
    const est = calcularEstatisticas(sorteiosDisponiveis);
    const pares = calcularParesFrequentes(sorteiosDisponiveis);
    const trios = calcularTriosFrequentes(sorteiosDisponiveis);
    const freqAno = calcularFrequenciaPorAno(sorteiosDisponiveis);

    const heuristicas = [
      pontuarPorFrequencia(est),
      pontuarPorAusencia(est),
      pontuarPorTendencia(est),
      pontuarPorGapMedio(est),
      pontuarPorPares(pares),
      pontuarPorTrios(trios)
    ];

    if (Object.keys(freqAno).length >= 2) {
      heuristicas.push(pontuarCrescimentoAno(freqAno));
    }

    const heuristicasNormalizadas = heuristicas.map(normalizarPontuacoes);
    const combinadas = combinarPontuacoes(...heuristicasNormalizadas);

    const topPrevistos = Object.entries(combinadas)
      .sort((a, b) => b[1] - a[1])
      .slice(0, 6)
      .map(([numero]) => Number(numero));

    const resultado = compararPrevisao(sorteio2012.numeros || [], topPrevistos);

    resultadosSimulacao.push({
      data: sorteio2012.data,
      ...resultado
    });

    sorteiosDisponiveis.push(sorteio2012);
  });

  const total = resultadosSimulacao.length;
  const mediaAcertos = +(resultadosSimulacao.reduce((s, r) => s + r.num_acertos, 0) / total).toFixed(2);
  const distribuicao = {};
  for (let i = 0; i <= 6; i++) distribuicao[i] = 0;
  resultadosSimulacao.forEach(r => distribuicao[r.num_acertos]++);

  const relatorioFinal = {
    gerado_em: new Date().toISOString(),
    total_sorteios_simulados: total,
    media_acertos: mediaAcertos,
    distribuicao_acertos: distribuicao,
    simulacoes: resultadosSimulacao
  };

  garantirPasta(PASTA_ESTATISTICAS);
  const destino = path.join(PASTA_ESTATISTICAS, 'analise_desvio.json');
  fs.writeFileSync(destino, JSON.stringify(relatorioFinal, null, 2), 'utf-8');
  console.log(`✅ Simulação guardada em ${destino}`);
}

// --- Executar as duas funções ---

mainPrevisao();
mainSimulacao();
