const fs = require('fs');
const path = require('path');

const PASTA_DADOS = path.join(__dirname, '..', 'dados');
const PASTA_ESTATISTICAS = path.join(__dirname, '..', 'estatisticas');

const METODO = 'frequencia_basica';
const VERSAO = '1.0';
const DESCRICAO = 'Contagem total de aparições desde 2011';
const PARAMETROS = {
  periodo: "total",
  grupo_idade: null,
  janela_temporal: null
};

// Parse de data "dd/mm/yyyy"
function parseData(dataStr) {
  const partes = dataStr.split('/');
  if (partes.length !== 3) return new Date(0);
  const [dia, mes, ano] = partes.map(Number);
  return new Date(ano, mes - 1, dia);
}

// Listar ficheiros com nome de ano
function listarFicheirosAnos() {
  return fs.readdirSync(PASTA_DADOS).filter(f => {
    const ano = f.replace('.json', '');
    return /^\d{4}$/.test(ano) && +ano >= 2011 && +ano <= 2025;
  });
}

// Ler sorteios de ficheiro
function lerSorteiosAno(nomeFicheiro) {
  const caminho = path.join(PASTA_DADOS, nomeFicheiro);
  const conteudo = fs.readFileSync(caminho, 'utf-8');
  const dados = JSON.parse(conteudo);
  const ano = nomeFicheiro.replace('.json', '');
  return dados[ano] || [];
}

// Junta todos os sorteios e ordena
function carregarTodosSorteios() {
  const ficheiros = listarFicheirosAnos();
  let todos = [];
  const porAno = {};

  ficheiros.forEach(fich => {
    try {
      const sorteios = lerSorteiosAno(fich);
      todos = todos.concat(sorteios);
      const ano = fich.replace('.json', '');
      porAno[ano] = sorteios.length;
    } catch (e) {
      console.warn(`[Aviso] Erro a ler ${fich}:`, e.message);
    }
  });

  todos.sort((a, b) => parseData(a.data) - parseData(b.data));
  return { todos, porAno, ficheiros };
}

// Estatísticas por número
function calcularEstatisticas(sorteios) {
  const total = sorteios.length;
  const estatisticas = {};

  for (let numero = 1; numero <= 49; numero++) {
    let num_saidas = 0;
    let ultimo_idx = -1;

    sorteios.forEach((sorteio, idx) => {
      if (sorteio.numeros?.includes(numero)) {
        num_saidas++;
        ultimo_idx = idx;
      }
    });

    const percent = total ? Number(((num_saidas / total) * 100).toFixed(2)) : 0;

    let ultimo_sorteio = "-";
    let data_ultimo = "-";
    let ausencias = total;

    if (ultimo_idx >= 0) {
      ultimo_sorteio = sorteios[ultimo_idx].concurso || "-";
      data_ultimo = sorteios[ultimo_idx].data || "-";
      ausencias = total - ultimo_idx - 1;
    }

    estatisticas[numero.toString()] = {
      numero,
      num_saidas,
      percent_saidas: percent,
      ultimo_sorteio,
      data_ultimo,
      ausencias
    };
  }

  return estatisticas;
}

// Prever número com maior ausência, mas que tenha saído pelo menos minSaidas vezes
function preverPorAusenciaComFrequencia(estatisticas, minSaidas = 80) {
  const candidatos = Object.values(estatisticas)
    .filter(e => e.num_saidas >= minSaidas)
    .sort((a, b) => b.ausencias - a.ausencias);
  return candidatos[0]?.numero || null;
}

// Prever número mais frequente entre os que não saíram nos últimos minAusencias sorteios
function preverPorRecenteInatividade(estatisticas, minAusencias = 10) {
  const candidatos = Object.values(estatisticas)
    .filter(e => e.ausencias >= minAusencias)
    .sort((a, b) => b.num_saidas - a.num_saidas);
  return candidatos[0]?.numero || null;
}

// Combina previsões e escolhe o número mais votado
function preverPorVotacao(estatisticas) {
  const sugestoes = [
    preverPorAusenciaComFrequencia(estatisticas),
    preverPorRecenteInatividade(estatisticas)
  ].filter(Boolean);

  if (sugestoes.length === 0) return null;

  const contagem = {};
  sugestoes.forEach(num => {
    contagem[num] = (contagem[num] || 0) + 1;
  });

  const ordenados = Object.entries(contagem).sort((a, b) => b[1] - a[1]);
  return Number(ordenados[0][0]);
}

// Cria pasta se não existir
function garantirPasta(pasta) {
  if (!fs.existsSync(pasta)) fs.mkdirSync(pasta, { recursive: true });
}

// Função principal
function main() {
  console.time('tempo_execucao');

  console.log(`[${METODO}] A carregar sorteios...`);
  const { todos: sorteios, porAno, ficheiros } = carregarTodosSorteios();

  if (!sorteios.length) {
    console.error("Erro: Nenhum sorteio encontrado.");
    return;
  }

  const data_inicio = sorteios[0].data || "-";
  const data_fim = sorteios[sorteios.length - 1].data || "-";

  const estatisticas = calcularEstatisticas(sorteios);

  // Previsão combinada usando as heurísticas
  const numeroPrevisto = preverPorVotacao(estatisticas);
  const sugestoes = numeroPrevisto ? [numeroPrevisto] : [];

  console.timeEnd('tempo_execucao');

  const resultado = {
    metodo: METODO,
    versao: VERSAO,
    descricao: DESCRICAO,
    gerado_em: new Date().toISOString(),
    total_sorteios: sorteios.length,
    data_inicio,
    data_fim,
    parametros: PARAMETROS,
    sugestoes,
    estatisticas,
    sorteios_por_ano: porAno,
    debug_info: {
      ficheiros_usados: ficheiros.sort(),
      tempo_execucao_ms: 0
    }
  };

  const tempo_inicio = performance.now?.() || Date.now();
  const destino = path.join(PASTA_ESTATISTICAS, `estatisticas_${METODO}.json`);

  garantirPasta(PASTA_ESTATISTICAS);
  fs.writeFileSync(destino, JSON.stringify(resultado, null, 2), 'utf-8');

  const tempo_fim = performance.now?.() || Date.now();
  resultado.debug_info.tempo_execucao_ms = Math.round(tempo_fim - tempo_inicio);

  fs.writeFileSync(destino, JSON.stringify(resultado, null, 2), 'utf-8');
  console.log(`[${METODO}] Estatísticas guardadas em: ${destino}`);
}

main();
