const fs = require('fs');
const path = require('path');

// Configurações
const PASTA_DADOS = path.join(__dirname, '..', 'dados');
const PASTA_ESTATISTICAS = path.join(__dirname, '..', 'estatisticas');

// Parse de data no formato "dd/mm/yyyy"
function parseData(dataStr) {
  const partes = dataStr.split('/');
  if (partes.length !== 3) return new Date(0);
  const [dia, mes, ano] = partes.map(Number);
  return new Date(ano, mes - 1, dia);
}

// Lista ficheiros de anos válidos
function listarFicheirosAnos() {
  return fs.readdirSync(PASTA_DADOS).filter(f => {
    const ano = f.replace('.json', '');
    return /^\d{4}$/.test(ano) && +ano >= 2011 && +ano <= 2025;
  });
}

// Lê um ficheiro de sorteios
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

// Calcula estatísticas básicas
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

// Heurística: maior frequência
function pontuarPorFrequencia(est) {
  const ordenado = Object.values(est).sort((a, b) => b.num_saidas - a.num_saidas);
  return atribuirPontos(ordenado, 3);
}

// Heurística: maior ausência
function pontuarPorAusencia(est) {
  const ordenado = Object.values(est).sort((a, b) => b.ausencias - a.ausencias);
  return atribuirPontos(ordenado, 2);
}

// Heurística: tendência de subida (último gap menor que o anterior)
function pontuarPorTendencia(est) {
  const candidatos = Object.values(est).filter(e => e.tendencia !== null && e.tendencia <= 10);
  return atribuirPontos(candidatos, 2);
}

// Heurística: gap médio próximo de 40 (repetição com padrão)
function pontuarPorGapMedio(est) {
  const ordenado = Object.values(est)
    .filter(e => e.gap_medio !== null)
    .map(e => ({ ...e, desvio: Math.abs(e.gap_medio - 40) }))
    .sort((a, b) => a.desvio - b.desvio);
  return atribuirPontos(ordenado, 1);
}

// Distribui pontos aos N primeiros
function atribuirPontos(lista, peso) {
  const pontos = {};
  lista.slice(0, 10).forEach((e, idx) => {
    const score = (10 - idx) * peso;
    pontos[e.numero] = (pontos[e.numero] || 0) + score;
  });
  return pontos;
}

// Junta múltiplas heurísticas
function combinarPontuacoes(...listas) {
  const combinadas = {};
  listas.forEach(lista => {
    for (const [num, score] of Object.entries(lista)) {
      combinadas[num] = (combinadas[num] || 0) + score;
    }
  });
  return combinadas;
}

// Garante que pasta existe
function garantirPasta(pasta) {
  if (!fs.existsSync(pasta)) fs.mkdirSync(pasta, { recursive: true });
}

// Função principal
function main() {
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

  // Combina tudo
  const pontosCombinados = combinarPontuacoes(pontosTotal, pontosRecentes);

  // Ordenar pelos mais prováveis
  const provaveis = Object.entries(pontosCombinados)
    .sort((a, b) => b[1] - a[1])
    .slice(0, 2)
    .map(([numero]) => Number(numero));

  console.log(`\n🔮 Números mais prováveis no próximo sorteio: ${provaveis.join(', ')}`);

  // Salvar resultado
  const resultado = {
    gerado_em: new Date().toISOString(),
    total_sorteios: sorteios.length,
    heuristicas: {
      total: pontosTotal,
      ultimos50: pontosRecentes
    },
    combinadas: pontosCombinados,
    sugestao_final: provaveis
  };

  garantirPasta(PASTA_ESTATISTICAS);
  const destino = path.join(PASTA_ESTATISTICAS, 'estatisticas_teste.json');
  fs.writeFileSync(destino, JSON.stringify(resultado, null, 2), 'utf-8');
  console.log(`\n✅ Resultado guardado em ${destino}`);
}

main();
