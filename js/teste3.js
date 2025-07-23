// totoloto_analise.js

const fs = require('fs');
const path = require('path');

// --- Configurações ---
const PASTA_DADOS = path.join(__dirname, '..', 'dados');
const PASTA_ESTATISTICAS = path.join(__dirname, '..', 'estatisticas');

// --- Utilitários ---
function parseData(dataStr) {
  const [dia, mes, ano] = dataStr.split('/').map(Number);
  return new Date(ano, mes - 1, dia);
}

function garantirPasta(pasta) {
  if (!fs.existsSync(pasta)) fs.mkdirSync(pasta, { recursive: true });
}

function compararPrevisao(reais, previstos) {
  const acertos = reais.filter(n => previstos.includes(n));
  return { reais, previstos, acertos, num_acertos: acertos.length };
}

// --- Leitura de dados ---
function listarFicheirosAnos() {
  return fs.readdirSync(PASTA_DADOS).filter(f => /^\d{4}\.json$/.test(f));
}

function lerSorteiosAno(nomeFicheiro) {
  const ano = nomeFicheiro.replace('.json', '');
  const conteudo = fs.readFileSync(path.join(PASTA_DADOS, nomeFicheiro), 'utf-8');
  const dados = JSON.parse(conteudo);
  return dados[ano] || [];
}

function carregarTodosSorteios() {
  return listarFicheirosAnos()
    .flatMap(f => lerSorteiosAno(f))
    .sort((a, b) => parseData(a.data) - parseData(b.data));
}

// --- Estatísticas ---
function calcularEstatisticas(sorteios) {
  const total = sorteios.length;
  const estatisticas = {};

  for (let numero = 1; numero <= 49; numero++) {
    const indices = sorteios.map((s, i) => s.numeros?.includes(numero) ? i : -1).filter(i => i !== -1);
    const gaps = indices.slice(1).map((v, i) => v - indices[i]);
    const num_saidas = indices.length;

    estatisticas[numero] = {
      numero,
      num_saidas,
      percent_saidas: +(num_saidas / total * 100).toFixed(2),
      ausencias: indices.length ? total - indices[indices.length - 1] - 1 : total,
      gap_medio: gaps.length ? +(gaps.reduce((a, b) => a + b) / gaps.length).toFixed(2) : null,
      tendencia: indices.length >= 2 ? indices[indices.length - 1] - indices[indices.length - 2] : null
    };
  }

  return estatisticas;
}

function atribuirPontos(lista, peso, limite = 10) {
  const pontos = {};
  lista.slice(0, limite).forEach((e, idx) => {
    const score = (limite - idx) * peso;
    pontos[e.numero] = (pontos[e.numero] || 0) + score;
  });
  return pontos;
}

function pontuarPorFrequencia(est) {
  return atribuirPontos(Object.values(est).sort((a, b) => b.num_saidas - a.num_saidas), 3);
}

function pontuarPorAusencia(est) {
  return atribuirPontos(Object.values(est).sort((a, b) => b.ausencias - a.ausencias), 2);
}

function pontuarPorTendencia(est) {
  return atribuirPontos(Object.values(est).filter(e => e.tendencia !== null && e.tendencia <= 10), 2);
}

function pontuarPorGapMedio(est) {
  const lista = Object.values(est)
    .filter(e => e.gap_medio !== null)
    .map(e => ({ ...e, desvio: Math.abs(e.gap_medio - 40) }))
    .sort((a, b) => a.desvio - b.desvio);
  return atribuirPontos(lista, 1);
}

function calcularParesFrequentes(sorteios) {
  const paresCount = {};
  sorteios.forEach(({ numeros = [] }) => {
    numeros.forEach((n1, i) => {
      for (let j = i + 1; j < numeros.length; j++) {
        const par = [n1, numeros[j]].sort((a, b) => a - b).join('-');
        paresCount[par] = (paresCount[par] || 0) + 1;
      }
    });
  });
  return paresCount;
}

function pontuarPorPares(paresFreq) {
  return Object.entries(paresFreq).sort((a, b) => b[1] - a[1]).slice(0, 20).reduce((acc, [par, _, idx]) => {
    const score = 15 - idx;
    par.split('-').map(Number).forEach(n => acc[n] = (acc[n] || 0) + score);
    return acc;
  }, {});
}

function calcularTriosFrequentes(sorteios) {
  const triosCount = {};
  sorteios.forEach(({ numeros = [] }) => {
    for (let i = 0; i < numeros.length; i++) {
      for (let j = i + 1; j < numeros.length; j++) {
        for (let k = j + 1; k < numeros.length; k++) {
          const trio = [numeros[i], numeros[j], numeros[k]].sort((a, b) => a - b).join('-');
          triosCount[trio] = (triosCount[trio] || 0) + 1;
        }
      }
    }
  });
  return triosCount;
}

function pontuarPorTrios(triosFreq) {
  return Object.entries(triosFreq).sort((a, b) => b[1] - a[1]).slice(0, 10).reduce((acc, [trio, _, idx]) => {
    const score = 20 - idx * 2;
    trio.split('-').map(Number).forEach(n => acc[n] = (acc[n] || 0) + score);
    return acc;
  }, {});
}

function calcularFrequenciaPorAno(sorteios) {
  const freq = {};
  sorteios.forEach(({ data, numeros = [] }) => {
    const ano = parseData(data).getFullYear();
    if (!freq[ano]) freq[ano] = {};
    numeros.forEach(n => freq[ano][n] = (freq[ano][n] || 0) + 1);
  });
  return freq;
}

function pontuarCrescimentoAno(freqAno) {
  const anos = Object.keys(freqAno).map(Number).sort();
  const pontos = {};
  for (let num = 1; num <= 49; num++) {
    let crescimentos = 0;
    for (let i = 1; i < anos.length; i++) {
      const a1 = freqAno[anos[i - 1]][num] || 0;
      const a2 = freqAno[anos[i]][num] || 0;
      if (a2 > a1) crescimentos++;
    }
    if (crescimentos >= 2) pontos[num] = crescimentos * 3;
  }
  return pontos;
}

function combinarPontuacoes(...listas) {
  return listas.reduce((acc, lista) => {
    Object.entries(lista).forEach(([num, score]) => acc[num] = (acc[num] || 0) + score);
    return acc;
  }, {});
}

function normalizarPontuacoes(pontos) {
  const valores = Object.values(pontos);
  const min = Math.min(...valores), max = Math.max(...valores);
  return Object.fromEntries(Object.entries(pontos).map(([n, v]) => [n, +((v - min) / (max - min || 1)).toFixed(4)]));
}

// --- Previsão ---
function mainPrevisao() {
  const sorteios = carregarTodosSorteios();
  const ultimos50 = sorteios.slice(-50);

  const totalEst = calcularEstatisticas(sorteios);
  const recentEst = calcularEstatisticas(ultimos50);
  const freqAno = calcularFrequenciaPorAno(sorteios);

  const pontos = combinarPontuacoes(
    pontuarPorFrequencia(totalEst),
    pontuarPorAusencia(totalEst),
    pontuarPorTendencia(totalEst),
    pontuarPorGapMedio(totalEst),
    pontuarPorFrequencia(recentEst),
    pontuarPorTendencia(recentEst),
    pontuarPorGapMedio(recentEst),
    pontuarPorPares(calcularParesFrequentes(sorteios)),
    pontuarPorTrios(calcularTriosFrequentes(sorteios)),
    pontuarCrescimentoAno(freqAno)
  );

  const provaveis = Object.entries(pontos).sort((a, b) => b[1] - a[1]).slice(0, 2).map(([n]) => +n);

  const resultado = {
    gerado_em: new Date().toISOString(),
    total_sorteios: sorteios.length,
    combinadas: pontos,
    sugestao_final: provaveis
  };

  garantirPasta(PASTA_ESTATISTICAS);
  fs.writeFileSync(path.join(PASTA_ESTATISTICAS, 'estatisticas_teste.json'), JSON.stringify(resultado, null, 2));
  console.log("\n✅ Resultado guardado em estatisticas_teste.json");
}

// --- Simulação ---
function mainSimulacao() {
  const dados2011 = lerSorteiosAno('2011.json');
  const dados2012 = lerSorteiosAno('2012.json');
  const resultados = [];
  let acumulado = [...dados2011];

  dados2012.forEach(sorteio => {
    const estat = calcularEstatisticas(acumulado);
    const heuristicas = [
      pontuarPorFrequencia(estat),
      pontuarPorAusencia(estat),
      pontuarPorTendencia(estat),
      pontuarPorGapMedio(estat),
      pontuarPorPares(calcularParesFrequentes(acumulado)),
      pontuarPorTrios(calcularTriosFrequentes(acumulado))
    ];

    const freqAno = calcularFrequenciaPorAno(acumulado);
    if (Object.keys(freqAno).length >= 2) heuristicas.push(pontuarCrescimentoAno(freqAno));

    const combinadas = combinarPontuacoes(...heuristicas.map(normalizarPontuacoes));
    const previstos = Object.entries(combinadas).sort((a, b) => b[1] - a[1]).slice(0, 6).map(([n]) => +n);
    resultados.push({ data: sorteio.data, ...compararPrevisao(sorteio.numeros || [], previstos) });
    acumulado.push(sorteio);
  });

  const total = resultados.length;
  const media = +(resultados.reduce((s, r) => s + r.num_acertos, 0) / total).toFixed(2);
  const distribuicao = Object.fromEntries([...Array(7)].map((_, i) => [i, resultados.filter(r => r.num_acertos === i).length]));

  garantirPasta(PASTA_ESTATISTICAS);
  fs.writeFileSync(path.join(PASTA_ESTATISTICAS, 'analise_desvio.json'), JSON.stringify({
    gerado_em: new Date().toISOString(),
    total_sorteios_simulados: total,
    media_acertos: media,
    distribuicao_acertos: distribuicao,
    simulacoes: resultados
  }, null, 2));

  console.log("\n✅ Simulação guardada em analise_desvio.json");
}

// --- Execução ---
mainPrevisao();
mainSimulacao();
